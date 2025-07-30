from dataclasses import dataclass
from typing import TypeVar, Generic, Type, Any, Iterator
from abc import ABC

from pydantic import BaseModel as _BaseModel, ValidationInfo

T = TypeVar("T")


@dataclass(frozen=True)
class ValueObject(Generic[T], ABC):
    value: T

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value!r})"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def __json__(self) -> Any:
        # 序列化输出裸值
        return self.value

    @classmethod
    def __get_validators__(cls) -> Iterator:
        yield cls.validate

    @classmethod
    def validate(
        cls: Type["ValueObject"], v: Any, info: ValidationInfo = None, **kwargs
    ) -> "ValueObject":
        if isinstance(v, cls):
            return v
        cls.validate_value(v)
        return cls(v)

    @classmethod
    def validate_value(cls, v: Any):
        # 子类覆写实现具体校验逻辑
        pass


class DTO(_BaseModel):
    class Config:
        json_encoders = {ValueObject: lambda v: v.__json__() if v is not None else None}
        from_attributes = True  # ✅ Pydantic v2 用这个代替 orm_mode
