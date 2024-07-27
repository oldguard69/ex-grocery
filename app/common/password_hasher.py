import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()


def is_password_correct(plain_password: str, hashed_password: str) -> bool:
    """Return true if the plain_password and hashed_password is the same"""
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())