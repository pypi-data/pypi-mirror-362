import inspect
from typing import List, Optional, Union, overload

from knowlang.configs import EmbeddingConfig

from .embedding_providers import EMBEDDING_PROVIDER_REGISTRY
from .types import EmbeddingInputType, EmbeddingVector, EmbeddingParams


def to_batch(input: Union[str, List[str]]) -> List[str]:
    return [input] if isinstance(input, str) else input


@overload
async def generate_embedding(
    input: str, config: EmbeddingConfig, input_type: Optional[EmbeddingInputType]
) -> EmbeddingVector: ...


@overload
async def generate_embedding(
    input: List[str], config: EmbeddingConfig, input_type: Optional[EmbeddingInputType]
) -> List[EmbeddingVector]: ...


async def generate_embedding(
    input: Union[str, List[str]],
    config: EmbeddingConfig,
    input_type: Optional[EmbeddingInputType] = EmbeddingInputType.DOCUMENT,
) -> Union[EmbeddingVector, List[EmbeddingVector]]:
    """
    Generate embeddings for single text input or batch of texts.

    Args:
        input: Single string or list of strings to embed
        config: Configuration object containing provider and model information

    Returns:
        Single embedding vector for single input, or list of embedding vectors for batch input

    Raises:
        ValueError: If input type is invalid or provider is not supported
        RuntimeError: If embedding generation fails
    """
    if not input:
        raise ValueError("Input cannot be empty")

    inputs = to_batch(input)
    provider_function = EMBEDDING_PROVIDER_REGISTRY.get(config.model_provider)

    if provider_function is None:
        raise ValueError(f"Unsupported provider: {config.model_provider}")

    params = EmbeddingParams(
        cfg=config,
        inputs=inputs,
        input_type=input_type,
    )

    try:
        if inspect.iscoroutinefunction(provider_function):
            # If the provider function is async, await it
            embeddings = await provider_function(params)
        else:
            embeddings = provider_function(params)
        return embeddings[0] if isinstance(input, str) else embeddings
    except Exception as e:
        raise RuntimeError(f"Failed to generate embeddings: {str(e)}") from e
