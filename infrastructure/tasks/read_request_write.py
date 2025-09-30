from application.use_cases import ReadRequestWriteUseCase
from infrastructure.excel import ExcelWriter
from infrastructure.http import HttpManager
from infrastructure.queue import queue_manager
from infrastructure.storage import StorageManager


async def read_request_write():
    use_case = ReadRequestWriteUseCase(
        queue_manager=queue_manager,
        http_manager=HttpManager(),
        excel_manager=ExcelWriter(),
        storage_manager=StorageManager(),
    )

    while True:
        await use_case.execute()
