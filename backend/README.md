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

# 📂 구조 예시
backend/
├─ main.py
├─ routes/
├─ models/
├─ data/
└─ utils/
