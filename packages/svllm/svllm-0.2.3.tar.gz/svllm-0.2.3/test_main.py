from fastapi.testclient import TestClient
import src.svllm as svllm
from tests.models import run_models_tests
from tests.chat import run_chat_tests
from tests.complete import run_complete_tests
from tests.embed import run_embed_tests

svllm.set_chat(svllm.examples.chat)
svllm.set_complete(svllm.examples.complete)
svllm.set_embed(svllm.examples.embed)

client = TestClient(svllm.create_app())

def test_models():
    run_models_tests(client)

def test_chat():
    run_chat_tests(client)

def test_complete():
    run_complete_tests(client)

def test_embed():
    run_embed_tests(client)
