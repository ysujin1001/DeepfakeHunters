import React from 'react';
import '../styles/home.css';

export default function Home() {
  return (
    <div className="home-container">
      <h1 className="home-title">
        AI는 세상을 <span className="highlight-blue">창조</span>하는 손이자,
        <br />
        <span className="highlight-red">진실</span>을 지키는 눈입니다.
      </h1>

      <p className="home-subtitle">
        우리는 그 눈으로, 진짜를 봅니다.
        <br />
        Deepfake Hunters의 세계에 오신 것을 환영합니다.
      </p>

      <div className="home-buttons">
        <a href="/generate" className="btn btn-generate">
          Generate
        </a>
        <a href="/detect" className="btn btn-detect">
          Detect
        </a>
      </div>

      <footer className="home-footer">© 2025 Deepfake Hunters</footer>
    </div>
  );
}
