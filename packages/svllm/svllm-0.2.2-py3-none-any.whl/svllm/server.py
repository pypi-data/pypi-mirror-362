from fastapi import FastAPI, APIRouter
from .routes import add_routes as add_system_routes
from .openai import add_routes as add_openai_routes

def create_app(title='svllm', description='svllm api', prefix='', root_path='', *args, **kwargs) -> FastAPI:
    app = FastAPI(title=title, description=description, root_path=root_path, *args, **kwargs)
    app.include_router(add_system_routes(APIRouter(prefix=prefix)))
    app.include_router(add_openai_routes(APIRouter(prefix=prefix + '/v1')))
    return app
