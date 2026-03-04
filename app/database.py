from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. DB 저장 위치 설정 (현재 폴더에 orbit.db 파일로 저장)
SQLALCHEMY_DATABASE_URL = "sqlite:///./orbit.db"

# 2. DB 연결 엔진 생성
# SQLite를 사용할 때만 connect_args=["check_same_thread": False]가 필요
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. 데이터베이스와 대화할 세션(통로) 관리자
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 모든 모델(User, Post 등)이 상속받을 기본 클래스
Base = declarative_base()

# 5. DB 세션을 가져오는 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()