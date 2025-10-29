# Path: backend/app/api/routes_upload.py
# Desc: 이미지 업로드 / 삭제 / 목록 조회 (DB 기록 + soft delete 로그)

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.database import SessionLocal
from app.models.db_models import Upload
from datetime import datetime
import os, shutil, uuid

router = APIRouter()

# 파일 저장 폴더
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ==========================================================
# 1️⃣ 이미지 업로드
# ==========================================================
@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    db = SessionLocal()
    try:
        # 확장자 추출
        original_name = file.filename
        file_ext = os.path.splitext(original_name)[1].lstrip(".")  # ex) 'jpg'

        # 안전한 파일명 생성
        safe_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}.{file_ext}"
        save_path = os.path.join(UPLOAD_DIR, safe_name)

        # 파일 저장
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # DB 기록
        record = Upload(
            filename=safe_name,
            original_name=original_name,
            file_ext=file_ext,
            result="pending",
            uploaded_at=datetime.utcnow()
        )
        db.add(record)
        db.commit()

        return {
            "message": "파일 업로드 성공",
            "server_filename": safe_name,
            "user_filename": original_name
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


# ==========================================================
# 2️⃣ 업로드 목록 조회 (삭제되지 않은 항목만)
# ==========================================================
@router.get("/uploads")
def get_upload_list():
    db = SessionLocal()
    try:
        uploads = (
            db.query(Upload)
            .filter(Upload.is_deleted == False)
            .order_by(Upload.uploaded_at.desc())
            .all()
        )
        return uploads
    finally:
        db.close()


# ==========================================================
# 3️⃣ 파일 삭제 (Soft Delete)
# ==========================================================
@router.delete("/upload/{file_id}")
def delete_uploaded_file(file_id: int):
    db = SessionLocal()
    try:
        record = db.query(Upload).filter(Upload.id == file_id).first()
        if not record:
            raise HTTPException(status_code=404, detail="해당 파일을 찾을 수 없습니다.")

        # 실제 파일 삭제
        file_path = os.path.join(UPLOAD_DIR, record.filename)
        if os.path.exists(file_path):
            os.remove(file_path)

        # DB에 삭제 로그 남기기
        record.is_deleted = True
        record.deleted_at = datetime.utcnow()
        db.commit()

        return {"message": f"{record.original_name} 삭제 완료 (삭제 로그 기록됨)"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


# ==========================================================
# 4️⃣ (선택) 삭제된 파일 로그 조회 (관리자용)
# ==========================================================
@router.get("/uploads/deleted")
def get_deleted_uploads():
    db = SessionLocal()
    try:
        deleted = (
            db.query(Upload)
            .filter(Upload.is_deleted == True)
            .order_by(Upload.deleted_at.desc())
            .all()
        )
        return deleted
    finally:
        db.close()
