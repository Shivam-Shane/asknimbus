import React from 'react';
import '../styles/Home.css';
import { useChatbot } from '../components/ChatbotContext';

const Home = () => {
  const { openChatPopup } = useChatbot();

  return (
    <div className="home-container">
      <section className="hero-section">
        <h1 className="hero-title">Master AWS with AskNimbus</h1>
        <p className="hero-description">
          Accelerate your cloud journey with our AI-powered chatbot, leveraging AWS re:Post and official{' '}
          <a href="https://docs.aws.amazon.com" target="_blank" rel="noopener noreferrer" className="text-link">
            AWS documentation
          </a>{' '}
          to learn services, troubleshoot issues, and boost your skills.
        </p>
        <button className="cta-button" onClick={openChatPopup}>
          Start Chatting Now
        </button>
      </section>
      <section className="features-section">
        <h2 className="features-title">Why Choose AskNimbus?</h2>
        <div className="features-grid">
          <div className="feature-card">
            <h3 className="feature-title">Instant AWS Insights</h3>
            <p className="feature-description">
              Get real-time answers sourced from{' '}
              <a href="https://repost.aws" target="_blank" rel="noopener noreferrer" className="text-link">
                AWS re:Post
              </a>{' '}
              and AWS documentation.
            </p>
          </div>
          <div className="feature-card">
            <h3 className="feature-title">Interactive Learning</h3>
            <p className="feature-description">
              Engage with our AI to master AWS services step-by-step, from EC2 to Lambda.
            </p>
          </div>
          <div className="feature-card">
            <h3 className="feature-title">24/7 Support</h3>
            <p className="feature-description">
              Access help anytime with our responsive chatbot, designed for your cloud needs.
            </p>
          </div>
        </div>
        <p className="features-cta">
          Explore{' '}
          <a href="https://repost.aws" target="_blank" rel="noopener noreferrer" className="text-link">
            AWS re:Post
          </a>{' '}
          for community insights or dive into{' '}
          <a href="https://docs.aws.amazon.com" target="_blank" rel="noopener noreferrer" className="text-link">
            AWS documentation
          </a>{' '}
          for in-depth resources.
        </p>
      </section>
    </div>
  );
};

export default Home;