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
async def read_index():
    # 사용자가 접속하면 같은 폴더에 있는 index.html을 보여줍니다. [cite: 2026-03-01]
    return FileResponse('index.html')