import asyncio
import logging
import base64
from functools import partial
from typing import Dict, List, Optional
from elasticsearch import NotFoundError
from elasticsearch.helpers import bulk

from .utils import rrf


class Collection:
    """Collection (knowledge base) abstraction, corresponding to an ES index"""
    
    def __init__(self, client, name: str, user, model=None):
        self.client = client
        self.name = name
        self.user = user
        self.model = model
        
        # Index naming convention
        if model:
            self.index_name = f"{model.model_id}__{user.username}__{name}"
        else:
            self.index_name = f"{user.username}__{name}"
    
    def add(self, document_id: str, name: str, file_content: Optional[bytes] = None,
            text_content: Optional[str] = None, metadata: Optional[Dict] = None,
            chunks: Optional[List[Dict]] = None,
            timeout: int = 600) -> Dict:
        """
        Add a document to the collection using parent/child structure
        
        Args:
            document_id: Document ID
            name: Document name
            file_content: File content (binary)
            text_content: Text content
            metadata: Metadata
            chunks: Pre-processed chunks of text with embeddings (optional)
            timeout: Timeout
        """
        # Ensure at least one content source is provided
        if not file_content and not text_content and not chunks:
            raise ValueError("Must provide file_content, text_content, or chunks")

        # Step 1: If text_content is not provided but file_content is, extract text from the file.
        if not text_content and file_content:
            text_content = self._extract_text_from_file(file_content)

        # Step 2: If chunks are not provided but text_content is, split the text into chunks.
        if not chunks and text_content:
            chunks = self._split_text_to_chunks(text_content)

        # Step 3: Now, chunks should be available. Use bulk operation to add the parent and chunks.
        if chunks:
            return self._add_with_chunks(document_id, name, chunks, metadata, timeout)
        else:
            # This case should not be reached if the logic is correct and inputs are valid.
            raise ValueError("Could not generate chunks from the provided content.")
    
    def _extract_text_from_file(self, file_content: bytes) -> str:
        """Extract text from file using attachment processor"""
        try:
            # Create a temporary document to extract text
            temp_doc = {
                "data": base64.b64encode(file_content).decode()
            }
            
            # Use ingest simulate to extract text
            response = self.client.client.ingest.simulate(
                body={
                    "pipeline": {
                        "processors": [
                            {
                                "attachment": {
                                    "field": "data",
                                    "target_field": "attachment",
                                    "properties": ["content", "title", "content_type"],
                                    "remove_binary": True,
                                    "ignore_missing": True
                                }
                            }
                        ]
                    },
                    "docs": [{"_source": temp_doc}]
                }
            )
            
            extracted_content = response['docs'][0]['doc']['_source'].get('attachment', {}).get('content', '')
            return extracted_content
            
        except Exception as e:
            logging.error(f"Failed to extract text from file: {e}")
            raise
    
    def _split_text_to_chunks(self, text: str) -> List[Dict]:
        """Split text into chunks using the splitter"""
        try:
            # Use ingest simulate to split text
            response = self.client.client.ingest.simulate(
                body={
                    "pipeline": {
                        "processors": [
                            self.client.splitter.get_processor()
                        ]
                    },
                    "docs": [{"_source": {"attachment": {"content": text}}}]
                }
            )
            
            chunks = response['docs'][0]['doc']['_source'].get('chunks', [])
            return chunks
            
        except Exception as e:
            logging.error(f"Failed to split text: {e}")
            raise
    
    def _add_with_chunks(self, document_id: str, name: str, chunks: List[Dict], 
                        metadata: Optional[Dict] = None, timeout: int = 600) -> Dict:
        """Add document using parent/child structure with bulk operations"""
        actions = []
        
        # Add parent document
        actions.append({
            "_op_type": "index",
            "_index": self.index_name,
            "_id": document_id,
            "_source": {
                "doc_chunk_relation": "document",
                "name": name,
                "document_metadata": metadata or {}
            }
        })
        
        # Add child chunks (embedding will be handled by default pipeline)
        for i, chunk in enumerate(chunks):
            chunk_id = f"{document_id}_{i}"
            chunk_source = {
                "doc_chunk_relation": {"name": "chunk", "parent": document_id},
                "content": chunk.get("content", ""),
                "metadata": chunk.get("metadata", {})
            }
            
            # If embedding is already provided, include it
            if "embedding" in chunk:
                chunk_source["embedding"] = chunk["embedding"]
            
            actions.append({
                "_op_type": "index",
                "_index": self.index_name,
                "_id": chunk_id,
                "routing": document_id,
                "_source": chunk_source
            })
        
        try:
            success, failed = bulk(
                self.client.client,
                actions,
                refresh='wait_for',
                request_timeout=timeout,
                chunk_size=200,
                max_retries=2,
                initial_backoff=2,
                raise_on_error=False
            )
            
            if failed:
                logging.error(f"Add failed for doc {document_id}: {failed}")
                raise Exception(f"Failed to add some chunks: {failed}")
            
            return {"result": "created", "chunks_added": len(chunks)}
            
        except Exception as e:
            logging.error(f"Failed to add document with chunks: {e}")
            raise
    
    async def query(self, query_text: str, metadata_filter: Optional[Dict] = None, 
                   size: int = 5, include_embedding: bool = True) -> List[Dict]:
        """
        Query the collection using parent/child structure with has_parent filtering
        
        Args:
            query_text: Query text
            metadata_filter: Metadata filter conditions
            size: Number of results to return
            include_embedding: Whether to include vector search
        """
        # Build parent filters
        parent_filters = []
        if metadata_filter:
            for key, value in metadata_filter.items():
                if isinstance(value, list):
                    parent_filters.append({
                        "terms": {f"document_metadata.{key}": value}
                    })
                else:
                    parent_filters.append({
                        "term": {f"document_metadata.{key}": value}
                    })
        
        # Child filter based on parent
        chunk_filter = {
            "has_parent": {
                "parent_type": "document",
                "query": {"bool": {"filter": parent_filters}} if parent_filters else {"match_all": {}}
            }
        }
        
        # Text search
        text_search_body = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"content": query_text}}
                    ],
                    "filter": [chunk_filter]
                }
            },
            "size": size * 2,
            "_source": ["content", "metadata"]
        }
        
        # Execute search tasks
        searches = []
        
        # Text search task
        text_search = partial(self.client.async_client.search, index=self.index_name, body=text_search_body)
        searches.append(text_search())
        
        # Vector search (if a model is configured)
        if include_embedding and self.model:
            vector_search_body = {
                "knn": {
                    "field": "embedding",
                    "query_vector_builder": {
                        "text_embedding": {
                            "model_id": self.model.inference_id,
                            "model_text": query_text,
                        }
                    },
                    "k": size * 2,
                    "num_candidates": size * 10,
                    "filter": [chunk_filter]
                },
                "size": size * 2,
                "_source": ["content", "metadata"]
            }
            
            vector_search = partial(self.client.async_client.search, index=self.index_name, body=vector_search_body)
            searches.append(vector_search())
        
        # Execute all searches
        responses = await asyncio.gather(*searches, return_exceptions=True)
        
        # Process results and prepare for RRF merging
        search_results = []
        all_chunk_data = {}
        
        for i, response in enumerate(responses):
            if isinstance(response, Exception):
                logging.warning(f"Search execution failed: {response}")
                continue
            
            search_type = "text" if i == 0 else "vector"
            chunk_results = []
            
            for hit in response['hits']['hits']:
                chunk_key = hit['_id']
                chunk_results.append((chunk_key, hit['_score']))
                
                # Store detailed information for the chunk
                if chunk_key not in all_chunk_data:
                    all_chunk_data[chunk_key] = {
                        'document_id': hit.get('_routing', chunk_key.split('_')[0]),
                        'chunk_content': hit['_source'].get('content', ''),
                        'metadata': hit['_source'].get('metadata', {}),
                        'score': [{
                            'search_type': search_type,
                            'score': hit['_score'],
                        }]
                    }
                else:
                    all_chunk_data[chunk_key]['score'].append({
                        'search_type': search_type,
                        'score': hit['_score'],
                    })
            
            search_results.append(chunk_results)
        
        # Merge results using RRF algorithm
        if len(search_results) == 1:
            merged_results = search_results[0]
        elif len(search_results) > 1:
            merged_results = rrf(*search_results, k=60)
        else:
            merged_results = []
        
        # Get parent documents for final results
        parent_ids = list(set(all_chunk_data[chunk_key]['document_id'] for chunk_key, _ in merged_results[:size]))
        parent_docs = {}
        
        if parent_ids:
            try:
                docs_response = self.client.client.mget(index=self.index_name, body={"ids": parent_ids})
                parent_docs = {doc['_id']: doc['_source'] for doc in docs_response['docs'] if doc['found']}
            except Exception as e:
                logging.warning(f"Failed to get parent documents: {e}")
        
        # Build final results
        final_results = []
        for chunk_key, rrf_score in merged_results[:size]:
            if chunk_key in all_chunk_data:
                result = all_chunk_data[chunk_key].copy()
                result['rrf_score'] = rrf_score
                result['final_score'] = rrf_score
                
                # Add parent document information
                parent_id = result['document_id']
                if parent_id in parent_docs:
                    result['document_name'] = parent_docs[parent_id].get('name', '')
                    result['document_metadata'] = parent_docs[parent_id].get('document_metadata', {})
                else:
                    result['document_name'] = ''
                    result['document_metadata'] = {}
                
                final_results.append(result)
        
        return final_results
    
    def get(self, document_id: str) -> Optional[Dict]:
        """Get the specified document (parent only)"""
        try:
            response = self.client.client.get(
                index=self.index_name,
                id=document_id
            )
            return response['_source']
        except NotFoundError:
            return None
        except Exception as e:
            logging.error(f"Failed to get document: {e}")
            raise
    
    def delete(self, document_id: str) -> bool:
        """Delete the specified document and all its chunks"""
        try:
            # Delete all child chunks first
            self.client.client.delete_by_query(
                index=self.index_name,
                body={
                    "query": {
                        "has_parent": {
                            "parent_type": "document",
                            "query": {"term": {"_id": document_id}}
                        }
                    }
                },
                refresh=True,
                conflicts='proceed'
            )
            
            # Delete parent document
            self.client.client.delete(
                index=self.index_name,
                id=document_id,
                refresh='wait_for'
            )
            return True
        except NotFoundError:
            return False
        except Exception as e:
            logging.error(f"Failed to delete document: {e}")
            raise
    
    def list_documents(self, offset: int = 0, limit: int = 10) -> Dict:
        """List documents in the collection (parent documents only)"""
        try:
            response = self.client.client.search(
                index=self.index_name,
                body={
                    "query": {
                        "term": {"doc_chunk_relation": "document"}
                    },
                    "_source": ["name", "document_metadata"],
                    "from": offset,
                    "size": limit
                }
            )            
            return {
                "total": response['hits']['total']['value'],
                "documents": [
                    {
                        "id": hit['_id'],
                        "name": hit['_source'].get('name', ''),
                        "metadata": hit['_source'].get('document_metadata', {})
                    }
                    for hit in response['hits']['hits']
                ]
            }
        except NotFoundError:
            return {"total": 0, "documents": []}
        except Exception as e:
            logging.error(f"Failed to list documents: {e}")
            raise
    
    def drop(self):
        """Delete the entire collection"""
        try:
            if self.client.client.indices.exists(index=self.index_name):
                self.client.client.indices.delete(index=self.index_name)
                logging.debug(f"Deleted index successfully: {self.index_name}")
        except Exception as e:
            logging.error(f"Failed to delete collection: {e}")
            raise