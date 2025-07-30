from fastapi.testclient import TestClient

def run_embed_tests(client: TestClient):
    print('Running embedding tests...')
    response = client.post('/v1/embeddings', json={
        'model': 'svllm-embed',
        'input': ['hello', 'world'],
    })
    assert response.status_code == 200
    assert 'data' in response.json()
    assert isinstance(response.json()['data'], list)
    assert len(response.json()['data']) == 2
    assert 'embedding' in response.json()['data'][0]
    assert isinstance(response.json()['data'][0]['embedding'], list)
    assert len(response.json()['data'][0]['embedding']) > 0
