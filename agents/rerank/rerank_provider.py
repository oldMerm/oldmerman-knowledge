"""Description
各类重排序功能的集成，通过URL访问，获取统一的响应结果

Date: 2026-6-23
Created by oldmerman
"""
from config import get_settings
from db.dao import ModelsRepository, TokensUsageRepository

import requests

from utils import get_logger, get_config_client

logger = get_logger(__name__)
Settings = get_settings()
RERANK_CONFIG_KEY = "rerank_config"


def set_rerank(model_id: int, user_id: str):
    dao = ModelsRepository.as_dependency()
    model_param = dao.select_model(model_id)
    metadata = {
        "rerank.enabled": True,
        "model_id": model_id,
        "model": model_param.model_name,
        "base_url": model_param.base_url,
        "api_key": model_param.api_key,
    }
    get_config_client().set_config(RERANK_CONFIG_KEY, metadata, user_id,"重排序模型的相关配置，如是否开启，请求所需数据等")


def rerank(query: str, documents: list[str], user_id: str):
    metadata = get_config_client().get_config(RERANK_CONFIG_KEY)
    if not metadata.get("rerank.enabled"):
        return documents

    # 获取数据，构造请求体
    api_key = metadata.get("api_key", "")
    url = metadata.get("base_url", "")
    model = metadata.get("model", "")
    model_id = metadata.get("model_id", 0)
    if not url or not model or not api_key or not model_id:
        metadata = {"rerank.enabled": False}
        get_config_client().set_config(RERANK_CONFIG_KEY, metadata, "system")
        return documents
    payload = {
        "model": model,
        "query": query,
        "documents": documents,
        "top_n": Settings.RERANK_TOP_N
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(url=url, json=payload, headers=headers)
    if response.status_code == 200:
        # rerank正常响应，记录token消耗
        result = response.json()
        sorted_documents = [documents[item["index"]] for item in result["results"]]
        TokensUsageRepository.as_dependency().add(user_id, model_id, result["usage"])
        return sorted_documents
    else:
        # 响应出错
        logger.warning(f"请求失败, code: {response.status_code}")
    return documents


if __name__ == "__main__":
    # set_rerank(1013, "f191749f-e9ed-4fcf-8a77-98a4d1a36f1c")
    # {'created': 1782217062, 'id': 'xxxx', 'request_id': 'xxxx',
    # 'results': [
    # {'index': 2, 'relevance_score': 1.0},
    # {'index': 1, 'relevance_score': 1.0},
    # {'index': 0, 'relevance_score': 1.0},
    # {'index': 3, 'relevance_score': 0.9999993},
    # {'index': 4, 'relevance_score': 0.99999654}],
    # 'usage': {'completion_tokens': 0, 'prompt_tokens': 723, 'total_tokens': 723}}
    m_query = "如何有效预防和管理高血压？"
    m_documents = [

        # 2. 高度相关 - 具体饮食建议
        "DASH饮食（得舒饮食）被证明能有效降低血压，强调多吃蔬菜、水果、全谷物和低脂乳制品，减少红肉和甜食。",

        # 3. 中度相关 - 生活方式管理
        "管理高血压除了药物治疗外，戒烟限酒、减轻压力、保证充足睡眠也是重要的非药物治疗手段。",

        # 4. 中度相关 - 药物管理
        "常用降压药包括ACEI、ARB、钙通道阻滞剂和利尿剂，患者需要遵医嘱规律服药，不可随意停药或换药。",

        # 5. 低度相关 - 相关但偏诊断
        "高血压的诊断标准是收缩压≥140mmHg和/或舒张压≥90mmHg，需要非同日三次测量才能确诊。",

        # 6. 不相关 - 糖尿病话题
        "1型糖尿病是由于胰岛素绝对缺乏引起的，患者需要终身依赖胰岛素治疗，并定期监测血糖水平。",

        # 7. 不相关 - 心脏病话题
        "冠心病是由于冠状动脉粥样硬化导致血管狭窄或阻塞，典型症状是胸痛，常在劳累或情绪激动时诱发。",

        # 8. 不相关 - 运动健身一般话题
        "力量训练可以增加肌肉量和基础代谢率，建议每周进行2-3次，每次针对主要肌群进行8-12次重复训练。",

        # 9. 不相关 - 营养补充剂
        "维生素D对钙吸收至关重要，缺乏维生素D可能导致骨质疏松，建议老年人适当补充维生素D和钙剂。",

        # 10. 不相关 - 完全无关
        "2024年巴黎奥运会新增了霹雳舞项目，这是奥运会首次引入街舞元素，吸引了大量年轻观众关注。",

        # 1. 高度相关 - 直接回答
        "预防高血压需要控制钠盐摄入，每日不超过5克，同时保持规律运动，每周至少150分钟中等强度有氧运动。",
    ]
    ranked_document = rerank(m_query, m_documents, "f191749f-e9ed-4fcf-8a77-98a4d1a36f1c")
    print(ranked_document)
