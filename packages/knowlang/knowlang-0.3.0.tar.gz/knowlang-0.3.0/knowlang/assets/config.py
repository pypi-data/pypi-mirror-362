from pydantic import BaseModel, Field
from typing_extensions import Generic, TypeVar

from knowlang.assets.models import DomainManagerData, MetaDataT
from knowlang.configs.retrieval_config import SearchConfig
from knowlang.database.config import VectorStoreConfig

ProcessorConfigT = TypeVar(
    "ProcessorConfigT",
    bound="ProcessorConfigBase",
    covariant=True,
    default="ProcessorConfigBase",
)


class ProcessorConfigBase(BaseModel):
    """Base class for processor configurations."""

    vector_store: VectorStoreConfig = Field(
        default_factory=VectorStoreConfig,
        description="Configuration for the vector store used by the processor",
    )


class DomainMixinConfig(BaseModel):
    source_cls: str  # Class identifier (e.g., "CodebaseAssetSource")
    indexer_cls: str  # Class identifier
    parser_cls: str  # Class identifier


class BaseDomainConfig(BaseModel, Generic[MetaDataT, ProcessorConfigT]):
    domain_type: str
    enabled: bool = True
    domain_data: DomainManagerData[MetaDataT]
    mixins: DomainMixinConfig
    processor_config: ProcessorConfigT
    search_config: SearchConfig = Field(
        default_factory=SearchConfig,
        description="Configuration for search operations in the domain",
    )
