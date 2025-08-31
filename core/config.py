from pydantic import AfterValidator
from pydantic_settings import BaseSettings
from typing import List, Annotated


def parse_allowed_origins(v: str)->List[str]:
    return  v.split(',') if v else []

class Settings(BaseSettings):
    API_PREFIX: str = '/api'
    DEBUG: bool = False
    DATABASE_URL: str = ''
    ALLOWED_ORIGINS: Annotated[str, AfterValidator(parse_allowed_origins)]=''
    OPEN_API_KEY:str = ''
    BASE_OPEN_API_URL: str =''

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True

settings = Settings()