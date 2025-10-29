# Path: backend/data/preprocess/face_crop_resize_pad.py
# Desc: 얼굴 자동 검출 + margin 확대 + 비율 유지 + 224x224 패딩 저장

import os
import cv2
from PIL import Image, ImageOps
from facenet_pytorch import MTCNN
import torch
from tqdm import tqdm

# =============================================
# 1️⃣ 경로 설정
# =============================================
# 현재 파일 위치: backend/data/preprocess
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # backend/data 기준
input_dir = os.path.join(BASE_DIR, "test_images")
output_dir = os.path.join(BASE_DIR, "cropped_faces")
os.makedirs(output_dir, exist_ok=True)

# 디버깅용 출력
print("📁 input_dir =", input_dir)
print("📁 output_dir =", output_dir)
if not os.path.exists(input_dir):
    print("❌ 입력 폴더가 존재하지 않습니다!")
else:
    print("🔎 파일 목록 =", os.listdir(input_dir))


# =============================================
# 2️⃣ 디바이스 및 MTCNN 초기화
# =============================================
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"💻 Using device: {device}")

mtcnn = MTCNN(keep_all=True, device=device, thresholds=[0.6, 0.7, 0.7])

# =============================================
# 3️⃣ 파일 목록
# =============================================
files = [f for f in os.listdir(input_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

# =============================================
# 4️⃣ 얼굴 검출 + margin 적용 + 비율 유지 + 패딩 저장
# =============================================
for fname in tqdm(files, desc="🔍 얼굴 검출 중", unit="img"):
    fpath = os.path.join(input_dir, fname)

    cv_img = cv2.imread(fpath)
    if cv_img is None:
        print(f"\n❌ OpenCV 로드 실패: {fname}")
        continue

    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv_img)
    width, height = img.size

    boxes, probs = mtcnn.detect(img)
    if boxes is None:
        print(f"\n❌ 얼굴 미검출: {fname}")
        continue

    for i, (box, prob) in enumerate(zip(boxes, probs)):
        if prob < 0.9:
            continue

        x1, y1, x2, y2 = box
        w, h = x2 - x1, y2 - y1
        margin = 0.2
        x1 = max(0, int(x1 - w * margin / 2))
        y1 = max(0, int(y1 - h * margin / 2))
        x2 = min(width, int(x2 + w * margin / 2))
        y2 = min(height, int(y2 + h * margin / 2))

        face = img.crop((x1, y1, x2, y2))
        face.thumbnail((224, 224), Image.BICUBIC)
        face = ImageOps.pad(face, (224, 224), color=(0, 0, 0))

        out_name = f"{os.path.splitext(fname)[0]}_face{i+1}.jpg"
        out_path = os.path.join(output_dir, out_name)

        try:
            face.save(out_path, format="JPEG", quality=95)
            print(f"✅ 얼굴 저장: {out_name}")
        except Exception as e:
            print(f"\n⚠️ 저장 실패: {out_name} ({e})")

print("\n🎉 완료! 모든 얼굴이 아래 폴더에 저장됨:")
print(output_dir)
