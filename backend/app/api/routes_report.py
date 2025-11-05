# backend/app/api/routes_report.py
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import FileResponse
from backend.app.services.report_heatmap_service import generate_heatmap_report
import tempfile, os

router = APIRouter()

@router.post("/report")
async def generate_heatmap_pdf(request: Request):
    """
    LangChain 기반 딥페이크 히트맵 분석 PDF 생성
    - 프론트엔드에서 result(JSON)을 body로 전송해야 함
    - 반환값: PDF 파일
    """
    
    try:
        # 1️⃣ 프론트엔드에서 보낸 분석 결과(JSON) 수신
        result_data = await request.json()

        # 2️⃣ LangChain + FPDF로 PDF 생성
        pdf_path = generate_heatmap_report(result_data)

        # 3️⃣ 임시 파일 생성 (다운로드를 위해)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        os.rename(pdf_path, tmp.name)

        # 4️⃣ 클라이언트로 PDF 파일 반환
        return FileResponse(
            tmp.name,
            filename="Deepfake_Heatmap_Report.pdf",
            media_type="application/pdf"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF 생성 중 오류 발생: {str(e)}")