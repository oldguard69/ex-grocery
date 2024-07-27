import os
from datetime import datetime, timedelta, UTC
from typing import Any

import jwt

# Secret key for encoding and decoding JWTs
SECRET_KEY = os.environ["SECRET_KEY"]


def generate_jwt(
    payload: dict, secret_key: str = SECRET_KEY, algorithm: str = "HS256"
) -> str:

    payload_copy = payload.copy()
    payload_copy["exp"] = datetime.now(UTC) + timedelta(hours=1)
    token = jwt.encode(payload_copy, secret_key, algorithm=algorithm)
    return token


def verify_jwt(
    token: str, secret_key: str = SECRET_KEY, algorithm: str = "HS256"
) -> dict:
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=[algorithm])
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
