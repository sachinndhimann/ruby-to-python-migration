import requests
import requests_mock

def test_api():
    with requests_mock.Mocker() as mocker:
        mocker.get('http://localhost:3000/api/items', status_code=200, json=["item1", "item2"])
        mocker.post('http://localhost:3000/api/items', status_code=201, json=["item3"])
        response = requests.get('http://localhost:3000/api/items')
        assert response.status_code == 200
        assert all(item in response.json() for item in ["item1", "item2"])

        response = requests.post('http://localhost:3000/api/items', json={"item": {"name": "item3"}})
        assert response.status_code == 201
        assert all(item in response.json() for item in ["item3"])

