from abc import ABC, abstractmethod
from typing import Optional, List

from models.persons import DetailedPerson, Person, ListPerson


class AbstractDbPersonRepository(ABC):
    @abstractmethod
    async def get_person_by_id(self, person_id: str) -> Optional[DetailedPerson]:
        raise NotImplementedError

    @abstractmethod
    async def get_persons(
            self, sort: Optional[str], query: Optional[str], page_size: int, page_number: int
    ) -> Optional[List[DetailedPerson]]:
        raise NotImplementedError


class AbstractCachePersonRepository(ABC):
    @abstractmethod
    async def get_person_by_id(self, person_id: str) -> Optional[DetailedPerson]:
        raise NotImplementedError

    @abstractmethod
    async def save_person_by_id(self, person: DetailedPerson) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_persons(
            self, sort: Optional[str], query: Optional[str], page_number: int, page_size: int
    ) -> Optional[ListPerson]:
        raise NotImplementedError

    @abstractmethod
    async def save_persons(
            self,
            sort: Optional[str],
            query: Optional[str],
            page_number: int,
            page_size: int,
            persons: List[DetailedPerson],
    ) -> None:
        raise NotImplementedError
