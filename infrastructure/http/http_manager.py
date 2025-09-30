from asyncio import as_completed, create_task, gather, Semaphore, TimeoutError
from json import JSONDecodeError, loads
from typing import AsyncGenerator

from aiohttp import ClientError, ClientSession
from backoff import expo, full_jitter, on_exception

from settings import settings

from application.exceptions import HTTPManagerException


class HttpManager:

    def __init__(self) -> None:
        self.semaphore = Semaphore(settings.concurrency_limit)
        self.session = ClientSession()

    async def ensure_session(self) -> None:
        if getattr(self.session, 'closed', True):
            self.session = ClientSession()

    @on_exception(expo, (ClientError, TimeoutError), max_tries=8, jitter=full_jitter)
    async def fetch_one(self, query: str, page_number: int):
        await self.ensure_session()

        try:
            async with self.semaphore:
                request_parameters = await self.build_parameters(query=query, page_number=page_number)
                async with self.session.get(
                    url=settings.wb_base_url,
                    params=request_parameters,
                ) as response:
                    try:
                        result = loads(await response.text())
                    except JSONDecodeError:
                        raise HTTPManagerException('Could not parse response.')
                    else:
                        result.update({'query': query, 'page_number': page_number})
                        return result
        except ClientError as exception:
            raise HTTPManagerException(f'An aiohttp exception occured and risen following: {str(exception)}.')
        except TimeoutError:
            raise HTTPManagerException(f'The request has timed out even with backoff.')

    async def build_parameters(self, query: str, page_number: int) -> dict:
        return {
            'ab_testing': 'false',
            'appType': '1',
            'curr': 'rub',
            'dest': '-1257786',
            'inheritFilters': 'false',
            'lang': 'ru',
            'page': '1',
            'query': query,
            'resultset': 'catalog',
            'sort': 'popular',
            'spp': '30',
            'suppressSpellcheck': 'false',
            'page': page_number,
        }
    
    async def fetch_all(self, queries: list) -> AsyncGenerator:
        tasks = []
        for query in queries:
            for page_number in range(1, 12):
                tasks.append(create_task(self.fetch_one(query, page_number)))

        try:
            for future in as_completed(tasks):
                yield await future
        finally:
            for task in tasks:
                if not task.done():
                    task.cancel()
            await gather(*tasks, return_exceptions=True)
            await self.session.close()
