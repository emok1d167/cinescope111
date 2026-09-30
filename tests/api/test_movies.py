import allure
import pytest

from models.movie_models import MovieModel, MoviesResponseModel
from utils.data_generator import DataGenerator
from db_requester.movie_model import Movie

@pytest.mark.smoke
@pytest.mark.regression
@allure.epic("API")
@allure.feature("Movies")
@allure.story("Получение списка фильмов")
@allure.title("Успешное получение списка фильмов")
@allure.severity(allure.severity_level.NORMAL)
def test_get_movies_success(common_user):
    with allure.step("Отправить запрос на получение списка фильмов"):
        response = common_user.api.movies_api.get_movies()
        response_data = response.json()

    with allure.step("Провалидировать структуру ответа через Pydantic"):
        movies_response = MoviesResponseModel.model_validate(response_data)

    with allure.step("Проверить данные пагинации и наличие фильмов"):
        assert movies_response.page >= 1
        assert movies_response.pageSize > 0
        assert movies_response.count >= 0
        assert movies_response.pageCount >= 0
        assert movies_response.movies


@pytest.mark.regression
@allure.epic("API")
@allure.feature("Movies")
@allure.story("Фильтрация фильмов")
@allure.title("Фильтрация списка фильмов по локации MSK")
@allure.severity(allure.severity_level.NORMAL)
def test_get_movies_filter_location(common_user):
    with allure.step("Получить фильмы с фильтром по локации MSK"):
        response = common_user.api.movies_api.get_movies(
            params={"locations": "MSK"}
        )

    with allure.step("Провалидировать структуру ответа через Pydantic"):
        movies_response = MoviesResponseModel.model_validate(response.json())

    with allure.step("Проверить локацию полученных фильмов"):
        assert movies_response.movies

        for movie in movies_response.movies:
            assert movie.location == "MSK"


@pytest.mark.smoke
@pytest.mark.regression
@allure.epic("API")
@allure.feature("Movies")
@allure.story("Создание фильма")
@allure.title("Успешное создание фильма")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_movie(super_admin):
    with allure.step("Подготовить данные фильма"):
        movie_data = DataGenerator.generate_random_movie()

    with allure.step("Отправить запрос на создание фильма"):
        response = super_admin.api.movies_api.create_movie(movie_data)
        response_data = response.json()

    with allure.step("Проверить данные созданного фильма"):
        assert "id" in response_data
        assert response_data["name"] == movie_data["name"]
        assert response_data["price"] == movie_data["price"]
        assert response_data["description"] == movie_data["description"]
        assert response_data["location"] == movie_data["location"]
        assert response_data["published"] == movie_data["published"]
        assert response_data["genreId"] == movie_data["genreId"]


@pytest.mark.regression
@allure.epic("API")
@allure.feature("Movies")
@allure.story("Получение фильма")
@allure.title("Успешное получение фильма по ID")
@allure.severity(allure.severity_level.NORMAL)
def test_get_movie(common_user, created_movie):
    movie_id = created_movie["id"]

    with allure.step(f"Получить фильм с ID {movie_id}"):
        response = common_user.api.movies_api.get_movie(movie_id)

    with allure.step("Провалидировать структуру фильма через Pydantic"):
        movie = MovieModel.model_validate(response.json())

    with allure.step("Проверить данные полученного фильма"):
        assert movie.id == created_movie["id"]
        assert movie.name == created_movie["name"]


@pytest.mark.regression
@allure.epic("API")
@allure.feature("Movies")
@allure.story("Редактирование фильма")
@allure.title("Успешное изменение названия фильма")
@allure.severity(allure.severity_level.CRITICAL)
def test_update_movie(super_admin, created_movie):
    movie_id = created_movie["id"]

    with allure.step("Подготовить новое название фильма"):
        random_movie = DataGenerator.generate_random_movie()
        updated_movie_data = {
            "name": random_movie["name"]
        }

    with allure.step(f"Изменить фильм с ID {movie_id}"):
        response = super_admin.api.movies_api.update_movie(
            movie_id,
            updated_movie_data
        )
        response_data = response.json()

    with allure.step("Проверить изменённое название фильма"):
        assert response_data["name"] == updated_movie_data["name"]


@pytest.mark.regression
@allure.epic("API")
@allure.feature("Movies")
@allure.story("Удаление фильма")
@allure.title("Успешное удаление фильма")
@allure.severity(allure.severity_level.CRITICAL)
def test_delete_movie(super_admin, created_movie):
    movie_id = created_movie["id"]

    with allure.step(f"Удалить фильм с ID {movie_id}"):
        response = super_admin.api.movies_api.delete_movie(movie_id)
        response_data = response.json()

    with allure.step("Проверить ID удалённого фильма"):
        assert response_data["id"] == movie_id


