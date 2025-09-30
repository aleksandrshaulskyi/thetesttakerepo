from abc import ABC, abstractmethod
from typing import AsyncGenerator


class HttpManagerPort(ABC):

    @abstractmethod
    async def fetch_one(self, query: str, page_number: int) -> str:
        ...

    @abstractmethod
    async def build_parameters(self, query: str, page_number: int) -> dict:
        ...

    @abstractmethod
    async def fetch_all(self, queries: set) -> AsyncGenerator:
        ...

    @abstractmethod
    async def close(self) -> None:
        ...
