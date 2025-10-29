# Path: backend/app/models/db_models.py
# Desc: 업로드 이미지 정보 저장 (파일명, 결과, 업로드 시각)

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.core.database import Base

class Upload(Base):
    __tablename__ = "uploads"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)         # 서버에 저장된 안전한 파일명
    original_name = Column(String(255))                    # 사용자가 업로드한 원본 파일명
    file_ext = Column(String(10))                          # 파일 확장자 (jpg, png 등)
    result = Column(String(50))                            # 딥페이크 탐지 결과
    uploaded_at = Column(DateTime, default=datetime.utcnow)

