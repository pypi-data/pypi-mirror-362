from .__about__ import __version__
from .server import create_app
from .protocol import Chat, Complete, Embed, Model, Message, LengthException
from . import base, examples, openai, protocol, routes

set_chat = base.set_chat
get_chat = base.get_chat

set_complete = base.set_complete
get_complete = base.get_complete

set_embed = base.set_embed
get_embed = base.get_embed

set_models = base.set_models
get_models = base.get_models

__all__ = [
    '__version__',
    'create_app',

    'set_chat',
    'get_chat',

    'set_complete',
    'get_complete',

    'set_embed',
    'get_embed',

    'set_models',
    'get_models',

    'base',
    'examples',
    'protocol',
    'routes',

    'Chat',
    'Complete',
    'Embed',
    'Model',
    'Message',
    'LengthException',

    'openai',
]
