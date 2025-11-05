import base64, io, os, datetime, json
from fpdf import FPDF
from PIL import Image
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv() 


# ==========================================================
# 📁 1. 결과 저장 경로 설정
# ==========================================================
BASE_RESULT_DIR = os.path.join("data", "results")
IMAGE_DIR = os.path.join(BASE_RESULT_DIR, "images")
PDF_DIR = os.path.join(BASE_RESULT_DIR, "pdfs")
LOG_DIR = os.path.join(BASE_RESULT_DIR, "logs")

# 폴더 자동 생성
for folder in [BASE_RESULT_DIR, IMAGE_DIR, PDF_DIR, LOG_DIR]:
    os.makedirs(folder, exist_ok=True)

# ==========================================================
# 🧠 2. 보고서 생성 함수
# ==========================================================
def generate_heatmap_report(result_data):
    """
    Grad-CAM 히트맵 분석 중심의 PDF 보고서 생성
    result_data 예시:
    {
        "result": "Fake",
        "fake_probability": 0.873,
        "gradcam": "<base64>",
        "model_type": "korean",
        "model_name": "MobileNetV3-Small"
    }
    """

    # ------------------------------------------------------
    # 1. Grad-CAM 이미지 저장
    # ------------------------------------------------------
    gradcam_b64 = result_data["gradcam"]
    gradcam_bytes = base64.b64decode(gradcam_b64)
    gradcam_img = Image.open(io.BytesIO(gradcam_bytes))

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    image_filename = f"gradcam_{timestamp}.png"
    gradcam_path = os.path.join(IMAGE_DIR, image_filename)
    gradcam_img.save(gradcam_path)

    # ------------------------------------------------------
    # 2. LangChain LLM 프롬프트 구성 및 실행
    # ------------------------------------------------------
    prompt = PromptTemplate(
        input_variables=["result", "prob", "type"],
        template=(
            "너는 딥페이크 탐지 전문가야. 아래 정보를 기반으로 Grad-CAM 히트맵을 해석해.\n\n"
            "모델 유형: {type}\n"
            "예측 결과: {result}\n"
            "딥페이크 확률: {prob:.2f}%\n\n"
            "붉은색 영역은 모델이 딥페이크 판단의 근거로 본 부분이야. "
            "이 시각 정보를 기반으로 모델이 어떻게 판단했는지, "
            "합성 흔적·피부 질감·조명 왜곡 등 시각적 근거를 기술적으로 분석해줘. "
            "또한 인간 전문가의 관점에서 신뢰도와 한계점도 함께 설명해줘."
            "아울러, 언급하지 않은 심층 결과가 있으면 함께 상세히 설명해줘."
        ),
    )

    llm = ChatOpenAI(model="gpt-4o-mini")

    analysis_text = llm.invoke(
        prompt.format(
            type="한국인 이미지 분석 모델" if result_data["model_type"] == "korean" else "외국인 이미지 분석 모델",
            result=result_data["result"],
            prob=result_data["fake_probability"] * 100,
        )
    ).content

    # ------------------------------------------------------
    # 3. PDF 보고서 생성
    # ------------------------------------------------------
    pdf = FPDF()
    pdf.add_page()

    # 제목
    pdf.add_font("malgun", "", r"C:\Windows\Fonts\malgun.ttf", uni=True)   # 일반
    pdf.add_font("malgun", "B", r"C:\Windows\Fonts\malgunbd.ttf", uni=True)   # 굵은체
    pdf.set_font("malgun", "B", size=16)
    pdf.cell(0, 10, "딥페이크 히트맵 분석 보고서", ln=True, align="C")

    # (1) 분석 개요
    pdf.set_font("malgun", "B", size=13)
    pdf.cell(0, 10, "1. 분석 개요", ln=True)
    pdf.set_font("malgun", size=11)

    model_name = result_data.get("model_name", "MobileNetV3-Small (PyTorch)")
    model_type = "한국인 전용 모델" if result_data["model_type"] == "korean" else "외국인 전용 모델"
    analyzed_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    pdf.multi_cell(
        0,
        8,
        f"- 모델명: {model_name}\n"
        f"- 모델 유형: {model_type}\n"
        f"- 분석 일시: {analyzed_at}\n"
        f"- 예측 결과: {result_data['result']}\n"
        f"- 딥페이크 확률: {(result_data['fake_probability'] * 100):.2f}%\n",
    )

    # (2) Grad-CAM 시각화
    pdf.ln(8)
    pdf.set_font("malgun", "B", 13)
    pdf.cell(0, 10, "2. Grad-CAM 시각화", ln=True)
    pdf.image(gradcam_path, x=25, y=pdf.get_y() + 5, w=160)
    pdf.ln(95)

    # (3) LangChain 기반 AI 해석
    pdf.set_font("malgun", "B", 13)
    pdf.cell(0, 10, "3️. LangChain 기반 AI 해석", ln=True)
    pdf.set_font("malgun", size=11)
    pdf.multi_cell(0, 7, analysis_text)

    # (4) 결론 및 권장 조치
    pdf.ln(5)
    pdf.set_font("malgun", "B", 13)
    pdf.cell(0, 10, "4️. 결론 및 권장 조치", ln=True)
    pdf.set_font("malgun", size=11)
    pdf.multi_cell(
        0,
        7,
        "본 분석은 Grad-CAM 시각 주목도를 중심으로 진행되었습니다.\n"
        "AI의 결과는 참고용으로 사용해야 하며, 법적 판단이나 공식 증거로 사용되지 않습니다.\n"
        "결과의 신뢰도를 높이기 위해 다양한 이미지 소스로 교차 검증을 권장합니다.",
    )

    # PDF 저장
    pdf_filename = f"heatmap_report_{timestamp}.pdf"
    pdf_path = os.path.join(PDF_DIR, pdf_filename)
    pdf.output(pdf_path)

    # ------------------------------------------------------
    # 4. 로그 JSON 생성 (DB 연동 대비)
    # ------------------------------------------------------
    log_data = {
        "created_at": analyzed_at,
        "model_name": model_name,
        "model_type": model_type,
        "result": result_data["result"],
        "fake_probability": result_data["fake_probability"],
        "gradcam_image": gradcam_path,
        "pdf_path": pdf_path,
    }

    log_filename = f"report_log_{timestamp}.json"
    with open(os.path.join(LOG_DIR, log_filename), "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=4, ensure_ascii=False)

    # 최종 PDF 경로 반환
    return pdf_path