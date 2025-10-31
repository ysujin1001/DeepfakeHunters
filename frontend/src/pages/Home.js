import React, { useEffect, useState } from 'react';
import '../styles/home.css';

export default function Home() {
  const [showAI, setShowAI] = useState(false);
  const [showWarning, setShowWarning] = useState(false);
  const [alertMode, setAlertMode] = useState(false);
  const [reset, setReset] = useState(false);

  useEffect(() => {
    const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

    const cycle = async () => {
      // ① 초기 상태: 원본 표시
      setShowAI(false);
      setShowWarning(false);
      setAlertMode(false);
      setReset(false);
      await wait(2000);

      // ③ AI 이미지 뜨자마자 경고 + 테두리 깜빡임
      setShowAI(true);
      setShowWarning(true);
      setAlertMode(true);
      await wait(2000);

      // ④ 모두 페이드아웃
      setReset(true);
      setShowAI(false);
      setShowWarning(false);
      setAlertMode(false);
      await wait(500);
    };

    cycle();
    const loop = setInterval(cycle, 4500); // 전체 루프 시간
    return () => clearInterval(loop);
  }, []);

  return (
    <div className="home-container">
      {/* 왼쪽 텍스트 영역 */}
      <div className="home-text">
        <h1 className="home-title">
          AI는 세상을 <span className="blue">창조</span>하는 손이자,
          <br />
          <span className="red">진실</span>을 지키는{' '}
          <span className="yellow">눈</span>입니다
        </h1>

        <div className="home-section">
          <div className="section-number">1</div>
          <div>
            <h3 className="section-title">창조의 얼굴</h3>
            <p>
              AI는{' '}
              <span className="highlight-blue">상상을 현실로 바꾸는 힘</span>을
              지녔습니다 <br />
              얼굴을 만들고, 공간을 재현하며, 아직 존재하지 않는 세상을 그립니다
            </p>
          </div>
        </div>

        <div className="home-section">
          <div className="section-number">2</div>
          <div>
            <h3 className="section-title">진실의 얼굴</h3>
            <p>
              그러나 같은 기술이 진실을 왜곡할 수도 있습니다
              <br />
              우리는 AI가 만든 세계 속에서
              <span className="highlight-red"> ‘진짜’를 구별하는 눈</span>이
              되어야 합니다
            </p>
          </div>
        </div>

        <div className="home-section">
          <div className="section-number">3</div>
          <div>
            <h3 className="section-title">Deepfake Hunters의 약속</h3>
            <p>
              우리는 AI의 창조성을 존중하면서도, 그 안의 윤리를 지켜냅니다
              <br />
              기술이 사람을 속이는 대신,{' '}
              <span className="highlight-yellow">사람을 보호하도록</span> 만드는
              것이 우리의 목표입니다
            </p>
          </div>
        </div>
      </div>

      {/* 오른쪽 이미지 영역 */}
      <div className={`home-image ${alertMode ? 'alert-border' : ''}`}>
        {/* 원본 이미지 */}
        <img
          src="/images/homeImage_origin.jpg"
          alt="Original"
          className={`home-img base ${showAI ? 'fade-out' : 'fade-in'} ${
            reset ? 'reset' : ''
          }`}
        />

        {/* AI 생성 이미지 */}
        <img
          src="/images/homeImage_ai.jpg"
          alt="AI Generated"
          className={`home-img ai ${showAI ? 'fade-in' : 'fade-out'} ${
            reset ? 'reset' : ''
          }`}
        />

        {/* 경고 표시 */}
        {showWarning && (
          <div className={`deepfake-warning ${reset ? 'fade-out' : 'fade-in'}`}>
            ⚠ Deepfake!
          </div>
        )}
      </div>
    </div>
  );
}
