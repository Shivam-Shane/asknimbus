// src/App.js
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Home from './components/Home';
import TermsPrivacy from './components/TermsPrivacy';
import ContactUs from './components/ContactUs';
import Footer from './components/Footer';
import Chatbot from './components/chatbot';
import { ChatbotProvider } from './components/ChatbotContext'; // Import the provider
import './App.css';
import './styles/NavIcon.css';

const App = () => {
  return (
    <ChatbotProvider>
      <BrowserRouter>
        <div className="app-container">
          <Link to="/" className="home-icon" data-tooltip="Home">
            <img src="/logonew.png" alt="Home Icon" />
          </Link>
          <main className="flex-grow">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/terms-privacy" element={<TermsPrivacy />} />
              <Route path="/contact-us" element={<ContactUs />} />
            </Routes>
          </main>
          <Chatbot />
          <Footer />
        </div>
      </BrowserRouter>
    </ChatbotProvider>
  );
};

export default App;