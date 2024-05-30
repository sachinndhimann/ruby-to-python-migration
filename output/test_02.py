import requests
import requests_mock

def test_api():
    with requests_mock.Mocker() as mocker:
        mocker.get('http://localhost:3000/api/items/1', status_code=200, json=["item1"])
        mocker.put('http://localhost:3000/api/items/1', status_code=200, json=["updated_item1"])
        response = requests.get('http://localhost:3000/api/items/1')
        assert response.status_code == 200
        assert all(item in response.json() for item in ["item1"])

        response = requests.put('http://localhost:3000/api/items/1', json={"item": {"name": "updated_item1"}})
        assert response.status_code == 200
        assert all(item in response.json() for item in ["updated_item1"])

