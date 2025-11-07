🧠 Deepfake Analysis & LangChain PDF Report System

- 딥페이크 판별 + Grad-CAM 시각화 + LangChain 기반 리포트 자동화 구조 문서

📘 1. 개요

- 이 문서는 업로드된 아래 Python 파일들을 기반으로 LangChain + Grad-CAM 기반 딥페이크 리포트 자동 생성 시스템의
  전체 동작 구조, 코드 흐름, 연결 관계를 상세히 설명한다.

📁 2. 주요 구성 파일
| 파일명 | 역할 |
| --------------------------------------------------------------------- | ---------------------------------------------- |
| `Deepfake_Discrimination_model_MobileNet_v3_final.py` | MobileNetV3-Small 기반 딥페이크 분류 모델 학습 |
| `Deepfake_Evaluation_MobileNet_v3_final_application_number_option.py` | 학습된 모델 로드 → Grad-CAM 분석 수행 |
| `detect_service.py` | API 호출 시 실제 판별 수행 로직 (`predict_fake`) |
| `routes_report.py` | FastAPI 라우터 — `/api/report` PDF 보고서 생성 |
| `report_heatmap_service.py` | LangChain + PDFKit 기반 보고서 생성기 |
| `test_full_local_analysis.py` | 로컬 통합 테스트용 (API 없이 E2E 테스트) |

⚙️ 3. 전체 파이프라인 요약
[Frontend]
↓
(1) 사용자 이미지 업로드
↓
[FastAPI Backend]
├── /api/predict → 딥페이크 판별
│ ↓
│ predict_fake() 호출 → MobileNetV3 추론 + Grad-CAM
│ ↓
│ 결과(JSON): pred_label, confidence, gradcam(base64)
│
├── /api/report → LangChain PDF 생성
│ ↓
│ generate_heatmap_report() 호출
│ ↓
│ LLM 요약 + Grad-CAM 이미지 결합 → PDF 저장
│
└── /api/restore → 얼굴 복원 (Real-ESRGAN)

🧩 4. 주요 코드 동작 흐름
1️⃣ 모델 학습

- 파일: Deepfake_Discrimination_model_MobileNet_v3_final.py
  . MobileNetV3-Small을 이용한 Real/Fake 이진 분류 모델 학습
  . Early Stopping + StepLR 스케줄러 포함
  . Grad-CAM 구현 포함
  . 학습 결과 저장: ai/models/mobilenetv3_deepfake_final.pth

2️⃣ Grad-CAM 분석

- 파일: Deepfake_Evaluation_MobileNet_v3_final_application_number_option.py
- 핵심 함수: analyze_image_with_model_type(path, model_type)
  . 모델 로드 → 이미지 추론 → 확률 계산
  . Grad-CAM으로 시각적 활성도 추출
  . 결과 예시:
  {
  "pred_label": "Fake",
  "confidence": 97.35,
  "gradcam_path": "ai/gradcam_results/gradcam_20251107_145512.png",
  "fake_intensity": 0.56
  }

3️⃣ 딥페이크 탐지 서비스

- 파일: detect_service.py
- 함수 predict_fake()에서:
  . 프론트 업로드 이미지 파일을 수신
  . analyze_image_with_model_type() 호출
  . 결과(JSON) 반환:
  {
  "pred_label": "Fake",
  "confidence": 97.35,
  "fake_probability": 0.56,
  "gradcam": "<base64_image_data>"
  }

4️⃣ FastAPI 라우팅

- 파일: routes_report.py
  . /api/predict: 이미지 업로드 → predict_fake() 호출
  . /api/report: Grad-CAM 결과 기반 PDF 리포트 생성
  . /api/restore: 이미지 복원 기능 (선택적)

5️⃣ PDF 보고서 생성 (LangChain 핵심)

- 파일: report_heatmap_service.py
- 입력: gradcam, fake_probability, model_type, result_text
  . LangChain 기반 PromptTemplate 구성
  . LLMChain 실행 → 분석 요약문 생성
  . FPDF 또는 PDFKit으로 시각자료 + 요약 텍스트 결합
  . 최종 PDF 예시: /reports/Deepfake_Report_20251107.pdf

6️⃣ 로컬 테스트

- 파일: test_full_local_analysis.py
  . 모델 추론 + Grad-CAM + PDF 생성까지 단일 실행 가능
  . API 없이 전체 기능 검증 가능

