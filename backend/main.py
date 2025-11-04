# Path: backend/main.py
# Desc: FastAPI 서버 진입점 — DB 테이블 자동 생성 + 업로드/탐지 라우터 연결 +
#       AI 모델 기반 딥페이크 판별 + 전역 에러 핸들러 + 30일 경과 삭제 자동 정리

# ✅ 서버 실행 명령 (로컬 개발용)
# uvicorn main:app --reload --port 8001
import io
import asyncio
from datetime import datetime, timedelta
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import torch
from torchvision import transforms
from pathlib import Path
from torchvision import models

# ✅ 내부 모듈 임포트
from backend.app.api.routes_upload import router as upload_router
from backend.app.api.routes_detect import router as detect_router
from backend.app.core.database import Base, engine, SessionLocal
from backend.app.models import db_models
from backend.app.models.db_models import Upload

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
# 5️⃣ 딥페이크 판별 모델 로드 (Custom MobilenetV3)
# ======================================================
from ai.modules.predictor import DeepfakePredictor

try:
    predictor = DeepfakePredictor()
    model = predictor.model
    transform = predictor.transform

    # 모델 이름 출력
    model_name = predictor.model.__class__.__name__
    print(f"✅ [INFO] 딥페이크 탐지 모델 로드 완료 — ({model_name} / mobilenetv3_deepfake_final.pth)")

except Exception as e:
    model = None
    transform = None
    print(f"❌ [MODEL] 로드 실패: {e}")

# ======================================================
# 6️⃣ /api/predict — 딥페이크 예측 API
# ======================================================
@app.post("/api/predict")
async def predict(file: UploadFile = File(...)):
    """
    업로드된 이미지를 분석하여 딥페이크 여부를 예측
    """
    if model is None:
        return JSONResponse(status_code=500, content={"error": "모델이 로드되지 않았습니다."})

    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        tensor = transform(image).unsqueeze(0)

        with torch.no_grad():
            output = model(tensor)
            prob = torch.sigmoid(output).item()

        result = "딥페이크로 판단됨" if prob >= 0.5 else "실제 이미지로 판단됨"

        # ✅ 추가 부분 — 모델 정보 함께 반환
        return {
            "fake_probability": round(prob, 4),
            "result": result,
            "image_path": f"data/temp/{file.filename}",
            "model_name": predictor.model.__class__.__name__,            # ✅ 모델 이름
            "model_path": os.path.abspath("ai/models/mobilenetv3_deepfake_final.pth")  # ✅ 모델 경로
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# ======================================================
# 7️⃣ 전역 에러 핸들러
# ======================================================
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": f"서버 내부 에러가 발생했습니다: {str(exc)}"}
    )

# ======================================================
# 8️⃣ 백그라운드 작업 — 30일 지난 soft delete 항목 자동 정리
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
# 9️⃣ 서버 시작 시 백그라운드 태스크 실행
# ======================================================
@app.on_event("startup")
async def start_cleanup_task():
    asyncio.create_task(cleanup_deleted_uploads())
