#!/usr/bin/env python3

import argparse, os, sys, json, httpx
from dataclasses import dataclass
from termcolor import colored
from typing import Optional, List

def get_request(base_url: str, key: str):
    headers = { 'Authorization': f'Bearer {key}' } if key else {}
    return httpx.Client(base_url=base_url, headers=headers, timeout=30)

def get_input():
    content = ''
    while not content:
        try:
            content = input(colored('>>> ', 'green'))
        except EOFError:
            print(colored('switch to multiline mode, end with Ctrl+D/EOF', 'green'))
            print(colored('>>>> ', 'cyan'), end='', flush=True)
            content = sys.stdin.read()
            print()
            break
    return content

@dataclass
class RequestArgs:
    model: str
    max_tokens: Optional[int] = None
    temperature: Optional[float] = 1.0
    top_p: Optional[float] = 1.0
    stop: Optional[List[str]] = None
    stream: bool = True

chat_history: list[dict] = []

def run_chat(request: httpx.Client, args: RequestArgs, history = True):
    url = f'/chat/completions'

    messages = [{ 'role': 'user', 'content': get_input() }]
    if history:
        chat_history.extend(messages)
        messages = chat_history
    payload = { **args.__dict__, 'messages': messages }

    if not args.stream:
        content_text = ''
        response = request.post(url, json=payload)
        if response.status_code != 200:
            if history:
                chat_history.pop()
            print(colored(f'{json.dumps(response.json(), indent=2)}', 'red'))
            return

        data = response.json()
        if 'choices' in data and len(data['choices']) > 0:
            choice = data['choices'][0]
            if 'message' in choice and 'content' in choice['message']:
                content_text = choice['message']['content']
        print(content_text)
        if history:
            chat_history.append({ 'role': 'assistant', 'content': content_text })
        return

    with request.stream(method='POST', url=url, json=payload) as response:
        if response.status_code != 200:
            if history:
                chat_history.pop()
            body = ''.join([chunk for chunk in response.iter_lines()])
            print(colored(f'{json.dumps(json.loads(body), indent=2)}', 'red'))
            return

        content_text = ''
        for chunk in response.iter_lines():
            chunk = chunk.strip()
            if chunk.startswith('data:'):
                chunk = chunk[5:].strip()
            if not chunk or chunk == '[DONE]':
                continue
            data = json.loads(chunk)
            if not data.get('choices'):
                continue
            choice = data['choices'][0]
            if 'delta' in choice and 'content' in choice['delta']:
                content_text += choice['delta']['content']
                print(choice['delta']['content'], end='', flush=True)
        print()
        if history:
            chat_history.append({ 'role': 'assistant', 'content': content_text })

def run_completion(request: httpx.Client, args: RequestArgs):
    url = f'/completions'
    payload = { **args.__dict__, 'prompt': get_input() }

    if not args.stream:
        content_text = ''
        response = request.post(url, json=payload)
        if response.status_code != 200:
            print(colored(f'{json.dumps(response.json(), indent=2)}', 'red'))
            return

        data = response.json()
        if 'choices' in data and len(data['choices']) > 0:
            choice = data['choices'][0]
            if 'text' in choice:
                content_text = choice['text']
        print(content_text)
        return

    with request.stream(method='POST', url=url, json=payload) as response:
        if response.status_code != 200:
            body = ''.join([chunk for chunk in response.iter_lines()])
            print(colored(f'{json.dumps(json.loads(body), indent=2)}', 'red'))
            return
        for chunk in response.iter_lines():
            chunk = chunk.strip()
            if chunk.startswith('data:'):
                chunk = chunk[5:].strip()
            if not chunk or chunk == '[DONE]':
                continue
            data = json.loads(chunk)
            if not data.get('choices'):
                continue
            choice = data['choices'][0]
            if 'text' in choice:
                print(choice['text'], end='', flush=True)
        print()


def run_embed(request: httpx.Client, model: str):
    url = f'/embeddings'
    payload = { 'model': model, 'input': get_input() }

    response = request.post(url, json=payload)
    if response.status_code != 200:
        print(colored(f'{json.dumps(response.json(), indent=2)}', 'red'))
        return

    data = response.json()
    if 'data' in data and len(data['data']) > 0:
        embedding = data['data'][0].get('embedding')
        if embedding:
            print(embedding)

def main():
    parser = argparse.ArgumentParser(epilog='Tips: you can switch to multiline mode using Ctrl+D/EOF.')
    parser.add_argument('--chat', action='store_true', help='chat mode (default)')
    parser.add_argument('--complete', action='store_true', help='completion mode')
    parser.add_argument('--embed', action='store_true', help='embedding mode')
    parser.add_argument('--no-history', action='store_true', help='chat without history (only for chat mode)')
    parser.add_argument('--no-stream', action='store_true', help='disable streaming output (default: False)')

    parser.add_argument('--model', type=str, required=False, default=None,
                        help='model name (default: svllm-chat/complete/embed)')
    parser.add_argument('--max-tokens', type=int, required=False, default=64,
                        help='maximum number of tokens to chat/generate (default: 64)')
    parser.add_argument('--temperature', type=float, required=False, default=1.0,
                        help='temperature for sampling (default: 1.0)')
    parser.add_argument('--top-p', type=float, required=False, default=1.0,
                        help='top-p for nucleus sampling (default: 1.0)')
    parser.add_argument('--top-k', type=int, required=False, default=-1,
                        help='top-k for sampling (default: -1, no top-k)')
    parser.add_argument('--stop', action='append', required=False, default=None,
                        help='stop sequence for generation (default: None)')

    api_key = os.environ.get('SVLLM_API_KEY')
    parser.add_argument('--key', type=str, required=False, default=api_key, help='API key for authentication')
    parser.add_argument('base_url', type=str, nargs='?', default='http://127.0.0.1:5261/v1', help='base URL for the API')

    cmd_args = parser.parse_args()

    if not cmd_args.chat and not cmd_args.complete and not cmd_args.embed:
        cmd_args.chat = True
    if not cmd_args.model:
        cmd_args.model = 'svllm-chat' if cmd_args.chat else \
                         'svllm-complete' if cmd_args.complete else \
                         'svllm-embed'

    request_args = RequestArgs(model=cmd_args.model)

    if cmd_args.max_tokens is not None:
        request_args.max_tokens = cmd_args.max_tokens
    if cmd_args.temperature is not None:
        request_args.temperature = cmd_args.temperature
    if cmd_args.top_p is not None:
        request_args.top_p = cmd_args.top_p
    if cmd_args.stop is not None:
        request_args.stop = cmd_args.stop
    if cmd_args.no_stream:
        request_args.stream = False

    request = get_request(cmd_args.base_url, cmd_args.key)
    if cmd_args.chat:
        print(colored(f'Chat mode with model: {cmd_args.model}', 'blue'))
        while True:
            try:
                run_chat(request, request_args, not cmd_args.no_history)
            except KeyboardInterrupt:
                print(colored('\nExiting chat mode.', 'red'))
                break
    elif cmd_args.complete:
        print(colored(f'Completion mode with model: {cmd_args.model}', 'blue'))
        while True:
            try:
                run_completion(request, request_args)
            except KeyboardInterrupt:
                print(colored('\nExiting completion mode.', 'red'))
                break
    elif cmd_args.embed:
        print(colored(f'Embedding mode with model: {cmd_args.model}', 'blue'))
        while True:
            try:
                run_embed(request, request_args.model)
            except KeyboardInterrupt:
                print(colored('\nExiting embedding mode.', 'red'))
                break

if __name__ == "__main__":
    main()
