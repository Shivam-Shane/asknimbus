import React from 'react';
import '../styles/TermsPrivacy.css';

const TermsPrivacy = () => {
  return (
    <div className="terms-privacy-container">
      <header className="terms-header">
        <h1 className="terms-title">Terms & Privacy Policy</h1>
        <p className="terms-subtitle">
          Understand how AskNimbus operates and protects your data while leveraging AWS resources.
        </p>
      </header>
      <main className="terms-content">
        <section className="terms-section">
          <h2 className="section-title">Terms of Use</h2>
          <p className="section-text">
            By accessing or using AskNimbus, you agree to be bound by these Terms of Use. AskNimbus is designed to assist users in learning about AWS services through our AI-powered chatbot, which sources information from publicly available AWS re:Post discussions and AWS documentation. You agree to use the service for lawful purposes only and to respect all applicable intellectual property rights.
          </p>
          <p className="section-text">
            AskNimbus provides information based on AWS re:Post (available at{' '}
            <a href="https://repost.aws" target="_blank" rel="noopener noreferrer" className="text-link">
              https://repost.aws
            </a>) and AWS official documentation (available at{' '}
            <a href="https://docs.aws.amazon.com" target="_blank" rel="noopener noreferrer" className="text-link">
              https://docs.aws.amazon.com
            </a>). While we strive to provide accurate and up-to-date information, you are responsible for verifying the accuracy of responses for critical applications. For AWS's official terms, please refer to the{' '}
            <a href="https://aws.amazon.com/service-terms/" target="_blank" rel="noopener noreferrer" className="text-link">
              AWS Service Terms
            </a>.
          </p>
        </section>
        <section className="terms-section">
          <h2 className="section-title">Privacy Policy</h2>
          <p className="section-text">
            At AskNimbus, your privacy is our priority. We collect minimal data, such as chat inputs and temporary session IDs, solely to enhance your experience and maintain conversation continuity. This data is stored locally in your browser with a 24-hour expiry or on redis cache having expire of 1 hour and is not shared with third parties without your explicit consent.
          </p>
          <p className="section-text">
            Our chatbot leverages publicly available AWS re:Post content and AWS documentation to generate responses. No personal data is transmitted to external servers unless explicitly required for functionality (e.g., session management). For details on how AWS handles data, please review the{' '}
            <a href="https://aws.amazon.com/privacy/" target="_blank" rel="noopener noreferrer" className="text-link">
              AWS Privacy Notice
            </a>.
          </p>
        </section>
        <section className="terms-section">
          <h2 className="section-title">Data Usage and Intellectual Property</h2>
          <p className="section-text">
            AskNimbus does not store personal data beyond the session unless necessary for service delivery. All AWS-related content provided by the chatbot, including responses derived from AWS re:Post and AWS documentation, is subject to AWS's copyright and intellectual property policies. We do not claim ownership of this content and provide it for educational purposes only.
          </p>
          <p className="section-text">
            Users are prohibited from reproducing, distributing, or modifying AWS content accessed through AskNimbus without proper authorization from AWS. For more information, see AWS's{' '}
            <a href="https://aws.amazon.com/legal/" target="_blank" rel="noopener noreferrer" className="text-link">
              Legal Agreements
            </a>.
          </p>
        </section>
        <section className="terms-section">
          <h2 className="section-title">Contact Us</h2>
          <p className="section-text">
            If you have questions about these terms or our privacy practices, please contact us at{' '}
            <a href="mailto:data.console.store@gmail.com" className="text-link">
              data.console.store@gmail.com
            </a>.
          </p>
        </section>
      </main>
    </div>
  );
};

export default TermsPrivacy;