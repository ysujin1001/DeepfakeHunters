# Path: backend/app/services/detect_service.py
# Desc: 딥페이크 탐지 모델 로드 및 예측 로직 (더미 버전)

import random
import time

# ✅ 1. 모델 로드 함수 (실제 모델 로드 전 단계)
def load_model():
    #print("✅ [INFO] 딥페이크 탐지 모델 로드 완료 (현재는 더미 모드)")
    # 실제로는 예: model = torch.load("data/models/detector.pt")
    return "dummy_model"

# ✅ 2. 예측 함수 (현재는 랜덤 확률 반환)
def predict_fake(model, image_path: str) -> dict:
    time.sleep(1)  # 모델 추론 대기 시뮬레이션
    probability = round(random.uniform(0, 1), 3)
    result = "딥페이크로 판단됨" if probability > 0.5 else "진짜 얼굴로 판단됨"

    return {
        "fake_probability": probability,
        "result": result,
        "image_path": image_path
    }
