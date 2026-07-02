"""Description
公共工具包

Date: 2026-7-2
Created by oldmerman
"""
import datetime
import random


def generate_thread_id(sign: str) -> str:
    """生成根据提供标识生成唯一的 thread_id """
    time_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    random_num = random.randint(100000, 999999)
    thread_id = f"{sign}-{time_str}-{random_num}"
    return thread_id

if __name__ == "__main__":
    print(generate_thread_id("::1")) # ::1-20260702200840-569910