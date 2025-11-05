# Path: backend/app/services/detect_service.py
# Desc: 딥페이크 탐지 모델 로드 및 예측 로직 (절대경로 안정화 + 다국적 모델 지원)

import base64
import io
import os
from pathlib import Path
from PIL import Image
from ai.modules.predictor import DeepfakePredictor

# ==========================================================
# ✅ 1. 모델 경로 설정
# ==========================================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
MODEL_DIR = BASE_DIR / "ai" / "models"

# ==========================================================
# ✅ 2. 모델 로드
# ==========================================================
try:
    MODEL_PATHS = {
        "korean": str(MODEL_DIR / "mobilenetv3_deepfake_final.pth"),
        "foreign": str(MODEL_DIR / "mobilenetv3_deepfake_final_foriegn2.pth"),
    }

    predictor_korean = DeepfakePredictor(MODEL_PATHS["korean"])
    predictor_foreign = DeepfakePredictor(MODEL_PATHS["foreign"])
    print("✅ [INFO] 딥페이크 탐지 모델 로드 완료 (한국인 + 외국인)")

except Exception as e:
    predictor_korean = predictor_foreign = None
    print(f"❌ [detect_service] 모델 로드 실패: {e}")


# ==========================================================
# ✅ 3. 모델 선택 함수
# ==========================================================
def load_model(model_type: str = "korean"):
    if model_type == "foreign":
        return predictor_foreign
    return predictor_korean


# ==========================================================
# ✅ 4. 예측 함수
# ==========================================================
def predict_fake(image_path: str, model_type: str = "korean") -> dict:
    predictor = load_model(model_type)
    if predictor is None:
        return {"error": f"{model_type} 모델이 로드되지 않았습니다."}

    # 이미지 열기
    try:
        image = Image.open(image_path).convert("RGB")
    except Exception as e:
        return {"error": f"이미지 로드 실패: {e}"}

    # 예측 수행
    prob, result = predictor.predict(image)

    # 이미지 base64 인코딩 (시각화용)
    gradcam_b64 = ""
    if os.path.exists(image_path):
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        gradcam_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    return {
        "pred_label": "Fake" if prob >= 0.5 else "Real",
        "confidence": round(prob * 100, 2),
        "fake_probability": round(prob, 4),
        "gradcam": gradcam_b64,
        "result": result,
    }
