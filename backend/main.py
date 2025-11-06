# Path: backend/main.py
# Desc: FastAPI 서버 진입점 — DB 생성 + 업로드/탐지/복원 라우터 + 모델 로드 + 자동 정리

# ✅ 실행 명령
# uvicorn backend.main:app --reload --port 8001

import asyncio
from datetime import datetime, timedelta
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# ✅ .env 로드 추가
from dotenv import load_dotenv
import os

# ------------------------------------------------------
# 0️⃣ 환경 변수 로드 (.env)
# ------------------------------------------------------
load_dotenv()
print("✅ DATABASE_URL:", os.getenv("DATABASE_URL"))

# ✅ 내부 모듈
from backend.app.core.database import Base, engine, SessionLocal
from backend.app.models.db_models import Upload
from ai.modules.predictor import DeepfakePredictor
from ai.modules.restorer import FaceRestorer
from backend.app.api.routes_upload import router as upload_router
from backend.app.api.routes_detect import router as detect_router

# ======================================================
# 1️⃣ DB 초기화
# ======================================================
Base.metadata.create_all(bind=engine)

# ======================================================
# 2️⃣ FastAPI 인스턴스
# ======================================================
app = FastAPI(title="Deepfake Detection & Restoration API")

# ======================================================
# 3️⃣ CORS 설정
# ======================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
# ✅ 정적 파일 (복원 이미지 접근 허용)
# ======================================================
app.mount("/data", StaticFiles(directory="data"), name="data")

# ======================================================
# 5️⃣ 모델 로드
# ======================================================
try:
    predictor_kr = DeepfakePredictor("ai/models/mobilenetv3_deepfake_final.pth")
    predictor_foreign = DeepfakePredictor("ai/models/mobilenetv3_deepfake_final_foriegn2.pth")
    restorer = FaceRestorer("ai/models/RealESRGAN_x4plus.pth")

    print("✅ [INFO] 한국인 탐지 모델 로드 완료")
    print("✅ [INFO] 외국인 탐지 모델 로드 완료")
    print("✅ [INFO] 복원 모델 로드 완료")
    print("✅ [INFO] 모든 모델 초기화 성공 (탐지 + 복원)")

except Exception as e:
    predictor_kr = predictor_foreign = restorer = None
    print(f"❌ [MODEL LOAD ERROR]: {e}")

# ======================================================
# 6️⃣ 전역 에러 핸들러
# ======================================================
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": f"서버 내부 오류: {str(exc)}"},
    )

# ======================================================
# 7️⃣ 자동 정리 태스크
# ======================================================
async def cleanup_deleted_uploads():
    """30일 이상 지난 삭제된 업로드 데이터를 주기적으로 정리"""
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
            print(f"❌ 자동 정리 중 오류: {e}")
        finally:
            db.close()

        await asyncio.sleep(60 * 60 * 24)  # 하루마다 반복


@app.on_event("startup")
async def start_cleanup_task():
    asyncio.create_task(cleanup_deleted_uploads())
