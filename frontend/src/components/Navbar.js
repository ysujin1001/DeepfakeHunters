import React from 'react';
import { NavLink } from 'react-router-dom';
import '../styles/navbar.css';

export default function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-left">
        {/* public 폴더 이미지는 / 로 시작해서 접근 */}
        <img
          src="/images/teamImage.jpg"
          alt="Deepfake Hunters team"
          className="navbar-logo"
        />
        <div className="navbar-title">
          <span>
            Deepfake <br />
            Hunters
          </span>
        </div>
      </div>

      <div className="navbar-menu">
        <NavLink to="/" className="nav-item">
          Home
        </NavLink>
        <NavLink to="/generate" className="nav-item">
          Generate
        </NavLink>
        <NavLink to="/detect" className="nav-item">
          Detect
        </NavLink>
        <NavLink to="/conclusion" className="nav-item">
          conclusion
        </NavLink>
      </div>
    </nav>
  );
}