@pytest.mark.regression
@pytest.mark.negative
@allure.epic("API")
@allure.feature("Movies")
@allure.story("Фильтрация фильмов")
@allure.title("Ошибка 400 при фильтрации по невалидной локации")
@allure.severity(allure.severity_level.NORMAL)
def test_get_movies_with_invalid_location_return_400(common_user):
    with allure.step("Отправить запрос с невалидной локацией"):
        response = common_user.api.movies_api.get_movies(
            params={"locations": "INVALID"},
            expected_status=400
        )
        response_data = response.json()

    with allure.step("Проверить ошибку Bad Request"):
        assert response_data["statusCode"] == 400
        assert response_data["message"] in (
            "Некорректные данные",
            "Bad Request"
        )


@pytest.mark.regression
@pytest.mark.negative
@allure.epic("API")
@allure.feature("Movies")
@allure.story("Создание фильма")
@allure.title("Ошибка 400 при создании фильма с невалидной локацией")
@allure.severity(allure.severity_level.NORMAL)
def test_create_movie_invalid_location_return_400(super_admin):
    with allure.step("Подготовить данные с невалидной локацией"):
        movie_data = DataGenerator.generate_random_movie()
        movie_data["location"] = "INVALID"

    with allure.step("Отправить запрос на создание фильма"):
        response = super_admin.api.movies_api.create_movie(
            movie_data,
            expected_status=400
        )
        response_data = response.json()

    with allure.step("Проверить ошибку Bad Request"):
        assert response_data["statusCode"] == 400
        assert response_data["error"] == "Bad Request"
        assert (
            "Поле location должно быть одним из: MSK, SPB"
            in response_data["message"]
        )


@pytest.mark.regression
@pytest.mark.negative
@allure.epic("API")
@allure.feature("Movies")
@allure.story("Создание фильма")
@allure.title("Ошибка 409 при создании фильма с существующим названием")
@allure.severity(allure.severity_level.NORMAL)
def test_create_movie_with_existing_name_return_409(super_admin):
    movie_data = DataGenerator.generate_random_movie()

    with allure.step("Создать первый фильм"):
        super_admin.api.movies_api.create_movie(movie_data)

    with allure.step("Повторно создать фильм с тем же названием"):
        response = super_admin.api.movies_api.create_movie(
            movie_data,
            expected_status=409
        )
        response_data = response.json()

    with allure.step("Проверить ошибку Conflict"):
        assert response_data["statusCode"] == 409
        assert response_data["error"] == "Conflict"
        assert (
            "Фильм с таким названием уже существует"
            in response_data["message"]
        )


@pytest.mark.regression
@pytest.mark.negative
@allure.epic("API")
@allure.feature("Movies")
@allure.story("Получение фильма")
@allure.title("Ошибка 404 при получении несуществующего фильма")
@allure.severity(allure.severity_level.NORMAL)
def test_get_movie_not_found_return_404(
    super_admin,
    created_movie
):
    movie_id = created_movie["id"]

    with allure.step(f"Удалить фильм с ID {movie_id}"):
        super_admin.api.movies_api.delete_movie(movie_id)

    with allure.step("Попытаться получить удалённый фильм"):
        response = super_admin.api.movies_api.get_movie(
            movie_id,
            expected_status=404
        )
        response_data = response.json()

    with allure.step("Проверить ошибку Not Found"):
        assert response_data["statusCode"] == 404
        assert response_data["message"] in (
            "Not Found",
            "Фильм не найден"
        )


@pytest.mark.xfail(
    reason=(
        "API возвращает 404 для невалидного movie_id "
        "вместо заявленного в Swagger 400"
    )
)
@pytest.mark.regression
@pytest.mark.negative
@allure.epic("API")
@allure.feature("Movies")
@allure.story("Удаление фильма")
@allure.title("Ошибка 400 при удалении фильма с невалидным ID")
@allure.severity(allure.severity_level.NORMAL)
def test_delete_movie_invalid_parameters_return_400(super_admin):
    invalid_movie_id = "INVALID"

    with allure.step("Отправить запрос на удаление с невалидным ID"):
        response = super_admin.api.movies_api.delete_movie(
            invalid_movie_id,
            expected_status=400
        )

    with allure.step("Проверить статус ответа"):
        assert response.status_code == 400


@pytest.mark.regression
@pytest.mark.negative
@allure.epic("API")
@allure.feature("Movies")
@allure.story("Удаление фильма")
@allure.title("Ошибка 404 при повторном удалении фильма")
@allure.severity(allure.severity_level.NORMAL)
def test_delete_movie_not_found_return_404(
    super_admin,
    created_movie
):
    movie_id = created_movie["id"]

    with allure.step(f"Удалить фильм с ID {movie_id}"):
        super_admin.api.movies_api.delete_movie(movie_id)

    with allure.step("Повторно удалить тот же фильм"):
        response = super_admin.api.movies_api.delete_movie(
            movie_id,
            expected_status=404
        )
        response_data = response.json()

    with allure.step("Проверить ошибку Not Found"):
        assert response_data["statusCode"] == 404
        assert response_data["message"] in (
            "Not Found",
            "Фильм не найден"
        )


