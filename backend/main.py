# Path: backend/main.py
# Desc: FastAPI 서버 진입점 — DB 생성 + 업로드/탐지/복원 라우터 + 모델 로드 + 자동 정리

# ✅ 실행 명령
# (루트에서 실행해야 함)
# cd E:\yun\DeepfakeHunters
# uvicorn backend.main:app --reload --port 8001

import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import asyncio
from datetime import datetime, timedelta
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from dotenv import load_dotenv
# ------------------------------------------------------
# 0️⃣ 환경 변수 로드 (.env)
# ------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent  # backend/
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

db_url = os.getenv("DB_URL")
openai_key = os.getenv("OPENAI_API_KEY")

print("✅ .env 로드 완료")
print("✅ DB_URL:", db_url)
print("✅ OPENAI_API_KEY 감지됨" if openai_key else "⚠️ OPENAI_API_KEY 누락")

# ------------------------------------------------------
# 1️⃣ 내부 모듈 임포트
# ------------------------------------------------------
from ai.modules.predictor import DeepfakePredictor
from ai.modules.restorer import FaceRestorer
from backend.app.core.database import Base, engine, SessionLocal
from backend.app.models.db_models import Upload
from backend.app.api.routes_upload import router as upload_router
from backend.app.api.routes_detect import router as detect_router

# ------------------------------------------------------
# 2️⃣ DB 초기화
# ------------------------------------------------------
Base.metadata.create_all(bind=engine)

# ------------------------------------------------------
# 3️⃣ FastAPI 인스턴스
# ------------------------------------------------------
app = FastAPI(title="Deepfake Detection & Restoration API")

# ------------------------------------------------------
# 4️⃣ CORS 설정
# ------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 필요 시 도메인 지정 가능
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------
# 5️⃣ 라우터 연결
# ------------------------------------------------------
app.include_router(upload_router, prefix="/api")
app.include_router(detect_router, prefix="/api")

# ------------------------------------------------------
# 6️⃣ 정적 파일 제공 (복원 결과 이미지 접근 허용)
# ------------------------------------------------------
app.mount("/data", StaticFiles(directory="data"), name="data")

# ------------------------------------------------------
# 7️⃣ 모델 로드 (탐지 + 복원)
# ------------------------------------------------------
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

# ------------------------------------------------------
# 8️⃣ 전역 에러 핸들러
# ------------------------------------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": f"서버 내부 오류: {str(exc)}"},
    )

# ------------------------------------------------------
# 9️⃣ 자동 정리 태스크
# ------------------------------------------------------
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

if __name__ == "__main__":
    import uvicorn
    print("🚀 FastAPI 서버 실행 중 (http://127.0.0.1:8000)")
    uvicorn.run(
        "main:app",          # 모듈:앱 경로
        host="0.0.0.0",              # 외부 접속 허용
        port=8000,
        reload=True,                 # 코드 변경 시 자동 리로드
    )