# FastAPI를 사용한 오너클랜 매니저 백엔드 개발

## 프로젝트 개요
오너클랜 API를 이용하여 상품을 관리하는 웹 애플리케이션의 백엔드를 개발합니다. Python FastAPI를 사용하여 RESTful API를 구현하고, MySQL 데이터베이스를 사용하여 상품 정보를 관리합니다.

## 기술 스택
- Python FastAPI
- SQLAlchemy (MySQL)
- Python 3.9+
- Visual Studio Code

## 초기 프로젝트 구조
```
ownerclan-manager/
└── backend/
    ├── app/
    │   ├── __init__.py
    │   ├── main.py
    │   ├── core/
    │   │   ├── __init__.py
    │   │   └── config.py
    │   └── db/
    │       ├── __init__.py
    │       └── base.py
    ├── requirements.txt
    └── .env
```

## 필요한 코드 파일들

### requirements.txt
```python
fastapi==0.105.0
uvicorn==0.24.0
sqlalchemy==2.0.23
aiomysql==0.2.0
python-dotenv==1.0.0
httpx==0.25.2
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
```

### app/main.py
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Ownerclan Manager")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Ownerclan Manager API"}
```

### app/core/config.py
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Ownerclan Manager"
    PROJECT_VERSION: str = "1.0.0"
    
    MYSQL_USER: str = os.getenv("MYSQL_USER", "ownerclan_user")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "password")
    MYSQL_SERVER: str = os.getenv("MYSQL_SERVER", "localhost")
    MYSQL_PORT: str = os.getenv("MYSQL_PORT", "3306")
    MYSQL_DB: str = os.getenv("MYSQL_DB", "ownerclan_db")
    DATABASE_URL: str = f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}:{MYSQL_PORT}/{MYSQL_DB}"

    OWNERCLAN_API_URL: str = os.getenv("OWNERCLAN_API_URL", "https://api-sandbox.ownerclan.com/v1/graphql")
    OWNERCLAN_USERNAME: str = os.getenv("OWNERCLAN_USERNAME")
    OWNERCLAN_PASSWORD: str = os.getenv("OWNERCLAN_PASSWORD")

settings = Settings()
```

### app/db/base.py
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
```

### .env
```plaintext
MYSQL_USER=ownerclan_user
MYSQL_PASSWORD=your_password
MYSQL_SERVER=localhost
MYSQL_PORT=3306
MYSQL_DB=ownerclan_db

OWNERCLAN_API_URL=https://api-sandbox.ownerclan.com/v1/graphql
OWNERCLAN_USERNAME=your_username
OWNERCLAN_PASSWORD=your_password
```

## 개발 환경 설정 단계

1. Python 가상환경 생성 및 활성화:
```bash
# 프로젝트 디렉토리 생성
mkdir ownerclan-manager
cd ownerclan-manager
mkdir backend
cd backend

# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
.\venv\Scripts\activate
```

2. 패키지 설치:
```bash
pip install -r requirements.txt
```

3. 서버 실행:
```bash
uvicorn app.main:app --reload
```

## 다음 구현할 기능

1. 오너클랜 API 연동:
   - JWT 토큰 인증
   - 상품 검색 API
   - 상품 상세 조회 API

2. 데이터베이스 모델:
   - 상품 테이블
   - 상품 옵션 테이블
   - 상품 이미지 테이블

3. API 엔드포인트:
   - 상품 검색
   - 상품 저장
   - 상품 수정
   - 상품 삭제

## 참고사항
- Windows에서는 PowerShell 실행 정책 변경이 필요할 수 있음 (관리자 권한으로 실행):
```powershell
Set-ExecutionPolicy RemoteSigned
```
- VS Code에서는 Python 확장프로그램 설치 필요
- JWT 토큰은 오너클랜 API 인증에 사용됨
