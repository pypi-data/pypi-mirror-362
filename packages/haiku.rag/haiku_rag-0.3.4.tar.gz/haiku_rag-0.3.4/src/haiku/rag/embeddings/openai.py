try:
    from openai import AsyncOpenAI

    from haiku.rag.config import Config
    from haiku.rag.embeddings.base import EmbedderBase

    class Embedder(EmbedderBase):
        _model: str = Config.EMBEDDINGS_MODEL
        _vector_dim: int = 1536

        async def embed(self, text: str) -> list[float]:
            client = AsyncOpenAI()
            response = await client.embeddings.create(
                model=self._model,
                input=text,
            )
            return response.data[0].embedding

except ImportError:
    pass
