from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.constants import RoleEnum
from app.common.database import create_new_session
from app.common.jwt_helper import generate_jwt, verify_jwt
from app.common.models import User
from app.common.otp_manager import OtpManager
from app.common.password_hasher import hash_password, is_password_correct
from app.common.schemas import LoginDto, RegisterDto, VerifyEmailDto


def find_user_by_email(session: Session, email: str) -> User | None:
    return session.scalar(select(User).where(User.email == email))


def get_current_user_without_email_verified_require(
    authorization: Annotated[str | None, Header()] = None,
    session: Session = Depends(create_new_session),
) -> User:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing Authorization Token",
        )
    if not authorization.startswith("Bearer"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Token"
        )
    try:
        token = authorization.split(" ")[1]
        decoded_token = verify_jwt(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(  # noqa: B904
            status_code=status.HTTP_400_BAD_REQUEST, detail="Token has expired"
        )
    except (jwt.InvalidTokenError, Exception):
        raise HTTPException(  # noqa: B904
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        )

    user = session.scalar(select(User).where(User.email == decoded_token["email"]))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user


def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    session: Session = Depends(create_new_session),
) -> User:
    user = get_current_user_without_email_verified_require(authorization, session)
    if not user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Email has not verified"
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


def handle_register(session: Session, register_dto: RegisterDto) -> dict:
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
            otp_secret=OtpManager.generate_secret(),
        )
    )
    session.commit()
    return {"message": "success"}


def send_verification_email(session: Session, user: User) -> dict:
    if user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already verified the email",
        )
    if not user.otp_secret:
        user.otp_secret = OtpManager.generate_secret()

    otp_manager = OtpManager(user.otp_secret)
    user.otp_random_int = otp_manager.generate_random_integer()
    otp = otp_manager.generate_otp(user.otp_random_int)
    print(f"Send this otp to user: {otp}")
    user.otp_expired_at = datetime.now(UTC) + timedelta(seconds=30)
    session.add(user)
    session.commit()
    return {"message": "Email sent"}


def verify_email(session: Session, user: User, body: VerifyEmailDto) -> dict:
    otp_manager = OtpManager(user.otp_secret)
    is_otp_valid = otp_manager.verify_otp(body.otp, user.otp_random_int)
    is_otp_expired = user.otp_expired_at < datetime.now(UTC)
    if is_otp_valid and not is_otp_expired:
        user.otp_random_int = None
        user.otp_expired_at = None
        user.email_verified = True
        session.add(user)
        session.commit()
        return {"message": "Email verified"}
    if not is_otp_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid otp"
        )
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Otp expired")
