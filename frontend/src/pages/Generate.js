import React from 'react';
import '../styles/generate.css';

export default function Generate() {
  return (
    <div className="generate-container">
      <h1 className="generate-title">
        AI가 인간의 얼굴을 어떻게 <span className="blue">재구성</span>하는지
        체험해 보세요
      </h1>

      {/* upload, arrow, generate 영역 */}
      <div className="generate-main">
        {/* [1] Upload Part */}
        <div className="box">
          <h3>Upload Image</h3>
          <div className="content-area">
            <div className="inner-box">
              이미지를 Drag & Drop 하거나
              <br />이 창을 클릭해 주세요
            </div>
          </div>
          <div className="button-group">
            <button className="generate-btn">Generate</button>
          </div>
        </div>

        {/* [2] Arrow */}
        <div className="arrow-box">
          <img src="/images/arrow.jpg" alt="arrow" />
        </div>

        {/* [3] Generate Result */}
        <div className="box">
          <h3>Generate Image</h3>
          <div className="content-area">
            <div className="inner-box">
              Loading icon
              <br />
            </div>
          </div>
          <div className="button-group">
            <button>Download</button>
            <button>Regenerate</button>
            <button>Detect</button>
          </div>
        </div>
      </div>
    </div>
  );
}
