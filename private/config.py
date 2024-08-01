from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    endpoint_url: str
    bucket_name: str
    access_key: SecretStr
    secret_key: SecretStr

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


config = Settings()
