import asyncio, random
from typing import List

zen = '''\
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
'''

async def chat(messages: List[dict]):
    # print('Received messages:', messages)
    for line in zen.split('\n'):
        await asyncio.sleep(0.1)
        yield line + '\n'
        # if line.startswith('Errors'):
        #     raise svllm.LengthException()

chat.__model__ = 'svllm-chat'
chat.__owner__ = 'svllm'

async def complete(prompt: str):
    # Simulate a chat function that generates text based on the prompt
    for line in zen.split('\n'):
        await asyncio.sleep(0.1)
        yield line + '\n'
        # if line.startswith('Errors'):
        #     raise svllm.LengthException()

complete.__model__ = 'svllm-complete'
complete.__owner__ = 'svllm'

async def embed(input: List[str]):
    # Simulate an embedding function that returns a list of floats
    await asyncio.sleep(0.1)
    return [[round(random.random(), 4) for _ in range(64)] for _ in range(len(input))]

embed.__model__ = 'svllm-embed'
embed.__owner__ = 'svllm'
