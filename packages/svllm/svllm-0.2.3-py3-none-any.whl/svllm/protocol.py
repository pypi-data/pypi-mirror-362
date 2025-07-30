import time
from fastapi import Request
from typing import (
    Protocol,
    TypedDict,
    Callable,
    Any,
    Literal,
    Optional,
    List,
    Union,
    Generator,
    AsyncGenerator,
    Coroutine,
    runtime_checkable,
)

class Model(TypedDict):
    id: str
    owned_by: str = 'svllm'
    created: int = int(time.time())

class Message(TypedDict):
    role: Literal['user', 'assistant', 'system']
    content: str

class ModelInfo(Protocol):
    __model__: Optional[str] = None
    __owner__: Optional[str] = None

@runtime_checkable
class ChatSync(ModelInfo, Protocol):
    '''examples:
    def chat(messages: List[Message]) -> str:
        # `callback` can be used to stream response
        # callback('hello world, ')
        return 'hello world again'
    '''
    def __call__(
        self,
        messages: List[Message],
        model: str,
        request: Request,
        temperature: Optional[float] = 1.0,
        top_p: Optional[float] = 1.0,
        top_k: Optional[int] = -1,
        max_tokens: Optional[int] = None,
        stop: Optional[Union[str, List[str]]] = None,
        stream: Optional[bool] = False,
        presence_penalty: Optional[float] = 0.0,
        frequency_penalty: Optional[float] = 0.0,
        user: Optional[str] = None,
        callback: Optional[Callable[[str], Any]] = None,
    ) -> str:
        ...

@runtime_checkable
class ChatGenerator(ModelInfo, Protocol):
    '''examples:
    def chat(messages: List[Message]) -> Generator[str, Any, Optional[str]]:
        for chunk in ['hello', ' ', 'world']:
            yield chunk
    '''
    def __call__(
        self,
        messages: List[Message],
        model: str,
        request: Request,
        temperature: Optional[float] = 1.0,
        top_p: Optional[float] = 1.0,
        top_k: Optional[int] = -1,
        max_tokens: Optional[int] = None,
        stop: Optional[Union[str, List[str]]] = None,
        stream: Optional[bool] = False,
        presence_penalty: Optional[float] = 0.0,
        frequency_penalty: Optional[float] = 0.0,
        user: Optional[str] = None,
    ) -> Generator[str, Any, Optional[str]]:
        ...

@runtime_checkable
class ChatCoroutine(ModelInfo, Protocol):
    '''examples:
    async def chat(messages: List[Message]) -> Coroutine[Any, Any, str]:
        return 'hello world'
    '''
    async def __call__(
        self,
        messages: List[Message],
        model: str,
        request: Request,
        temperature: Optional[float] = 1.0,
        top_p: Optional[float] = 1.0,
        top_k: Optional[int] = -1,
        max_tokens: Optional[int] = None,
        stop: Optional[Union[str, List[str]]] = None,
        stream: Optional[bool] = False,
        presence_penalty: Optional[float] = 0.0,
        frequency_penalty: Optional[float] = 0.0,
        user: Optional[str] = None,
        callback: Optional[Callable[[str], Any]] = None,
    ) -> Coroutine[Any, Any, str]:
        ...

@runtime_checkable
class ChatAsyncGenerator(ModelInfo, Protocol):
    '''examples:
    async def chat(messages: List[Message]) -> AsyncGenerator[str, str]:
        for chunk in ['hello', ' ', 'world']:
            yield chunk
    '''
    async def __call__(
        self,
        messages: List[Message],
        model: str,
        request: Request,
        temperature: Optional[float] = 1.0,
        top_p: Optional[float] = 1.0,
        top_k: Optional[int] = -1,
        max_tokens: Optional[int] = None,
        stop: Optional[Union[str, List[str]]] = None,
        stream: Optional[bool] = False,
        presence_penalty: Optional[float] = 0.0,
        frequency_penalty: Optional[float] = 0.0,
        user: Optional[str] = None,
    ) -> AsyncGenerator[str, str]:
        ...

Chat = Union[
    ChatSync,
    ChatGenerator,
    ChatCoroutine,
    ChatAsyncGenerator,
]

@runtime_checkable
class CompleteSync(ModelInfo, Protocol):
    '''examples:
    def complete(prompt: str) -> str:
        # `callback` can be used to stream response
        # callback('hello world, ')
        return 'hello world again'
    '''
    def __call__(
        self,
        prompt: str,
        model: str,
        request: Request,
        suffix: Optional[str] = None,
        temperature: Optional[float] = 1.0,
        top_p: Optional[float] = 1.0,
        top_k: Optional[int] = -1,
        max_tokens: Optional[int] = None,
        stop: Optional[Union[str, List[str]]] = None,
        stream: Optional[bool] = False,
        logprobs: Optional[int] = None,
        echo: Optional[bool] = False,
        presence_penalty: Optional[float] = 0.0,
        frequency_penalty: Optional[float] = 0.0,
        user: Optional[str] = None,
        best_of: Optional[int] = None,
        callback: Optional[Callable[[str], Any]] = None,
    ) -> str:
        ...

