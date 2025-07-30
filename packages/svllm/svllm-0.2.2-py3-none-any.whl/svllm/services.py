import time, os
from typing import List

from .protocol import SystemStatus, HistoryItem
from fastapi import HTTPException, Depends, Query
from fastapi.security import HTTPBearer

_secret: str = os.getenv('SVLLM_SECRET', '')

_status: SystemStatus = SystemStatus(
    start_time=time.time(),
    history=1000,
    chat_count=0,
    complete_count=0,
    embed_count=0,
)
_history: List[HistoryItem] = []

# fastapi depends
def auth_admin(
        authorization = Depends(HTTPBearer(auto_error=False)),
        secret: str | None = Query(None, alias='secret')) -> None:
    if not _secret:
        raise HTTPException(status_code=500, detail='System secret not configured.')
    bearer_secret = authorization.credentials if authorization else ''
    if bearer_secret != _secret and secret != _secret:
        raise HTTPException(status_code=401, detail='Unauthorized')

def truncate_history(max_length: int = 1000) -> List[HistoryItem]:
    global _history
    if len(_history) > max_length:
        _history = _history[-max_length:]
    return _history

def get_history(
        type: str = 'all',
        page: int = 1,
        per_page: int = 10,
        _auth = Depends(auth_admin)) -> List[HistoryItem]:
    items = _history
    if type != 'all':
        items = [item for item in _history if item['type'] == type]
    return items[(page - 1) * per_page: page * per_page]

def get_system_status(_auth = Depends(auth_admin)) -> SystemStatus:
    return _status

def set_system_status(payload: dict, _auth = Depends(auth_admin)) -> SystemStatus:
    if 'history' in payload:
        _status['history'] = payload['history']
        truncate_history(_status['history'])
    if 'start_time' in payload:
        _status['start_time'] = payload['start_time']
    if 'chat_count' in payload:
        _status['chat_count'] = payload['chat_count']
    if 'complete_count' in payload:
        _status['complete_count'] = payload['complete_count']
    if 'embed_count' in payload:
        _status['embed_count'] = payload['embed_count']
    return _status

def add_history(item: HistoryItem) -> List[HistoryItem]:
    global _history
    if not _status['history']:
        return _history
    _history.append(item)
    return truncate_history(_status['history'])
