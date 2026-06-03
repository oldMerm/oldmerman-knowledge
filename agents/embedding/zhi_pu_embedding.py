"""Description
embedding client about zhi_pu

Date: 2026-5-21
Created by oldmerman
"""

import os

from dotenv import load_dotenv
from zai import ZhipuAiClient

from agents.embedding.common import EmbeddingsGetterParam, EmbeddingsResponseParam

load_dotenv()

def get_zhi_pu_embedding(api_key: str):
    return ZhipuAiClient(api_key=api_key).embeddings

class ZhiPuEmbedding:

    @staticmethod
    def embeddings(param: EmbeddingsGetterParam) -> EmbeddingsResponseParam:
        embedding = get_zhi_pu_embedding(param.api_key)
        response = embedding.create(
            input=param.doc,
            model=param.model_name if param.model_name is not None else "embedding-3",
            dimensions=param.dimensions
        )
        return EmbeddingsResponseParam(
            model_name=response.model,
            data=[emb.embedding for emb in response.data],
            tokens={
                "prompt_tokens": response.usage.prompt_tokens | 0,
                "completion_tokens": response.usage.completion_tokens | 0,
                "total_tokens": response.usage.total_tokens | 0
            }
        )

if __name__ == "__main__":
    client = get_zhi_pu_embedding(os.getenv("ZHI_PU_API_KEY"))
    res = client.create(input=["今天天气如何呢?", "我今天中午吃了两碗饭"], model="embedding-3")
    print(res.data)
    print(res.usage.prompt_tokens)
    print(res.usage.completion_tokens)
    print(res.usage.total_tokens)