import { useState, useEffect } from 'react';
import '../styles/conclusion.css';

export default function Conclusion() {
  const [showOriginal, setShowOriginal] = useState(true);

  useEffect(() => {
    let switchTimeout;

    const cycle = () => {
      // ✅ 1️⃣ 원본 이미지 표시
      setShowOriginal(true);
      switchTimeout = setTimeout(() => {
        // ✅ 2️⃣ 반전 이미지 즉시 전환
        setShowOriginal(false);
      }, 2000);
    };

    cycle();
    const interval = setInterval(cycle, 5000); // 총 주기: 3 + 1초 = 4초
    return () => {
      clearInterval(interval);
      clearTimeout(switchTimeout);
    };
  }, []);

  return (
    <div className="conclusion-container">
      <h1 className="conclusion-sub-title">
        AI는 세상을 <span className="blue">창조</span>하는 손이자,
        <span className="red"> 진실</span>을 지키는 눈입니다
      </h1>
      <h1 className="conclusion-main-title">
        우리는 그 눈으로, <span className="red">진짜를 봅니다</span>
      </h1>

      <div className="conclusion-image">
        <img
          src={
            showOriginal
              ? '/images/watching.jpg'
              : '/images/watching_reverse.png'
          }
          alt="Looking Ahead"
        />
      </div>
    </div>
  );
}
