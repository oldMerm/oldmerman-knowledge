import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, status
from pydantic import BaseModel

"""Description
The package of jwt token

Date: 2026-4-22
Created by oldmerman
"""

load_dotenv()

TOKEN_EXPIRE_HOURS = 2


class TokenData(BaseModel):
    user_id: str
    username: str

# 获取jwt密钥
def get_jwt_secret() -> str:
    secret = os.getenv("JWT_SECRET")
    if not secret:
        raise ValueError("JWT_SECRET environment variable not set")
    return secret

# 验签逻辑
def verify_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(
            token,
            get_jwt_secret(),
            algorithms=["HS256"],
            options={"require_exp": True}
        )
        user_id = payload.get("user_id")
        username = payload.get("username")
        if user_id is None or username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        return TokenData(user_id=user_id, username=username)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

# 签发token
def create_token(user_id: str, username: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "user_id": user_id,
        "username": username,
        "iat": now,
        "exp": now + timedelta(hours=TOKEN_EXPIRE_HOURS) # 添加过期时间，decode时自动校验过期
    }
    return jwt.encode(payload, get_jwt_secret(), algorithm="HS256")