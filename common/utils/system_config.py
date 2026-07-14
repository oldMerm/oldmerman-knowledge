"""Description
系统配置，支持缓存

Date: 2026-6-23
Created by oldmerman
"""
import json
import time
import uuid
from typing import Optional

from db.connection import get_db_connection


class SystemConfig:

    def __init__(self, cache_ttl: int = 10):
        self.cache_ttl = cache_ttl
        self._cache = {} # key: config_key, value: dict
        self._cache_time = {}

    def get_config(self, key: str) -> Optional[dict]:
        """获取配置信息，JSON格式"""
        now = time.time()

        # 检查缓存
        if key in self._cache and (now - self._cache_time.get(key, 0) < self.cache_ttl):
            return self._cache[key]

        # 未查到缓存，走数据库
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                sql = "SELECT config_value FROM system_configs WHERE config_key = %s"
                cur.execute(sql, (key, ))
                row = cur.fetchone()

        if row:
            value = dict(row[0])
        else:
            value = {}

        # 更新缓存
        self._cache[key] = value
        self._cache_time[key] = now
        return value

    def set_config(self, key: str, new_config: dict, user_id: str, description: str = None) -> bool:
        """新增(或修改)需要缓存的系统配置"""
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO system_configs (config_key, config_value, description, updated_by)
                    VALUES (%s, %s::jsonb, %s, %s) ON CONFLICT (config_key) DO
                    UPDATE
                        SET config_value = EXCLUDED.config_value, updated_at = CURRENT_TIMESTAMP, updated_by = EXCLUDED.updated_by
                    """,
                    (key, json.dumps(new_config), description, user_id)
                )
                conn.commit()

        # 清理缓存
        self._cache.pop(key, None)
        self._cache_time.pop(key, None)
        return True

config_client = SystemConfig()
def get_config_client() -> SystemConfig:
    return config_client


if __name__ == "__main__":
    client = SystemConfig()
    print(client.get_config("rerank_config"))