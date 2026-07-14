"""Description
网页端基础对话功能实现

Date: 2026-6-18
Created by oldmerman
"""
import contextvars
import datetime
import json

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field
from starlette.responses import StreamingResponse

from agents import AgentsFactory, AgentType
from agents.rerank.rerank_provider import rerank
from agents.types import CommonContext
from common.utils.common_utils import agent_time_record
from db import ChromaVectorHelper
from common.utils import get_logger, ListSeparator

logger = get_logger(__name__)
router = APIRouter(prefix="/chat", tags=["agent"])

# 定义上下文变量，提供外部（如装饰器）读取
current_ai_metadata = contextvars.ContextVar("current_ai_metadata")


class OChatRequest(BaseModel):
    user_prompt: str = Field(description="请求的内容")
    sign: str = Field(description="请求标识，随机的六位字符串")


@router.post("")
@agent_time_record
async def chat(dto: OChatRequest, req: Request):
    user_prompt = dto.user_prompt
    client_ip = req.client.host  # 记录调用者ip地址
    if user_prompt is None:
        return None

    logger.info(f"用户: {client_ip} 请求， prompt: {user_prompt}")
    factory = AgentsFactory()
    param = factory.build_agent(AgentType.COMMON)
    documents = ChromaVectorHelper().query(client_ip, [user_prompt]).get("documents")
    # 重排序，根据系统配置判断，若不开启则会原样返回
    ranked_document = await rerank(user_prompt, ListSeparator.convert_str_list(documents), client_ip)

    # 构建提示词
    prompt = f"参考文档: {ranked_document}, \n用户输入: {user_prompt}"
    # sign生成于前端(前端可重新生成使线程id过期)，后端拼接时间戳实现自动过期(1h)
    thread_id = f"{client_ip}-{dto.sign}-{datetime.datetime.now().strftime('%Y%m%d%H')}"

    # 设置上下文变量
    current_ai_metadata.set({"thread_id": thread_id, "model_id": param.model_id, "user_prompt": user_prompt})

    async def generate_response():
        for chunk in param.agent.stream(
                {"messages": [
                    {"role": "user", "content": prompt}
                ]},
                {"configurable": {"thread_id": thread_id}},
                context=CommonContext(user_id=client_ip, model_id=param.model_id, model_name=param.model_name),
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
