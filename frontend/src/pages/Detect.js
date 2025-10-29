// Path: src/pages/Detect.js
// Desc: 이미지 업로드 + 동의 체크 + 서버 예측 + 팀원 UI 일부 병합

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
  };

  const handleDetect = async () => {
    if (!file) return alert("파일을 선택하세요!");
    if (!allChecked) return alert("체크박스에 모두 동의해주세요.");

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      // 업로드
      await fetch(`${process.env.REACT_APP_API_URL}/api/upload`, {
        method: "POST",
        body: formData,
      });

      // 예측
      const res = await fetch(`${process.env.REACT_APP_API_URL}/api/predict`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      setResult({ error: "서버 오류 발생" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="detect-container">
      <h1 className="detect-title">
        진실을 확인하세요 – AI가 이미지 <span className="red">진위 여부</span>를
        분석합니다.
      </h1>

      <div className="detect-main">
        {/* [1] 업로드 영역 */}
        <div className="box">
          <h3>Upload Image</h3>
          <div className="content-area">
            <label className="upload-box">
              <input type="file" accept="image/*" onChange={handleFileChange} />
              {image ? (
                <img src={image} alt="preview" className="preview" />
              ) : (
                <div className="inner-box">
                  이미지를 Drag & Drop 하거나 클릭하여 업로드
                </div>
              )}
            </label>
          </div>

          {/* 체크박스 */}
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
              AI 분석 결과는 참고용이며 법적 증거로 사용되지 않음을 이해합니다.
            </label>
          </div>

          <div className="button-group">
            <button
              className="detect-btn"
              disabled={!file || !allChecked || loading}
              onClick={handleDetect}
            >
              {loading ? "분석 중..." : "탐지 시작"}
            </button>
          </div>
        </div>

        {/* [2] 화살표 영역 */}
        <div className="arrow-box">
          <img src="/images/arrow.jpg" alt="arrow" />
        </div>

        {/* [3] 결과 영역 */}
        <div className="box">
          <h3>Detection Results</h3>
          <div className="content-area">
            {result ? (
              result.error ? (
                <p className="error-text">{result.error}</p>
              ) : (
                <div className="result-box">
                  <p className="result-line">
                    <span className="blue">결과:</span> {result.result}
                  </p>
                  <p className="result-line">
                    <span className="blue">딥페이크 확률:</span>{" "}
                    {(result.fake_probability * 100).toFixed(1)}%
                  </p>
                </div>
              )
            ) : (
              <p className="result-placeholder">아직 분석 결과가 없습니다.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
