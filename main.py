from fastapi import FastAPI
from fastapi.responses import FileResponse  # 👈 [추가] 파일을 보내주기 위한 도구입니다
from app.database import engine, Base
from app.models import user
from app.api import logins, sign_up 

# 서버 켤 때 DB 테이블 자동 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Orbit SNS System")

# API 라우터 연결
app.include_router(sign_up.router, prefix="/signup", tags=["Registration"])
app.include_router(logins.router, prefix="/login", tags=["Authentication"])


@app.get("/")
async def read_home():
    # 이제 http://127.0.0.1:8000 접속 시 '진짜 대문'인 home.html을 보여ㅑ줌
    return FileResponse('home.html')

@app.get("/register")
async def read_signup_page():
    # http://127.0.0.1:8000/register 접속 시 기존 가입창(index.html)을 보여줌
    return FileResponse('index.html')