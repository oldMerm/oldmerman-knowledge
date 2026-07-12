"""Description
公共工具包

Date: 2026-7-2
Created by oldmerman
"""
import inspect
import random
from datetime import datetime
from functools import wraps

from common.utils import get_logger
from db.dao.request_time_log_repository import RequestTimeLogRepository
from db.entities import RequestTimeLog

logger = get_logger(__name__)


def generate_thread_id(sign: str) -> str:
    """生成根据提供标识生成唯一的 thread_id """
    time_str = datetime.now().strftime('%Y%m%d%H%M%S')
    random_num = random.randint(100000, 999999)
    thread_id = f"{sign}-{time_str}-{random_num}"
    return thread_id


def agent_time_record(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        """耗时记录，用于记录大模型的响应耗时"""
        from routes.chat import current_ai_metadata

        start = datetime.now()
        result = await func(*args, **kwargs)
        end = datetime.now()

        # 记录耗时
        request_time = end - start

        # 获取函数签
        func_sign = inspect.signature(func)

        # 获取函数名
        func_name = func.__name__

        # 获取函数所在模块
        func_module = func.__module__

        session_metadata = current_ai_metadata.get(None)
        prompt = session_metadata.get("user_prompt")
        thread_id = session_metadata.get("thread_id")
        model_id = session_metadata.get("model_id")
        total_seconds = request_time.total_seconds()

        logger.info(f"函数调用: {func_module}.{func_name}{func_sign}, 响应耗时: {total_seconds}s")
        logger.info(f"用户提示词: {prompt}, thread_id: {thread_id}")
        RequestTimeLogRepository.as_dependency().log(
            param=RequestTimeLog(thread_id=thread_id, total_duration=total_seconds, prompt=prompt, model_id=model_id))
        return result

    return wrapper


if __name__ == "__main__":
    print(generate_thread_id("::1"))  # ::1-20260702200840-569910
