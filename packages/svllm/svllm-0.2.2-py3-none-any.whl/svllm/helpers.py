import inspect, asyncio, time, typing

def tokens(str: str) -> int:
    return len(str)

async def asyncgen(
        func: typing.Callable,
        kvargs: dict,
    ) -> typing.AsyncGenerator[str, None]:

    '''Convert a chat/complete function to an async generator.'''
    sentinel = object()
    queue = asyncio.Queue()

    sig = inspect.signature(func)
    if 'callback' in sig.parameters:
        def callback(chunk: str):
            queue.put_nowait(chunk)
        kvargs['callback'] = callback

    async def async_task():
        try:
            if inspect.isasyncgenfunction(func):
                async for chunk in func(**kvargs):
                    queue.put_nowait(chunk)
            elif inspect.iscoroutinefunction(func):
                queue.put_nowait(await func(**kvargs))
            elif inspect.isgeneratorfunction(func):
                def iter_gen():
                    for chunk in func(**kvargs):
                        queue.put_nowait(chunk)
                await asyncio.to_thread(iter_gen)
            else:
                co = asyncio.to_thread(func, **kvargs)
                queue.put_nowait(await co)
        finally:
            queue.put_nowait(sentinel)

    asyncio.create_task(async_task())

    while True:
        chunk = await queue.get()
        if not chunk:
            continue
        if chunk is sentinel:
            break
        yield chunk

async def agg(ag: typing.AsyncGenerator, interval: float = 0.05):
    '''Aggregate async generator chunks into a single string.'''
    content, timestamp = '', time.time()
    async for chunk in ag:
        content += chunk
        if time.time() - timestamp > interval:
            yield content
            content, timestamp = '', time.time()
    if content:
        yield content
