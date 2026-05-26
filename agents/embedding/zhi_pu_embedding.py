"""Description
embedding client about zhi_pu

Date: 2026-5-21
Created by oldmerman
"""

import os

from dotenv import load_dotenv
from zai import ZhipuAiClient

load_dotenv()

def get_zhi_pu_embedding(api_key: str):
    return ZhipuAiClient(api_key=api_key).embeddings
