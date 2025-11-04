# backend/app/api/routes_report.py
from fastapi import APIRouter
from fastapi.responses import FileResponse
import subprocess
import os
import tempfile

router = APIRouter()

@router.post("/report")
async def generate_pdf_report():
    """
    LangChain 기반 딥페이크 분석 리포트 PDF 생성 및 반환
    """
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    subprocess.run(["python", "generate_full_report.py"], check=True)

    # 생성된 PDF가 기본 경로에 있다면 복사/이동
    generated_pdf = "Deepfake_Report.pdf"  # deepfake_report.py 내부 생성 파일명
    if os.path.exists(generated_pdf):
        os.rename(generated_pdf, temp_pdf.name)

    return FileResponse(
        temp_pdf.name,
        filename="Deepfake_Analysis_Report.pdf",
        media_type="application/pdf"
    )
