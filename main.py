from fastapi import FastAPI
from app.database import engine, Base
from app.models import user
from app.api import logins, sign_up # 👈 깔끔하게 폴더에서 불러오기 [cite: 2026-03-01]

# 서버 켤 때 DB 테이블 자동 생성 [cite: 2026-03-01]
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Orbit SNS System")

# 👈 sign_up.router 로 이름을 맞춰줍니다 [cite: 2026-02-25]
app.include_router(sign_up.router, prefix="/signup", tags=["Registration"])
app.include_router(logins.router, prefix="/login", tags=["Authentication"])

@app.get("/")
def root():
    return {"message": "Orbit SNS 서버가 정상 작동 중입니다!"}
