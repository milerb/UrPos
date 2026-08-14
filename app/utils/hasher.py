from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


class Hasher:
    """
    Class for hashing algorithm.
    """

    # Add parameters here to pass as arguments to the PasswordHasher.
    hasher = PasswordHasher()

    def hash(self, password: str, salt: bytes | None = None) -> str:
        """
        Hashes given password with given salt if not None.
        """
        hashed_password: str = self.hasher.hash(password=password, salt=salt)
        return hashed_password

    def verify(self, stored_hash: str | bytes, user_password: str) -> bool:
        """
        Verifies password hash.
        Returns True is matched otherwise False.
        """
        try:
            self.hasher.verify(hash=stored_hash, password=user_password)
        except VerifyMismatchError:
            return False
        return True
