from abc import ABC, abstractmethod


class ExcelWriterPort(ABC):

    @abstractmethod
    def execute(self, rows_data: dict, path: str) -> None:
        ...

    @abstractmethod
    async def write_rows(self, rows_data: dict, path: str) -> None:
        ...
