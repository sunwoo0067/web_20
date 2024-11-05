from typing import Any
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    id: Any
    __name__: str
    
    # 테이블 이름을 자동으로 생성
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
