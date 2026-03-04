from pydantic import BaseModel, EmailStr

# 회원가입 시 클라이언트가 보내야 하는 데이터의 규격입니다.
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str