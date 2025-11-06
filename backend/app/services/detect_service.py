# Path: backend/app/services/detect_service.py
# Desc: 딥페이크 탐지 모델 로드 및 예측 로직 (실제 모델 연결 버전)

import base64, io, os, sys, re
from PIL import Image

# ==========================================================
# ✅ 1. Python 모듈 경로 등록
# ==========================================================
# FastAPI 실행 시 현재 디렉토리는 backend/
sys.path.append(r"C:\AI\project\AdvancedProject\DeepfakeHunters\ai\modules")

# ✅ analyze_image_with_model_type 함수 import
from Deepfake_Evaluation_MobileNet_v3_final_application_number_option import analyze_image_with_model_type


# ==========================================================
# ✅ 2. 모델 로드 함수 (유지)
# ==========================================================
def load_model():
    """
    한국인 / 외국인 모델 경로를 반환하는 단순 매핑 함수
    (지금은 analyze_image_with_model_type 내부에서 경로를 자동 처리하므로 참고용)
    """
    return {
        "korean": "ai/models/mobilenetv3_deepfake_final.pth",
        "foreign": "ai/models/mobilenetv3_deepfake_final_foriegn2.pth",
    }



# ==========================================================
# ✅ 3. 예측 함수 (딥페이크 판별)
# ==========================================================
def predict_fake(model_dict, image_path: str, model_type="korean") -> dict:
    """
    지정된 모델 타입(korean/foriegn)에 따라 이미지를 분석하고 결과 반환
    """

    # ✅ analyze_image_with_model_type 함수 호출
    pred_label, confidence, report = analyze_image_with_model_type(
        image_path=image_path,
        model_type=model_type,
        visualize=False
    )

    # ✅ 이미지(base64) 변환 (Grad-CAM 결과를 아직 별도 파일로 저장하지 않으므로 원본 사용)
    gradcam_b64 = ""
    if os.path.exists(image_path):
        img = Image.open(image_path)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        gradcam_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    # ✅ Grad-CAM 평균값 기반 딥페이크 시각적 강도 (확장 가능)
    fake_probability = 0.0  # 기본값 (analyze_image_with_model_type에서 cam 반환 시 교체 가능)

    # ✅ 결과 JSON 구성
    return {
<<<<<<< Updated upstream
        "pred_label": pred_label,                    # 예: "Fake"
        "confidence": confidence,                    # 예: 85.68
        "fake_probability": fake_probability,        # Grad-CAM 평균값 기반 (0.0~1.0)
        "gradcam": gradcam_b64,                      # base64 이미지
        "result": report                             # 보고서 문장
=======
    "pred_label": "Fake" if prob >= 0.5 else "Real",
    "confidence": round(prob * 100, 2),
    "fake_probability": round(prob, 4),
    "gradcam": gradcam_b64,
    "result": result,
    "image_path": image_path,  # ✅ 실제 파일 경로 추가
>>>>>>> Stashed changes
    }
