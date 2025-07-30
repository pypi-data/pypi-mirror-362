from dataclasses import dataclass
from uuid import UUID
from sqlalchemy.types import TypeDecorator, UUID as saUUID
from sneakydog_primitives_demo.value_objects import ValueObject


@dataclass(frozen=True)
class AnnotationId(ValueObject[UUID]): ...


# 2. 自定义 SQLAlchemy 类型
class EmailTypeDecorator(TypeDecorator):
    impl = saUUID
    cache_ok = True  # ✅ SQLAlchemy 2.x 要求设置

    def process_bind_param(self, value, dialect):
        # 存到数据库前
        if isinstance(value, AnnotationId):
            return value.value
        elif isinstance(value, str):
            return value
        elif value is None:
            return None
        else:
            raise ValueError("Invalid AnnotationId")

    def process_result_value(self, value, dialect):
        # 从数据库读出时
        if value is not None:
            return AnnotationId(value)
        return None
