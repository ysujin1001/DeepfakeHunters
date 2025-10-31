// Path: src/pages/Generate.js
// Desc: 이미지 업로드 + 윤리 동의 + AI 생성 요청 페이지 (Detect 스타일 반영)

import { useState } from 'react';
import '../styles/generate.css';

export default function Generate() {
  const [genImage, setGenImage] = useState(null);
  const [genFile, setGenFile] = useState(null);
  const [genResult, setGenResult] = useState(null);
  const [genLoading, setGenLoading] = useState(false);
  const [ethicsChecked, setEthicsChecked] = useState(false);

  const allChecked = ethicsChecked;

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (!selected) return;
    setGenFile(selected);
    setGenImage(URL.createObjectURL(selected));
    setGenResult(null);
  };

  const handleGenerate = async () => {
    if (!genFile) return alert('파일을 선택하세요!');
    if (!allChecked) return alert('체크박스에 동의해주세요.');

    setGenLoading(true);
    const formData = new FormData();
    formData.append('file', genFile);

    try {
      const res = await fetch(`${process.env.REACT_APP_API_URL}/api/generate`, {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      setGenResult(data);
    } catch (err) {
      console.error(err);
      setGenResult({ error: '서버 오류가 발생했습니다.' });
    } finally {
      setGenLoading(false);
    }
  };

  return (
    <div className="generate-container">
      <h1 className="generate-title">
        AI가 인간의 얼굴을 어떻게 <span className="blue">재구성</span>하는지
        체험해 보세요
      </h1>

      <div className="generate-main">
        {/* [1️⃣ 업로드 영역] */}
        <div className="generate-box">
          <h3>Upload Image</h3>
          <div className="generate-content-area">
            <label className="generate-upload-box">
              <input type="file" accept="image/*" onChange={handleFileChange} />
              {genImage ? (
                <img src={genImage} alt="preview" className="preview" />
              ) : (
                <div className="generate-inner-box">
                  이미지를 Drag & Drop 하거나
                  <br />이 창을 클릭해 주세요
                </div>
              )}
            </label>
          </div>

          {/* 체크박스 */}
          <div className="generate-consent-section">
            <label className="generate-checkbox-text">
              <input
                type="checkbox"
                checked={ethicsChecked}
                onChange={() => setEthicsChecked((prev) => !prev)}
              />
              <p>
                AI로 생성된 이미지를 타인비방, 범죄, 허위정보 생성 등 목적으로
                사용하지 않겠습니다
              </p>
            </label>
          </div>

          {/* 버튼 */}
          <div className="generate-button-group">
            <button
              disabled={!genFile || !allChecked || genLoading}
              onClick={handleGenerate}
            >
              {genLoading ? '생성 중...' : 'Generate'}
            </button>
          </div>
        </div>

        {/* [➡️ 화살표] */}
        <div className="generate-arrow-box">
          <img src="/images/arrow.jpg" alt="arrow" />
        </div>

        {/* [2️⃣ 결과 영역] */}
        <div className="generate-box">
          <h3>Generated Result</h3>
          <div className="generate-content-area">
            {genResult ? (
              genResult.error ? (
                <p className="generate-error-text">{genResult.error}</p>
              ) : (
                <div className="generate-result-box">
                  <img
                    src={genResult.generated_image_url}
                    alt="Generated Result"
                    className="preview"
                  />
                </div>
              )
            ) : (
              <p className="result-placeholder">
                아직 생성된 이미지가 없습니다.
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
