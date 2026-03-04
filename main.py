from fastapi import FastAPI
from app.database import engine, Base
from app.models import user  #  중요
from app.api import logins, signs_up 

# 이 코드가 실행되는 순간 orbit.db 파일에 'users' 테이블이 생성될거래
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Orbit SNS System")

# 이렇게 연결하면 브라우저에서 /signup, /login 주소로 접근할 수 있음
app.include_router(signs_up.router, prefix="/signup", tags=["Registration"])
app.include_router(logins.router, prefix="/login", tags=["Authentication"])

@app.get("/")
def root():
    return {"message": "Orbit SNS 서버가 정상 작동 중입니다!"}