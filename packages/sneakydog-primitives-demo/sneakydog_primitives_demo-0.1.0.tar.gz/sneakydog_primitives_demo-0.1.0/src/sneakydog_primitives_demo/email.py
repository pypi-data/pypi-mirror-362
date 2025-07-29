from dataclasses import dataclass
from sneakydog_primitives_demo.value_objects import ValueObject

@dataclass(frozen=True)
class Email(ValueObject[str]):

    @classmethod
    def validate_value(cls, value: str):
        if '@' not in value:
            raise ValueError(f"Invalid email: {value}")