// Path: src/pages/Detect.js
// Desc: 이미지 업로드 + 체크박스 동의 + 딥페이크 판별 결과 표시 (파일 경로는 콘솔에만 표시)

import { useState } from "react";
import "../styles/detect.css";

export default function Detect() {
  const [image, setImage] = useState(null);
  const [file, setFile] = useState(null);
  const [rightsChecked, setRightsChecked] = useState(false);
  const [disclaimerChecked, setDisclaimerChecked] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const allChecked = rightsChecked && disclaimerChecked;

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (!selected) return;
    setFile(selected);
    setImage(URL.createObjectURL(selected));
    setResult(null);
    console.log("🖼️ 선택된 파일:", selected.name);
  };

  const handleDetect = async () => {
  if (!file) return alert("파일을 선택하세요!");
  if (!allChecked) return alert("체크박스에 모두 동의해주세요.");

  setLoading(true);
  const formData = new FormData();
  formData.append("file", file);

  try {
    // 1️⃣ 업로드 요청
    const uploadRes = await fetch(`${process.env.REACT_APP_API_URL}/api/upload`, {
      method: "POST",
      body: formData,
    });
    const uploadData = await uploadRes.json();
    console.log("✅ 업로드 성공:", uploadData);

    // 2️⃣ 예측 요청 (FormData 새로 생성)
    const predictForm = new FormData();
    predictForm.append("file", file);

    const predictRes = await fetch(`${process.env.REACT_APP_API_URL}/api/predict`, {
      method: "POST",
      body: predictForm,
    });
    const predictData = await predictRes.json();
    console.log("✅ 예측 결과:", predictData);

    setResult(predictData);
  } catch (err) {
    console.error("🚨 분석 오류:", err);
    setResult({ error: "서버와 통신할 수 없습니다." });
  } finally {
    setLoading(false);
  }
};


  // 가운데 정렬 인라인 스타일
  const containerStyle = {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    minHeight: "100vh",
    textAlign: "center",
  };

  return (
    <div className="detect-container" style={containerStyle}>
      <h2 className="detect-title">Deepfake Detection</h2>

      <div className="detect-card">
        {/* 이미지 업로드 */}
        <div className="upload-section">
          <label className="upload-box">
            <input type="file" accept="image/*" onChange={handleFileChange} />
            {image ? (
              <img src={image} alt="preview" className="preview" />
            ) : (
              <span>이미지를 업로드하거나 클릭하세요</span>
            )}
          </label>
        </div>

        {/* 체크박스 동의 */}
        <div className="consent-section">
          <label>
            <input
              type="checkbox"
              checked={rightsChecked}
              onChange={() => setRightsChecked((prev) => !prev)}
            />
            이 이미지는 타인의 초상권 또는 저작권을 침해하지 않습니다.
          </label>
          <label>
            <input
              type="checkbox"
              checked={disclaimerChecked}
              onChange={() => setDisclaimerChecked((prev) => !prev)}
            />
            AI 분석 결과는 참고용이며, 법적 증거로 사용되지 않음을 이해합니다.
          </label>
        </div>

        {/* 분석 버튼 */}
        <button
          className="btn-detect"
          disabled={!file || !allChecked || loading}
          onClick={handleDetect}
        >
          {loading ? "분석 중..." : "업로드 및 탐지"}
        </button>

        {/* 결과 표시 (경로 제외) */}
        {result && (
          <div className="result-card">
            {result.error ? (
              <p className="error-text">{result.error}</p>
            ) : (
              <>
                <p>
                  <strong>결과:</strong> {result.result}
                </p>
                <p>
                  <strong>딥페이크 확률:</strong>{" "}
                  {(result.fake_probability * 100).toFixed(1)}%
                </p>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