🧠 5. LangChain 리포트 생성 체인 구조
graph TD
A[generate_heatmap_report()] --> B[PromptTemplate 구성]
B --> C[LLMChain 실행 (LangChain)]
C --> D[분석 요약 생성]
D --> E[PDF 생성기 (FPDF/PDFKit)]
E --> F[결과 PDF 파일 저장]

📜 Step별 동작
| 단계 | 기능 | 설명 |
| ---------------- | ------------------ | ---------------------------------------- |
| ① PromptTemplate | 리포트용 자연어 템플릿 구성 | “이 이미지는 {fake_probability}% 확률로 딥페이크입니다” |
| ② LLMChain | GPT-4 or Claude 호출 | 결과 해석 요약문 생성 |
| ③ Output | AI 분석 문장 | “눈 주변 합성 흔적이 탐지됨” 등 |
| ④ PDF Generator | Grad-CAM + 텍스트 결합 | 보고서 시각화 |
| ⑤ PDF Output | 파일 저장 | `/reports/Deepfake_Report_20251107.pdf` |

💡 예시 코드 (LangChain 요약 체인)
prompt = PromptTemplate(
input_variables=["model_type", "fake_probability", "result_text"],
template=(
"다음은 {model_type} 모델로 분석한 딥페이크 결과입니다.\n"
"딥페이크 확률: {fake_probability:.2f}%\n"
"AI 분석 요약: {result_text}\n"
"이를 기반으로 전문 보고서를 작성하세요."
),
)

chain = LLMChain(prompt=prompt, llm=ChatOpenAI(model="gpt-4"))
summary = chain.run({
"model_type": "MobileNetV3",
"fake_probability": 95.3,
"result_text": "눈 주변에서 합성 흔적이 감지됨."
})

💡 결과 예시:
“모델은 해당 얼굴을 딥페이크로 판단했습니다.
눈가의 블러링과 피부 질감 불균일성이 주요 근거로 보입니다.”

🧾 6. PDF 리포트 구조
| 구역 | 설명 |
| ------ | ------------------------ |
| 표지 | Deepfake Analysis Report |
| 이미지 섹션 | 원본 + Grad-CAM |
| 분석 정보 | 모델명 / 확률 / 판정 결과 |
| AI 리포트 | LangChain 생성 자연어 설명 |
| 결론 | “딥페이크 가능성이 높습니다.” |

🔗 7. 전체 연동 아키텍처
graph TD
A[Frontend - Detect.js] -->|POST /api/predict| B[FastAPI routes_detect.py]
B -->|call| C[detect_service.py (predict_fake)]
C -->|call| D[Deepfake_Evaluation_MobileNet_v3_final_application_number_option.py]
D -->|load| E[Deepfake_Discrimination_model_MobileNet_v3_final.py]
B -->|POST /api/report| F[report_heatmap_service.py]
F -->|use| G[LangChain + PDF generation]

🧾 8. 최종 PDF 생성 흐름
graph TD
A[Frontend Detect.js] --> B[/api/report]
B --> C[report_heatmap_service.py]
C --> D1[LangChain PromptTemplate]
C --> D2[LLMChain (GPT-4)]
C --> D3[FPDF Generator]
D1 --> D2 --> D3
D3 --> E[Deepfake_Report_20251107.pdf]

✅ 9. 종합 결론

| 항목              | 상태 | 설명               |
| ----------------- | ---- | ------------------ |
| 모델 학습 코드    | ✅   | MobileNetV3 기반   |
| Grad-CAM 시각화   | ✅   | 시각 근거 생성     |
| 딥페이크 판별 API | ✅   | `/api/predict`     |
| LangChain 리포트  | ✅   | PDF 생성 완전 지원 |
| PDF 렌더링        | ✅   | Grad-CAM + 텍스트  |
| 테스트 스크립트   | ✅   | 로컬 E2E 가능      |
| 프론트 연동       | ✅   | 완벽 호환          |

🎯 10. 결론 요약

현재 구성된 코드 세트는
딥페이크 판별 → Grad-CAM 시각화 → LangChain 리포트 생성 → PDF 출력
까지의 완전한 엔드투엔드(E2E) 파이프라인을 포함하고 있다.

별도 모듈 추가 없이 바로 LangChain 기반 보고서 자동화를 수행할 수 있으며,
로컬 환경에서도 test_full_local_analysis.py로 전체 검증 가능하다.
