from typing import Annotated

from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Header, Depends

from app.common.models import User
from app.common.jwt_helper import verify_jwt, generate_jwt
from app.common.schemas import LoginDto, RegisterDto
from app.common.password_hasher import is_password_correct, hash_password
from app.common.constants import RoleEnum
from app.common.database import create_new_session


def find_user_by_email(session: Session, email: str) -> User | None:
    return session.scalar(select(User).where(User.email == email))


def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    session: Session = Depends(create_new_session),
):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Missing Authorization Token"
        )
    if not authorization.startswith("Bearer"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Token"
        )
    try:
        token = authorization.split(" ")[1]
        decoded_token = verify_jwt(token)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Token"
        )

    user = session.scalar(select(User).where(User.email == decoded_token["email"]))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user


def handle_login(session: Session, login_dto: LoginDto) -> dict:
    user = find_user_by_email(session, login_dto.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or password is incorrect",
        )
    if not is_password_correct(login_dto.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or password is incorrect",
        )
    return {
        "access_token": generate_jwt(
            {
                "email": user.email,
                "role": {
                    "role_id": user.role.role_id,
                    "description": user.role.description,
                },
            }
        ),
        "token_type": "bearer",
    }


def handle_register(session: Session, register_dto: RegisterDto):
    user = find_user_by_email(session, register_dto.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There is already an account with this email",
        )
    session.add(
        User(
            email=register_dto.email,
            hashed_password=hash_password(register_dto.password),
            role_id=RoleEnum.CUSTOMER,
        )
    )
    session.commit()
    return {"message": "success"}
