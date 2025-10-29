# backend/app/core/reset_db.py
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.core.database import Base, engine
from app.models import db_models

print("⚠️ 모든 테이블 초기화 중...")
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
print("✅ DB 재생성 완료")
