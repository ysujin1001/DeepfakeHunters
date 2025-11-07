// Path: src/pages/Conclusion.js
import { useState, useEffect } from 'react';
import '../styles/conclusion.css';

export default function Conclusion() {
  // ======================================================
  // 🧠 상태 정의
  // ======================================================
  const [showOriginal, setShowOriginal] = useState(true);

  // ======================================================
  // 🔁 이미지 전환 사이클 (원본 ↔ 반전)
  // ======================================================
  useEffect(() => {
    let switchTimeout;

    const cycle = () => {
      // ① 원본 이미지 표시
      setShowOriginal(true);

      // ② 1초 후 반전 이미지로 전환
      switchTimeout = setTimeout(() => {
        setShowOriginal(false);
      }, 1000);
    };

    // 사이클 실행 및 반복
    cycle();
    const interval = setInterval(cycle, 2000); // 총 주기: 1 + 1초 = 2초

    // 🔧 클린업
    return () => {
      clearInterval(interval);
      clearTimeout(switchTimeout);
    };
  }, []);

  // ======================================================
  // 🖥️ 렌더링
  // ======================================================
  return (
    <div className="conclusion-container">
      <h1 className="conclusion-sub-title">
        AI는 이미지를 분석해 <span className="blue">진실을 찾아내고, </span>
        복원해
        <span className="red"> 잃어버린 기억을 되살립니다</span>
        <br />
      </h1>

      {/* 메인 타이틀 */}
      <h1 className="conclusion-main-title">
        우린 그 진실이 사람을 해치지 않도록,
        <br />
        <span className="yellow">오늘도 조용히 — 지켜보고 있습니다</span>
      </h1>

      {/* 이미지 영역 */}
      <div className="conclusion-image">
        <img
          src={
            showOriginal
              ? '/images/watching_reverse.png'
              : '/images/watching_color.png'
          }
          alt="Looking Ahead"
        />
      </div>
    </div>
  );
}
