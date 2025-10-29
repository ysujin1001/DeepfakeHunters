import React, { useState } from 'react';
import '../styles/generate.css'; // 스타일은 전부 이 파일에서 관리

export default function Generate() {
  const [image, setImage] = useState(null);
  const [agreement, setAgreement] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [generatedImage, setGeneratedImage] = useState(null);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(URL.createObjectURL(file));
      setGeneratedImage(null);
    }
  };

  const handleGenerate = () => {
    if (!agreement || !image) return;
    setIsLoading(true);

    // TODO: 추후 API 연동 부분 (현재는 임시 로딩 시뮬레이션)
    setTimeout(() => {
      setGeneratedImage('/placeholder_result.jpg'); // 임시용 더미 이미지
      setIsLoading(false);
    }, 2000);
  };

  return (
    <div className="generate-container">
      <h1 className="generate-title">Generate Image</h1>
      <p className="generate-description">
        AI가 인간의 얼굴을 어떻게 재구성하는지 체험해 보세요.
      </p>

      <div
        className="upload-area"
        onClick={() => document.getElementById('fileInput').click()}
      >
        {image ? (
          <img src={image} alt="preview" className="preview-image" />
        ) : (
          <p>이미지를 Drag & Drop 하거나 클릭해서 업로드하세요</p>
        )}
        <input
          id="fileInput"
          type="file"
          accept="image/*"
          style={{ display: 'none' }}
          onChange={handleImageUpload}
        />
      </div>

      <div className="agreement">
        <input
          type="checkbox"
          id="agree"
          checked={agreement}
          onChange={() => setAgreement(!agreement)}
        />
        <label htmlFor="agree">
          AI로 생성된 이미지를 타인 비방, 범죄, 허위 정보 생성 등의 목적으로
          사용하지 않겠습니다.
        </label>
      </div>

      <button
        className="btn-generate"
        onClick={handleGenerate}
        disabled={!agreement || !image}
      >
        {isLoading ? 'Loading...' : 'Generate'}
      </button>

      {generatedImage && (
        <div className="result-area">
          <h3>결과 이미지</h3>
          <img src={generatedImage} alt="generated" className="result-image" />
          <div className="result-buttons">
            <button className="btn">Download</button>
            <button className="btn">Regenerate</button>
          </div>
        </div>
      )}
    </div>
  );
}
