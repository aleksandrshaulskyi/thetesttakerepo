from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, Iterable


class ExcelReaderPort(ABC):
    '''
    A port for openpyxl reader.
    '''

    @abstractmethod
    def execute(path: str, sheet: str, batch_size: int) -> Iterable[list[tuple[Any, ...]]]:
        '''
        A sync method to read a batch of rows (openpyxl is sycn).
        '''
        ...

    async def read(path: str, sheet: str, batch_size: int) -> AsyncGenerator[list[tuple[Any, ...]], None]:
        ''''
        An async wrapper that should be run in a separate thread in order to avoid blocking the loop.
        '''
        ...
