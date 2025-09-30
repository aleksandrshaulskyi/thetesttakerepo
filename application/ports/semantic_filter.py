from abc import ABC, abstractmethod


class SemanticFilterPort(ABC):

    @abstractmethod
    async def process(self) -> set:
        ...

    @abstractmethod
    async def extract_candidates(self, data: list) -> list:
        ...

    @abstractmethod
    async def get_candidate_data(self, query: str, data: list) -> dict:
        ...
