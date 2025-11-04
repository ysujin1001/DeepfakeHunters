// Path: src/pages/Detect.js
// Desc: 이미지 업로드 + 동의 체크 + 서버 예측 + 팀원 UI 일부 병합

import { useState } from 'react';
import '../styles/detect.css';

export default function Detect() {
  const [image, setImage] = useState(null); // 미리보기용 이미지 URL
  const [file, setFile] = useState(null); // 실제 업로드 파일 객체
  const [rightsChecked, setRightsChecked] = useState(false); // 초상권/저작권 동의 여부
  const [disclaimerChecked, setDisclaimerChecked] = useState(false); // 법적 고지 동의 여부
  const [loading, setLoading] = useState(false); // 분석 중 상태
  const [result, setResult] = useState(null); // 서버 응답 결과 (예측값)

  const allChecked = rightsChecked && disclaimerChecked;

  // ✅ [추가] PDF 다운로드용 상태 & 핸들러
  const [reportUrl, setReportUrl] = useState(null);

  const handleDownloadPDF = async () => {
    try {
      const res = await fetch(`${process.env.REACT_APP_API_URL}/api/report`, {
        method: 'POST',
      });

      if (!res.ok) throw new Error('PDF 생성 실패');

      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      setReportUrl(url);

      // 파일 저장창 자동 열기
      const a = document.createElement('a');
      a.href = url;
      a.download = 'Deepfake_Analysis_Report.pdf';
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error('PDF 생성 오류:', err);
      alert('PDF 생성 중 문제가 발생했습니다.');
    }
  };
  // ✅ [추가 끝]

  // 이미지 업로드
  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (!selected) return;
    setFile(selected);
    setImage(URL.createObjectURL(selected));
    setResult(null);
  };

  // AI 판별 요청
  const handleDetect = async () => {
    if (!file) return alert('파일을 선택하세요!');
    if (!allChecked) return alert('체크박스에 모두 동의해주세요.');

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      // 업로드 요청
      await fetch(`${process.env.REACT_APP_API_URL}/api/upload`, {
        method: 'POST',
        body: formData,
      });

      // 예측 요청
      const res = await fetch(`${process.env.REACT_APP_API_URL}/api/predict`, {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      setResult({ error: '서버 오류 발생' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="detect-container">
      <h1 className="detect-title">
        이 이미지는 진짜일까요? – AI는 픽셀 단위로{' '}
        <span className="red"> 진실을 추적</span>합니다
      </h1>

      <div className="detect-main">
        {/* [1] 업로드 영역 */}
        <div className="detect-box">
          <h3>Upload Image</h3>
          <div className="detect-content-area">
            <label className="detect-upload-box">
              <input type="file" accept="image/*" onChange={handleFileChange} />
              {image ? (
                <img src={image} alt="preview" className="preview" />
              ) : (
                <div className="detect-inner-box">
                  이 창을 클릭하여
                  <br />
                  파일을 첨부해 주세요
                </div>
              )}
            </label>
          </div>

          {/* 체크박스 */}
          <div className="detect-consent-section">
            <label className="detect-checkbox-text">
              <input
                type="checkbox"
                checked={rightsChecked}
                onChange={() => setRightsChecked((prev) => !prev)}
              />
              <p>이 이미지는 타인의 초상권 또는 저작권을 침해하지 않습니다</p>
            </label>
            <label className="detect-checkbox-text">
              <input
                type="checkbox"
                checked={disclaimerChecked}
                onChange={() => setDisclaimerChecked((prev) => !prev)}
              />
              <p>
                AI 분석 결과는 참고용이며 법적 증거로 사용되지 않음을 이해합니다
              </p>
            </label>
          </div>

          <div className="detect-button-group">
            <button
              className="detect-btn"
              disabled={!file || !allChecked || loading}
              onClick={handleDetect}
            >
              {loading ? '분석 중...' : 'Detect'}
            </button>
          </div>
        </div>

        {/* [2] 화살표 영역 */}
        <div className="detect-arrow-box">
          <img src="/images/arrow.jpg" alt="arrow" />
        </div>

        {/* [3] 결과 영역 */}
        <div className="detect-box">
          <h3>Detection Results</h3>
          <div className="detect-content-area">
            {result ? (
              result.error ? (
                <p className="detect-error-text">{result.error}</p>
              ) : (
                <div className="detect-result-box">
                  {/* ✅ Grad-CAM 히트맵 이미지 표시 */}
                  {result.gradcam && (
                    <img
                      src={`data:image/png;base64,${result.gradcam}`}
                      alt="Grad-CAM heatmap"
                      className="gradcam-preview"
                    />
                  )}
                </div>
              )
            ) : (
              <p className="result-placeholder">분석 이미지가 나타납니다</p>
            )}
          </div>

          {/* ✅ 결과요약박스 + PDF 버튼 병렬 배치 */}
          <div className="result-summary-row">
            <div
              className={`result-summary-box ${
                result && !result.error ? 'active' : ''
              }`}
            >
              {result && !result.error ? (
                <>
                  <p className="detect-result-line">
                    <span className="blue">- 결과 :</span> {result.result}
                  </p>
                  <p className="detect-result-line">
                    <span className="blue">- 딥페이크 확률 :</span>{' '}
                    {(result.fake_probability * 100).toFixed(1)}%
                  </p>
                </>
              ) : (
                <p className="detect-result-placeholder">
                  분석 결과를 확인하세요
                </p>
              )}
            </div>

            <button
              className="pdf-btn"
              onClick={handleDownloadPDF}
              disabled={!result || result.error}
            >
              📄 PDF 보고서
              <br /> 다운로드
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
