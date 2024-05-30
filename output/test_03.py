import requests
import requests_mock

def test_api():
    with requests_mock.Mocker() as mocker:
        mocker.get('http://localhost:3000/api/items/999', status_code=404, json=[])
        mocker.delete('http://localhost:3000/api/items/1', status_code=204, json=[])
        response = requests.get('http://localhost:3000/api/items/999')
        assert response.status_code == 404

        response = requests.delete('http://localhost:3000/api/items/1')
        assert response.status_code == 204

