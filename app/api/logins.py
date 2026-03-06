from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.login import LoginRequest, Token
from app.core.security import verify_password, create_access_token

router = APIRouter()

@router.post("/", response_model=Token)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # 1. 유저 존재 여부 확인
    user = db.query(User).filter(User.email == request.email).first()
    
    # 2. 비밀번호 대조
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="아이디 또는 비밀번호가 틀렸습니다.")

    # 3. 토큰 발행
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}