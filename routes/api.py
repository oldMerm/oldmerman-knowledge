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
from common.utils.common_utils import agent_time_record
from db.connection import get_db_connection
from common.utils import get_logger


load_dotenv()

logger = get_logger(__name__)

router = APIRouter(prefix="/v1", tags=["api"])


class ArticleGenBody(BaseModel):
    article_id: str
    article_name: str
    content: str
    model_id: str = None


@router.post("")
@agent_time_record
async def chat(dto: ArticleGenBody):
    # 暂不启用
    return None
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

    user_prompt = dto.content
    async def generate_response():
        param = AgentsFactory().build_agent(AgentType.DIGEST)
        for chunk in param.agent.stream(
                {"messages": [{"role": "user", "content": user_prompt}]},
                context=ArticleContext(article_id=dto.article_id, article_name=dto.article_name,
                                              model_id=param.model_id, model_name=param.model_name, user_id="merman-blog"), # user_id可覆盖
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
