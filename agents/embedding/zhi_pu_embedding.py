"""Description
embedding client about zhi_pu

Date: 2026-5-21
Created by oldmerman
"""
from typing import Tuple, List, Dict
from zai import ZhipuAiClient

from agents.embedding.embedding_base import BaseEmbeddingAdapter
from agents.embedding.embedding_common import EmbeddingsGetterParam


class ZhiPuEmbedding(BaseEmbeddingAdapter):

    def _get_client(self, param: EmbeddingsGetterParam):
        return ZhipuAiClient(api_key=param.api_key).embeddings

    def _send_request(self, client, batch: List[str], param: EmbeddingsGetterParam):
        return client.create(
            input=param.doc,
            model=param.model_name if param.model_name is not None else "embedding-3",
            dimensions=param.dimensions
        )

    def _parse_response(self, response) -> Tuple[List[List[float]], Dict[str, int], str]:
        embeddings = [emb.embedding for emb in response.data]
        usage = response.usage
        model_name = response.model
        return embeddings, usage, model_name

    def _get_batch_size(self) -> int:
        return 60
