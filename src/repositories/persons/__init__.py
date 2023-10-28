from abc import ABC, abstractmethod

from models.persons import DetailedPerson, ListPerson
from models.films import ListBaseFilm


class AbstractDbPersonRepository(ABC):
    @abstractmethod
    async def get_person_by_id(self, person_id: str) -> DetailedPerson | None:
        raise NotImplementedError

    @abstractmethod
    async def get_persons(
        self, page_number: int, page_size: int, sort: str | None = None, query: str | None = None
    ) -> list[DetailedPerson]:
        raise NotImplementedError

    @abstractmethod
    async def get_films_by_person_id(self, person_id: str) -> ListBaseFilm:
        raise NotImplementedError


class AbstractCachePersonRepository(ABC):
    @abstractmethod
    async def get_person_by_id(self, person_id: str) -> DetailedPerson | None:
        raise NotImplementedError

    @abstractmethod
    async def save_person_by_id(self, person: DetailedPerson) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_persons(
        self, page_number: int, page_size: int, sort: str | None = None, query: str | None = None
    ) -> ListPerson | None:
        raise NotImplementedError

    @abstractmethod
    async def save_persons(
        self,
        page_number: int,
        page_size: int,
        persons: list[DetailedPerson],
        sort: str | None = None,
        query: str | None = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_films_by_person_id(self, person_id: str) -> ListBaseFilm | None:
        raise NotImplementedError

    @abstractmethod
    async def save_films_by_person_id(self, person_id: str, films: ListBaseFilm) -> None:
        raise NotImplementedError
