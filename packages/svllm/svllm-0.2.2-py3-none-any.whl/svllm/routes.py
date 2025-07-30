from fastapi import APIRouter
from typing import List
from . import services, protocol

def add_routes(router: APIRouter) -> APIRouter:
    router.add_api_route(
        '/system/status',
        services.get_system_status,
        methods=['GET'],
        response_model=protocol.SystemStatus,
        tags=['System'],
    )

    router.add_api_route(
        '/system/status',
        services.set_system_status,
        methods=['POST'],
        response_model=protocol.SystemStatus,
        tags=['System'],
    )

    router.add_api_route(
        '/system/history',
        services.get_history,
        methods=['GET'],
        response_model=List[protocol.HistoryItem],
        tags=['System'],
    )
    return router
