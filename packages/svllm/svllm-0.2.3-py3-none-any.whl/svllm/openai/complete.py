import inspect, time
from fastapi import Request
from fastapi.responses import StreamingResponse

from ..protocol import LengthException, Complete, RequestItem, ResponseItem
from ..base import get_complete as g_get_complete
from ..helpers import agg, asyncgen, tokens
from ..services import add_history, get_system_status
from . import helpers
from .protocol import (
    CompletionRequest,
    CompletionResponse,
    CompletionResponseChoice,
    CompletionResponseStreamChoice,
    CompletionStreamResponse,
    UsageInfo,
)

def get_arguments(request: CompletionRequest, sig: inspect.Signature) -> dict:
    arguments = {}
    if 'prompt' in sig.parameters:
        arguments['prompt'] = request.prompt
    if 'model' in sig.parameters:
        arguments['model'] = request.model
    if 'suffix' in sig.parameters:
        arguments['suffix'] = request.suffix
    if 'temperature' in sig.parameters:
        arguments['temperature'] = request.temperature
    if 'top_p' in sig.parameters:
        arguments['top_p'] = request.top_p
    if 'top_k' in sig.parameters:
        arguments['top_k'] = request.top_k
    if 'max_tokens' in sig.parameters:
        arguments['max_tokens'] = request.max_tokens
    if 'stop' in sig.parameters:
        arguments['stop'] = request.stop
    if 'stream' in sig.parameters:
        arguments['stream'] = request.stream
    if 'logprobs' in sig.parameters:
        arguments['logprobs'] = request.logprobs
    if 'echo' in sig.parameters:
        arguments['echo'] = request.echo
    if 'presence_penalty' in sig.parameters:
        arguments['presence_penalty'] = request.presence_penalty
    if 'frequency_penalty' in sig.parameters:
        arguments['frequency_penalty'] = request.frequency_penalty
    if 'user' in sig.parameters:
        arguments['user'] = request.user
    if 'best_of' in sig.parameters:
        arguments['best_of'] = request.best_of
    return arguments

async def get_completion_response(
        request: CompletionRequest,
        complete: Complete,
        arguments: dict,
    ) -> CompletionResponse:
    history_request = RequestItem(
        content=request.prompt,
        timestamp=time.time(),
    )

    async def create_choice(index: int) -> CompletionResponseChoice:
        answer = ''
        try:
            async for chunk in asyncgen(complete, arguments):
                answer += chunk
            return CompletionResponseChoice(
                index=index,
                text=answer,
                finish_reason='stop',
                # TODO: logprobs
            )
        except LengthException as e:
            return CompletionResponseChoice(
                index=index,
                message=answer,
                finish_reason='length',
            )
        finally:
            history_response = ResponseItem(
                content=answer,
                timestamp=time.time(),
            )
            add_history({
                'request': history_request,
                'response': history_response,
                'type': 'complete',
            })

    choices = [await create_choice(i) for i in range(request.n or 1)] # serial
    prompt_tokens = sum(map(lambda text: tokens(text), request.prompt))
    completion_tokens = sum(map(lambda c: tokens(c.text), choices))

    return CompletionResponse(
        model=request.model,
        choices=choices,
        usage=UsageInfo(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        ),
    )

async def get_completion_stream_response(
        request: CompletionRequest,
        complete: Complete,
        arguments: dict,
    ) -> StreamingResponse:
    history_request = RequestItem(
        content=request.prompt,
        timestamp=time.time(),
    )

    async def create_stream_choice(index: int):
        try:
            response_content = ''
            async for chunk in agg(asyncgen(complete, arguments)):
                response_content += chunk
                yield CompletionResponseStreamChoice(
                    index=index,
                    text=chunk,
                    finish_reason=None,
                    # TODO: logprobs
                )
            yield CompletionResponseStreamChoice(
                index=index,
                text='',
                finish_reason='stop',
            )
        except LengthException as e:
            yield CompletionResponseStreamChoice(
                index=index,
                text='',
                finish_reason='length',
            )
        finally:
            history_response = ResponseItem(
                content=response_content,
                timestamp=time.time(),
            )
            add_history({
                'request': history_request,
                'response': history_response,
                'type': 'complete',
            })

    all_choices = [
        CompletionResponseStreamChoice(
            index=i,
            text='',
            finish_reason=None,
        ) for i in range(request.n or 1)
    ]

    async def stream_response():
        nonlocal all_choices
        for i in range(request.n or 1): # serial
            async for choice in create_stream_choice(i):
                all_choices[i] = choice
                yield 'data: ' + CompletionStreamResponse(
                    model=request.model,
                    choices=all_choices,
                ).model_dump_json() + '\n\n'
        yield 'data: [DONE]\n\n'
    return StreamingResponse(stream_response(), media_type='text/event-stream')

async def create_completions(request: CompletionRequest, raw_request: Request):
    try:
        complete = g_get_complete()
        if not complete:
            return helpers.create_501_error('complete')

        complete_sig = inspect.signature(complete)
        arguments = get_arguments(request, complete_sig)

        if 'request' in complete_sig.parameters:
            arguments['request'] = raw_request

        if not request.stream:
            return await get_completion_response(request, complete, arguments)

        return await get_completion_stream_response(request, complete, arguments)
    except Exception as e:
        return helpers.create_500_error(str(e))
