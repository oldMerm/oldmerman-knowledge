"""Description
异步http客户端，用于ai耗时请求

Date: 2026-7-4
Created by oldmerman
"""
import httpx
from typing import Optional

class AsyncHTTPClient:
    """异步HTTP客户端"""
    _instance: Optional[httpx.AsyncClient] = None

    @classmethod
    def get_client(cls) -> httpx.AsyncClient:
        if cls._instance is None:
            cls._instance = httpx.AsyncClient(
                timeout=httpx.Timeout(30.0),
                limits=httpx.Limits(
                    max_keepalive_connections=20,
                    max_connections=100
                )
            )

        return cls._instance

    @classmethod
    async def close(cls):
        if cls._instance:
            await cls._instance.aclose()
            cls._instance = None


def get_http_client() -> httpx.AsyncClient:
    return AsyncHTTPClient.get_client()