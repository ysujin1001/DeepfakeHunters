# Path: backend/app/api/routes_detect.py
# Desc: 딥페이크 탐지 및 얼굴 복원 라우터 (/api/predict, /api/restore)

import os
import io
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from PIL import Image
from backend.app.services.detect_service import predict_fake
from ai.modules.restorer import FaceRestorer
import numpy as np

router = APIRouter()

# ======================================================
# ✅ 모델 및 경로 설정
# ======================================================
RESTORE_MODEL_PATH = "ai/models/RealESRGAN_x4plus.pth"

try:
    restorer = FaceRestorer(RESTORE_MODEL_PATH)
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
        os.makedirs("data/temp", exist_ok=True)
        temp_path = f"data/temp/{file.filename}"

        # ✅ 파일 저장
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        print(f"📸 [PREDICT] 요청 파일: {file.filename} / 모델: {model_type}")

        # ✅ 예측 수행
        result = predict_fake(temp_path, model_type=model_type)
        result["model_type"] = model_type

        # ✅ 결과 로그 출력
        print("📤 [PREDICT RESULT]", result)

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
    흐릿하거나 저화질 얼굴 이미지를 복원 (경량 CPU 버전)
    """
    try:
        if restorer is None:
            raise HTTPException(status_code=500, detail="복원 모델이 로드되지 않았습니다.")

        # ✅ 이미지 로드
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # ✅ PIL → numpy 변환 → 복원 수행
        restored = restorer.restore(np.array(image))

        # ✅ 저장 경로 설정
        save_dir = Path("data/restored")
        save_dir.mkdir(parents=True, exist_ok=True)
        save_path = save_dir / f"restored_{file.filename}"

        # ✅ numpy → PIL 변환 후 저장
        Image.fromarray(restored).save(save_path)

        # ✅ URL 반환
        return {
            "restored_image_url": f"http://127.0.0.1:8001/{save_path}"
        }

    except Exception as e:
        print(f"❌ [RESTORE ERROR]: {e}")
        raise HTTPException(status_code=500, detail=f"복원 중 오류 발생: {str(e)}")
