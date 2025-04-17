import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class UserId:
    value: str

    def __post_init__(self):
        if not self.value:
            object.__setattr__(self, "value", str(uuid.uuid4()))

    def __str__(self) -> str:
        return self.value