@runtime_checkable
class CompleteGenerator(ModelInfo, Protocol):
    '''examples:
    def complete(prompt: str) -> Generator[str, Any, Optional[str]]:
        for chunk in ['hello', ' ', 'world']:
            yield chunk
    '''
    def __call__(
        self,
        prompt: str,
        model: str,
        request: Request,
        suffix: Optional[str] = None,
        temperature: Optional[float] = 1.0,
        top_p: Optional[float] = 1.0,
        top_k: Optional[int] = -1,
        max_tokens: Optional[int] = None,
        stop: Optional[Union[str, List[str]]] = None,
        stream: Optional[bool] = False,
        logprobs: Optional[int] = None,
        echo: Optional[bool] = False,
        presence_penalty: Optional[float] = 0.0,
        frequency_penalty: Optional[float] = 0.0,
        user: Optional[str] = None,
        best_of: Optional[int] = None,
    ) -> Generator[str, Any, Optional[str]]:
        ...

@runtime_checkable
class CompleteCoroutine(ModelInfo, Protocol):
    '''examples:
    async def complete(prompt: str) -> Coroutine[Any, Any, str]:
        return 'hello world'
    '''
    async def __call__(
        self,
        prompt: str,
        model: str,
        request: Request,
        suffix: Optional[str] = None,
        temperature: Optional[float] = 1.0,
        top_p: Optional[float] = 1.0,
        top_k: Optional[int] = -1,
        max_tokens: Optional[int] = None,
        stop: Optional[Union[str, List[str]]] = None,
        stream: Optional[bool] = False,
        logprobs: Optional[int] = None,
        echo: Optional[bool] = False,
        presence_penalty: Optional[float] = 0.0,
        frequency_penalty: Optional[float] = 0.0,
        user: Optional[str] = None,
        best_of: Optional[int] = None,
        callback: Optional[Callable[[str], Any]] = None,
    ) -> Coroutine[Any, Any, str]:
        ...

@runtime_checkable
class CompleteAsyncGenerator(ModelInfo, Protocol):
    '''examples:
    async def complete(prompt: str) -> AsyncGenerator[str, str]:
        for chunk in ['hello', ' ', 'world']:
            yield chunk
    '''
    async def __call__(
        self,
        prompt: str,
        model: str,
        request: Request,
        suffix: Optional[str] = None,
        temperature: Optional[float] = 1.0,
        top_p: Optional[float] = 1.0,
        top_k: Optional[int] = -1,
        max_tokens: Optional[int] = None,
        stop: Optional[Union[str, List[str]]] = None,
        stream: Optional[bool] = False,
        logprobs: Optional[int] = None,
        echo: Optional[bool] = False,
        presence_penalty: Optional[float] = 0.0,
        frequency_penalty: Optional[float] = 0.0,
        user: Optional[str] = None,
        best_of: Optional[int] = None,
    ) -> AsyncGenerator[str, str]:
        ...

Complete = Union[
    CompleteSync,
    CompleteGenerator,
    CompleteCoroutine,
    CompleteAsyncGenerator,
]

@runtime_checkable
class EmbedSync(ModelInfo, Protocol):
    '''examples:
    def embed(input: List[str]) -> List[List[float]]:
        return [[0.1, 0.2, 0.3], ...]
    '''
    def __call__(
        self,
        input: List[str],
        model: str,
        request: Request,
        engine: Optional[str] = None,
        user: Optional[str] = None,
        encoding_format: Optional[str] = None,
    ) -> List[List[float]]:
        ...

@runtime_checkable
class EmbedAsync(ModelInfo, Protocol):
    '''examples:
    async def embed(input: List[str]) -> Coroutine[Any, Any, List[List[float]]]:
        return [[0.1, 0.2, 0.3], ...]
    '''
    async def __call__(
        self,
        input: List[str],
        model: str,
        request: Request,
        engine: Optional[str] = None,
        user: Optional[str] = None,
        encoding_format: Optional[str] = None,
    ) -> List[List[float]]:
        ...

Embed = Union[
    EmbedSync,
    EmbedAsync,
]

# Exception for token length exceeding
class LengthException(Exception):
    def __init__(self, message: str = ''):
        super().__init__(message)
        self.message = message

class RequestItem(TypedDict):
    content: Any
    timestamp: float

class ResponseItem(TypedDict):
    content: Any
    timestamp: float

class HistoryItem(TypedDict):
    request: RequestItem
    response: ResponseItem
    type: Literal['chat', 'complete', 'embed'] = 'chat'

class SystemStatus(TypedDict):
    history: int = 0 # history length
    start_time: float = 0
    chat_count: int = 0
    complete_count: int = 0
    embed_count: int = 0
