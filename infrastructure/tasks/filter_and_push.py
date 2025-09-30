from application.use_cases import FilterAndPushUseCase

from infrastructure.semantic_filter import SemanticFilter
from infrastructure.queue import queue_manager


async def filter_and_push():
    await FilterAndPushUseCase(
        filtering_manager=SemanticFilter(),
        queue_manager=queue_manager,
    ).execute()
