import time

import pytest
import logging

from testdata.es_mapping import movies_index_mapping

LOGGER = logging.getLogger(__name__)


@pytest.mark.asyncio
class TestMovies:
    index_name = 'movies'
    endpoint = '/api/v1/films/'

    @pytest.fixture(scope="class", autouse=True)
    async def prepare_db(self, es_write_data, clear_db_data):
        # 1. Удаляем индекс, если существует. Очищаем кеш.
        await clear_db_data(self.index_name)
        # 2. Загружаем данные в ES
        await es_write_data(self.index_name, movies_index_mapping, 60)
        time.sleep(1)  # waiting for ES to process new data

    @pytest.mark.parametrize(
        'query_data, expected_answer',
        [
            (
                    {},
                    {'status': 200, 'length': 10}
            ),
            (
                    {'query': 'Star', 'page_size': 30, 'page_number': 2},
                    {'status': 200, 'length': 30}
            ),
            (
                    {'query': 'Mashed potato'},
                    {'status': 200, 'length': 0}
            )
        ]
    )
    async def test_search(self, make_get_request, query_data, expected_answer):
        # 3. Запрашиваем данные по API
        response, body = await make_get_request(self.endpoint, query_data)
        # 4. Проверяем ответ
        assert response.status == expected_answer['status']
        assert len(body) == expected_answer['length']

    @pytest.mark.parametrize(
        'query_data, expected_answer',
        [
            (
                    {'query': 'Star', 'page_size': 30, 'page_number': 2},
                    {'status': 200, 'length': 30}
            ),
        ]
    )
    async def test_cache(self, es_index_remove, make_get_request, query_data, expected_answer):
        # 1. Удаляем индекс
        await es_index_remove(self.index_name)
        # 3. Запрашиваем данные (из кеша)
        response, body = await make_get_request(self.endpoint, query_data)
        # 4. Проверяем ответ
        assert response.status == expected_answer['status']
        assert len(body) == expected_answer['length']
