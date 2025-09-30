from settings import settings

from application.exceptions import OpenPyXlException
from application.ports import ExcelReaderPort, QueueManagerPort, StorageManagerPort


class CheckAndReadUseCase:

    def __init__(
        self,
        excel_reader: ExcelReaderPort,
        queue_manager: QueueManagerPort,
        storage_manager: StorageManagerPort,
    ) -> None:
        self.excel_reader = excel_reader
        self.queue_manager = queue_manager
        self.storage_manager = storage_manager

    async def execute(self) -> None:
        if (path := await self.storage_manager.check_and_get_path()) is not None:

            print(f'Found a new file at: {path}.')

            queue = await self.queue_manager.get_filtering_queue()

            print(f'Starting to read the file...')

            try:
                async for batch in self.excel_reader.read(path, settings.default_sheet_name, settings.default_batch_size):
                    await queue.put(batch)
            except OpenPyXlException:
                pass  # Add logging.
            else:
                print('Read the file...')

        else:
            print('No files found in in-storage/non-processed the directory for processing...')
