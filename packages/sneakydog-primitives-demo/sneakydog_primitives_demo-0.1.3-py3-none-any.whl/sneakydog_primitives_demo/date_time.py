from dataclasses import dataclass
from datetime import datetime
from sneakydog_primitives_demo.value_objects import ValueObject


@dataclass(frozen=True)
class DateTime(ValueObject[datetime]): ...