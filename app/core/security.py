from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

# 암호화 도구 설정 [cite: 2026-03-01]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "orbit_secret_key"  # 실제 배포 시에는 더 복잡하게 바꿔야 함
ALGORITHM = "HS256"

# 1. 비밀번호 암호화 (회원가입 시 사용)
def get_password_hash(password: str):
    return pwd_context.hash(password)

# 2. 비밀번호 확인 (로그인 시 사용)
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# 3. 액세스 토큰 생성 (로그인 성공 시 발급) [cite: 2026-03-01]
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60) # 1시간 유효 나중에 이야기해서 바꾸자
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)