from abc import ABC, abstractmethod


class IPasswordHasher(ABC):
    @abstractmethod
    def hash(self, password: str) -> str:
        """Generate a hash from a text password."""
        pass

    @abstractmethod
    def verify(self, password: str, hashed_password: str) -> bool:
        """Verify is a password matches the hashed one."""
        pass
