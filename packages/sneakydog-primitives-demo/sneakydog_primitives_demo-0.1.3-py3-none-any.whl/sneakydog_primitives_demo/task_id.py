from dataclasses import dataclass
from uuid import UUID
from sneakydog_primitives_demo.value_objects import ValueObject


@dataclass(frozen=True)
class TaskId(ValueObject[UUID]): ...