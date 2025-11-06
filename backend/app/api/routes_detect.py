# Path: backend/app/api/routes_detect.py
# Desc: 딥페이크 탐지 및 얼굴 복원 라우터 (/api/predict, /api/restore)

import os
import io
import uuid
from datetime import datetime
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from PIL import Image
from backend.app.services.detect_service import predict_fake
from ai.modules.restorer import FaceRestorer
import numpy as np

router = APIRouter()

# ======================================================
# ✅ 경로 및 모델 설정
# ======================================================
BASE_DIR = Path(__file__).resolve().parents[3]  # backend 폴더 기준
UPLOAD_DIR = BASE_DIR / "data" / "uploads"
RESTORE_DIR = BASE_DIR / "data" / "restored"
MODEL_PATH = BASE_DIR / "ai" / "models" / "RealESRGAN_x4plus.pth"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
RESTORE_DIR.mkdir(parents=True, exist_ok=True)

# ======================================================
# ✅ 복원 모델 로드
# ======================================================
try:
    restorer = FaceRestorer(str(MODEL_PATH))
    print("✅ [INFO] 복원 모델 로드 완료")
except Exception as e:
    restorer = None
    print(f"❌ [MODEL LOAD ERROR]: {e}")

# ======================================================
# 1️⃣ /api/predict — 딥페이크 탐지
# ======================================================
@router.post("/predict")
async def predict_image(
    file: UploadFile = File(...),
    model_type: str = Form("korean")
):
    """
    업로드된 이미지를 모델에 전달해 딥페이크 탐지 결과 반환
    """
    try:
        # ✅ 파일명: YYYYMMDD_HHMMSS_UUID.확장자
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex[:6]
        ext = os.path.splitext(file.filename)[1]
        safe_name = f"{timestamp}_{unique_id}{ext}"

        # ✅ 저장 경로
        save_path = UPLOAD_DIR / safe_name

        # ✅ 파일 저장
        with open(save_path, "wb") as f:
            f.write(await file.read())

        print(f"📸 [PREDICT] 요청 파일: {safe_name} / 모델: {model_type}")

        # ✅ 예측 수행
        result = predict_fake(str(save_path), model_type=model_type)
        result["model_type"] = model_type

        # ✅ 결과 로그 출력 (gradcam 제외)
        log_result = {k: v for k, v in result.items() if k != "gradcam"}
        print(f"📤 [PREDICT RESULT] {log_result}")

        # ✅ 결과 반환
        return JSONResponse(status_code=200, content=result)

    except Exception as e:
        print(f"❌ [PREDICT ERROR]: {e}")
        raise HTTPException(status_code=500, detail=f"탐지 중 오류 발생: {str(e)}")

# ======================================================
# 2️⃣ /api/restore — 얼굴 복원
# ======================================================
@router.post("/restore")
async def restore_image(file: UploadFile = File(...)):
    """
    흐릿하거나 저화질 얼굴 이미지를 복원 (RealESRGAN CPU 버전)
    """
    try:
        if restorer is None:
            raise HTTPException(status_code=500, detail="복원 모델이 로드되지 않았습니다.")

        # ✅ 이미지 로드
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # ✅ PIL → numpy 변환 → 복원 수행
        restored = restorer.restore(np.array(image))

        # ✅ 파일명: YYYYMMDD_HHMMSS_UUID_restored.확장자
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex[:6]
        ext = os.path.splitext(file.filename)[1]
        safe_name = f"{timestamp}_{unique_id}_restored{ext}"

        # ✅ 저장 경로 설정
        save_path = RESTORE_DIR / safe_name

        # ✅ numpy → PIL 변환 후 저장
        Image.fromarray(restored).save(save_path)

        print(f"💾 [RESTORE] 복원 완료 → {save_path}")

        # ✅ URL 반환 (FastAPI static mount 기반)
        return {
            "restored_image_url": f"http://127.0.0.1:8001/data/restored/{safe_name}"
        }

    except Exception as e:
        print(f"❌ [RESTORE ERROR]: {e}")
        raise HTTPException(status_code=500, detail=f"복원 중 오류 발생: {str(e)}")
