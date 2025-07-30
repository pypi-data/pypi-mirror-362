from fastapi.testclient import TestClient

def run_models_tests(client: TestClient):
    print('Running models tests...')
    response = client.get('/v1/models')
    assert response.status_code == 200
    assert 'data' in response.json()
    assert isinstance(response.json()['data'], list)
    assert len(response.json()['data']) == 3
    assert response.json()['data'][0]['id'] == 'svllm-chat'
    assert response.json()['data'][1]['id'] == 'svllm-complete'
    assert response.json()['data'][2]['id'] == 'svllm-embed'
