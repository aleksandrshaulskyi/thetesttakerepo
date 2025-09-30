from asyncio import Queue

from application.ports import QueueManagerPort


class QueueManager(QueueManagerPort):

    def __init__(self) -> None:
        self.filtering_queue = Queue()
        self.http_queue = Queue()

    async def get_filtering_queue(self) -> Queue:
        return self.filtering_queue
    
    async def get_http_queue(self) -> Queue:
        return self.http_queue

queue_manager = QueueManager()
