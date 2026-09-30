import requests
import pytest
from clients.api_manager import ApiManager
from constants.roles import Roles
from entities.user import User
from resources.user_creds import SuperAdminCreds
from utils.data_generator import DataGenerator
from custom_requester.custom_requester import CustomRequester
from config.base_urls import AUTH_BASE_URL
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from db_requester.db_client import get_db_session


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
        "roles": [Roles.USER.value]
    }

@pytest.fixture(scope="function")
def registered_user(api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user).json()
    test_user["id"] = response["id"]
    return test_user

# @pytest.fixture(scope="session")
# def super_admin_api_manager(api_manager):
#     login_data = {
#         "email": os.getenv("SUPER_ADMIN_EMAIL"),
#         "password": os.getenv("SUPER_ADMIN_PASSWORD"),
#     }
#
#     response = api_manager.auth_api.login_user(login_data)
#     response_data = response.json()
#
#     access_token = response_data["accessToken"]
#
#     api_manager.session.headers.update(
#         {"Authorization": f"Bearer {access_token}"}
#     )
#
#     return api_manager

@pytest.fixture(scope="function")
def created_movie(super_admin):
    movie_data = DataGenerator.generate_random_movie()
    response = super_admin.api.movies_api.create_movie(movie_data)
    response_data = response.json()

    return response_data

@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session
    )

    response = super_admin.api.auth_api.login_user(super_admin.creds)
    access_token = response.json()["accessToken"]

    super_admin.api.session.headers.update({
        "Authorization": f"Bearer {access_token}"
    })

    return super_admin

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data["email"],
        creation_user_data["password"],
        [Roles.USER.value],
        new_session
    )

    response = super_admin.api.user_api.create_user(creation_user_data)
    user_id = response.json()["id"]

    response = common_user.api.auth_api.login_user(common_user.creds)
    access_token = response.json()["accessToken"]

    common_user.api.session.headers.update({
        "Authorization": f"Bearer {access_token}"
    })

    yield common_user

    super_admin.api.user_api.delete_user(user_id)

@pytest.fixture(scope="function")
def creation_user_data(test_user):
    updated_data = test_user.copy()
    updated_data.update({
    "verified": True,
    "banned": False
    })
    return updated_data


@pytest.fixture
def admin_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    admin_data = creation_user_data.copy()
    admin_data["roles"] = [Roles.ADMIN.value]

    admin_user = User(
        admin_data["email"],
        admin_data["password"],
        [Roles.ADMIN.value],
        new_session
    )

    super_admin.api.user_api.create_user(admin_data)

    response = admin_user.api.auth_api.login_user(admin_user.creds)
    access_token = response.json()["accessToken"]

    admin_user.api.session.headers.update({
        "Authorization": f"Bearer {access_token}"
    })

    return admin_user


@pytest.fixture(scope="module")
def db_session() -> Session:
    """
    Фикстура, которая создает и возвращает сессию для работы с базой данных
    После завершения теста сессия автоматически закрывается
    """
    db_session = get_db_session()
    yield db_session
    db_session.close()




@pytest.fixture(scope="function")
def created_test_user(db_helper):
    """
    Фикстура, которая создает тестового пользователя в БД
    и удаляет его после завершения теста
    """
    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    yield user
    # Cleanup после теста
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)