import os
from datetime import UTC, datetime, timedelta

import jwt

# Secret key for encoding and decoding JWTs
SECRET_KEY = os.environ["SECRET_KEY"]


def generate_jwt(
    payload: dict, secret_key: str = SECRET_KEY, algorithm: str = "HS256"
) -> str:

    payload_copy = payload.copy()
    payload_copy["exp"] = datetime.now(UTC) + timedelta(hours=1)
    return jwt.encode(payload_copy, secret_key, algorithm=algorithm)


def verify_jwt(
    token: str, secret_key: str = SECRET_KEY, algorithm: str = "HS256"
) -> dict:
    try:
        return jwt.decode(token, secret_key, algorithms=[algorithm])
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
