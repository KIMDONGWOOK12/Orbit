import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.database import get_db
from app.models.user import User
from app.schemas.login import Token, LoginRequest # Token과 LoginRequest 스키마
from app.core.security import verify_password, create_access_token

router = APIRouter()

# ---------------------------------------------------------
# [1] 일반 로그인 API 
# (아이디/비밀번호 직접 입력 방식)
# ---------------------------------------------------------
@router.post("/login", response_model=Token)
def login_general(request: LoginRequest, db: Session = Depends(get_db)):
    # 1. 유저 확인
    user = db.query(User).filter(User.email == request.email).first()
    
    # 2. 비밀번호 대조
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="아이디 또는 비밀번호가 틀렸습니다.")

    # 3. 토큰 발행
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# ---------------------------------------------------------
# [2] 구글 소셜 로그인 API
# (프론트엔드에서 구글 토큰을 받아오는 방식)
# ---------------------------------------------------------
class GoogleLoginRequest(BaseModel):
    access_token: str  

def verify_google_token(access_token: str):
    """구글 서버에 토큰을 보내서 유저 이메일을 받아오는 함수"""
    google_userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
    response = requests.get(
        google_userinfo_url,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    if response.status_code != 200:
        return None
    user_info = response.json()
    return user_info.get("email")

@router.post("/login/google", response_model=Token)
def login_google(request: GoogleLoginRequest, db: Session = Depends(get_db)):
    # 1. 구글 서버에 토큰 검증 요청
    google_email = verify_google_token(request.access_token)
    
    if not google_email:
        raise HTTPException(status_code=400, detail="유효하지 않은 구글 토큰입니다.")

    # 2. DB 확인
    user = db.query(User).filter(User.email == google_email).first()

    # 3. 신규 유저라면 자동 회원가입
    if not user:
        new_user = User(email=google_email, hashed_password="GOOGLE_SOCIAL_USER")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        user = new_user

    # 4. 토큰 발행 (일반 로그인과 동일한 형태의 토큰!)
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}