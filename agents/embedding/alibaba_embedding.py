"""Description
embedding client about alibaba

Date: 2026-6-24
Created by oldmerman
"""
import os

from dotenv import load_dotenv
from openai import OpenAI

from agents.embedding.embedding_common import EmbeddingsGetterParam, EmbeddingsResponseParam, EmbeddingUtils
from utils import ListSeparator

load_dotenv()


def get_alibaba_embedding(api_key: str, base_url: str):
    return OpenAI(api_key=api_key, base_url=base_url).embeddings


class AlibabaEmbedding:

    @staticmethod
    def embeddings(param: EmbeddingsGetterParam) -> EmbeddingsResponseParam:
        embedding = get_alibaba_embedding(param.api_key, param.base_url)
        origin_list = param.doc

        all_embeddings = []
        total_prompt_tokens = 0
        total_completion_tokens = 0
        total_tokens = 0
        model_name = None

        BATCH_SIZE = 10
        if len(origin_list) <= BATCH_SIZE:
            # 单次处理
            pre_response = embedding.create(
                input=param.doc,
                model=param.model_name if param.model_name is not None else "text-embedding-v4",
                dimensions=param.dimensions
            )
            response = EmbeddingUtils.dict_to_request_obj(pre_response.model_dump_json())
            all_embeddings = [emb.embedding for emb in response.data]
            model_name = response.model
            total_prompt_tokens = response.usage.prompt_tokens
            total_completion_tokens = response.usage.completion_tokens
            total_tokens = response.usage.total_tokens
        else:
            # 分批处理
            batches = ListSeparator.chunk_array(origin_list, BATCH_SIZE)

            for batch in batches:
                pre_response = embedding.create(
                    input=batch,
                    model=param.model_name if param.model_name is not None else "text-embedding-v4",
                    dimensions=param.dimensions
                )
                response = EmbeddingUtils.dict_to_request_obj(pre_response.model_dump_json())
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
    # {"data": [
    #   {
    #       "embedding": [
    #                   0.027053870260715485,
    #                  -0.05642286688089371,
    #                  -0.03267631307244301,
    #                  -0.019893525168299675,
    #                   0.003697996260598302
    #                  ], "index": 0, "object": "embedding"
    #   }],
    #  "model": "text-embedding-v4", "object": "list", "usage": {"prompt_tokens": 11, "total_tokens": 11},
    #  "id": "d2538ad0-30dd-9fcf-bcbd-06bbbce70d06"}

    client = get_alibaba_embedding(os.getenv("ALIBABA_API_KEY"),
                                   f"https://{os.getenv("ALIBABA_WORKSPACE_ID")}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")

    input_text = "老鱼人是一个热爱编程的计算机专业大学生"
    completion = client.create(
        model="text-embedding-v4",
        input=input_text
    )

    o_result = completion.model_dump_json()
    m_response = EmbeddingUtils.dict_to_request_obj(o_result)
    m_all_embeddings = [emb.embedding for emb in m_response.data]
    m_usage = m_response.usage
    m_total_prompt_tokens = m_usage.prompt_tokens
    m_total_completion_tokens = m_usage.completion_tokens
    m_total_tokens = m_usage.total_tokens
    print(f"embeddings: {m_all_embeddings}")
    print(f"prompt_tokens: {m_total_prompt_tokens}")
    print(f"completion_tokens: {m_total_completion_tokens}")