// Path: src/components/Layout.js
// Desc: 전체 페이지 레이아웃 (Navbar + Main + Footer)

import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';
import Footer from './Footer';
import '../styles/layout.css';

export default function Layout() {
  // ======================================================
  // 🖥️ 렌더링
  // ======================================================
  return (
    <div className="layout-container">
      {/* 상단 네비게이션 바 */}
      <Navbar />

      {/* 메인 콘텐츠 영역 */}
      <main className="layout-main">
        <Outlet />
      </main>

      {/* 하단 푸터 */}
      <Footer />
    </div>
  );
}
