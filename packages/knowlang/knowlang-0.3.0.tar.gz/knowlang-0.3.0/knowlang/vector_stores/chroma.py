from __future__ import annotations

from itertools import zip_longest
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple

from knowlang.core.types import VectorStoreProvider
from knowlang.database.config import VectorStoreConfig
from knowlang.vector_stores.base import (
    SearchResult,
    VectorStore,
    VectorStoreError,
    VectorStoreInitError,
)
from knowlang.vector_stores.factory import register_vector_store


@register_vector_store(VectorStoreProvider.CHROMA)
class ChromaVectorStore(VectorStore):
    """ChromaDB implementation of VectorStore"""

    @classmethod
    def from_cfg(cls, cfg: VectorStoreConfig) -> "ChromaVectorStore":
        """Create ChromaVectorStore from VectorStoreConfig."""
        return cls(
            config=cfg,
            persist_directory=cfg.connection_string,
            collection_name=cfg.table_name,
        )

    def accumulate_result(
        self,
        acc: List[SearchResult],
        record: Tuple[str, float, Dict[str, Any]],
        score_threshold: Optional[float] = None,
    ) -> List[SearchResult]:
        doc, meta, dist = record
        score = 1.0 - dist  # Convert distance to similarity score
        if score_threshold is None or score >= score_threshold:
            acc.append(SearchResult(document=doc, metadata=meta, score=score))
        return acc

    def __init__(
        self,
        config: VectorStoreConfig,
        persist_directory: Path,
        collection_name: str,
        similarity_metric: Literal["cosine"] = "cosine",
    ):
        self.config = config
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.similarity_metric = similarity_metric
        self.client = None
        self.collection = None

    async def initialize(self) -> None:
        """Initialize ChromaDB client and collection"""
        try:
            import chromadb
            from chromadb.config import Settings
        except ImportError as e:
            raise ImportError(
                'ChromaDB is not installed. Please install it using `pip install "knowlang[chroma]"`.'
            ) from e

        try:
            self.client = chromadb.PersistentClient(
                path=str(self.persist_directory),
                settings=Settings(anonymized_telemetry=False, allow_reset=True),
            )
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": self.similarity_metric},
            )
        except Exception as e:
            raise VectorStoreInitError(
                f"Failed to initialize ChromaDB: {str(e)}"
            ) from e

    async def add_documents(
        self,
        documents: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict[str, Any]],
        ids: Optional[List[str]] = None,
    ) -> None:
        self.assert_initialized()
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids or [str(i) for i in range(len(documents))],
        )

    async def query(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        score_threshold: Optional[float] = None,
    ) -> List[Tuple[str, float, Dict[str, Any]]]:
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["metadatas", "documents", "distances"],
        )
        records = zip_longest(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
            fillvalue={},
        )

        return self.accumulate_result(
            acc=[], record=records, score_threshold=score_threshold
        )

    def assert_initialized(self) -> None:
        """Assert that the vector store is initialized"""
        if self.collection is None:
            raise ValueError(f"{self.__class__.__name__} is not initialized.")

    async def delete(self, ids: List[str]) -> None:
        self.assert_initialized()
        self.collection.delete(ids=ids)

    async def get_documents(self, ids: List[str]) -> Optional[List[SearchResult]]:
        self.assert_initialized()
        try:
            results = self.collection.get(ids=ids)
            return [
                SearchResult(
                    document=result["documents"][0],
                    metadata=result["metadatas"][0],
                    score=1.0,  # Perfect match for direct retrieval
                )
                for result in results
                if result["documents"]
            ]
        except Exception as e:
            raise VectorStoreError(f"Failed to retrieve documents: {str(e)}") from e

    async def update_document(
        self, id: str, document: str, embedding: List[float], metadata: Dict[str, Any]
    ) -> None:
        self.assert_initialized()
        self.collection.upsert(
            ids=[id], documents=[document], embeddings=[embedding], metadatas=[metadata]
        )

    async def get_all(self) -> List[SearchResult]:
        raise NotImplementedError("ChromaDB fetching all documents not implemented yet")
