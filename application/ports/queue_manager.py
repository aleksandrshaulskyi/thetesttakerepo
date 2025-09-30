from abc import ABC, abstractmethod
from typing import TypeVar


T = TypeVar('T')

class QueueManagerPort:

    @abstractmethod
    async def get_filtering_queue(self) -> T:
        ...

    @abstractmethod
    async def get_http_queue(self) -> T:
        ...
