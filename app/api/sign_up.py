from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.sign_up import UserCreate
from app.core.security import get_password_hash

router = APIRouter()

@router.post("/")
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
    return {"message": "회원가입이 완료되었습니다!"}