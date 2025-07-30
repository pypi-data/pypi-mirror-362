from fastapi import FastAPI, APIRouter
from .routes import add_routes as add_system_routes
from .openai import add_routes as add_openai_routes

def create_app(title='svllm', description='svllm api', prefix='/v1', root_path='', *args, **kwargs) -> FastAPI:
    app = FastAPI(title=title, description=description, root_path=root_path, *args, **kwargs)
    app.include_router(add_system_routes(APIRouter(prefix='')))
    app.include_router(add_openai_routes(APIRouter(prefix=prefix)))
    return app
