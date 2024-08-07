import os
from dotenv import load_dotenv
from pathlib import Path

import oracledb
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager

# 1. 환경 변수
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PWD = os.getenv("DB_PWD")
DB_DSN = os.getenv("DB_DSN")
DB_CONFIG_DIR = os.path.join(os.path.dirname(__file__), os.getenv("DB_CONFIG_DIR"))
DB_WALLET_LOCATION = os.path.join(os.path.dirname(__file__), os.getenv("DB_WALLET_LOCATION"))
DB_WALLET_PASSWORD = os.getenv("DB_WALLET_PWD")

# 2. 연결 설정 함수 분리 
def get_oracle_connection():
    """Oracle 데이터베이스 연결을 반환하는 함수"""
    try:
        connection = oracledb.connect(
            user=DB_USER,
            password=DB_PWD,
            dsn=DB_DSN,
            config_dir=DB_CONFIG_DIR,
            wallet_location=DB_WALLET_LOCATION,
            wallet_password=DB_WALLET_PASSWORD,
        )
        return connection
    except oracledb.Error as e:
        print(f"Oracle Database 연결 오류: {e}")
        raise  # 예외를 다시 발생시켜 상위 호출자에게 알림

# 3. SQLAlchemy 엔진 생성 (ORM 연동)
engine = create_engine(
    "oracle+oracledb://",
    creator=get_oracle_connection  # 연결 생성 함수를 creator로 전달
)

# 4. 세션 관리 (스레드 안전성)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = scoped_session(SessionLocal)

# 5. Base 모델 정의 (ORM 모델 기반)
Base = declarative_base()

# 6. 세션 컨텍스트 매니저 (with 문 사용 편의성)
@contextmanager
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
