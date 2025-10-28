// /api/predict 엔드포인트로 이미지를 전송 →
// 모델이 분석 후 fake_probability, result, image_path 를 반환

import { useState } from 'react';
import '../styles/detect.css';

export default function Detect() {
  const [image, setImage] = useState(null);
  const [file, setFile] = useState(null);
  const [consent, setConsent] = useState({ rights: false, disclaimer: false });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const allChecked = consent.rights && consent.disclaimer;

  // 이미지 파일 선택
  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (!selected) return;
    setFile(selected);
    setImage(URL.createObjectURL(selected));
    setResult(null);
  };

  // FastAPI로 분석 요청
  const handleDetect = async () => {
    if (!file || !allChecked) return;
    setLoading(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('http://localhost:8000/api/predict', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) throw new Error('서버 응답 오류');
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      setResult({ error: '❌ 분석 실패: 서버와 통신할 수 없습니다.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="detect-container">
      <h2>Deepfake Detection</h2>

      <label className="upload-box">
        <input type="file" accept="image/*" onChange={handleFileChange} />
        {image ? (
          <img src={image} alt="preview" className="preview" />
        ) : (
          <span>이미지를 업로드하거나 클릭하세요</span>
        )}
      </label>

      <div className="consent">
        <label>
          <input
            type="checkbox"
            checked={consent.rights}
            onChange={(e) =>
              setConsent({ ...consent, rights: e.target.checked })
            }
          />
          이 이미지는 타인의 초상권 또는 저작권을 침해하지 않습니다.
        </label>

        <label>
          <input
            type="checkbox"
            checked={consent.disclaimer}
            onChange={(e) =>
              setConsent({ ...consent, disclaimer: e.target.checked })
            }
          />
          AI 분석 결과는 참고용이며, 법적 증거로 사용되지 않음을 이해합니다.
        </label>
      </div>

      <button
        disabled={!allChecked || !file || loading}
        onClick={handleDetect}
        className="btn-detect"
      >
        {loading ? 'Analyzing...' : 'Check Authenticity'}
      </button>

      {result && (
        <div className="detect-result">
          {result.error ? (
            <p>{result.error}</p>
          ) : (
            <>
              <p>
                🧠 Fake Probability: {Math.round(result.fake_probability * 100)}
                %
              </p>
              <p>📊 Result: {result.result}</p>
              <p>📁 Image Path: {result.image_path}</p>
            </>
          )}
        </div>
      )}
    </div>
  );
}
