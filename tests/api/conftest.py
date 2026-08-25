import requests
import pytest
from clients.api_manager import ApiManager
from utils.data_generator import DataGenerator
from custom_requester.custom_requester import CustomRequester
from config.base_urls import AUTH_BASE_URL
from faker import Faker


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
    fake = Faker()
    password = DataGenerator.generate_random_password()
    return {
        "email": fake.email(),
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