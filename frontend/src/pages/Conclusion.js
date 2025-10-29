import '../styles/conclusion.css';

export default function Conclusion() {
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
        <img src="/images/watching.jpg" alt="Looking Ahead" />
      </div>
      <p className="credit">© 2025 Deepfake Hunters</p>
    </div>
  );
}
