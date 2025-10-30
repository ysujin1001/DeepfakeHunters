# Path: backend/main.py
# Desc: FastAPI 서버 진입점 — DB 테이블 자동 생성 + 업로드/탐지 라우터 연결 + 전역 에러 핸들러 + 30일 경과 삭제 로그 자동 정리

# ✅ 서버 실행 명령 (참고용)
# uvicorn main:app --reload

import asyncio
from datetime import datetime, timedelta
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# ✅ 라우터 임포트
from app.api.routes_upload import router as upload_router
from app.api.routes_detect import router as detect_router

# ✅ DB 임포트 및 테이블 생성
from app.core.database import Base, engine, SessionLocal
from app.models import db_models
from app.models.db_models import Upload

# ======================================================
# 1️⃣ DB 초기화 (테이블 자동 생성)
# ======================================================
Base.metadata.create_all(bind=engine)

# ======================================================
# 2️⃣ FastAPI 인스턴스 생성
# ======================================================
app = FastAPI(title="Deepfake Detection API")

# ======================================================
# 3️⃣ CORS 설정 (프론트엔드 연동용)
# ======================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # 개발 중 전체 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================================
# 4️⃣ 라우터 연결
# ======================================================
app.include_router(upload_router, prefix="/api")
app.include_router(detect_router, prefix="/api")

# ======================================================
# 5️⃣ 전역 에러 핸들러
# ======================================================
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": f"서버 내부 에러가 발생했습니다: {str(exc)}"}
    )


# ======================================================
# 6️⃣ 백그라운드 작업 — 30일 지난 soft delete 항목 자동 정리
# ======================================================
async def cleanup_deleted_uploads():
    """
    30일 이상 지난 soft delete 항목을 DB에서 완전 삭제
    하루에 한 번 실행됨
    """
    while True:
        db = SessionLocal()
        try:
            threshold = datetime.utcnow() - timedelta(days=30)
            old_records = (
                db.query(Upload)
                .filter(Upload.is_deleted == True)
                .filter(Upload.deleted_at < threshold)
                .all()
            )

            if old_records:
                for record in old_records:
                    db.delete(record)
                db.commit()
                print(f"🧹 {len(old_records)}개 항목 정리 완료 ({datetime.utcnow()})")
            else:
                print(f"✅ 정리할 항목 없음 ({datetime.utcnow()})")

        except Exception as e:
            print("❌ 자동 정리 중 오류 발생:", e)
        finally:
            db.close()

        # 하루(24시간)마다 반복
        await asyncio.sleep(60 * 60 * 24)


# ======================================================
# 7️⃣ 서버 시작 시 백그라운드 태스크 실행
# ======================================================
@app.on_event("startup")
async def start_cleanup_task():
    asyncio.create_task(cleanup_deleted_uploads())
