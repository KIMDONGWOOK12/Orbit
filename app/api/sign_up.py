import requests
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.user import User
from app.schemas.sign_up import UserCreate
from app.core.security import get_password_hash

router = APIRouter()

# ---------------------------------------------------------
# 1. 일반 회원가입
# ---------------------------------------------------------
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(request: UserCreate, db: Session = Depends(get_db)):
    # 이메일 중복 확인
    db_user = db.query(User).filter(User.email == request.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="이미 가입된 이메일입니다.")

    # 유저 생성 및 저장
    new_user = User(
        email=request.email,
        hashed_password=get_password_hash(request.password),
        name=request.name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "message": f"{new_user.name}님, 일반 회원가입이 완료되었습니다!",
        "user_id": new_user.id
    }


# ---------------------------------------------------------
# 2. 구글 OAuth2 회원가입 (및 로그인 처리)
# ---------------------------------------------------------
# 프론트엔드에서 받을 구글 토큰 스키마
class GoogleSignupRequest(BaseModel):
    access_token: str

@router.post("/google", status_code=status.HTTP_200_OK)
def google_sign_up(request: GoogleSignupRequest, db: Session = Depends(get_db)):
    """구글 토큰을 받아 회원가입 또는 로그인을 처리합니다."""
    
    # 1. 구글 서버에 토큰을 보내서 유저 정보 받아오기
    google_userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
    response = requests.get(
        google_userinfo_url,
        headers={"Authorization": f"Bearer {request.access_token}"}
    )
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="유효하지 않은 구글 토큰입니다.")
        
    user_info = response.json()
    google_email = user_info.get("email")
    google_name = user_info.get("name") # 구글에서 설정한 이름도 가져옵니다!

    # 2. 우리 DB에 이메일이 있는지 확인
    db_user = db.query(User).filter(User.email == google_email).first()

    # 3. 없으면 새로 가입시키기 (회원가입 로직)
    if not db_user:
        db_user = User(
            email=google_email,
            hashed_password="GOOGLE_SOCIAL_USER", # 소셜 유저는 비밀번호가 필요 없습니다
            name=google_name # 구글에서 받아온 이름 저장
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        message = f"{db_user.name}님, 구글 계정으로 첫 가입을 환영합니다!"
    else:
        message = f"{db_user.name}님, 구글 계정으로 로그인되었습니다."

    # (주의) 실무에서는 여기서 회원가입 완료 후 바로 JWT(access_token)를 
    # 발급해서 리턴해주는 것이 좋습니다. (로그인 API와 동일하게)
    
    return {
        "message": message,
        "user_email": db_user.email,
        "name": db_user.name
    }