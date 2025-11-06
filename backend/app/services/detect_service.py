# Path: backend/app/services/detect_service.py
# Desc: 딥페이크 탐지 + Grad-CAM 시각화 (최신 개선 버전)

import base64
import sys
import os
from pathlib import Path
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
AI_DIR = BASE_DIR / "ai"
if str(AI_DIR) not in sys.path:
    sys.path.append(str(AI_DIR))

from modules.Deepfake_Evaluation_MobileNet_v3_final_application_number_option import analyze_image_with_model_type


def predict_fake(image_path: str, model_type: str = "korean") -> dict:
    """
    Grad-CAM 기반 딥페이크 예측 함수 (시각화 이미지 + 활성도 반환)
    """
    try:
        pred_label, confidence, report, gradcam_path, fake_intensity = analyze_image_with_model_type(
            path=image_path,
            model_type=model_type,
            visualize=True,
        )

        # ✅ Grad-CAM 이미지 base64 변환
        gradcam_b64 = None
        if gradcam_path and os.path.exists(gradcam_path):
            with open(gradcam_path, "rb") as f:
                gradcam_b64 = base64.b64encode(f.read()).decode("utf-8")

        # ✅ 결과 반환
        return {
            "pred_label": pred_label,
            "confidence": round(confidence, 2),
            "report": report,
            "gradcam": gradcam_b64,
            "image_path": image_path,
            "fake_probability": round(fake_intensity, 3) if fake_intensity else None,
        }

    except Exception as e:
        print(f"❌ [PREDICT ERROR]: {e}")
        return {"error": f"예측 중 오류 발생: {str(e)}"}
