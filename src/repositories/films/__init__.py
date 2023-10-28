from abc import ABC, abstractmethod
from typing import Optional, List

from models.films import DetailedFilm, ListBaseFilm
from models.base_models import BaseFilm


class AbstractDbFilmRepository(ABC):
    @abstractmethod
    async def get_film_by_id(self, film_id: str) -> Optional[DetailedFilm]:
        raise NotImplementedError

    @abstractmethod
    async def get_film_genres(self, film_id: str) -> Optional[List[str]]:
        raise NotImplementedError

    @abstractmethod
    async def get_films(
        self,
        page_number: int = 1,
        page_size: int = 10,
        sort: Optional[str] = None,
        query: Optional[str] = None,
        genre: Optional[str] = None,
    ) -> List[BaseFilm]:
        raise NotImplementedError


class AbstractCacheFilmRepository(ABC):
    @abstractmethod
    async def get_film_by_id(self, film_id: str) -> Optional[DetailedFilm]:
        raise NotImplementedError

    @abstractmethod
    async def save_film_by_id(self, film: DetailedFilm) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_films(
        self,
        page_number: int,
        page_size: int,
        sort: Optional[str] = None,
        query: Optional[str] = None,
        genre: Optional[str] = None,
    ) -> Optional[ListBaseFilm]:
        raise NotImplementedError

    @abstractmethod
    async def save_films(
        self,
        page_number: int,
        page_size: int,
        films: List[BaseFilm],
        sort: Optional[str] = None,
        query: Optional[str] = None,
        genre: Optional[str] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_alike_films(self, film_id: str) -> Optional[List[BaseFilm]]:
        raise NotImplementedError

    @abstractmethod
    async def save_alike_films(self, film_id: str, films: List[BaseFilm]) -> None:
        raise NotImplementedError
