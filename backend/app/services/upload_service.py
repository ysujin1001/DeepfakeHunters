# Path: backend/app/services/upload_service.py
# Desc: 업로드 파일 저장 및 유효성 검증 로직 (상대경로 + 날짜 기반 랜덤 파일명)

import os
import uuid
import datetime
from fastapi import UploadFile, HTTPException

# 상대경로 (backend 기준)
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_file(file: UploadFile):
    """
    업로드된 파일을 data/uploads에 저장.
    파일명은 [날짜_시간_마이크로초_UUID6자리.확장자] 형식으로 생성되어 충돌 방지.
    예: 20251027_143512_123456_ab12f3.jpg
    """
    # 파일명 유효성 검사
    if not file.filename:
        raise HTTPException(status_code=400, detail="파일 이름이 비어 있습니다.")

    # 확장자 확인
    ext = file.filename.split(".")[-1].lower()
    if ext not in ["jpg", "jpeg", "png"]:
        raise HTTPException(status_code=415, detail="지원하지 않는 파일 형식입니다.")

    # 고유 파일명 생성 (날짜 + 시간 + 마이크로초 + uuid 일부)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    short_uid = str(uuid.uuid4())[:6]
    new_filename = f"{timestamp}_{short_uid}.{ext}"

    # 실제 저장 경로
    file_path = os.path.join(UPLOAD_DIR, new_filename)

    # 파일 저장
    content = await file.read()
    with open(file_path, "wb") as buffer:
        buffer.write(content)

    # 파일명, 경로 반환
    return new_filename, file_path
