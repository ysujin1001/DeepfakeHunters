// Path: src/components/Navbar.js
// Desc: 상단 네비게이션 바 (텍스트 순환 + 메뉴 Tooltip)

import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import '../styles/navbar.css';

export default function Navbar() {
  // ======================================================
  // 🧠 상태 정의
  // ======================================================
  const texts = [
    <span className="special-text">2팀</span>,
    <>
      Deepfake <br /> Hunters
    </>,
    <>
      딥페이크 <br /> 헌 터 스
    </>,
  ];

  const [index, setIndex] = useState(0);
  const [fadeState, setFadeState] = useState('fade-in');

  // ======================================================
  // 🔁 텍스트 페이드 전환 (2초 표시 → 0.8초 전환)
  // ======================================================
  useEffect(() => {
    let fadeOutTimeout;
    let switchTimeout;

    const startCycle = () => {
      // ① 2초 동안 현재 텍스트 유지
      fadeOutTimeout = setTimeout(() => {
        setFadeState('fade-out');

        // ② 0.8초 후 다음 텍스트로 전환
        switchTimeout = setTimeout(() => {
          setIndex((prev) => (prev + 1) % texts.length);
          setFadeState('fade-in');
        }, 800);
      }, 2000);
    };

    startCycle();

    const interval = setInterval(startCycle, 2800); // 2초 표시 + 0.8초 전환

    // 🧹 클린업
    return () => {
      clearInterval(interval);
      clearTimeout(fadeOutTimeout);
      clearTimeout(switchTimeout);
    };
  }, []);

  // ======================================================
  // 🖥️ 렌더링
  // ======================================================
  return (
    <nav className="navbar">
      {/* ------------------------------ */}
      {/* 🔹 좌측 로고 & 텍스트 순환 영역 */}
      {/* ------------------------------ */}
      <div className="navbar-left">
        <img
          src="/images/teamImage.jpg"
          alt="Deepfake Hunters team"
          className="navbar-logo"
        />

        {/* 3단계 순환 텍스트 */}
        <div className="navbar-title">
          <span className={`fade-text ${fadeState}`}>{texts[index]}</span>
        </div>
      </div>

      {/* ------------------------------ */}
      {/* 🔹 우측 메뉴 (hover 시 한글 Tooltip) */}
      {/* ------------------------------ */}
      <div className="navbar-menu">
        <NavLink to="/" className="nav-item">
          Home
          <span className="nav-tooltip">홈</span>
        </NavLink>
        <NavLink to="/detect" className="nav-item">
          Detect<span className="nav-tooltip">딥페이크 판별</span>
        </NavLink>
        <NavLink to="/restore" className="nav-item">
          Restore
          <span className="nav-tooltip">이미지 복원</span>
        </NavLink>
        <NavLink to="/conclusion" className="nav-item">
          Conclusion
          <span className="nav-tooltip">엔딩까지 완벽한 서비스!</span>
        </NavLink>
      </div>
    </nav>
  );
}
