# Path: backend/app/core/cleanup.py
# Desc: 30일 지난 soft delete 항목 자동 정리

import asyncio
from datetime import datetime, timedelta
from app.core.database import SessionLocal
from app.models.db_models import Upload

async def cleanup_deleted_uploads():
    """
    30일 이상 지난 soft delete 항목을 DB에서 완전 삭제
    """
    while True:
        db = SessionLocal()
        try:
            threshold = datetime.utcnow() - timedelta(days=30)
            deleted_items = (
                db.query(Upload)
                .filter(Upload.is_deleted == True)
                .filter(Upload.deleted_at < threshold)
                .all()
            )

            count = len(deleted_items)
            if count > 0:
                for item in deleted_items:
                    db.delete(item)
                db.commit()
                print(f"🧹 DB 정리 완료: {count}개 삭제됨 ({datetime.utcnow()})")
            else:
                print(f"✅ 정리할 항목 없음 ({datetime.utcnow()})")

        except Exception as e:
            print("❌ 정리 중 오류 발생:", e)
        finally:
            db.close()

        # 24시간마다 반복
        await asyncio.sleep(60 * 60 * 24)
