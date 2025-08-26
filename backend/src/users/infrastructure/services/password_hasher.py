import bcrypt

from src.users.domain.interfaces.password_hasher import IPasswordHasher


class BcryptPasswordHasher(IPasswordHasher):
    def hash(self, password: str) -> str:
        """
        Generate a bcrypt hash from a text password.

        :param password: Text password.
        :return: Hashed password as a UTF-8 encoded string.
        """
        pwd_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(pwd_bytes, salt)
        return hashed.decode("utf-8")
    
    def verify(self, password: str, hashed_password: str) -> bool:
        """
        Verify if a password matches the hashed one.

        :param password: Text password to check.
        :param hashed_password: Hashed password stored in the database.
        :return: True if the password matches, False otherwise.
        """
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))