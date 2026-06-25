"""Description
网页端基础对话功能实现

Date: 2026-6-18
Created by oldmerman
"""
import json

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field
from starlette.responses import StreamingResponse

from agents import AgentsFactory, AgentType
from agents.prompt import COMMON_PROMPT
from agents.rerank.rerank_provider import rerank
from agents.types import CommonContext
from db import ChromaVectorHelper
from utils import get_logger, ListSeparator

logger = get_logger(__name__)
router = APIRouter(prefix="/chat", tags=["agent"])


class OChatRequest(BaseModel):
    user_prompt: str = Field(description="请求的内容")
    collection_name: str = Field(description="选择的知识库名称")


@router.post("")
async def chat(dto: OChatRequest, req: Request):
    user_prompt = dto.user_prompt
    collection_name = dto.collection_name
    client_ip = req.client.host # 记录调用者ip地址
    if user_prompt is None or collection_name is None:
        return None

    factory = AgentsFactory()
    param = factory.build_agent(AgentType.COMMON)
    documents = ChromaVectorHelper(collection_name=collection_name).query([user_prompt]).get("documents")
    print(documents)
    # 重排序，根据系统配置判断，若不开启则会原样返回
    ranked_document = rerank(user_prompt, ListSeparator.convert_str_list(documents), client_ip)
    print(ranked_document)

    # 构建系统提示词
    system_msg = f"{COMMON_PROMPT}, Use this context:\n{ranked_document}"

    async def generate_response():
        for chunk in param.agent.stream(
                {"messages": [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_prompt}
                ]},
                context=CommonContext(user_id=client_ip, model_id=param.model_id,
                                          model_name=param.model_name),
                version="v2",
                stream_mode="messages"
        ):
            if chunk["type"] == "messages":
                token, metadata = chunk["data"]
                node_type = metadata.get('langgraph_node')
                if node_type == 'model':
                    token_text = getattr(token, 'content', '') or getattr(token, 'text', '')
                    if token_text:
                        yield f"data: {json.dumps({'chunk': token_text, 'type': 'content'})}\n\n"
                elif node_type == 'tool':
                    pass

        yield f"data: {json.dumps({'chunk': 'Finished', 'type': 'end'})}\n\n"

    return StreamingResponse(
        generate_response(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"}
    )