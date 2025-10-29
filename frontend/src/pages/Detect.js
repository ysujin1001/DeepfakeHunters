// /api/predict 엔드포인트로 이미지를 전송 →
// 모델이 분석 후 fake_probability, result, image_path 를 반환

import React from 'react';
import '../styles/detect.css';

export default function Detect() {
  return (
    <div className="detect-container">
      <h1 className="detect-title">
        진실을 확인하세요 – AI가 이미지 <span className="red">진위 여부</span>를
        분석합니다.
      </h1>

      <div className="detect-main">
        {/* [1] Upload Section */}
        <div className="box">
          <h3>Upload Image</h3>
          <div className="content-area">
            <div className="inner-box">
              이미지를 Drag & Drop 하거나
              <br />이 창을 클릭해 주세요
            </div>
          </div>
          <div className="button-group">
            <button className="detect-btn">Detect</button>
          </div>
        </div>

        {/* [2] Arrow Section */}
        <div className="arrow-box">
          <img src="/images/arrow.jpg" alt="arrow" />
        </div>

        {/* [3] Result Section */}
        <div className="box">
          <h3>Detection Results</h3>
          <div className="content-area">
            <div className="result-box">
              <p className="result-line">
                - <span className="blue">Confidence:</span> 92% (Fake)
              </p>
              <p className="result-line">
                - <span className="blue">Authenticity Score:</span> 0.14
              </p>
            </div>
          </div>
          <div className="button-group">
            <button>Download</button>
            <button>Redetect</button>
          </div>
        </div>
      </div>
    </div>
  );
}
