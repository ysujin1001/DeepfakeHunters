# Path: backend/app/services/detect_service.py
# Desc: 딥페이크 탐지 + Grad-CAM 시각화 (option 모델 버전)

import base64
import io
import os
import sys
from pathlib import Path
from PIL import Image

# ==========================================================
# ✅ 1. 경로 세팅 (ai 폴더를 Python path에 포함)
# ==========================================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
AI_DIR = BASE_DIR / "ai"
if str(AI_DIR) not in sys.path:
    sys.path.append(str(AI_DIR))

# ✅ Grad-CAM 포함한 분석 모듈 (modules 폴더)
from modules.Deepfake_Evaluation_MobileNet_v3_final_application_number_option import analyze_image_with_model_type

# ==========================================================
# ✅ 2. 모델 경로 설정
# ==========================================================
MODEL_DIR = BASE_DIR / "ai" / "models"

# ==========================================================
# ✅ 3. 예측 함수 (Grad-CAM 포함)
# ==========================================================
def predict_fake(image_path: str, model_type: str = "korean") -> dict:
    """
    Grad-CAM 기반 딥페이크 예측 함수
    Args:
        image_path (str): 예측할 이미지 경로
        model_type (str): 'korean' 또는 'foreign'
    Returns:
        dict: 예측 결과 (라벨, 확률, Grad-CAM 이미지 포함)
    """
    try:
        # ✅ 1️⃣ Grad-CAM 분석 실행 (option 파일 내부 함수)
        pred_label, confidence, report = analyze_image_with_model_type(
            image_path=image_path,
            model_type=model_type,
            visualize=False  # matplotlib 창 띄우지 않음
        )

        # ✅ 2️⃣ Grad-CAM 오버레이 이미지 → base64로 변환
        image = Image.open(image_path).convert("RGB")
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        gradcam_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

        # ✅ 3️⃣ 결과 반환
        return {
            "pred_label": pred_label,
            "confidence": round(confidence, 2),
            "report": report,
            "gradcam": gradcam_b64,
            "image_path": image_path
        }

    except Exception as e:
        print(f"❌ [PREDICT ERROR]: {e}")
        return {"error": f"예측 중 오류 발생: {str(e)}"}
