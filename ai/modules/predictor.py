# Path: ai/modules/predictor.py
# Desc: 딥페이크 탐지용 MobileNetV3 모델 로더 + 예측기

import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import io, os

MODEL_PATH = "ai/models/mobilenetv3_deepfake_final.pth"

class DeepfakePredictor:
    def __init__(self):
        """
        MobileNetV3-Small 기반 state_dict 모델 로드 (2-class: Fake / Real)
        """
        try:
            # 1️⃣ 모델 정의 (학습 시와 동일하게)
            self.model = models.mobilenet_v3_small(weights=None)
            in_features = self.model.classifier[3].in_features
            self.model.classifier[3] = nn.Linear(in_features, 2)

            # 2️⃣ 가중치 로드
            abs_path = os.path.abspath(MODEL_PATH)
            print(f"📂 로드 시도 중인 모델 경로: {abs_path}")  # ✅ 경로 표시 복원

            state_dict = torch.load(MODEL_PATH, map_location="cpu")
            # print(f"🔍 로드된 state_dict 키 수: {len(state_dict.keys())}")
            self.model.load_state_dict(state_dict, strict=False)
            # param_count = sum(p.numel() for p in self.model.parameters())
            # print(f"🔢 모델 파라미터 개수: {param_count:,}")
            self.model.eval()

        except Exception as e:
            self.model = None
            print(f"❌ [MODEL] 로드 실패: {e}")

        # 3️⃣ 입력 이미지 전처리 파이프라인
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ])

        # 4️⃣ 클래스 레이블
        self.class_names = ["Fake", "Real"]

    def predict(self, image_bytes):
        if self.model is None:
            return {"error": "모델이 로드되지 않았습니다."}

        try:
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            tensor = self.transform(image).unsqueeze(0)

            with torch.no_grad():
                output = self.model(tensor)
                probs = torch.softmax(output, dim=1)[0]
                pred_idx = torch.argmax(probs).item()
                confidence = probs[pred_idx].item() * 100
                label = self.class_names[pred_idx]

            return {
                "fake_probability": round(float(probs[0].item()), 4),
                "real_probability": round(float(probs[1].item()), 4),
                "result": label,
                "confidence": round(confidence, 2)
            }

        except Exception as e:
            return {"error": f"예측 실패: {e}"}
