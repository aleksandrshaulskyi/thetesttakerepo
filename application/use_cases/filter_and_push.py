from application.ports import QueueManagerPort, SemanticFilterPort


class FilterAndPushUseCase:

    def __init__(self, filtering_manager: SemanticFilterPort, queue_manager: QueueManagerPort) -> None:
        self.filtering_manager = filtering_manager
        self.queue_manager = queue_manager

    async def execute(self) -> None:
        filtering_queue = await self.queue_manager.get_filtering_queue()
        http_queue = await self.queue_manager.get_http_queue()

        while True:
            data = await filtering_queue.get()

            print('Received data for filtering...')

            candidates = await self.filtering_manager.process(data=data)

            await http_queue.put(candidates)
