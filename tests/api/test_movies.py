import pytest

from utils.data_generator import DataGenerator


def test_get_movies_success(api_manager):
    response = api_manager.movies_api.get_movies()
    response_data = response.json()

    assert "movies" in response_data
    assert "count" in response_data
    assert "page" in response_data
    assert "pageSize" in response_data
    assert "pageCount" in response_data

    movies = response_data["movies"]

    assert isinstance(movies, list)
    assert isinstance(response_data["count"], int)
    assert isinstance(response_data["page"], int)
    assert isinstance(response_data["pageSize"], int)
    assert isinstance(response_data["pageCount"], int)

    for movie in movies:
        assert "id" in movie
        assert "name" in movie
        assert "price" in movie
        assert "description" in movie
        assert "imageUrl" in movie
        assert "location" in movie
        assert "published" in movie
        assert "genreId" in movie
        assert "genre" in movie
        assert "createdAt" in movie
        assert "rating" in movie


def test_get_movies_filter_location(api_manager):
    response = api_manager.movies_api.get_movies(
        params={"locations": "MSK"}
    )

    response_data = response.json()
    movies = response_data["movies"]

    for movie in movies:
        assert "MSK" in movie["location"]


def test_create_movie(super_admin_api_manager):
    movie_data = DataGenerator.generate_random_movie()

    response = super_admin_api_manager.movies_api.create_movie(movie_data)
    response_data = response.json()

    assert "id" in response_data
    assert response_data["name"] == movie_data["name"]
    assert response_data["price"] == movie_data["price"]
    assert response_data["description"] == movie_data["description"]
    assert response_data["location"] == movie_data["location"]
    assert response_data["published"] == movie_data["published"]
    assert response_data["genreId"] == movie_data["genreId"]


def test_get_movie(api_manager, created_movie):
    movie_id = created_movie["id"]

    response = api_manager.movies_api.get_movie(movie_id)
    response_data = response.json()

    assert created_movie["id"] == response_data["id"]
    assert created_movie["name"] == response_data["name"]


def test_update_movie(super_admin_api_manager, created_movie):
    movie_id = created_movie["id"]
    random_name = DataGenerator.generate_random_movie()

    updated_movie_data = {
        "name": random_name["name"]
    }

    response = super_admin_api_manager.movies_api.update_movie(
        movie_id,
        updated_movie_data
    )
    response_data = response.json()

    assert response_data["name"] == updated_movie_data["name"]


def test_delete_movie(super_admin_api_manager, created_movie):
    movie_id = created_movie["id"]

    response = super_admin_api_manager.movies_api.delete_movie(movie_id)
    response_data = response.json()

    assert response_data["id"] == movie_id


def test_get_movies_with_invalid_location_return_400(api_manager):
    response = api_manager.movies_api.get_movies(
        params={"locations": "INVALID"},
        expected_status=400
    )

    response_data = response.json()

    assert response_data["statusCode"] == 400
    assert response_data["error"] == "Bad Request"
    assert "Некорректные данные" in response_data["message"]


def test_create_movie_invalid_location_return_400(super_admin_api_manager):
    movie_data = DataGenerator.generate_random_movie()
    movie_data["location"] = "INVALID"

    response = super_admin_api_manager.movies_api.create_movie(
        movie_data,
        expected_status=400
    )
    response_data = response.json()

    assert response_data["statusCode"] == 400
    assert response_data["error"] == "Bad Request"
    assert "Поле location должно быть одним из: MSK, SPB" in response_data["message"]


def test_create_movie_with_existing_name_return_409(super_admin_api_manager):
    movie_data = DataGenerator.generate_random_movie()

    super_admin_api_manager.movies_api.create_movie(movie_data)

    response = super_admin_api_manager.movies_api.create_movie(
        movie_data,
        expected_status=409
    )
    response_data = response.json()

    assert response_data["statusCode"] == 409
    assert response_data["error"] == "Conflict"
    assert "Фильм с таким названием уже существует" in response_data["message"]


def test_get_movie_not_found_return_404(super_admin_api_manager,created_movie):
    movie_id = created_movie["id"]

    super_admin_api_manager.movies_api.delete_movie(movie_id)

    response = super_admin_api_manager.movies_api.get_movie(
        movie_id,
        expected_status=404
    )
    response_data = response.json()

    assert response_data["statusCode"] == 404
    assert response_data["error"] == "Not Found"
    assert "Фильм не найден" in response_data["message"]


@pytest.mark.xfail(reason="api возвращает 404 для невалидного movie_id вместо заявленного в swagger 400")
def test_delete_movie_invalid_parameters_return_400(super_admin_api_manager):
    invalid_movie_id = "INVALID"

    response = super_admin_api_manager.movies_api.delete_movie(
        invalid_movie_id,
        expected_status=400
    )

    response_data = response.json()

def test_delete_movie_not_found_return_404(super_admin_api_manager,created_movie):
    movie_id = created_movie["id"]

    super_admin_api_manager.movies_api.delete_movie(movie_id)

    response = super_admin_api_manager.movies_api.delete_movie(
        movie_id,
        expected_status=404
    )

    response_data = response.json()

    assert response_data["statusCode"] == 404
    assert response_data["error"] == "Not Found"
    assert "Фильм не найден" in response_data["message"]


def test_update_movie_invalid_parameters_return_400(super_admin_api_manager, created_movie):
    movie_id = created_movie["id"]

    updated_movie_data = {
        "name": 123
    }

    response = super_admin_api_manager.movies_api.update_movie(
        movie_id,
        updated_movie_data,
        expected_status=400
    )
    response_data = response.json()


    assert response_data["statusCode"] == 400
    assert response_data["error"] == "Bad Request"
    assert "Поле name должно быть строкой" in response_data["message"]   #приходит лист место стринги p.s почитать как лучше писать подобные асерты, может есть смысл тогда через ==


def test_update_movie_not_found_return_404(super_admin_api_manager,created_movie):
    movie_id = created_movie["id"]

    super_admin_api_manager.movies_api.delete_movie(movie_id)

    random_movie = DataGenerator.generate_random_movie()

    updated_movie_data = {
        "name": random_movie["name"]
    }

    response = super_admin_api_manager.movies_api.update_movie(
        movie_id,
        updated_movie_data,
        expected_status=404
    )

    response_data = response.json()

    assert response_data["statusCode"] == 404
    assert response_data["error"] == "Not Found"
    assert response_data["message"] == "Фильм не найден"