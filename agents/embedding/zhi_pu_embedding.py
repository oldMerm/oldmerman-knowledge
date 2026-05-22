from zai import ZhipuAiClient

"""Description
embedding register about zhi_pu

Date: 2026-5-21
Created by oldmerman
"""

def get_zhi_pu_embedding(api_key: str):
    return ZhipuAiClient(api_key=api_key)
