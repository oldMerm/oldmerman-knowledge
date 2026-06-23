"""Description
Controller about auth

Date: 2026-4-23
Created by oldmerman
"""

import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from dotenv import load_dotenv
from pydantic import BaseModel

from agents import AgentsFactory, AgentType
from agents.tool.article_summary import ArticleContext
from common import Result
from db.connection import get_db_connection
from utils.logger import get_logger


load_dotenv()

logger = get_logger(__name__)

router = APIRouter(prefix="/v1", tags=["agent"])


class ArticleGenBody(BaseModel):
    article_id: str
    article_name: str
    content: str
    model_id: str = None

@router.post("")
async def chat(dto: ArticleGenBody):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            query = """
                    SELECT article_summary
                    FROM cache.summary_cache
                    WHERE article_id = %s
                      AND created_at >= NOW() - INTERVAL '7 DAY'
                    """
            cur.execute(
                query,
                (dto.article_id,)
            )
            row = cur.fetchone()
            if row:
                return Result.success(data=row[0])

    async def generate_response():
        param = AgentsFactory().build_agent(AgentType.DIGEST)
        for chunk in param.agent.stream(
                {"messages": [{"role": "user", "content": dto.content}]},
                context=ArticleContext(article_id=dto.article_id, article_name=dto.article_name,
                                              model_id=param.model_id, model_name=param.model_name), # user_id可覆盖
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
                    pass  # 工具节点可单独处理
        yield f"data: {json.dumps({'chunk': 'Finished', 'type': 'end'})}\n\n"

    return StreamingResponse(
        generate_response(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"}
    )


if __name__ == "__main__":
    # 打开文件并读取内容
    with open(r'C:\Users\asus\Desktop\博客部署\文章\灰沙随水至 青田依水生.md', 'r', encoding='utf-8') as file:
        content = file.read()

    factory = AgentsFactory()
    param = factory.build_agent(AgentType.DIGEST)
    for chunk in param.agent.stream(
            {"messages": [{"role": "user", "content": content}]},
            context=ArticleContext(article_id="cc1babd11588417aac36f5472100f7c7", article_name="灰沙随水至 青田依水生",
                                          model_id=param.model_id, model_name=param.model_name),
            stream_mode="messages",
            version="v2"
    ):
        if chunk["type"] == "messages":
            token, metadata = chunk["data"]

            if metadata.get('langgraph_node') == 'model':
                text = getattr(token, 'content', '') or getattr(token, 'text', '')
                if text:
                    # 真实场景换成SSE向调用方响应一个个chunk即可
                    print(text, end='', flush=True)
