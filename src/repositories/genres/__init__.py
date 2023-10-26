from abc import ABC, abstractmethod
from typing import List, Optional

from models.genres import Genre


class AbstractDbGenresRepository(ABC):
    @abstractmethod
    async def get_genre_by_id(self, genre_id: str) -> Optional[Genre]:
        raise NotImplementedError

    @abstractmethod
    async def get_genres(self) -> List[Genre]:
        raise NotImplementedError


class AbstractCacheGenreRepository(ABC):
    @abstractmethod
    async def get_genre_by_id(self, genre_id: str) -> Optional[Genre]:
        raise NotImplementedError

    @abstractmethod
    async def save_genre_by_id(self, genre: Genre) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_genres(self) -> Optional[List[Genre]]:
        raise NotImplementedError

    @abstractmethod
    async def save_genres(self, genres: List[Genre]) -> None:
        raise NotImplementedError
