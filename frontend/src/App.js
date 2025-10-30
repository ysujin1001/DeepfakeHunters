import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Generate from './pages/Generate';
import Detect from './pages/Detect';
import Conclusion from './pages/Conclusion';
import Navbar from './components/Navbar';

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/generate" element={<Generate />} />
        <Route path="/detect" element={<Detect />} />
        <Route path="/conclusion" element={<Conclusion />} />
      </Routes>
    </BrowserRouter>
  );
}
