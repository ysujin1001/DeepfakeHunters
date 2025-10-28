# Path: backend/main.py
# Desc: FastAPI 서버 진입점 — 업로드 및 딥페이크 탐지 라우터 연결 + 전역 에러 핸들러

# ✅ 서버 실행 명령 (참고용)
# uvicorn backend.main:app --reload

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.routes_upload import router as upload_router
from app.api.routes_detect import router as detect_router

app = FastAPI(title="Deepfake Detection API")

# ✅ 라우터 연결
app.include_router(upload_router, prefix="/api")
app.include_router(detect_router, prefix="/api")

# ✅ 전역 에러 핸들러
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": f"서버 내부 에러가 발생했습니다: {str(exc)}"}
    )
