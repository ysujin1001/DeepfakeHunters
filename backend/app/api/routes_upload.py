# Path: backend/app/api/routes_upload.py
# Desc: 이미지 업로드를 처리하는 FastAPI 라우터 (POST /api/upload)

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.services.upload_service import save_file

router = APIRouter()

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """
    업로드된 이미지를 data/uploads에 저장
    """
    try:
        filename, file_path = await save_file(file)
        print(f"📥 [UPLOAD] {filename} 저장 완료 → {file_path}")

        return JSONResponse(
            status_code=200,
            content={"message": "업로드 성공", "filename": filename, "path": file_path}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"업로드 실패: {str(e)}")
