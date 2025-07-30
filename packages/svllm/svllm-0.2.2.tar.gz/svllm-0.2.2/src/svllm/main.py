#!/usr/bin/env python3

import sys, datetime, argparse, importlib, svllm, uvicorn
from fastapi import Request, Response
from termcolor import colored

def import_from(location: str, name: str):
    module_str, _, attrs_str = location.partition(':')
    if not module_str:
        raise ValueError(f'{name} must be in the format \'module:attr\'.')
    instance = importlib.import_module(module_str)
    for attr in (attrs_str or name).split('.'):
        instance = getattr(instance, attr, None)
    if not instance:
        raise ImportError(f'\'{attrs_str or name}\' not found in \'{module_str}\'')
    return (instance, f'{module_str}:{attrs_str or name}')

def log(message: str, level='INFO'):
    color: str = 'red' if level == 'ERROR' else 'green' if level == 'INFO' else 'yellow'
    time_part = colored(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]', 'cyan')
    print(time_part, f'{colored(level, color)}: {message}')

async def log_request(request: Request):
    log(f'Request {request.method} {request.url}', 'DEBUG')
    try:
        body = await request.body()
        if body:
            log(f'Request body: {body.decode()}', 'DEBUG')
    except Exception as e:
        log(f'Error reading request body: {e}', 'DEBUG')

async def log_response(response: Response):
    log(f'Response {response.status_code}', 'DEBUG')
    if hasattr(response, 'body_iterator'):
        original_body_iterator = response.body_iterator
        async def new_iterator():
            async for chunk in original_body_iterator:
                log(f'Response chunk: {chunk.decode()}', 'DEBUG')
                yield chunk
        response.body_iterator = new_iterator()
    elif hasattr(response, 'body'):
        try:
            log(f'Response body: {response.body.decode()}')
        except Exception as e:
            log(f'Error reading response body: {e}', 'DEBUG')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--chat', type=str, required=False, help='chat function')
    parser.add_argument('--complete', type=str, required=False, help='complete function')
    parser.add_argument('--embed', type=str, required=False, help='embed function')

    parser.add_argument('--prefix', type=str, default='/v1', required=False, help='api prefix')
    parser.add_argument('--host', type=str, default='127.0.0.1', required=False, help='host address')
    parser.add_argument('--port', type=int, default=5261, required=False, help='port number')
    parser.add_argument('--debug', action='store_true', required=False, help='print debug output')

    cmd_args = parser.parse_args()
    sys.path.insert(0, '.')

    if cmd_args.chat:
        chat, location = import_from(cmd_args.chat, 'chat')
        svllm.base.set_chat(chat)
        log(f'Chat function set to ' + colored(location, 'yellow'))

    if cmd_args.complete:
        complete, location = import_from(cmd_args.complete, 'complete')
        svllm.base.set_complete(complete)
        log(f'Complete function set to ' + colored(location, 'yellow'))

    if cmd_args.embed:
        embed, location = import_from(cmd_args.embed, 'embed')
        svllm.base.set_embed(embed)
        log(f'Embed function set to ' + colored(location, 'yellow'))

    app = svllm.create_app(prefix=cmd_args.prefix)

    if cmd_args.debug:
        @app.middleware('http')
        async def debug_middleware(request: Request, call_next):
            await log_request(request)
            response = await call_next(request)
            await log_response(response)
            return response

    uvicorn.run(app, host=cmd_args.host, port=cmd_args.port)

if __name__ == "__main__":
    main()
