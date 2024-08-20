import random

import pyotp


class OtpManager:
    def __init__(self, secret: str) -> None:
        self._hotp = pyotp.HOTP(secret)

    @staticmethod
    def generate_secret() -> str:
        return pyotp.random_base32()

    @staticmethod
    def generate_random_integer(
        lower_bound: int = 1, upper_bound: int = 10_000_000
    ) -> int:
        return random.randint(lower_bound, upper_bound)

    def generate_otp(self, random_int: int) -> str:
        return self._hotp.generate_otp(random_int)

    def verify_otp(self, otp: str, random_int: int) -> bool:
        """Return true if the otp is valid"""
        return self._hotp.verify(otp, random_int)
