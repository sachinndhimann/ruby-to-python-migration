import requests
import requests_mock

def test_api():
    with requests_mock.Mocker() as mocker:
        mocker.get('http://localhost:3000/api/users', status_code=200, json=["user1", "user2"])
        mocker.post('http://localhost:3000/api/users', status_code=201, json=["user3"])
        response = requests.get('http://localhost:3000/api/users')
        assert response.status_code == 200
        assert all(item in response.json() for item in ["user1", "user2"])

        response = requests.post('http://localhost:3000/api/users', json={"user": {"name": "user3", "email": "user3@example.com"}})
        assert response.status_code == 201
        assert all(item in response.json() for item in ["user3"])

