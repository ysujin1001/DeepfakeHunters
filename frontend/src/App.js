import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import Detect from './pages/Detect';
import Restore from './pages/Restore';
import Conclusion from './pages/Conclusion';
import Navbar from './components/Navbar';

export default function App() {
  return (
    <Router>
      <Routes>
        {/* Layout을 Route의 element로 지정 */}
        <Route element={<Layout />}>
          <Route path="/" element={<Home />} />
          <Route path="/detect" element={<Detect />} />
          <Route path="/restore" element={<Restore />} />
          <Route path="/conclusion" element={<Conclusion />} />
        </Route>
      </Routes>
    </Router>
  );
}
