import os

from dotenv import load_dotenv
from zai import ZhipuAiClient

from agents.embedding.embedding_provider import EmbeddingsGetterParam

"""Description
embedding client about zhi_pu

Date: 2026-5-21
Created by oldmerman
"""

load_dotenv()

def get_zhi_pu_embedding(api_key: str):
    return ZhipuAiClient(api_key=api_key).embeddings

def zhi_pu_embedding(param: EmbeddingsGetterParam):
    embedding = get_zhi_pu_embedding(param.api_key)
    return embedding.create(
        input=param.doc,
        model=param.model_name if param.model_name is not None else "embedding-3",
        dimensions=param.dimensions,
    )

if __name__ == "__main__":
    res = get_zhi_pu_embedding(os.getenv("ZHI_PU_API_KEY")).create(
        input=[
            '回忆是一行行无从剪接的风景，爱始终年轻',
            '你说把爱渐渐放开会走很远，又何必去改变已错过的时间'
        ],
        model='embedding-3',
        dimensions=512
    )
    print(res)

