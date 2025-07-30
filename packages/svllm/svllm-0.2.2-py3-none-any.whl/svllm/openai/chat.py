import inspect, time
from typing import List
from fastapi import Request
from fastapi.responses import StreamingResponse

from ..protocol import LengthException, Message, Chat, RequestItem, ResponseItem
from ..base import get_chat as g_get_chat
from ..helpers import agg, asyncgen, tokens
from ..services import add_history
from . import helpers
from .protocol import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionResponseChoice,
    ChatCompletionResponseStreamChoice,
    ChatCompletionStreamResponse,
    ChatMessage,
    DeltaMessage,
    UsageInfo,
)

def get_messages(request: ChatCompletionRequest) -> List[Message]:
    openai_messages = request.messages
    if isinstance(openai_messages, str):
        return [{ 'role': 'user', 'content': openai_messages }]
    elif isinstance(openai_messages, list):
        messages: List[Message] = []
        for (idx, msg) in enumerate(openai_messages):
            if 'content' not in msg:
                raise ValueError(f'Message at index {idx} is missing \'content\' field.')
            # ignore no `text` type` content now
            if isinstance(msg['content'], dict) and msg['content'].get('type') != 'text':
                continue
            if isinstance(msg['content'], dict) and 'text' not in msg['content']:
                raise ValueError(f'Message at index {idx} is missing \'text\' field in \'content\'.')

            # we need also handle `system` roles correctly here
            prev_role = messages[idx - 1]['role'] if idx > 0 else None
            role = msg.get('role', 'user' if prev_role != 'user' else 'assistant')
            content = msg['content'] if isinstance(msg['content'], str) else msg['content']['text']
            messages.append({ 'role': role, 'content': content })
        return messages

def get_arguments(request: ChatCompletionRequest, sig: inspect.Signature) -> dict:
    arguments = {}
    if 'model' in sig.parameters:
        arguments['model'] = request.model
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
    if 'presence_penalty' in sig.parameters:
        arguments['presence_penalty'] = request.presence_penalty
    if 'frequency_penalty' in sig.parameters:
        arguments['frequency_penalty'] = request.frequency_penalty
    if 'user' in sig.parameters:
        arguments['user'] = request.user
    return arguments

async def get_chat_completion_response(
        request: ChatCompletionRequest,
        chat: Chat,
        arguments: dict,
        messages: List[Message] = [],
    ) -> ChatCompletionResponse:
    history_request = RequestItem(
        content=request.messages,
        timestamp=time.time(),
    )

    async def create_choice(index: int) -> ChatCompletionResponseChoice:
        answer = ''
        try:
            async for chunk in asyncgen(chat, arguments):
                answer += chunk
            return ChatCompletionResponseChoice(
                index=index,
                message=ChatMessage(role='assistant', content=answer),
                finish_reason='stop',
            )
        except LengthException as e:
            return ChatCompletionResponseChoice(
                index=index,
                message=ChatMessage(role='assistant', content=answer),
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
                'type': 'chat',
            })

    choices = [await create_choice(i) for i in range(request.n or 1)] # serial
    prompt_tokens = sum(map(lambda m: tokens(m.get('content', '')), messages))
    completion_tokens = sum(map(lambda c: tokens(c.message.content), choices))

    return ChatCompletionResponse(
        model=request.model,
        choices=choices,
        usage=UsageInfo(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        ),
    )

async def get_chat_completion_stream_response(
        request: ChatCompletionRequest,
        chat: Chat,
        arguments: dict,
    ) -> StreamingResponse:
    history_request = RequestItem(
        content=request.messages,
        timestamp=time.time(),
    )

    async def create_stream_choice(index: int):
        try:
            response_content = ''
            async for chunk in agg(asyncgen(chat, arguments)):
                response_content += chunk
                yield ChatCompletionResponseStreamChoice(
                    index=index,
                    delta=DeltaMessage(role='assistant', content=chunk),
                    finish_reason=None,
                )
            yield ChatCompletionResponseStreamChoice(
                index=index,
                delta=DeltaMessage(),
                finish_reason='stop',
            )
        except LengthException as e:
            yield ChatCompletionResponseStreamChoice(
                index=index,
                delta=DeltaMessage(),
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
                'type': 'chat',
            })

    all_choices = [
        ChatCompletionResponseStreamChoice(
            index=i,
            delta=DeltaMessage(),
            finish_reason=None,
        ) for i in range(request.n or 1)
    ]

    async def stream_response():
        nonlocal all_choices
        for i in range(request.n or 1): # serial
            async for choice in create_stream_choice(i):
                all_choices[i] = choice
                yield 'data: ' + ChatCompletionStreamResponse(
                    model=request.model,
                    choices=all_choices,
                ).model_dump_json() + '\n\n'
        yield 'data: [DONE]\n\n'
    return StreamingResponse(stream_response(), media_type='text/event-stream')

async def create_chat_completions(request: ChatCompletionRequest, raw_request: Request):
    try:
        chat = g_get_chat()
        if not chat:
            return helpers.create_501_error('chat')

        chat_sig = inspect.signature(chat)
        arguments = get_arguments(request, chat_sig)

        if 'request' in chat_sig.parameters:
            arguments['request'] = raw_request

        messages = get_messages(request)
        if 'messages' in chat_sig.parameters:
            arguments['messages'] = messages

        if not request.stream:
            return await get_chat_completion_response(request, chat, arguments, messages)

        return await get_chat_completion_stream_response(request, chat, arguments)
    except ValueError as e:
        return helpers.create_500_error(str(e))
