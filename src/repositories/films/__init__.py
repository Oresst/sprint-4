from abc import ABC, abstractmethod

from models.films import DetailedFilm, ListBaseFilm
from models.base_models import BaseFilm


class AbstractDbFilmRepository(ABC):
    @abstractmethod
    async def get_film_by_id(self, film_id: str) -> DetailedFilm | None:
        raise NotImplementedError

    @abstractmethod
    async def get_film_genres(self, film_id: str) -> list[str] | None:
        raise NotImplementedError

    @abstractmethod
    async def get_films(
        self,
        page_number: int = 1,
        page_size: int = 10,
        sort: str | None = None,
        query: str | None = None,
        genre: str | None = None,
    ) -> list[BaseFilm]:
        raise NotImplementedError


class AbstractCacheFilmRepository(ABC):
    @abstractmethod
    async def get_film_by_id(self, film_id: str) -> DetailedFilm | None:
        raise NotImplementedError

    @abstractmethod
    async def save_film_by_id(self, film: DetailedFilm) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_films(
        self,
        page_number: int,
        page_size: int,
        sort: str | None = None,
        query: str | None = None,
        genre: str | None = None,
    ) -> ListBaseFilm | None:
        raise NotImplementedError

    @abstractmethod
    async def save_films(
        self,
        page_number: int,
        page_size: int,
        films: list[BaseFilm],
        sort: str | None = None,
        query: str | None = None,
        genre: str | None = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_alike_films(self, film_id: str) -> list[BaseFilm] | None:
        raise NotImplementedError

    @abstractmethod
    async def save_alike_films(self, film_id: str, films: list[BaseFilm]) -> None:
        raise NotImplementedError
