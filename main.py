from app.database import engine, Base
from app.models import user  # 방금 만든 유저 모델 불러오기

# DB 테이블 생성 (이미 있으면 생성 안 함)
Base.metadata.create_all(bind=engine)