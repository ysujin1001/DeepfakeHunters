import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt

# =====================================================
# 1️⃣ Grad-CAM 클래스
# =====================================================
class GradCAM:
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        self._register_hooks()

    def _register_hooks(self):
        def forward_hook(module, input, output):
            self.activations = output.detach()

        def backward_hook(module, grad_in, grad_out):
            self.gradients = grad_out[0].detach()

        self.target_layer.register_forward_hook(forward_hook)
        self.target_layer.register_backward_hook(backward_hook)

    def generate(self, input_tensor, class_idx):
        output = self.model(input_tensor)
        self.model.zero_grad()
        target = output[0, class_idx]
        target.backward()

        gradients = self.gradients.cpu().numpy()[0]
        activations = self.activations.cpu().numpy()[0]

        weights = np.mean(gradients, axis=(1, 2))
        cam = np.sum(weights[:, np.newaxis, np.newaxis] * activations, axis=0)
        cam = np.maximum(cam, 0)
        cam = cam / (np.max(cam) + 1e-8)
        return cam

# =====================================================
# 2️⃣ 이미지 로드 및 전처리
# =====================================================
def load_image(image_path, img_size=224):
    image = Image.open(image_path).convert("RGB")
    transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225]),
    ])
    input_tensor = transform(image).unsqueeze(0)
    return image, input_tensor

# =====================================================
# 3️⃣ 숫자 레이어 생성 (★ 제거)
# =====================================================
def generate_number_layer(cam, img_shape, grid_size=8):
    layer = np.zeros((img_shape[0], img_shape[1], 3), dtype=np.uint8)
    cam_resized = cv2.resize(cam, (img_shape[1], img_shape[0]))

    h, w = cam_resized.shape
    step_h, step_w = h // grid_size, w // grid_size
    font_scale = 0.5 * (step_h / 20)
    thickness = 1

    for i in range(grid_size):
        for j in range(grid_size):
            y, x = i * step_h + step_h // 2, j * step_w + step_w // 2
            score = cam_resized[y, x]
            number = int(np.clip(score * 9, 0, 9))
            cv2.putText(layer, str(number), (x - step_w//4, y + step_h//4),
                        cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)
    return layer

# =====================================================
# 4️⃣ Grad-CAM 오버레이
# =====================================================
def overlay_cam_on_image(img, cam):
    img = np.array(img).astype(np.uint8)
    cam_resized = cv2.resize(cam, (img.shape[1], img.shape[0]))
    heatmap = cv2.applyColorMap(np.uint8(255 * cam_resized), cv2.COLORMAP_JET)
    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
    overlay = cv2.addWeighted(img, 0.6, heatmap, 0.4, 0)
    return overlay

# =====================================================
# 5️⃣ 통합 보고서 생성
# =====================================================
def generate_integrated_report(pred_label, confidence):
    if pred_label == "Real":
        report = (
            f"이 이미지는 Real로 분류되었으며, 예측신뢰도는 {confidence:.2f}%입니다.\n"
            f"모델은 얼굴 이미지의 특징을 분석하여 자연스러운 피부 질감, 조명 반사, "
            f"세밀한 윤곽선 등 실제 이미지를 나타내는 시각적 패턴을 감지했습니다."
        )
    else:
        report = (
            f"이 이미지는 Fake로 분류되었으며, 예측신뢰도는 {confidence:.2f}%입니다.\n"
            f"모델은 이미지에서 비정상적인 질감, 경계선 왜곡, 조명 불균형 등 "
            f"딥페이크 생성 흔적을 감지했습니다."
        )
    return report

# =====================================================
# 6️⃣ 시각화
# =====================================================
def visualize_result(image, overlay, number_layer, report):
    final_overlay = cv2.addWeighted(overlay, 0.8, number_layer, 0.8, 0)
    plt.figure(figsize=(18, 6))

    # 1. 원본 이미지
    plt.subplot(1, 3, 1)
    plt.imshow(image)
    plt.title("원본 이미지")
    plt.axis("off")

    # 2. Grad-CAM + 숫자 오버레이
    plt.subplot(1, 3, 2)
    plt.imshow(final_overlay)
    plt.title("Grad-CAM + 숫자")
    plt.axis("off")

    # 3. 통합 보고서
    plt.subplot(1, 3, 3)
    plt.axis("off")
    plt.text(0, 0.5, report, fontsize=12, wrap=True)
    plt.tight_layout()
    plt.show()

# =====================================================
# 7️⃣ 분석 및 반환 기능
# =====================================================
def analyze_image(image_path, model_path, class_names=["Fake", "Real"], img_size=224, visualize=True):
    # 모델 정의
    model = models.mobilenet_v3_small(weights=None)
    in_features = model.classifier[3].in_features
    model.classifier[3] = nn.Linear(in_features, len(class_names))

    # state_dict 불러오기
    state_dict = torch.load(model_path, map_location="cpu")
    model.load_state_dict(state_dict, strict=False)
    model.eval()

    # 이미지 로드
    image, input_tensor = load_image(image_path, img_size)
    input_tensor = input_tensor.to("cpu")

    # 예측
    with torch.no_grad():
        output = model(input_tensor)
        probs = torch.softmax(output, dim=1)[0]
        pred_idx = torch.argmax(probs).item()
        confidence = probs[pred_idx].item() * 100
        pred_label = class_names[pred_idx]

    # Grad-CAM 생성
    target_layer = model.features[-1]
    cam_generator = GradCAM(model, target_layer)
    cam = cam_generator.generate(input_tensor, pred_idx)

    # 오버레이 및 숫자 레이어 생성
    overlay = overlay_cam_on_image(image, cam)
    number_layer = generate_number_layer(cam, np.array(image).shape, grid_size=8)

    # 통합 보고서
    report = generate_integrated_report(pred_label, confidence)

    # 시각화
    if visualize:
        visualize_result(image, overlay, number_layer, report)

    return image, overlay, number_layer, report, cam

# =====================================================
# 8️⃣ 실행 예시
# =====================================================
if __name__ == "__main__":
    image_path = "D:/AI_DEV_Course/Work_space/PROJECT/Advanced_Project_Team2/test_images/test1(man).png"
    model_path = "D:/AI_DEV_Course/Work_space/PROJECT/Advanced_Project_Team2/Model(MobileNet)/mobilenetv3_deepfake_final.pth"

    orig_img, overlay_img, number_layer, integrated_report, cam_map = analyze_image(
        image_path, model_path, class_names=["Fake", "Real"], visualize=True
    )

    print(integrated_report)

