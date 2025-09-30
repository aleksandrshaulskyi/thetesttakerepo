from abc import ABC, abstractmethod


class StorageManagerPort(ABC):

    @abstractmethod
    async def check_and_get_path(self) -> str | None:
        ...
