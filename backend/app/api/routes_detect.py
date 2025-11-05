# Path: backend/app/api/routes_detect.py
# Desc: 딥페이크 탐지 요청을 처리하는 라우터 (POST /api/predict)

import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from backend.app.services.upload_service import save_file
from backend.app.services.detect_service import load_model, predict_fake

router = APIRouter()

# 앱 시작 시 모델 1회 로드
model = load_model()

@router.post("/predict")
async def predict_image(
    file: UploadFile = File(...),
    model_type: str = Form("korean")
):
    """
    업로드된 이미지를 모델에 전달해 딥페이크 탐지 결과 반환
    """
    try:
        # ✅ 파일 저장 대신, 메모리 상에서 처리
        content = await file.read()

        # 파일이 실제로 필요한 경우에만 임시 저장
        temp_path = f"data/temp/{file.filename}"
        os.makedirs("data/temp", exist_ok=True)
        with open(temp_path, "wb") as f:
            f.write(content)

        print(f"📸 [PREDICT] 요청 파일: {file.filename} / 모델: {model_type}")

        # 모델 예측 수행
        result = predict_fake(model, temp_path, model_type=model_type)

        # ✅ 메타데이터 추가
        result["model_type"] = model_type
        result["model_path"] = os.path.abspath(model[model_type])
        
        # 로그 출력
        print("📤 [PREDICT RESULT]", result)

        # ✅ 임시 파일 삭제
        os.remove(temp_path)

        return JSONResponse(status_code=200, content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 에러: {str(e)}")
