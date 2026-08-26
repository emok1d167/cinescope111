import requests
import pytest
from clients.api_manager import ApiManager
from utils.data_generator import DataGenerator
from custom_requester.custom_requester import CustomRequester
from config.base_urls import AUTH_BASE_URL
import os
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session)

@pytest.fixture(scope="session")
def custom_requester(session):
    return CustomRequester(session=session, base_url=AUTH_BASE_URL)

@pytest.fixture(scope="function")
def test_user():
    password = DataGenerator.generate_random_password()
    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": password,
        "passwordRepeat": password,
        "roles": ["USER"]
    }

@pytest.fixture(scope="function")
def registered_user(api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user).json()
    test_user["id"] = response["id"]
    return test_user

@pytest.fixture(scope="session")
def super_admin_api_manager(api_manager):
    login_data = {
        "email": os.getenv("SUPER_ADMIN_EMAIL"),
        "password": os.getenv("SUPER_ADMIN_PASSWORD"),
    }

    response = api_manager.auth_api.login_user(login_data)
    response_data = response.json()

    access_token = response_data["accessToken"]

    api_manager.session.headers.update(
        {"Authorization": f"Bearer {access_token}"}
    )

    return api_manager

@pytest.fixture(scope="function")
def created_movie(super_admin_api_manager):
    movie_data = DataGenerator.generate_random_movie()
    response = super_admin_api_manager.movies_api.create_movie(movie_data)
    response_data = response.json()

    return response_data
