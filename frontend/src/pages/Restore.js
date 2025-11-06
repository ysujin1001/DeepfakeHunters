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

  // ✅ 파일 변경
  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (!selected) return;
    setReFile(selected);
    setReImage(URL.createObjectURL(selected));
    setReResult(null);
  };

  // ✅ 파일 첨부 버튼 클릭
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

  // ✅ 복원된 이미지 다운로드 (팝업 + 다운로드 실행)
  const handleDownload = () => {
    if (!reResult || !reResult.restored_image_url)
      return alert('복원된 이미지가 없습니다.');

    // 1️⃣ 팝업으로 다운로드 확인
    const confirmDownload = window.confirm(
      '복원된 이미지를 다운로드하시겠습니까?'
    );
    if (!confirmDownload) return;

    // 2️⃣ 파일 저장 실행
    fetch(reResult.restored_image_url)
      .then((res) => res.blob())
      .then((blob) => {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'restored_image.png';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        // 3️⃣ 다운로드 완료 알림
        alert('✅ 다운로드가 완료되었습니다!');
      })
      .catch(() => alert('다운로드 중 오류가 발생했습니다.'));
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
              <p className="restore-result-placeholder">
                복원 이미지가 나타납니다
              </p>
            )}
          </div>

          {/* ✅ 다운로드 버튼 */}
          <div className="restore-button-group">
            <button
              onClick={handleDownload}
              disabled={!reResult || reResult.error}
            >
              Download
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
