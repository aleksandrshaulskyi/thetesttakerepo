from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    #BASE
    search_sentence: str = 'Джемпер женский нарядный в полоску оверсайз больших размеров'
    default_sleep_time: int = 10
    #HTTP
    wb_base_url: str = 'https://u-search.wb.ru/exactmatch/ru/common/v18/search'
    concurrency_limit: int = 8
    #STORAGE
    in_storage: str = f'{Path(__file__).parent}/in-storage'
    out_storage: str = f'{Path(__file__).parent}/out-storage'
    #EXCEL
    default_sheet_name: str = 'Детальная информация'
    default_batch_size: int = 1000
    excel_max_row: int = 1048576
    excel_max_col: int = 2
    #SEMANTIC
    model_name: str = 'paraphrase-multilingual-MiniLM-L12-v2'
    acceptable_threshold: float = 0.8

    model_config = SettingsConfigDict()

settings = Settings()
