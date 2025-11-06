# Path: backend/app/api/routes_detect.py
# Desc: 딥페이크 탐지 + Grad-CAM + PDF 보고서 API (디버깅 로그 확장 버전)

import os
import io
import uuid
import traceback
from datetime import datetime
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Request
from fastapi.responses import JSONResponse, FileResponse
from PIL import Image
import numpy as np

from backend.app.services.detect_service import predict_fake
from backend.app.services.report_heatmap_service import generate_heatmap_report
from ai.modules.restorer import FaceRestorer

router = APIRouter()

# ======================================================
# ✅ 경로 설정
# ======================================================
BASE_DIR = Path(__file__).resolve().parents[3]
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
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex[:6]
        ext = os.path.splitext(file.filename)[1]
        safe_name = f"{timestamp}_{unique_id}{ext}"
        save_path = UPLOAD_DIR / safe_name

        with open(save_path, "wb") as f:
            f.write(await file.read())

        print(f"📸 [PREDICT] 요청 파일: {safe_name} / 모델: {model_type}")

        result = predict_fake(str(save_path), model_type=model_type)
        result["model_type"] = model_type

        print(f"📤 [PREDICT RESULT] {result}")
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

        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        restored = restorer.restore(np.array(image))

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex[:6]
        ext = os.path.splitext(file.filename)[1]
        safe_name = f"{timestamp}_{unique_id}_restored{ext}"
        save_path = RESTORE_DIR / safe_name
        Image.fromarray(restored).save(save_path)

        print(f"💾 [RESTORE] 복원 완료 → {save_path}")
        return {"restored_image_url": f"http://127.0.0.1:8001/data/restored/{safe_name}"}

    except Exception as e:
        print(f"❌ [RESTORE ERROR]: {e}")
        raise HTTPException(status_code=500, detail=f"복원 중 오류 발생: {str(e)}")


# ======================================================
# 3️⃣ /api/report — PDF 보고서 생성 (LangChain 연동)
# ======================================================
@router.post("/report")
async def generate_report(request: Request):
    """
    프런트엔드에서 전달된 분석 결과(JSON)를 바탕으로 PDF 보고서를 생성하고 반환
    """
    try:
        result = await request.json()
        print("🧾 [REPORT INPUT] 수신된 JSON:", result.keys())

        # ✅ 필수 필드 검증
        required_fields = ["gradcam", "result", "fake_probability", "model_type"]
        missing = [k for k in required_fields if k not in result]
        if missing:
            raise ValueError(f"필수 키 누락: {missing}")

        # ✅ 보고서 생성
        pdf_path = generate_heatmap_report(result)

        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF 파일 생성 실패: {pdf_path}")

        print(f"📄 [REPORT] PDF 생성 완료 → {pdf_path}")
        return FileResponse(pdf_path, filename=os.path.basename(pdf_path), media_type="application/pdf")

    except Exception as e:
        print("❌ [REPORT ERROR 발생]:")
        traceback.print_exc()  # 🔥 전체 스택 출력
        raise HTTPException(status_code=500, detail=str(e))
