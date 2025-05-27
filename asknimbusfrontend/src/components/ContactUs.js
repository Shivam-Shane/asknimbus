import React, { useState } from 'react';
import '../styles/ContactUs.css';

const ContactUs = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: '',
  });
  const [formStatus, setFormStatus] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Simulate form submission (no backend in this project)
    setFormStatus('Thank you for your message! We will get back to you soon.');
    setFormData({ name: '', email: '', message: '' });
    setTimeout(() => setFormStatus(''), 5000); // Clear message after 5 seconds
  };

  return (
    <div className="contact-us-container">
      <header className="contact-header">
        <h1 className="contact-title">Contact Us</h1>
        <p className="contact-subtitle">
          Have questions about AskNimbus or need help with AWS? Reach out to our team or explore{' '}
          <a href="https://repost.aws" target="_blank" rel="noopener noreferrer" className="text-link">
            AWS re:Post
          </a>{' '}
          for community-driven AWS support.
        </p>
      </header>
      <main className="contact-content">
        <div className="contact-form-card">
          <h2 className="form-title">Send Us a Message</h2>
          <form onSubmit={handleSubmit} className="contact-form">
            <div className="form-group">
              <label htmlFor="name" className="form-label">
                Name
              </label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                placeholder="Your name"
                className="form-input"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="email" className="form-label">
                Email
              </label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                placeholder="Your email"
                className="form-input"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="message" className="form-label">
                Message
              </label>
              <textarea
                id="message"
                name="message"
                value={formData.message}
                onChange={handleInputChange}
                placeholder="How can we help you?"
                className="form-textarea"
                rows="5"
                required
              ></textarea>
            </div>
            <button type="submit" className="contact-button">
              Send Message
            </button>
            {formStatus && <p className="form-status">{formStatus}</p>}
          </form>
        </div>
        <div className="contact-alternative">
          <h2 className="form-title">Other Ways to Reach Us</h2>
          <p className="section-text">
            Email us directly at{' '}
            <a href="mailto:data.console.store@gmail.com" className="text-link">
              data.console.store@gmail.com
            </a>
            .
          </p>
          <p className="section-text">
            For AWS-specific queries, visit{' '}
            <a href="https://repost.aws" target="_blank" rel="noopener noreferrer" className="text-link">
              AWS re:Post
            </a>{' '}
            or{' '}
            <a href="https://docs.aws.amazon.com" target="_blank" rel="noopener noreferrer" className="text-link">
              AWS Documentation
            </a>{' '}
            for detailed resources.
          </p>
        </div>
      </main>
    </div>
  );
};

export default ContactUs;