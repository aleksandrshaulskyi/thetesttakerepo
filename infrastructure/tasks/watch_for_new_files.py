from asyncio import sleep

from settings import settings

from application.use_cases import CheckAndReadUseCase
from infrastructure.excel import ExcelReader
from infrastructure.queue import queue_manager
from infrastructure.storage import StorageManager


async def watch_for_new_files():
    use_case = CheckAndReadUseCase(
        excel_reader=ExcelReader(),
        queue_manager=queue_manager,
        storage_manager=StorageManager()
    )

    while True:
        print('Checking in-storage directory for the non-processed files...')
        await use_case.execute()
        print(f'Going to sleep for {settings.default_sleep_time} seconds before the next check...')
        await sleep(settings.default_sleep_time)
