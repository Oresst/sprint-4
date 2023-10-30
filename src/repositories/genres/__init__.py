from abc import ABC, abstractmethod

from models.genres import Genre


class AbstractDbGenresRepository(ABC):
    @abstractmethod
    async def get_genre_by_id(self, genre_id: str) -> Genre | None:
        raise NotImplementedError

    @abstractmethod
    async def get_genres(self) -> list[Genre]:
        raise NotImplementedError


class AbstractCacheGenreRepository(ABC):
    @abstractmethod
    async def get_genre_by_id(self, genre_id: str) -> Genre | None:
        raise NotImplementedError

    @abstractmethod
    async def save_genre_by_id(self, genre: Genre) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_genres(self) -> list[Genre] | None:
        raise NotImplementedError

    @abstractmethod
    async def save_genres(self, genres: list[Genre]) -> None:
        raise NotImplementedError
