import asyncio, inspect
from typing import List
from fastapi import Request

from ..protocol import Embed
from ..base import get_embed as g_get_embed
from ..helpers import tokens
from . import helpers
from .protocol import Embedding, EmbeddingUsageInfo, EmbeddingsRequest, EmbeddingsResponse

def get_arguments(request: EmbeddingsRequest, sig: inspect.Signature) -> dict:
    arguments = {}
    if 'model' in sig.parameters:
        arguments['model'] = request.model
    if 'engine' in sig.parameters:
        arguments['engine'] = request.engine
    if 'user' in sig.parameters:
        arguments['user'] = request.user
    if 'encoding_format' in sig.parameters:
        arguments['encoding_format'] = request.encoding_format
    return arguments

async def embed_async(embed: Embed, kvargs: dict) -> List[List[float]]:
    result = await asyncio.to_thread(embed, **kvargs)
    return await result if inspect.iscoroutine(result) else result

async def create_embeddings(request: EmbeddingsRequest, raw_request: Request) -> EmbeddingsResponse:
    try:
        embed = g_get_embed()
        if not embed:
            return helpers.create_501_error('embed')

        embed_sig = inspect.signature(embed)
        arguments = get_arguments(request, embed_sig)

        if 'request' in embed_sig.parameters:
            arguments['request'] = raw_request

        input = request.input if isinstance(request.input, list) else [request.input]
        if 'input' in embed_sig.parameters:
            arguments['input'] = input

        embeddings: List[Embedding] = []
        for (i, data) in enumerate(await embed_async(embed, arguments)):
            embeddings.append(Embedding(embedding=data, index=i))

        prompt_tokens = sum(tokens(item) for item in input)

        return EmbeddingsResponse(
            model=request.model,
            data=embeddings,
            usage=EmbeddingUsageInfo(
                prompt_tokens=prompt_tokens,
                total_tokens=prompt_tokens,
            ),
        )
    except Exception as e:
        return helpers.create_500_error(str(e))
