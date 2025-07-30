from .protocol import Chat, Complete, Embed, Model, ModelInfo
from typing import Optional, List

''' chat '''

_chat: Optional[Chat] = None

def set_chat(chat: Chat) -> Chat:
    '''Set the chat function.'''
    global _chat
    _chat = chat
    return

def get_chat() -> Optional[Chat]:
    '''Get the chat function.'''
    return _chat

''' complete '''

_complete: Optional[Complete] = None

def set_complete(complete: Complete) -> Complete:
    '''Set the complete function.'''
    global _complete
    _complete = complete
    return _complete

def get_complete() -> Optional[Complete]:
    '''Get the complete function.'''
    return _complete

''' embed '''

_embed: Optional[Embed] = None

def set_embed(embed: Embed) -> Embed:
    '''Set the embed function.'''
    global _embed
    _embed = embed
    return _embed

def get_embed() -> Optional[Embed]:
    '''Get the embed function.'''
    return _embed

''' models '''

_models: Optional[List[Model]] = None

def set_models(models: List[Model]) -> List[Model]:
    '''Set the list of models.'''
    global _models
    _models = models
    return _models

def get_models() -> List[Model]:
    '''Get the list of models.'''
    if _models is None:
        def _create_model(base: Optional[ModelInfo]):
            if base is None:
                return None
            model_id = getattr(base, '__model__', base.__name__)
            owned_by = getattr(base, '__owner__', 'svllm')
            return Model({ 'id': model_id, 'owned_by': owned_by })

        models = [
            _create_model(get_chat()),
            _create_model(get_complete()),
            _create_model(get_embed()),
        ]
        return [m for m in models if m is not None]
    return _models or []
