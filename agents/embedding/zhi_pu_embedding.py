"""Description
embedding client about zhi_pu

Date: 2026-5-21
Created by oldmerman
"""

import os

from dotenv import load_dotenv
from zai import ZhipuAiClient

from agents.embedding.common import EmbeddingsGetterParam, EmbeddingsResponseParam
from utils import ListSeparator

load_dotenv()

def get_zhi_pu_embedding(api_key: str):
    return ZhipuAiClient(api_key=api_key).embeddings

class ZhiPuEmbedding:

    @staticmethod
    def embeddings(param: EmbeddingsGetterParam) -> EmbeddingsResponseParam:
        embedding = get_zhi_pu_embedding(param.api_key)
        origin_list = param.doc

        all_embeddings = []
        total_prompt_tokens = 0
        total_completion_tokens = 0
        total_tokens = 0
        model_name = None

        BATCH_SIZE = 50
        if len(origin_list) <= BATCH_SIZE:
            # 单次处理
            response = embedding.create(
                input=param.doc,
                model=param.model_name if param.model_name is not None else "embedding-3",
                dimensions=param.dimensions
            )
            all_embeddings = [emb.embedding for emb in response.data]
            model_name = response.model
            total_prompt_tokens = response.usage.prompt_tokens
            total_completion_tokens = response.usage.completion_tokens
            total_tokens = response.usage.total_tokens
        else:
            # 分批处理
            batches = ListSeparator.chunk_array(origin_list, BATCH_SIZE)

            for batch in batches:
                response = embedding.create(
                    input=batch,
                    model=param.model_name if param.model_name is not None else "embedding-3",
                    dimensions=param.dimensions
                )

                # 收集 embedding 数据
                all_embeddings.extend([emb.embedding for emb in response.data])

                # 累加 token 使用量
                total_prompt_tokens += response.usage.prompt_tokens
                total_completion_tokens += response.usage.completion_tokens
                total_tokens += response.usage.total_tokens

                # 记录模型名称（所有批次应该相同）
                if model_name is None:
                    model_name = response.model

        return EmbeddingsResponseParam(
            model_name=model_name,
            data=all_embeddings,
            tokens={
                "prompt_tokens": total_prompt_tokens,
                "completion_tokens": total_completion_tokens,
                "total_tokens": total_tokens
            }
        )

if __name__ == "__main__":
    client = get_zhi_pu_embedding(os.getenv("ZHI_PU_API_KEY"))
    res = client.create(input=["今天天气如何呢?", "我今天中午吃了两碗饭"], model="embedding-3")
    print(res.data)
    print(res.usage.prompt_tokens)
    print(res.usage.completion_tokens)
    print(res.usage.total_tokens)