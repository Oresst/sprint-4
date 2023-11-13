import time
import logging
from http import HTTPStatus
from random import choice

import pytest

from testdata import genres_data

LOGGER = logging.getLogger(__name__)

test_item = choice(genres_data).copy()


@pytest.mark.asyncio
class TestGenres:
    index_name = 'genres'
    endpoint = '/api/v1/genres/'

    @pytest.fixture(scope="class", autouse=True)
    async def prepare_db(self, es_write_data, clear_db_data):
        # 1. Удаляем индекс, если существует. Очищаем кеш.
        await clear_db_data(self.index_name)
        # 2. Загружаем данные в ES
        await es_write_data(self.index_name)
        time.sleep(1)  # waiting for ES to process new data

    @pytest.mark.parametrize(
        '_id, expected_answer',
        [
            ('biuOIGByo', {'status': HTTPStatus.NOT_FOUND}),
            (test_item["id"], {'status': HTTPStatus.OK}),
            (f'{test_item["id"]}/popular', {'status': HTTPStatus.OK}),
        ]
    )
    async def test_genre(self, make_get_request, _id, expected_answer):
        uri = f'{self.endpoint}{_id}'
        response, body = await make_get_request(uri, {})
        assert response.status == expected_answer['status']

    @pytest.mark.parametrize(
        'query_data, expected_answer',
        [
            (  # get all rows
                    {'page_size': 10000},
                    {'status': HTTPStatus.OK}
            ),
        ]
    )
    async def test_search(self, make_get_request, query_data, expected_answer):
        response, body = await make_get_request(self.endpoint, query_data)
        assert response.status == expected_answer['status']
        if 'length' in expected_answer:
            assert len(body) == expected_answer['length']

    @pytest.mark.parametrize(
        'cache_data, query_data, expected_answer',
        [
            (
                    {'k': 'genres', 'v': '{"genres":[{"id":"","name":"TESTS"}]}'},
                    {},
                    {'status': HTTPStatus.OK, 'length': 1, 'name': 'TESTS'}
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
        assert body[0]['name'] == expected_answer['name']
