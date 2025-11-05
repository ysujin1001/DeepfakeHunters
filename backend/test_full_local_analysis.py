# ==========================================================
# Path: backend/test_full_local_analysis.py
# Desc: 모델 분석 결과 + Grad-CAM + LangChain PDF 보고서 자동 연동
# ==========================================================
import os, io, sys, base64, traceback
from PIL import Image

# ==========================================================
# ✅ 1. 프로젝트 루트 경로 자동 인식
# ==========================================================
try:
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
except NameError:
    PROJECT_ROOT = os.path.abspath(os.path.join(os.getcwd(), ".."))

BACKEND_PATH = os.path.join(PROJECT_ROOT, "backend")
AI_MODULES_PATH = os.path.join(PROJECT_ROOT, "ai", "modules")

# Python 모듈 경로 등록
for path in [PROJECT_ROOT, BACKEND_PATH, AI_MODULES_PATH]:
    if path not in sys.path:
        sys.path.append(path)

print(f"✅ PROJECT_ROOT: {PROJECT_ROOT}")


# ==========================================================
# ✅ 2. 필요한 함수 불러오기
# ==========================================================
try:
    from Deepfake_Evaluation_MobileNet_v3_final_application_number_option import analyze_image_with_model_type
    from backend.app.services.report_heatmap_service import generate_heatmap_report
except Exception as e:
    print("❌ 모듈 임포트 실패:")
    print(traceback.format_exc())
    sys.exit(1)



# ==========================================================
# 📁 3. 테스트 이미지 경로
# ==========================================================
image_path = os.path.join(
    PROJECT_ROOT,
    "frontend",
    "public",
    "test_images",
    "detect",
    "test2.jpg"
)

if not os.path.exists(image_path):
    print(f"⚠️ 이미지 파일 없음: {image_path}")
else:
    print(f"✅ 테스트 이미지 경로: {image_path}")
    
    
# ==========================================================
# 🧠 4. 모델 분석 수행
# ==========================================================
try:
    print("\n🚀 딥페이크 분석 시작...")

    # ✅ 변경된 함수 호출
    pred_label, confidence, report = analyze_image_with_model_type(
        image_path=image_path,
        model_type="korean",     # 또는 "foriegn"
        visualize=False
    )

    print("✅ 모델 분석 완료")

    # Grad-CAM 시각화 이미지를 base64로 인코딩 (임시)
    with open(image_path, "rb") as f:
        encoded_overlay = base64.b64encode(f.read()).decode("utf-8")


# ==========================================================
# 📋 5. 분석 결과 JSON 구성
# ==========================================================
    result_data = {
        "pred_label": pred_label,
        "confidence": confidence,
        "fake_probability": 0.0,  # 시각적 강도 (향후 cam.mean() 반영 가능)
        "gradcam": encoded_overlay,
        "model_type": "korean",
        "model_name": "MobileNetV3-Small",
        "result": report
    }

# ==========================================================
# 📄 6. LangChain 기반 PDF 보고서 생성
# ==========================================================
    pdf_path = generate_heatmap_report(result_data)

    print("\n✅ 분석 및 PDF 생성 완료!")
    print(f"📁 PDF 파일 위치: {os.path.abspath(pdf_path)}")

    # PDF 파일 존재 확인
    if not os.path.exists(pdf_path):
        print("⚠️ PDF 파일이 지정된 경로에 없습니다. 경로 설정을 확인하세요.")
    else:
        print("✅ PDF 파일이 정상적으로 생성되었습니다.")

except Exception:
    print("\n❌ 오류 발생:")
    print(traceback.format_exc())