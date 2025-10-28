# 🧠 DeepfakeHunters  
AI 기반 얼굴 복원 및 딥페이크 탐지 웹서비스  



#### ==============================================================================

## 🧭 Branch Strategy
- `main`: 최종 배포용 브랜치 (발표 / 결과물 관리) | 조장만 병합
- `dev`: 통합 브랜치 (모든 PR은 여기로) | 전원 작성 가능
- `yunsujin`, `hrlee`, `jrheo`, `leeys` : 개인 작업 브랜치 | 개인별 작업 전용

## 🧱 Workflow
1. 개인 브랜치에서 작업  
2. 변경사항 커밋  
3. 원격 저장소로 push
4. GitHub에서 Pull Request 생성 (대상 브랜치: dev)
5. 조장이 dev에서 통합 테스트 후 main으로 병합
🔹 자세한 사용 예시 및 명령어 순서는 docs/_git bash 사용법.txt를 참고하세요.

## ⚙️ Local Environment Setup (using Conda)

모든 팀원이 동일한 개발 환경에서 FastAPI를 실행하기 위한 설정 가이드입니다.

### 🧱 Step-by-Step

```bash
# 1️⃣ Conda 환경 생성
conda create -n deepfakehunters python=3.10

# 2️⃣ 환경 활성화
conda activate deepfakehunters

# 3️⃣ 필수 패키지 설치
pip install fastapi uvicorn opencv-python numpy torch torchvision torchaudio
# (추후 모델링용 라이브러리 – e.g., deepface, insightface, gfpgan, onnxruntime 등 – 추가 예정)