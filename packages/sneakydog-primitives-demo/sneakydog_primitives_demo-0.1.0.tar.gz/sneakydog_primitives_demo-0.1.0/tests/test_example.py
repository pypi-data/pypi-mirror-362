import uuid
from sneakydog_primitives_demo.email import Email
from sneakydog_primitives_demo.user_id import UserId
from sneakydog_primitives_demo.project_id import ProjectId
from sneakydog_primitives_demo.value_objects import BaseModel


class User(BaseModel):
    userId: UserId
    projectId: ProjectId = None
    email: Email


user = User(email="test@example.com", userId=uuid.uuid4())
print(user.email)  # Email('test@example.com')
print(user.model_dump_json())  # {"email":"test@example.com"}

# user2 = User(email=Email("hello@world.com"))
# print(user2.email)

# # 校验示范
# try:
#     User(email="invalid-email")
# except Exception as e:
#     print(e)  # 会提示 Invalid email: invalid-email
