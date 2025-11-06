// Path: src/pages/Detect.js
// Desc: 업로드 박스 안에 ‘분석대상 선택’ 및 파일첨부 버튼 삽입

import { useState, useRef } from 'react';
import '../styles/detect.css';

export default function Detect() {
  const [image, setImage] = useState(null);
  const [file, setFile] = useState(null);
  const [rightsChecked, setRightsChecked] = useState(false);
  const [disclaimerChecked, setDisclaimerChecked] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [summaryText, setSummaryText] = useState('');
  const [reportUrl, setReportUrl] = useState(null);
  const [modelType, setModelType] = useState('korean'); // 분석 모델 선택

  const fileInputRef = useRef(null); // 숨겨진 파일 input 제어용 ref
  const allChecked = rightsChecked && disclaimerChecked;

  // 파일 선택
  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (!selected) return;
    setFile(selected);
    setImage(URL.createObjectURL(selected));
    setResult(null);
    setSummaryText('');
  };

  // 파일 첨부 버튼 클릭 시
  const handleUploadClick = () => {
    if (fileInputRef.current) fileInputRef.current.click();
  };

  // PDF 다운로드
  const handleDownloadPDF = async () => {
    try {
      const res = await fetch(`${process.env.REACT_APP_API_URL}/api/report`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(result), // ✅ 분석 결과 JSON 전송
      });
      if (!res.ok) throw new Error('PDF 생성 실패');

      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'Deepfake_Heatmap_Report.pdf';
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error(err);
      alert('PDF 생성 중 오류가 발생했습니다.');
    }
  };

  // AI 판별 요청
  const handleDetect = async () => {
    if (!file) return alert('파일을 선택하세요!');
    if (!allChecked) return alert('체크박스에 모두 동의해주세요.');

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('model_type', modelType);

    try {
      // ✅ 업로드
      await fetch(`${process.env.REACT_APP_API_URL}/api/upload`, {
        method: 'POST',
        body: formData,
      });

      // ✅ 예측 요청
      const res = await fetch(`${process.env.REACT_APP_API_URL}/api/predict`, {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();

      // ✅ 수정됨: 백엔드에서 문장이 아닌 숫자 데이터만 받음
      setResult(data);

      // ✅ 수정됨: 프런트에서 문장 조합
      if (!data.error && data.pred_label && data.confidence !== undefined) {
        const { pred_label, confidence, fake_probability } = data;
        let msg = '';

        if (pred_label === 'Fake') {
          msg = `Fake! (신뢰도: ${confidence.toFixed(2)}%)`;
        } else if (pred_label === 'Real') {
          msg = `Real! (신뢰도: ${confidence.toFixed(2)}%)`;
        } else {
          msg = '분류 결과를 가져올 수 없습니다.';
        }

        setSummaryText(msg);
      } else {
        setSummaryText('분석 결과를 가져올 수 없습니다.');
      }
    } catch (err) {
      console.error(err);
      setResult({ error: '서버 오류 발생' });
      setSummaryText('서버 오류로 분석을 완료할 수 없습니다.');
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
            {image ? (
              <img src={image} alt="preview" className="preview" />
            ) : (
              <div className="detect-inner-box">
                {/* ✅ 분석 대상 선택 섹션 */}
                <div className="detect-model-box">
                  <p className="model-select-title">
                    # 분석대상을 선택하세요 (택1)
                  </p>
                  <div className="detect-model-select">
                    <label>
                      <input
                        type="radio"
                        value="korean"
                        checked={modelType === 'korean'}
                        onChange={(e) => setModelType(e.target.value)}
                      />
                      한국인 이미지
                    </label>
                    <label>
                      <input
                        type="radio"
                        value="foreign"
                        checked={modelType === 'foreign'}
                        onChange={(e) => setModelType(e.target.value)}
                      />
                      외국인 이미지
                    </label>
                  </div>
                </div>

                {/* ✅ 파일 첨부 버튼 */}
                <button
                  className="detect-upload-btn"
                  onClick={handleUploadClick}
                >
                  이미지 파일 첨부
                </button>

                {/* 숨겨진 input */}
                <input
                  type="file"
                  accept="image/*"
                  ref={fileInputRef}
                  style={{ display: 'none' }}
                  onChange={handleFileChange}
                />
              </div>
            )}
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
              <p className="detect-result-placeholder">
                분석 이미지가 나타납니다
              </p>
            )}
          </div>

          <div className="result-summary-row">
            <div
              className={`result-summary-box ${
                result && !result.error ? 'active' : ''
              }`}
            >
              {result && !result.error ? (
                <>
                  <p className="detect-result-line">
                    <span className="blue">- 결과 :</span> {summaryText}
                  </p>
                  <p className="detect-result-line">
                    <span className="blue">- 시각적 활성도 :</span>{' '}
                    {result.fake_probability
                      ? `${(result.fake_probability * 100).toFixed(1)}%`
                      : 'N/A'}
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