@pytest.mark.regression
@pytest.mark.negative
@allure.epic("API")
@allure.feature("Movies")
@allure.story("Редактирование фильма")
@allure.title("Ошибка 400 при передаче невалидного имени фильма")
@allure.severity(allure.severity_level.NORMAL)
def test_update_movie_invalid_parameters_return_400(
    super_admin,
    created_movie
):
    movie_id = created_movie["id"]
    updated_movie_data = {
        "name": 123
    }

    with allure.step("Отправить невалидные данные для изменения фильма"):
        response = super_admin.api.movies_api.update_movie(
            movie_id,
            updated_movie_data,
            expected_status=400
        )
        response_data = response.json()

    with allure.step("Проверить ошибку Bad Request"):
        assert response_data["statusCode"] == 400
        assert response_data["error"] == "Bad Request"
        assert (
            "Поле name должно быть строкой"
            in response_data["message"]
        )


@pytest.mark.regression
@pytest.mark.negative
@allure.epic("API")
@allure.feature("Movies")
@allure.story("Редактирование фильма")
@allure.title("Ошибка 404 при изменении несуществующего фильма")
@allure.severity(allure.severity_level.NORMAL)
def test_update_movie_not_found_return_404(
    super_admin,
    created_movie
):
    movie_id = created_movie["id"]

    with allure.step(f"Удалить фильм с ID {movie_id}"):
        super_admin.api.movies_api.delete_movie(movie_id)

    with allure.step("Подготовить новые данные фильма"):
        random_movie = DataGenerator.generate_random_movie()
        updated_movie_data = {
            "name": random_movie["name"]
        }

    with allure.step("Попытаться изменить удалённый фильм"):
        response = super_admin.api.movies_api.update_movie(
            movie_id,
            updated_movie_data,
            expected_status=404
        )
        response_data = response.json()

    with allure.step("Проверить ошибку Not Found"):
        assert response_data["statusCode"] == 404
        assert response_data["error"] == "Not Found"
        assert response_data["message"] == "Фильм не найден"


@pytest.mark.regression
@pytest.mark.negative
@allure.epic("API")
@allure.feature("Movies")
@allure.story("Авторизация при создании фильма")
@allure.title("Пользователь с ролью USER не может создать фильм")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_movie_role_user(common_user):
    with allure.step("Подготовить данные фильма"):
        movie_data = DataGenerator.generate_random_movie()

    with allure.step("Попытаться создать фильм с ролью USER"):
        response = common_user.api.movies_api.create_movie(
            movie_data,
            expected_status=403
        )
        response_data = response.json()

    with allure.step("Проверить ошибку Forbidden"):
        assert response_data["statusCode"] == 403


@pytest.mark.regression
@pytest.mark.parametrize(
    "params, filter_type, expected",
    [
        (
            {"minPrice": 100, "maxPrice": 1000},
            "price",
            (100, 1000)
        ),
        (
            {"locations": "MSK"},
            "location",
            "MSK"
        ),
        (
            {"genreId": 8},
            "genre",
            8
        ),
    ],
)
@allure.epic("API")
@allure.feature("Movies")
@allure.story("Фильтрация фильмов")
@allure.title("Получение фильмов с различными фильтрами")
@allure.severity(allure.severity_level.NORMAL)
def test_get_movies_with_filters(
    api_manager,
    params,
    filter_type,
    expected
):
    with allure.step(f"Получить фильмы с параметрами {params}"):
        response = api_manager.movies_api.get_movies(
            params=params
        )

    with allure.step("Провалидировать ответ через Pydantic"):
        movies_response = MoviesResponseModel.model_validate(
            response.json()
        )

    with allure.step("Проверить, что список фильмов не пуст"):
        assert movies_response.movies, "Список фильмов пуст"

    with allure.step(f"Проверить фильтр {filter_type}"):
        for movie in movies_response.movies:
            if filter_type == "price":
                min_price, max_price = expected
                assert min_price <= movie.price <= max_price

            elif filter_type == "location":
                assert movie.location == expected

            elif filter_type == "genre":
                assert movie.genreId == expected


@pytest.mark.regression
@allure.epic("API")
@allure.feature("Movies")
@allure.story("Получение фильма")
@allure.title("Получение фильма по ID с проверкой данных в БД")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_movie(
    common_user,
    created_movie,
    db_session
):
    movie_id = created_movie["id"]

    with allure.step(f"Получить фильм с ID {movie_id}"):
        response = common_user.api.movies_api.get_movie(movie_id)
        movie = MovieModel.model_validate(response.json())

    with allure.step("Проверить данные фильма в API"):
        assert movie.id == created_movie["id"]
        assert movie.name == created_movie["name"]

    with allure.step("Проверить фильм в базе данных"):
        db_session.expire_all()

        db_movie = (
            db_session.query(Movie)
            .filter(Movie.id == movie.id)
            .one_or_none()
        )

        assert db_movie is not None
        assert db_movie.id == movie.id
        assert db_movie.name == movie.name
        assert db_movie.price == movie.price
        assert db_movie.description == movie.description
        assert db_movie.location == movie.location
        assert db_movie.published == movie.published
        assert db_movie.genre_id == movie.genreId