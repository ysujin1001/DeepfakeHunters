import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Generate from './pages/Generate';
import Detect from './pages/Detect';
import End from './pages/End';
import Navbar from './components/Navbar';

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/generate" element={<Generate />} />
        <Route path="/detect" element={<Detect />} />
        <Route path="/end" element={<End />} />
      </Routes>
    </BrowserRouter>
  );
}
