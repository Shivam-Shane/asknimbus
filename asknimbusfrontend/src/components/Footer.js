import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Footer.css';

const Footer = () => {
  return (
    <footer className="footer-container">
      <div className="footer-content">
        <p className="footer-text">© 2025 AskNimbus. All rights reserved.</p>
        <div className="footer-links">
          <Link to="/terms-privacy" className="footer-link">Terms & Privacy</Link>
          <Link to="/contact-us" className="footer-link">Contact Us</Link>
        </div>
      </div>
    </footer>
  );
};

export default Footer;