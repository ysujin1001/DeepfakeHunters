# Path: backend/app/models/db_models.py
# Desc: 업로드 이미지 정보 저장 (파일명, 결과, 업로드 시각, 삭제 로그 포함)

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from backend.app.core.database import Base

class Upload(Base):
    __tablename__ = "uploads"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)         # 서버에 저장된 안전한 파일명
    original_name = Column(String(255))                    # 사용자가 업로드한 원본 파일명
    file_ext = Column(String(10))                          # 파일 확장자 (jpg, png 등)
    result = Column(String(50))                            # 딥페이크 탐지 결과
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    # 🆕 삭제 관련 필드 (soft delete)
    is_deleted = Column(Boolean, default=False)            # 삭제 여부
    deleted_at = Column(DateTime, nullable=True)           # 삭제된 시각
