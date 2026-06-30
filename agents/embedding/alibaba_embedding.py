"""Description
embedding client about alibaba

Date: 2026-6-24
Created by oldmerman
"""
import os
from typing import Tuple, List, Dict

from dotenv import load_dotenv
from openai import OpenAI

from agents.embedding.embedding_base import BaseEmbeddingAdapter
from agents.embedding.embedding_common import EmbeddingsGetterParam, EmbeddingUtils

load_dotenv()

def get_alibaba_embedding(api_key: str, base_url: str):
    return OpenAI(api_key=api_key, base_url=base_url).embeddings


class AlibabaEmbedding(BaseEmbeddingAdapter):

    def _get_client(self, param: EmbeddingsGetterParam):
        return OpenAI(api_key=param.api_key, base_url=param.base_url).embeddings

    def _send_request(self, client, batch: List[str], param: EmbeddingsGetterParam):
        return client.create(
            input=param.doc,
            model=param.model_name if param.model_name is not None else "text-embedding-v4",
            dimensions=param.dimensions
        )

    def _parse_response(self, response) -> Tuple[List[List[float]], Dict[str, int], str]:
        pre_response = EmbeddingUtils.dict_to_request_obj(response.model_dump_json())
        embeddings = [emb.embedding for emb in pre_response.data]
        usage = pre_response.usage
        model_name = pre_response.model
        return embeddings, usage.to_dict(), model_name

    def _get_batch_size(self) -> int:
        return 10

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

    o_client = get_alibaba_embedding(os.getenv("ALIBABA_API_KEY"),
                                   f"https://{os.getenv("ALIBABA_WORKSPACE_ID")}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")

    input_text = "老鱼人是一个热爱编程的计算机专业大学生"
    completion = o_client.create(
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