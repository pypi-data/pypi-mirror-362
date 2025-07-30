import uuid
from sqlalchemy import create_engine
from sqlalchemy import String
from typing import Optional, Annotated
import json
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column,Session
from sneakydog_primitives_demo.email import Email, EmailTypeDecorator
from sneakydog_primitives_demo.user_id import UserId, UserIdTypeDecorator
from sneakydog_primitives_demo.project_id import ProjectId
from sneakydog_primitives_demo.value_objects import DTO
from sneakydog_primitives_demo.orm import EntityObject


class UserDTO(DTO):
    userId: UserId
    email: Email
    # class Config:
    #     from_attributes = True  # ✅ Pydantic v2 用这个代替 orm_mode


class Base(DeclarativeBase):
    pass


class UserEntity(EntityObject):
    __tablename__ = "user_account"
    userId: Mapped[UserId] = mapped_column(UserIdTypeDecorator(), primary_key=True)
    # projectId: ProjectId = None
    # id: Mapped[int] = mapped_column(primary_key=True)
    # name: Mapped[str] = mapped_column(String(30))
    # fullname: Mapped[Optional[str]]
    email: Mapped[Email] = mapped_column(EmailTypeDecorator())


user = UserDTO(email=Email("test@example.com"), userId=UserId(uuid.uuid4()))
print(user.email)  # Email('test@example.com')
print(user.model_dump_json())  # {"email":"test@example.com"}


engine = create_engine("sqlite:///test2.db", echo=True)
EntityObject.metadata.create_all(engine)
# user2 = User(email=Email("hello@world.com"))
# print(user2.email)
# with Session(engine) as session:
#     patrick = UserEntity(userId=UserId(uuid.uuid4()), email=Email("test@example.com"))
#     session.add(patrick)
#     session.commit()
    
with Session(engine) as session:
    stmt = select(UserEntity).where(UserEntity.email == Email("test@example.com"))
    userEntity = session.scalars(stmt).first() 
    print(userEntity)
    userDto = UserDTO.model_validate(userEntity)
    print(userDto.model_dump_json())
    

# # 校验示范
# try:
#     User(email="invalid-email")
# except Exception as e:
#     print(e)  # 会提示 Invalid email: invalid-email
