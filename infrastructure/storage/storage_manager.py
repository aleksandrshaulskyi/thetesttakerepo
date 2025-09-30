from pathlib import Path
from shutil import move

from settings import settings

from application.ports import StorageManagerPort


class StorageManager(StorageManagerPort):

    async def check_and_get_path(self) -> str | None:
        dir_path = Path(settings.in_storage)

        files = list(dir_path.glob('*.xlsx'))

        if files:
            file_path = str(max(files, key=lambda f: f.stat().st_mtime))
            return file_path
        return None
