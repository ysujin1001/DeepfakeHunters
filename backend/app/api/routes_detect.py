# Path: backend/app/api/routes_detect.py
# Desc: 딥페이크 탐지 요청을 처리하는 라우터 (POST /api/predict)

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.services.upload_service import save_file
from app.services.detect_service import load_model, predict_fake

router = APIRouter()

# 앱 시작 시 모델 1회 로드
model = load_model()

@router.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    """
    업로드된 이미지를 모델에 전달해 딥페이크 탐지 결과 반환
    """
    try:
        # 1️⃣ 업로드 파일 저장
        filename, file_path = await save_file(file)
        print(f"📸 [PREDICT] 요청 파일: {filename}")

        # 2️⃣ 모델 예측 수행
        result = predict_fake(model, file_path)

        # 3️⃣ 결과 로그 출력
        print("📤 [PREDICT RESULT]", result)

        # 4️⃣ 결과 반환
        return JSONResponse(status_code=200, content=result)
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 에러: {str(e)}")
