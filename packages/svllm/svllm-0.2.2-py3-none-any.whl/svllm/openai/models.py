from ..base import get_models as g_get_models
from .protocol import ModelList, ModelCard
from .helpers import create_500_error

def get_models() -> ModelList:
    try:
        data = list(map(lambda m: ModelCard(**m), g_get_models()))
        return ModelList(data=data)
    except Exception as e:
        return create_500_error(str(e))
