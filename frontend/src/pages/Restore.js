// Path: src/pages/Restore.js

import { useState, useRef } from 'react';
import '../styles/restore.css';

export default function Restore() {
  const [reImage, setReImage] = useState(null);
  const [reFile, setReFile] = useState(null);
  const [reResult, setReResult] = useState(null);
  const [reLoading, setReLoading] = useState(false);
  const [ethicsChecked, setEthicsChecked] = useState(false);

  const fileInputRef = useRef(null);
  const allChecked = ethicsChecked;

  // ✅ 파일 변경 핸들러
  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (!selected) return;
    setReFile(selected);
    setReImage(URL.createObjectURL(selected));
    setReResult(null);
  };

  // ✅ 버튼 클릭 → 파일 선택창 열기
  const handleUploadClick = () => {
    if (fileInputRef.current) fileInputRef.current.click();
  };

  // ✅ 복원 요청
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
            {/* ✅ 수정된 부분 시작 */}
            {reImage ? (
              <img src={reImage} alt="preview" className="preview" />
            ) : (
              <div className="restore-inner-box">
                <p className="upload-guide">복원할 얼굴 이미지를 첨부하세요</p>
                <button
                  className="restore-upload-btn"
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
            {/* ✅ 수정된 부분 끝 */}
          </div>

          {/* 체크박스 */}
          <div className="restore-consent-section">
            <label className="restore-checkbox-text">
              <input
                type="checkbox"
                checked={ethicsChecked}
                onChange={() => setEthicsChecked((prev) => !prev)}
              />
              <p>AI 이미지로 타인 비방·범죄·허위정보를 생성하지 않겠습니다</p>
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
              <p className="resore-result-placeholder">
                복원 이미지가 나타납니다
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
