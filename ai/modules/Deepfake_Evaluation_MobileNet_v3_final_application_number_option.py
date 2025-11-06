# Path: ai/modules/Deepfake_Evaluation_MobileNet_v3_final_application_number_option.py
# Desc: Grad-CAM 기반 딥페이크 분석 (상대경로 자동 인식)

import torch, torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import numpy as np, cv2, matplotlib.pyplot as plt
from pathlib import Path

# 기본 경로 설정
BASE_DIR = Path(__file__).resolve().parents[1]  # ai/
MODEL_DIR = BASE_DIR / "models"                 # ai/models/
print(f"🧠 [MODEL_DIR] {MODEL_DIR}")

# Grad-CAM 클래스
class GradCAM:
    def __init__(self, model, target_layer):
        self.model, self.target_layer = model, target_layer
        self.gradients = self.activations = None
        self.target_layer.register_forward_hook(lambda m, i, o: setattr(self, "activations", o.detach()))
        self.target_layer.register_backward_hook(lambda m, gi, go: setattr(self, "gradients", go[0].detach()))
    def generate(self, x, idx):
        out = self.model(x); self.model.zero_grad(); out[0, idx].backward()
        g, a = self.gradients.cpu().numpy()[0], self.activations.cpu().numpy()[0]
        w = np.mean(g, axis=(1, 2)); cam = np.maximum(np.sum(w[:, None, None] * a, 0), 0)
        return cam / (np.max(cam) + 1e-8)

# 이미지 로드
def load_image(path, size=224):
    img = Image.open(path).convert("RGB")
    t = transforms.Compose([
        transforms.Resize((size, size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])
    ])
    return img, t(img).unsqueeze(0)

# 숫자 오버레이
def generate_number_layer(cam, shape, grid=8):
    layer = np.zeros((shape[0], shape[1], 3), np.uint8)
    cam_r = cv2.resize(cam, (shape[1], shape[0]))
    h, w = cam_r.shape; sh, sw = h // grid, w // grid; fs = 0.5 * (sh / 20)
    for i in range(grid):
        for j in range(grid):
            y, x = i*sh+sh//2, j*sw+sw//2
            n = int(np.clip(cam_r[y,x]*9, 0, 9))
            cv2.putText(layer, str(n), (x-sw//4, y+sh//4),
                        cv2.FONT_HERSHEY_SIMPLEX, fs, (255,255,255), 1, cv2.LINE_AA)
    return layer

def overlay_cam_on_image(img, cam):
    img = np.array(img).astype(np.uint8)
    cam_r = cv2.resize(cam, (img.shape[1], img.shape[0]))
    heat = cv2.applyColorMap(np.uint8(255*cam_r), cv2.COLORMAP_JET)
    return cv2.addWeighted(img, 0.6, cv2.cvtColor(heat, cv2.COLOR_BGR2RGB), 0.4, 0)

def generate_integrated_report(label, conf):
    if label == "Real":
        return (f"이 이미지는 Real ({conf:.2f}%)\n"
                f"자연스러운 질감, 조명, 윤곽선 패턴이 실제 얼굴의 특징으로 인식되었습니다.")
    return (f"이 이미지는 Fake ({conf:.2f}%)\n"
            f"비정상적인 질감, 경계선 왜곡, 조명 불균형 등 딥페이크 흔적이 감지되었습니다.")

def analyze_image_with_model_type(path, model_type="korean", visualize=True):
    model_paths = {
        "korean": str(MODEL_DIR / "mobilenetv3_deepfake_final.pth"),
        "foriegn": str(MODEL_DIR / "mobilenetv3_deepfake_final_foriegn2.pth")
    }
    if model_type not in model_paths:
        raise ValueError("model_type은 'korean' 또는 'foriegn'만 가능합니다.")
    model_path = model_paths[model_type]
    print(f"✅ 선택된 모델: {model_type} ({model_path})")

    model = models.mobilenet_v3_small(weights=None)
    f = model.classifier[3].in_features
    model.classifier[3] = nn.Linear(f, 2)
    model.load_state_dict(torch.load(model_path, map_location="cpu"), strict=False)
    model.eval()

    img, x = load_image(path)
    with torch.no_grad():
        out = model(x); probs = torch.softmax(out, 1)[0]
        idx = torch.argmax(probs).item()
        conf = probs[idx].item()*100
        label = ["Fake","Real"][idx]

    cam = GradCAM(model, model.features[-1]).generate(x, idx)
    overlay = overlay_cam_on_image(img, cam)
    number_layer = generate_number_layer(cam, np.array(img).shape)
    report = generate_integrated_report(label, conf)

    if visualize:
        plt.figure(figsize=(18,6))
        plt.subplot(1,3,1); plt.imshow(img); plt.title("원본"); plt.axis("off")
        plt.subplot(1,3,2); plt.imshow(cv2.addWeighted(overlay,0.8,number_layer,0.8,0)); plt.title("Grad-CAM"); plt.axis("off")
        plt.subplot(1,3,3); plt.axis("off"); plt.text(0,0.5,report,fontsize=12,wrap=True)
        plt.tight_layout(); plt.show()

    return label, conf, report

if __name__ == "__main__":
    test_img = str(BASE_DIR.parent / "backend" / "data" / "test_images" / "test5.jpg")
    analyze_image_with_model_type(test_img, "korean")
