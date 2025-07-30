import asyncio
import logging
import os
from typing import Dict, List, Optional, Tuple

# Check for optional dependencies
try:
    import gradio as gr
    import pandas as pd
    HAS_WEB_DEPS = True
except ImportError as e:
    HAS_WEB_DEPS = False
    _missing_deps = str(e)

from .client import Client
from .user import User


def check_web_dependencies():
    """Check if web dependencies are available"""
    if not HAS_WEB_DEPS:
        raise ImportError(
            "Web interface dependencies are not installed. "
            "Install them with: uv add 'elasticrag[web]' or uv add gradio pandas"
        )


def get_event_loop():
    """Get the current event loop or create a new one if needed"""
    try:
        return asyncio.get_event_loop()
    except RuntimeError:
        # No event loop is running, create a new one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop

def syncify(func):
    """Decorator to run async functions in a synchronous context"""
    def wrapper(*args, **kwargs):
        loop = get_event_loop()
        return loop.run_until_complete(func(*args, **kwargs))
    return wrapper


class ElasticRAGServer:
    """Gradio-based management interface for ElasticRAG"""
    
    def __init__(self, client: Client, admin_username: str = None, admin_password: str = None):
        check_web_dependencies()  # Check dependencies on initialization
        
        self.client = client
        self.admin_username = admin_username or os.getenv("ELASTICRAG_ADMIN_USERNAME", "admin")
        self.admin_password = admin_password or os.getenv("ELASTICRAG_ADMIN_PASSWORD", "admin123")
        self.current_user = None
        self.is_admin = False
        
    def authenticate_user(self, username: str, password: str) -> Tuple[bool, str, Dict]:
        """Authenticate user and return status"""
        try:
            # Check if admin
            if username == self.admin_username and password == self.admin_password:
                self.current_user = username
                self.is_admin = True
                return True, "管理员登录成功", {"username": username, "role": "admin"}
            
            # Try regular user authentication
            try:
                user = self.client.authenticate(username, password)
                self.current_user = user
                self.is_admin = False
                return True, f"用户 {username} 登录成功", {"username": username, "role": "user"}
            except ValueError:
                return False, "用户名或密码错误", {}
                
        except Exception as e:
            return False, f"登录失败: {str(e)}", {}
    
    def logout_user(self):
        """Logout current user"""
        self.current_user = None
        self.is_admin = False
        return "已退出登录", {}
    
    def get_collection_choices(self) -> List[str]:
        """Get collection choices for dropdown"""
        if not self.current_user or self.is_admin:
            return []
        
        try:
            collections = self.client.list_collections()
            return [collection['name'] for collection in collections] if collections else []
        except Exception:
            return []
    
    def get_model_choices(self) -> List[str]:
        """Get model choices for dropdown"""
        try:
            models = self.client.list_models()
            return [model['model_id'] for model in models] if models else []
        except Exception:
            return []
    
    def get_document_choices(self, collection_name: str, model_id: str = None) -> List[str]:
        """Get document choices for dropdown"""
        if not self.current_user or self.is_admin or not collection_name:
            return []
        
        try:
            collection = self.client.get_collection(collection_name, model_id)
            documents_info = collection.list_documents(limit=100)
            return [doc['id'] for doc in documents_info['documents']] if documents_info['total'] > 0 else []
        except Exception:
            return []

    # Admin functions
    def list_all_users(self) -> pd.DataFrame:
        """List all users (admin only)"""
        if not self.is_admin:
            return pd.DataFrame({"错误": ["需要管理员权限"]})
        
        try:
            users_info = User.list_all_users(self.client.client, "user_auth", limit=100)
            if users_info['total'] == 0:
                return pd.DataFrame({"信息": ["暂无用户"]})
            
            users_data = []
            for user in users_info['users']:
                users_data.append({
                    "用户名": user['username'],
                    "创建时间": user['created_at'],
                    "最后登录": user['last_login'] or '从未登录',
                    "邮箱": user.get('metadata', {}).get('email', ''),
                    "角色": user.get('metadata', {}).get('role', ''),
                })
            
            return pd.DataFrame(users_data)
        except Exception as e:
            return pd.DataFrame({"错误": [f"获取用户列表失败: {str(e)}"]})
    
    def add_new_user(self, username: str, api_key: str, email: str, role: str) -> str:
        """Add new user (admin only)"""
        if not self.is_admin:
            return "需要管理员权限"
        
        if not username or not api_key:
            return "用户名和API密钥不能为空"
        
        try:
            metadata = {"email": email, "role": role} if email or role else {}
            success = self.client.add_user(username, api_key, metadata)
            return "用户添加成功" if success else "用户添加失败"
        except Exception as e:
            return f"添加用户失败: {str(e)}"
    
    def delete_user(self, username: str) -> str:
        """Delete user (admin only)"""
        if not self.is_admin:
            return "需要管理员权限"
        
        if not username:
            return "请输入用户名"
        
        if username == self.admin_username:
            return "不能删除管理员账户"
        
        try:
            success = self.client.delete_user(username)
            return "用户删除成功" if success else "用户删除失败（用户不存在）"
        except Exception as e:
            return f"删除用户失败: {str(e)}"
    
    def list_all_models(self) -> pd.DataFrame:
        """List all models"""
        try:
            models = self.client.list_models()
            if not models:
                return pd.DataFrame({"信息": ["暂无模型"]})
            
            models_data = []
            for model in models:
                models_data.append({
                    "模型ID": model['model_id'],
                    "服务类型": model['config'].get('service', 'unknown'),
                    "向量维度": model['dimensions'],
                    "配置": str(model['config'])
                })
            
            return pd.DataFrame(models_data)
        except Exception as e:
            return pd.DataFrame({"错误": [f"获取模型列表失败: {str(e)}"]})
    
    def add_new_model(self, model_id: str, service: str, api_key: str, url: str, dimensions: int) -> str:
        """Add new model (admin only)"""
        if not self.is_admin:
            return "需要管理员权限"
        
        if not model_id or not service:
            return "模型ID和服务类型不能为空"
        
        try:
            config = {
                "service": service,
                "service_settings": {
                    "api_key": api_key or "placeholder",
                    "url": url
                },
                "dimensions": dimensions or 384
            }
            
            if url:
                config["service_settings"]["url"] = url
            
            self.client.register_model(model_id, config)
            return f"模型 {model_id} 添加成功"
        except Exception as e:
            return f"添加模型失败: {str(e)}"
    
    # User functions
    def list_user_collections(self) -> pd.DataFrame:
        """List user collections"""
        if not self.current_user or self.is_admin:
            return pd.DataFrame({"错误": ["请先登录用户账户"]})
        
        try:
            collections = self.client.list_collections()
            if not collections:
                return pd.DataFrame({"信息": ["暂无集合"]})
            
            collections_data = []
            for collection in collections:
                collections_data.append({
                    "集合名称": collection['name'],
                    "模型ID": collection['model_id'],
                    "健康状态": collection['health'],
                    "状态": collection['status'],
                    "文档数量": collection['doc_count'],
                    "存储大小": collection['store_size']
                })
            
            return pd.DataFrame(collections_data)
        except Exception as e:
            return pd.DataFrame({"错误": [f"获取集合列表失败: {str(e)}"]})
    
    def list_collection_documents(self, collection_name: str, model_id: str = None) -> pd.DataFrame:
        """List documents in a collection"""
        if not self.current_user or self.is_admin:
            return pd.DataFrame({"错误": ["请先登录用户账户"]})
        
        if not collection_name:
            return pd.DataFrame({"信息": ["请选择集合"]})
        
        try:
            collection = self.client.get_collection(collection_name, model_id)
            documents_info = collection.list_documents(limit=100)
            
            if documents_info['total'] == 0:
                return pd.DataFrame({"信息": ["集合中暂无文档"]})
            
            documents_data = []
            for doc in documents_info['documents']:
                documents_data.append({
                    "文档ID": doc['id'],
                    "文档名称": doc['name'],
                    "元数据": str(doc.get('metadata', {}))
                })
            
            return pd.DataFrame(documents_data)
        except Exception as e:
            return pd.DataFrame({"错误": [f"获取文档列表失败: {str(e)}"]})
    
    def add_text_document(self, collection_name: str, model_id: str, doc_name: str, text_content: str) -> str:
        """Add text document to collection"""
        if not self.current_user or self.is_admin:
            return "请先登录用户账户"
        
        if not all([collection_name, doc_name, text_content]):
            return "集合名称、文档名称和文本内容不能为空"
        
        try:
            collection = self.client.get_collection(collection_name, model_id)
            doc_id = f"text_{hash(text_content) % 1000000}"
            
            collection.add(
                document_id=doc_id,
                name=doc_name,
                text_content=text_content,
                metadata={'type': 'text', 'source': 'gradio_ui'}
            )
            
            return f"文档 '{doc_name}' 添加成功"
        except Exception as e:
            return f"添加文档失败: {str(e)}"
    
    def delete_document(self, collection_name: str, model_id: str, document_id: str) -> str:
        """Delete document from collection"""
        if not self.current_user or self.is_admin:
            return "请先登录用户账户"
        
        if not all([collection_name, document_id]):
            return "集合名称和文档ID不能为空"
        
        try:
            collection = self.client.get_collection(collection_name, model_id)
            success = collection.delete(document_id)
            return "文档删除成功" if success else "文档删除失败（文档不存在）"
        except Exception as e:
            return f"删除文档失败: {str(e)}"
    
    async def search_documents(self, collection_name: str, model_id: str, query: str, size: int = 5) -> pd.DataFrame:
        """Search documents in collection"""
        if not self.current_user or self.is_admin:
            return pd.DataFrame({"错误": ["请先登录用户账户"]})
        
        if not all([collection_name, query]):
            return pd.DataFrame({"错误": ["集合名称和查询内容不能为空"]})
        
        try:
            collection = self.client.get_collection(collection_name, model_id)
            results = await collection.query(query_text=query, size=size)
            
            if not results:
                return pd.DataFrame({"信息": ["未找到相关文档"]})
            
            search_data = []
            for i, result in enumerate(results, 1):
                search_data.append({
                    "排名": i,
                    "文档名称": result['document_name'],
                    "内容预览": result['chunk_content'][:200] + "..." if len(result['chunk_content']) > 200 else result['chunk_content'],
                    "相关度分数": f"{result.get('final_score', result.get('score', 0)):.4f}",
                    "文档ID": result['document_id']
                })
            
            return pd.DataFrame(search_data)
        except Exception as e:
            return pd.DataFrame({"错误": [f"搜索失败: {str(e)}"]})
    
    def create_interface(self):
        """Create Gradio interface"""
        with gr.Blocks(title="ElasticRAG 管理后台", theme=gr.themes.Soft()) as app:
            gr.Markdown("# 🔍 ElasticRAG 管理后台")
            
            # Login state
            user_state = gr.State({})
            
            # Login form - will be hidden after login
            with gr.Group(visible=True) as login_form:
                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("### 登录")
                        username_input = gr.Textbox(label="用户名", placeholder="输入用户名")
                        password_input = gr.Textbox(label="密码", type="password", placeholder="输入密码")
                        with gr.Row():
                            login_btn = gr.Button("登录", variant="primary")
                        login_status = gr.Markdown("请登录以使用系统")
            
            # Main interface - will be shown after login
            with gr.Group(visible=False) as main_interface:
                with gr.Row():
                    with gr.Column(scale=4):
                        user_info_display = gr.Markdown("", visible=False)
                    with gr.Column(scale=1):
                        logout_btn = gr.Button("退出", variant="secondary")
                
                # Tab interface for all functions
                with gr.Tabs() as main_tabs:
                    # Admin tabs
                    with gr.Tab("用户管理", visible=False) as user_mgmt_tab:
                        gr.Markdown("### 👥 用户管理")
                        
                        with gr.Row():
                            with gr.Column():
                                refresh_users_btn = gr.Button("刷新用户列表", variant="secondary")
                                users_table = gr.DataFrame(label="用户列表")
                            
                            with gr.Column():
                                gr.Markdown("#### 添加新用户")
                                new_username = gr.Textbox(label="用户名")
                                new_api_key = gr.Textbox(label="API密钥")
                                new_email = gr.Textbox(label="邮箱")
                                new_role = gr.Textbox(label="角色")
                                add_user_btn = gr.Button("添加用户", variant="primary")
                                add_user_result = gr.Textbox(label="结果", interactive=False)
                                
                                gr.Markdown("#### 删除用户")
                                delete_username = gr.Textbox(label="要删除的用户名")
                                delete_user_btn = gr.Button("删除用户", variant="stop")
                                delete_user_result = gr.Textbox(label="结果", interactive=False)
                    
                    with gr.Tab("模型管理", visible=False) as model_mgmt_tab:
                        gr.Markdown("### 🤖 模型管理")
                        
                        with gr.Row():
                            with gr.Column():
                                refresh_models_btn = gr.Button("刷新模型列表", variant="secondary")
                                models_table = gr.DataFrame(label="模型列表")
                            
                            with gr.Column():
                                gr.Markdown("#### 添加新模型")
                                new_model_id = gr.Textbox(label="模型ID")
                                new_service = gr.Dropdown(
                                    choices=["hugging_face", "openai", "elasticsearch"],
                                    label="服务类型",
                                    value="hugging_face"
                                )
                                new_model_api_key = gr.Textbox(label="API密钥")
                                new_model_url = gr.Textbox(label="服务URL")
                                new_dimensions = gr.Number(label="向量维度", value=384)
                                add_model_btn = gr.Button("添加模型", variant="primary")
                                add_model_result = gr.Textbox(label="结果", interactive=False)
                    
                    # User tabs
                    with gr.Tab("集合管理", visible=False) as collection_mgmt_tab:
                        gr.Markdown("### 📚 集合管理")
                        
                        with gr.Row():
                            refresh_collections_btn = gr.Button("刷新集合列表", variant="secondary")
                            collections_table = gr.DataFrame(label="我的集合")
                        
                        gr.Markdown("### 📄 文档管理")
                        
                        with gr.Row():
                            with gr.Column():
                                collection_select = gr.Dropdown(
                                    label="集合名称", 
                                    choices=[],
                                    allow_custom_value=True,
                                    value=None
                                )
                                model_select = gr.Dropdown(
                                    label="模型ID（可选）", 
                                    choices=[],
                                    allow_custom_value=True,
                                    value=None
                                )
                                refresh_docs_btn = gr.Button("刷新文档列表", variant="secondary")
                                documents_table = gr.DataFrame(label="文档列表")
                            
                            with gr.Column():
                                gr.Markdown("#### 添加文本文档")
                                doc_collection = gr.Dropdown(
                                    label="集合名称",
                                    choices=[],
                                    allow_custom_value=True,
                                    value=None
                                )
                                doc_model = gr.Dropdown(
                                    label="模型ID（可选）",
                                    choices=[],
                                    allow_custom_value=True,
                                    value=None
                                )
                                doc_name = gr.Textbox(label="文档名称")
                                doc_content = gr.Textbox(label="文档内容", lines=5)
                                add_doc_btn = gr.Button("添加文档", variant="primary")
                                add_doc_result = gr.Textbox(label="结果", interactive=False)
                                
                                gr.Markdown("#### 删除文档")
                                delete_doc_collection = gr.Dropdown(
                                    label="集合名称",
                                    choices=[],
                                    allow_custom_value=True,
                                    value=None
                                )
                                delete_doc_model = gr.Dropdown(
                                    label="模型ID（可选）",
                                    choices=[],
                                    allow_custom_value=True,
                                    value=None
                                )
                                delete_doc_id = gr.Dropdown(
                                    label="文档ID",
                                    choices=[],
                                    allow_custom_value=True,
                                    value=None
                                )
                                delete_doc_btn = gr.Button("删除文档", variant="stop")
                                delete_doc_result = gr.Textbox(label="结果", interactive=False)
                    
                    with gr.Tab("搜索调试", visible=False) as search_debug_tab:
                        gr.Markdown("### 🔍 搜索调试")
                        
                        with gr.Row():
                            with gr.Column():
                                search_collection = gr.Dropdown(
                                    label="集合名称",
                                    choices=[],
                                    allow_custom_value=True,
                                    value=None
                                )
                                search_model = gr.Dropdown(
                                    label="模型ID（可选）",
                                    choices=[],
                                    allow_custom_value=True,
                                    value=None
                                )
                                search_query = gr.Textbox(label="搜索查询")
                                search_size = gr.Slider(label="返回结果数", minimum=1, maximum=20, value=5, step=1)
                                search_btn = gr.Button("搜索", variant="primary")
                            
                            with gr.Column():
                                search_results = gr.DataFrame(label="搜索结果")
            
            # Event handlers
            def handle_login(username, password):
                success, message, user_info = self.authenticate_user(username, password)
                if success:
                    is_admin = user_info.get('role') == 'admin'
                    user_display = f"**当前用户:** {user_info['username']} ({user_info['role']})"
                    
                    # Get dropdown choices
                    collection_choices = self.get_collection_choices() if not is_admin else []
                    model_choices = self.get_model_choices()
                    
                    return (
                        gr.update(visible=False),  # login_form
                        gr.update(visible=True),   # main_interface
                        user_display,              # user_info_display
                        gr.update(visible=True),   # user_info_display visibility
                        user_info,                 # user_state
                        gr.update(visible=is_admin),  # user_mgmt_tab
                        gr.update(visible=is_admin),  # model_mgmt_tab
                        gr.update(visible=not is_admin),  # collection_mgmt_tab
                        gr.update(visible=not is_admin),  # search_debug_tab
                        gr.update(choices=collection_choices),  # collection_select
                        gr.update(choices=model_choices),  # model_select
                        gr.update(choices=collection_choices),  # doc_collection
                        gr.update(choices=model_choices),  # doc_model
                        gr.update(choices=collection_choices),  # delete_doc_collection
                        gr.update(choices=model_choices),  # delete_doc_model
                        gr.update(choices=collection_choices),  # search_collection
                        gr.update(choices=model_choices),  # search_model
                        "",  # clear username
                        ""   # clear password
                    )
                else:
                    return (
                        gr.update(visible=True),   # login_form stays visible
                        gr.update(visible=False),  # main_interface
                        "",                        # user_info_display
                        gr.update(visible=False),  # user_info_display visibility
                        {},                        # user_state
                        gr.update(visible=False),  # user_mgmt_tab
                        gr.update(visible=False),  # model_mgmt_tab
                        gr.update(visible=False),  # collection_mgmt_tab
                        gr.update(visible=False),  # search_debug_tab
                        gr.update(choices=[]),  # collection_select
                        gr.update(choices=[]),  # model_select
                        gr.update(choices=[]),  # doc_collection
                        gr.update(choices=[]),  # doc_model
                        gr.update(choices=[]),  # delete_doc_collection
                        gr.update(choices=[]),  # delete_doc_model
                        gr.update(choices=[]),  # search_collection
                        gr.update(choices=[]),  # search_model
                        username,                  # keep username
                        password                   # keep password
                    )
            
            def handle_logout():
                message, user_info = self.logout_user()
                return (
                    gr.update(visible=True),   # login_form
                    gr.update(visible=False),  # main_interface
                    "",                        # user_info_display
                    gr.update(visible=False),  # user_info_display visibility
                    user_info,                 # user_state
                    gr.update(visible=False),  # user_mgmt_tab
                    gr.update(visible=False),  # model_mgmt_tab
                    gr.update(visible=False),  # collection_mgmt_tab
                    gr.update(visible=False),  # search_debug_tab
                    f"ℹ️ {message}"            # login_status
                )
            
            def update_document_choices(collection_name, model_id):
                """Update document choices when collection changes"""
                doc_choices = self.get_document_choices(collection_name, model_id)
                return gr.update(choices=doc_choices)
            
            def refresh_dropdown_choices():
                """Refresh all dropdown choices"""
                collection_choices = self.get_collection_choices()
                model_choices = self.get_model_choices()
                return (
                    gr.update(choices=collection_choices),  # collection_select
                    gr.update(choices=model_choices),       # model_select
                    gr.update(choices=collection_choices),  # doc_collection
                    gr.update(choices=model_choices),       # doc_model
                    gr.update(choices=collection_choices),  # delete_doc_collection
                    gr.update(choices=model_choices),       # delete_doc_model
                    gr.update(choices=collection_choices),  # search_collection
                    gr.update(choices=model_choices),       # search_model
                )
            
            # Async wrapper for search - handle existing event loop
            def search_wrapper(collection_name, model_id, query, size):
                return syncify(self.search_documents)(collection_name, model_id, query, size)
            
            # Connect events
            login_btn.click(
                handle_login,
                inputs=[username_input, password_input],
                outputs=[
                    login_form, main_interface, user_info_display, user_info_display,
                    user_state, user_mgmt_tab, model_mgmt_tab, collection_mgmt_tab, search_debug_tab,
                    collection_select, model_select, doc_collection, doc_model,
                    delete_doc_collection, delete_doc_model, search_collection, search_model,
                    username_input, password_input
                ]
            )
            
            logout_btn.click(
                handle_logout,
                outputs=[
                    login_form, main_interface, user_info_display, user_info_display,
                    user_state, user_mgmt_tab, model_mgmt_tab, collection_mgmt_tab, search_debug_tab,
                    login_status
                ]
            )
            
            # Admin events
            refresh_users_btn.click(self.list_all_users, outputs=[users_table])
            refresh_models_btn.click(self.list_all_models, outputs=[models_table])
            
            add_user_btn.click(
                self.add_new_user,
                inputs=[new_username, new_api_key, new_email, new_role],
                outputs=[add_user_result]
            )
            
            delete_user_btn.click(
                self.delete_user,
                inputs=[delete_username],
                outputs=[delete_user_result]
            )
            
            add_model_btn.click(
                self.add_new_model,
                inputs=[new_model_id, new_service, new_model_api_key, new_model_url, new_dimensions],
                outputs=[add_model_result]
            )
            
            # User events - 修复刷新集合事件
            refresh_collections_btn.click(
                lambda: (self.list_user_collections(), *refresh_dropdown_choices()),
                outputs=[collections_table, collection_select, model_select, doc_collection, doc_model,
                        delete_doc_collection, delete_doc_model, search_collection, search_model]
            )
            
            # Update document choices when collection selection changes
            collection_select.change(
                update_document_choices,
                inputs=[collection_select, model_select],
                outputs=[delete_doc_id]
            )
            
            delete_doc_collection.change(
                update_document_choices,
                inputs=[delete_doc_collection, delete_doc_model],
                outputs=[delete_doc_id]
            )
            
            refresh_docs_btn.click(
                self.list_collection_documents,
                inputs=[collection_select, model_select],
                outputs=[documents_table]
            )
            
            add_doc_btn.click(
                self.add_text_document,
                inputs=[doc_collection, doc_model, doc_name, doc_content],
                outputs=[add_doc_result]
            )
            
            delete_doc_btn.click(
                self.delete_document,
                inputs=[delete_doc_collection, delete_doc_model, delete_doc_id],
                outputs=[delete_doc_result]
            )
            
            search_btn.click(
                search_wrapper,
                inputs=[search_collection, search_model, search_query, search_size],
                outputs=[search_results]
            )
        
        return app
    
    def launch(self, host: str = "0.0.0.0", port: int = 7860, share: bool = False):
        """Launch the Gradio interface"""
        app = self.create_interface()
        app.launch(server_name=host, server_port=port, share=share)


def create_server(client: Client, admin_username: str = None, admin_password: str = None) -> ElasticRAGServer:
    """Create and return a server instance"""
    return ElasticRAGServer(client, admin_username, admin_password)
