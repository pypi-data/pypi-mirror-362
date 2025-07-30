from pydantic import BaseModel, Field

from knowlang.configs import EmbeddingConfig
from knowlang.configs.defaults import (
    DEFAULT_SQLITE_DB_CONNECTION_URL_ASYNC,
    DEFAULT_VECTOR_COLLECTION_NAME,
)
from knowlang.core.types import VectorStoreProvider


class DatabaseConfig(BaseModel):
    """Configuration for database connections"""

    provider: str = "sqlite"
    connection_url: str = DEFAULT_SQLITE_DB_CONNECTION_URL_ASYNC


class VectorStoreConfig(BaseModel):
    provider: VectorStoreProvider = Field(
        default=VectorStoreProvider.SQLITE, description="Vector Database provider"
    )
    connection_string: str = Field(
        default=DEFAULT_SQLITE_DB_CONNECTION_URL_ASYNC,
        description="Connection string for the vector store",
    )
    table_name: str = Field(
        default=DEFAULT_VECTOR_COLLECTION_NAME,
        description="Name of the table in the vector store",
    )
    embedding: EmbeddingConfig = Field(
        default_factory=EmbeddingConfig, description="Configuration for the embeddings"
    )
