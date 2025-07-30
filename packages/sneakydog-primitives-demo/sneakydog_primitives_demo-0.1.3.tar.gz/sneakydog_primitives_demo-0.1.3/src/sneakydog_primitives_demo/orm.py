from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column
from sqlalchemy.orm import Mapped, mapped_column
from sneakydog_primitives_demo.email import Email, EmailTypeDecorator
from sneakydog_primitives_demo.user_id import UserId, UserIdTypeDecorator
from typing import get_args, Annotated

type_map = {
    Email: EmailTypeDecorator,
    UserId: UserIdTypeDecorator,
    # 其他值对象 → 映射
}


class EntityObject(DeclarativeBase):
    pass
    # def __init_subclass__(cls, **kwargs):
    #     super().__init_subclass__(**kwargs)
    #     for attr_name, hint in cls.__annotations__.items():
    #         origin_type = get_args(hint)[0] if hasattr(hint, "__origin__") else hint
    #         if origin_type in type_map:
    #             if not hasattr(cls, attr_name):
    #                 setattr(cls, attr_name, mapped_column(type_map[origin_type]()))
