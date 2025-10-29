# 🧠 Backend Setup (FastAPI)

```bash
# 1. 가상환경 활성화
conda activate deepfakehunters

# 2. 폴더 이동
cd backend

# 3. 백엔드 패키지 설치
pip install python-multipart

# 5. 서버 실행
uvicorn main:app --reload
```

# 🧠 DB 연결
FastAPI + MySQL 연동 버전

```bash
# ✅ 가상환경 활성화
conda activate deepfakehunters

# ✅ 필수 패키지 설치
pip install fastapi uvicorn sqlalchemy pymysql cryptography python-multipart

# ✅ docker-compose 실행 (MySQL + FastAPI 통합)
cd backend              # backend 폴더로 이동
docker-compose up -d    # 컨테이너 빌드 및 실행
docker ps               # 실행 상태 확인
docker-compose down     # 컨테이너 중지

# 💡 참고 .env 파일 내부에 아래처럼 DB URL이 포함되어야 함
```

# 📂 구조 예시
backend/
├─ main.py
├─ routes/
├─ models/
├─ data/
└─ utils/

