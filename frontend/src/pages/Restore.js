// Path: src/pages/Restore.js
// Desc: 이미지 업로드 + 윤리 동의 + AI 생성 요청 페이지 (Detect 스타일 반영)

import { useState } from 'react';
import '../styles/restore.css';

export default function Restore() {
  const [reImage, setReImage] = useState(null);
  const [reFile, setReFile] = useState(null);
  const [reResult, setReResult] = useState(null);
  const [reLoading, setReLoading] = useState(false);
  const [ethicsChecked, setEthicsChecked] = useState(false);

  const allChecked = ethicsChecked;

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (!selected) return;
    setReFile(selected);
    setReImage(URL.createObjectURL(selected));
    setReResult(null);
  };

  const handleRestore = async () => {
    if (!reFile) return alert('파일을 선택하세요!');
    if (!allChecked) return alert('체크박스에 동의해주세요.');

    setReLoading(true);
    const formData = new FormData();
    formData.append('file', reFile);

    try {
      const res = await fetch(`${process.env.REACT_APP_API_URL}/api/restore`, {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      setReResult(data);
    } catch (err) {
      console.error(err);
      setReResult({ error: '서버 오류가 발생했습니다.' });
    } finally {
      setReLoading(false);
    }
  };

  return (
    <div className="restore-container">
      <h1 className="restore-title">
        흐릿한 얼굴, 사라진 기억 - AI가 <span className="blue">되살립니다</span>
      </h1>

      <div className="restore-main">
        {/* [1️⃣ 업로드 영역] */}
        <div className="restore-box">
          <h3>Upload Image</h3>
          <div className="restore-content-area">
            <label className="restore-upload-box">
              <input type="file" accept="image/*" onChange={handleFileChange} />
              {reImage ? (
                <img src={reImage} alt="preview" className="preview" />
              ) : (
                <div className="restore-inner-box">
                  이 창을 클릭하여
                  <br />
                  파일을 첨부해 주세요
                </div>
              )}
            </label>
          </div>

          {/* 체크박스 */}
          <div className="restore-consent-section">
            <label className="restore-checkbox-text">
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
          <div className="restore-button-group">
            <button
              disabled={!reFile || !allChecked || reLoading}
              onClick={handleRestore}
            >
              {reLoading ? '생성 중...' : 'Restore'}
            </button>
          </div>
        </div>

        {/* [➡️ 화살표] */}
        <div className="restore-arrow-box">
          <img src="/images/arrow.jpg" alt="arrow" />
        </div>

        {/* [2️⃣ 결과 영역] */}
        <div className="restore-box">
          <h3>Restored Result</h3>
          <div className="restore-content-area">
            {reResult ? (
              reResult.error ? (
                <p className="restore-error-text">{reResult.error}</p>
              ) : (
                <div className="restore-result-box">
                  <img
                    src={reResult.restored_image_url}
                    alt="Restored Result"
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
