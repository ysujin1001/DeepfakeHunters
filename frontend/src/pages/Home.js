import React from 'react';
import '../styles/home.css';
import Footer from '../components/Footer';

export default function Home() {
  return (
    <div className="home-container">
      {/* 왼쪽 텍스트 영역 */}
      <div className="home-text">
        <h1 className="home-title">
          AI는 세상을 <span className="blue">창조</span>하는 손이자,
          <br />
          <span className="red">진실</span>을 지키는 눈입니다
        </h1>

        <div className="home-section">
          <div className="section-number">1</div>
          <div>
            <h3 className="section-title">창조의 얼굴</h3>
            <p>
              AI는 상상을 현실로 바꾸는 힘을 지녔습니다 <br />
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
              <span className="highlight"> ‘진짜’를 구별하는 눈</span>이 되어야
              합니다
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
              기술이 사람을 속이는 대신, <strong>사람을 보호하도록</strong>{' '}
              만드는 것이 우리의 목표입니다
            </p>
          </div>
        </div>
      </div>

      {/* 오른쪽 이미지 영역 */}
      <div className="home-image">
        <img src="/images/homeImage_ex.jpg" alt="AI generated face" />
      </div>
    </div>
  );
}
