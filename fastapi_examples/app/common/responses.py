from fastapi import HTTPException, status

FORBIDDEN_RESPONSE = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Forbidden"
)
