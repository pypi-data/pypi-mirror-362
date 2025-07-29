from typing import Annotated, Literal, Optional

from pydantic import BaseModel, Field

from .local_directory import LocalDirectoryStorage
from .s3 import S3Storage


class LocalDirectoryConfig(BaseModel):
    backend: Literal["localdir"]
    directory: str


class S3Config(BaseModel):
    backend: Literal["s3"]
    bucket_name: str
    region: str
    access_key: Optional[str] = None
    secret_key: Optional[str] = None
    endpoint_url: Optional[str] = None
    presigned_url_ttl: int = 3600


StorageConfig = Annotated[
    LocalDirectoryConfig | S3Config,
    Field(discriminator="backend"),
]


def create_from_config(config: StorageConfig) -> LocalDirectoryStorage | S3Storage:
    """Creates a storage instance from the given configuration."""
    if config.backend == "localdir":
        return LocalDirectoryStorage(config.directory)
    elif config.backend == "s3":
        return S3Storage(
            bucket_name=config.bucket_name,
            region=config.region,
            access_key_id=config.access_key,
            secret_access_key=config.secret_key,
            endpoint_url=config.endpoint_url,
            presigned_url_ttl=config.presigned_url_ttl,
        )
    else:
        raise ValueError(f"Unsupported backend: {config.backend}")
