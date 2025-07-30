from fastapi.testclient import TestClient
import json

def run_sync_chat_tests(client: TestClient):
    print('Running sync chat tests...')
    response = client.post('/v1/chat/completions', json={
        'model': 'svllm-chat',
        'messages': [{'role': 'user', 'content': 'Hello'}],
        'stream': False
    })
    assert response.status_code == 200
    assert 'choices' in response.json()
    assert isinstance(response.json()['choices'], list)
    assert len(response.json()['choices']) == 1
    assert 'message' in response.json()['choices'][0]
    assert response.json()['choices'][0]['message']['role'] == 'assistant'
    assert 'content' in response.json()['choices'][0]['message']
    assert isinstance(response.json()['choices'][0]['message']['content'], str)
    assert response.json()['choices'][0]['message']['content'].startswith('The Zen of Python')


def run_stream_chat_tests(client: TestClient):
    print('Running stream chat tests...')
    response = client.post('/v1/chat/completions', json={
        'model': 'svllm-chat',
        'messages': [{'role': 'user', 'content': 'Hello'}],
        'stream': True
    })

    assert response.status_code == 200

    content = ''
    for chunk in response.iter_lines():
        chunk = chunk.strip()
        if chunk.startswith('data:'):
            chunk = chunk[5:].strip()
        if not chunk or chunk == '[DONE]':
            continue
        data = json.loads(chunk)
        assert 'choices' in data
        assert isinstance(data['choices'], list)
        assert len(data['choices']) == 1
        assert 'delta' in data['choices'][0]
        if 'content' in data['choices'][0]['delta']:
            content += data['choices'][0]['delta']['content']
    assert content.startswith('The Zen of Python')

def run_chat_tests(client: TestClient):
    run_sync_chat_tests(client)
    run_stream_chat_tests(client)
