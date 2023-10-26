from abc import ABC, abstractmethod
from typing import Optional, List

from models.films import DetailedFilm, BaseFilm, ListBaseFilm


class AbstractDbFilmRepository(ABC):
    @abstractmethod
    async def get_film_by_id(self, film_id: str) -> Optional[DetailedFilm]:
        raise NotImplementedError

    @abstractmethod
    async def get_films(
        self, sort: Optional[str], query: Optional[str], genre: Optional[str], page_size: int, page_number: int
    ) -> Optional[List[BaseFilm]]:
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
        self, sort: Optional[str], query: Optional[str], genre: Optional[str], page_number: int, page_size: int
    ) -> Optional[ListBaseFilm]:
        raise NotImplementedError

    @abstractmethod
    async def save_films(
        self,
        sort: Optional[str],
        query: Optional[str],
        genre: Optional[str],
        page_number: int,
        page_size: int,
        films: List[BaseFilm],
    ) -> None:
        raise NotImplementedError
