from dataclasses import dataclass
from sqlalchemy.types import TypeDecorator, String
from sneakydog_primitives_demo.value_objects import ValueObject


@dataclass(frozen=True)
class Email(ValueObject[str]):
    @classmethod
    def validate_value(cls, value: str):
        if "@" not in value:
            raise ValueError(f"Invalid email: {value}")


# 2. 自定义 SQLAlchemy 类型
class EmailTypeDecorator(TypeDecorator):
    impl = String
    cache_ok = True  # ✅ SQLAlchemy 2.x 要求设置

    def process_bind_param(self, value, dialect):
        # 存到数据库前
        if isinstance(value, Email):
            return value.value
        elif isinstance(value, str):
            return value
        elif value is None:
            return None
        else:
            raise ValueError("Invalid Email")

    def process_result_value(self, value, dialect):
        # 从数据库读出时
        if value is not None:
            return Email(value)
        return None
