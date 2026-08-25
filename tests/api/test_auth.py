import requests
from custom_requester.custom_requester import CustomRequester

BASE_URL = "https://auth.dev-cinescope.coconutqa.ru"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
session = requests.Session()
requester = CustomRequester(session, BASE_URL)


def test_register_user(custom_requester, test_user):
    response = custom_requester.send_request(
        method="POST",
        endpoint="/register",
        data=test_user,
        expected_status=201
    )

    assert response.json()["email"] == test_user["email"]

def test_login_user():
    response = session.post(
        f"{BASE_URL}/login",
        headers=HEADERS,
        json={"email": "user@example.com", "password": "Test1234!"}
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

def test_login1():
    response = requester.send_request(
        "GET",
        "/movies",
        params={"page": 1, "pageSize": 10}
    )


def test_register_user1(auth_api, test_user):
    response = auth_api.register_user(test_user)
    assert response.json()["email"] == test_user["email"]

class TestAuth:
    def test_register_user(self, api_manager, test_user):
        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()

        assert response_data["email"] == test_user["email"]
        # добавим еше проверок
        assert "id" in response_data
        assert "USER" in response_data["roles"]

    def test_register_and_login_user(self, api_manager, registered_user):
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()

        assert "accessToken" in response_data
        assert response_data["user"]["email"] == registered_user["email"]