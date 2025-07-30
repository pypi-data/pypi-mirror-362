from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Literal, Optional

from knowlang.database.config import VectorStoreConfig
from knowlang.utils import FancyLogger
from knowlang.vector_stores.base import (
    SearchResult,
    VectorStore,
    VectorStoreError,
    VectorStoreInitError,
)

# Type checking imports - only available during static analysis
if TYPE_CHECKING:
    try:
        import vecs
        from vecs.collection import Record
    except ImportError:
        # Define dummy types for type checking when vecs is not available
        Record = Any
        vecs = Any

LOG = FancyLogger(__name__)


class PostgresVectorStore(VectorStore):
    """Postgres implementation of VectorStore compatible with the pgvector extension using psycopg."""

    @classmethod
    def from_cfg(cls, cfg: VectorStoreConfig) -> "PostgresVectorStore":
        """Create PostgresVectorStore from VectorStoreConfig."""

        if not cfg.connection_string:
            raise VectorStoreInitError(
                "Connection url not set for PostgresVectorStore."
            )

        return cls(
            config=cfg,
            connection_string=cfg.connection_string,
            table_name=cfg.table_name,
            embedding_dim=cfg.embedding.dimension,
        )

    def __init__(
        self,
        config: VectorStoreConfig,
        connection_string: str,
        table_name: str,
        embedding_dim: int,
        similarity_metric: Literal["cosine"] = "cosine",
        content_field: Optional[str] = "content",
    ):
        super().__init__()

        self.config = config
        self.connection_string = connection_string
        self.table_name = table_name
        self.embedding_dim = embedding_dim
        self.similarity_metric = similarity_metric
        self.content_field = content_field
        self.collection = None

        # Store vecs module reference for later use
        self._vecs = None

    def assert_initialized(self) -> None:
        """Assert that the vector store is initialized"""
        if self.collection is None:
            raise ValueError(f"{self.__class__.__name__} is not initialized.")

    async def initialize(self) -> None:
        """Initialize the Postgres vector store client and create a collection of vectors."""
        # Dynamic import of vecs
        try:
            import vecs

            self._vecs = vecs
        except ImportError as e:
            raise ImportError(
                'Postgres vector store is not installed. Please install it using `pip install "knowlang[vecs]"`.'
            ) from e

        try:
            self.measure()  # Validate similarity metric
            vx = self._vecs.create_client(self.connection_string)
            self.collection = vx.get_or_create_collection(
                name=self.table_name, dimension=self.embedding_dim
            )
        except Exception as e:
            raise VectorStoreInitError(
                f"Failed to initialize PostgresVectorStore: {str(e)}"
            ) from e

        try:
            self.collection.create_index(measure=self.measure(), replace=False)
        except Exception:
            # index already exists, ignore
            LOG.info(f"Index already exists for collection {self.table_name}")
            return

    def measure(self):
        """Get the appropriate measure for the similarity metric"""
        if self._vecs is None:
            raise ValueError("vecs module not initialized. Call initialize() first.")

        if "cosine" in self.similarity_metric:
            return self._vecs.IndexMeasure.cosine_distance
        if "l1" in self.similarity_metric:
            return self._vecs.IndexMeasure.l1_distance
        if "l2" in self.similarity_metric:
            return self._vecs.IndexMeasure.l2_distance
        if "product" in self.similarity_metric:
            return self._vecs.IndexMeasure.max_inner_product
        raise VectorStoreError(
            f"Unsupported similarity metric: {self.similarity_metric}"
        )

    async def add_documents(
        self,
        documents: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict[str, Any]],
        ids: Optional[List[str]] = None,
    ) -> None:
        self.assert_initialized()
        if len(documents) != len(embeddings):
            raise VectorStoreError("Number of documents and embeddings must match.")
        if ids is None:
            ids = [str(i) for i in range(len(documents))]
        if len(documents) != len(ids):
            raise VectorStoreError("Number of documents and ids must match.")

        # Store the document content in metadata's content field
        for i, doc in enumerate(documents):
            if i < len(metadatas):
                metadatas[i][self.content_field] = doc

        vectors = [(id, emb, meta) for id, emb, meta in zip(ids, embeddings, metadatas)]
        self.collection.upsert(records=vectors)

    def accumulate_result(
        self,
        acc: List[SearchResult],
        record: Any,  # Changed from Record to Any to avoid import issues
        score_threshold: Optional[float] = None,
    ) -> List[SearchResult]:
        id, dist, meta = record
        score = 1.0 - dist  # Convert distance to similarity score
        if score_threshold is None or score >= score_threshold:
            acc.append(
                SearchResult(
                    document=meta.get(self.content_field, ""),
                    metadata=meta,
                    score=score,
                )
            )
        return acc

    async def query(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        score_threshold: Optional[float] = None,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[SearchResult]:
        records = self.collection.query(
            data=query_embedding,
            limit=top_k,
            measure=self.measure(),
            include_value=True,
            include_metadata=True,
            filters=filter,
        )

        return self.accumulate_result(
            acc=[], record=records, score_threshold=score_threshold
        )

    async def delete(self, ids: List[str]) -> None:
        self.assert_initialized()
        self.collection.delete(ids)

    async def get_documents(self, ids: List[str]) -> Optional[List[SearchResult]]:
        self.assert_initialized()
        results = self.collection.fetch(ids=ids)
        return results if results else None

    async def update_document(
        self, id: str, document: str, embedding: List[float], metadata: Dict[str, Any]
    ) -> None:
        self.assert_initialized()

        metadata[self.content_field] = document

        self.collection.upsert([(id, embedding, metadata)])

    async def get_all(self) -> List[SearchResult]:
        raise NotImplementedError("Postgres fetching all documents not implemented yet")
