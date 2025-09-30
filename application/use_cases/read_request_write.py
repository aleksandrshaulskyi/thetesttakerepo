from settings import settings

from application.exceptions import HTTPManagerException, OpenPyXlException
from application.ports import ExcelWriterPort, HttpManagerPort, QueueManagerPort, StorageManagerPort


class ReadRequestWriteUseCase:

    def __init__(
            self,
            queue_manager: QueueManagerPort,
            http_manager: HttpManagerPort,
            excel_manager: ExcelWriterPort,
            storage_manager: StorageManagerPort,
    ) -> None:
        self.queue_manager = queue_manager
        self.http_manager = http_manager
        self.excel_manager = excel_manager
        self.storage_manager = storage_manager

    async def execute(self) -> None:
        http_queue = await self.queue_manager.get_http_queue()

        while True:
            queries_data = await http_queue.get()

            print(f'Received {len(queries_data)} queries to try them as a search query parameter...')

            queries = await self.extract_queries(queries_data=queries_data)
            file_name = await self.extract_file_name(queries_data=queries_data)

            selected_queries = []

            try:
                async for response in self.http_manager.fetch_all(queries=queries):
                    if (index := await self.check_if_present(response=response)) is not None:
                        query_data = await self.get_query_data(response.get('query'), queries_data)
                        query_data.update(
                            {'index': await self.construct_final_index(response.get('page_number'), index)}
                        )
                        selected_queries.append(query_data)
            except HTTPManagerException:
                pass  # Log and put into the queue for failed operations.

            else:
                for selected_query_data in selected_queries:
                    try:
                        del selected_query_data['file_name']
                    except KeyError:
                        pass  # Log.
                try:
                    await self.excel_manager.write_rows(
                        rows_data=selected_queries,
                        path=f'{settings.out_storage}/{file_name}'
                    )
                    print('Wrote the results table...')
                except OpenPyXlException:
                    pass  # Log and retry.
                else:
                    print('Finished the processing.')

    async def check_if_present(self, response: dict) -> dict | None:
        print('Checking if target product is present in the list of products on provided page...')

        if (products := response.get('products')) is not None:

            for index, product in enumerate(products, start=1):
                if product.get('name') == settings.search_sentence:
                    print(f'Found the {settings.search_sentence}, it will be displayed in the results table...')
                    return index
        else:
            print('Got the response without products it seems...')  # Log and retry.

    async def construct_final_index(self, page_number: int, index: int) -> int:
        if page_number < 10:
            if index < 10:
                return int(f'{page_number}0{index}')
            return int(f'{page_number}{index}')
        else:
            if index < 10:
                return int(f'{page_number}0{index}')
            return int(f'{page_number}{index}')

    async def extract_queries(self, queries_data: list) -> list:
        return [query_data.get('query') for query_data in queries_data]

    async def get_query_data(self, query: str, queries_data: list) -> dict:
        index = next((index for index, item in enumerate(queries_data) if item.get('query') == query), None)
        return queries_data[index]
    
    async def extract_file_name(self, queries_data: dict) -> str:
        return queries_data[0].get('file_name')
