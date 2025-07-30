from fastapi import APIRouter

from . import chat, complete, embed, protocol, models

def add_routes(router: APIRouter) -> APIRouter:
    router.add_api_route(
        '/models',
        models.get_models,
        methods=['GET'],
        response_model=protocol.ModelList,
        tags=['OpenAI'],
    )

    router.add_api_route(
        '/chat/completions',
        chat.create_chat_completions,
        methods=['POST'],
        response_model=protocol.ChatCompletionResponse,
        tags=['OpenAI'],
    )

    router.add_api_route(
        '/completions',
        complete.create_completions,
        methods=['POST'],
        response_model=protocol.CompletionResponse,
        tags=['OpenAI'],
    )

    router.add_api_route(
        '/embeddings',
        embed.create_embeddings,
        methods=['POST'],
        response_model=protocol.EmbeddingsResponse,
        tags=['OpenAI'],
    )
    return router
