import time
import logging
from random import choice

import pytest
from http import HTTPStatus

from testdata import movies_data

LOGGER = logging.getLogger(__name__)

test_item = choice(movies_data).copy()


@pytest.mark.asyncio
class TestMovies:
    index_name = 'movies'
    endpoint = '/api/v1/films/'

    @pytest.fixture(scope="class", autouse=True)
    async def prepare_db(self, es_write_data, clear_db_data):
        # 1. Удаляем индекс, если существует. Очищаем кеш.
        await clear_db_data(self.index_name)
        # 2. Загружаем данные в ES
        await es_write_data(self.index_name)
        time.sleep(1)  # waiting for ES to process new data

    @pytest.mark.parametrize(
        'query_data, expected_answer',
        [
            (
                    {'query1': 'TEST', 'page_size1': 30},
                    {'status': HTTPStatus.OK, 'length': 10}
            ),
            (  # return a number of films
                    {'page_size': 3},
                    {'status': HTTPStatus.OK, 'length': 3}
            ),
            (  # search by a phrase
                    {'query': 'Star', 'page_size': 1},
                    {'status': HTTPStatus.OK, 'length': 1}
            ),
            (  # get all films
                    {'page_size': 60},
                    {'status': HTTPStatus.OK, 'length': 60}
            ),
        ]
    )
    async def test_search(self, make_get_request, query_data, expected_answer):
        response, body = await make_get_request(self.endpoint, query_data)
        assert response.status == expected_answer['status']
        assert len(body) == expected_answer['length']

    @pytest.mark.parametrize(
        'film_id, expected_answer',
        [
            ('biuOIGByo', {'status': HTTPStatus.NOT_FOUND}),
            (test_item["id"], {'status': HTTPStatus.OK}),
        ]
    )
    async def test_valid(self, make_get_request, film_id, expected_answer):
        uri = f'{self.endpoint}{film_id}'
        response, body = await make_get_request(uri, {})
        assert response.status == expected_answer['status']

    @pytest.mark.parametrize(
        'cache_data, query_data, expected_answer',
        [
            (
                    {'k': 'films-1-1', 'v': '{"films":[{"id":"","title":"","imdb_rating":-10}]}'},
                    {'page_number': 1, 'page_size': 1},
                    {'status': HTTPStatus.OK, 'length': 1, 'imdb_rating': -10}
            )
        ]
    )
    async def test_cache(
            self,
            es_index_remove, make_get_request, redis_client,
            cache_data, query_data, expected_answer
    ):
        # 1. Подменяем кэш
        await redis_client.set(cache_data['k'], cache_data['v'], 300)
        # 3. Запрашиваем данные по API
        response, body = await make_get_request(self.endpoint, query_data)
        # 4. Проверяем ответ
        assert response.status == expected_answer['status']
        assert len(body) == expected_answer['length']
        assert body[0]['imdb_rating'] == expected_answer['imdb_rating']
