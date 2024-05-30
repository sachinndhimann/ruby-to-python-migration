import requests
import requests_mock

def test_api():
    with requests_mock.Mocker() as mocker:
        mocker.get('http://localhost:3000/api/users/1', status_code=200, json=["user1"])
        mocker.put('http://localhost:3000/api/users/1', status_code=200, json=["updated_user1"])
        response = requests.get('http://localhost:3000/api/users/1')
        assert response.status_code == 200
        assert all(item in response.json() for item in ["user1"])

        response = requests.put('http://localhost:3000/api/users/1', json={"user": {"name": "updated_user1", "email": "updated_user1@example.com"}})
        assert response.status_code == 200
        assert all(item in response.json() for item in ["updated_user1"])

