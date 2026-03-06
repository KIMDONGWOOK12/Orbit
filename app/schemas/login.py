from pydantic import BaseModel, EmailStr

# 사용자가 로그인을 위해 보내는 데이터의 규격입니다
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# 로그인이 성공했을 때 서버가 돌려주는 데이터의 규격입니다
class Token(BaseModel):
    access_token: str
    token_type: str