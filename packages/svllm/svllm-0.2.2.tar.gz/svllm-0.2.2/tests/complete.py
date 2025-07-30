from fastapi.testclient import TestClient
import json

def run_sync_complete_tests(client: TestClient):
    print('Running sync complete tests...')
    response = client.post('/v1/completions', json={
        'model': 'svllm-complete',
        'prompt': 'Hello',
        'stream': False
    })
    assert response.status_code == 200
    assert 'choices' in response.json()
    assert isinstance(response.json()['choices'], list)
    assert len(response.json()['choices']) == 1
    assert 'text' in response.json()['choices'][0]
    assert isinstance(response.json()['choices'][0]['text'], str)
    assert response.json()['choices'][0]['text'].startswith('The Zen of Python')

def run_stream_complete_tests(client: TestClient):
    print('Running stream complete tests...')
    response = client.post('/v1/completions', json={
        'model': 'svllm-complete',
        'prompt': 'Hello',
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
        assert 'text' in data['choices'][0]
        assert isinstance(data['choices'][0]['text'], str)
        content += data['choices'][0]['text']
    assert content.startswith('The Zen of Python')

def run_complete_tests(client: TestClient):
    run_sync_complete_tests(client)
    run_stream_complete_tests(client)
