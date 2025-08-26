from dataclasses import dataclass


@dataclass
class EntityBase:
    @property
    def dict(self):
        return self.__dict__
