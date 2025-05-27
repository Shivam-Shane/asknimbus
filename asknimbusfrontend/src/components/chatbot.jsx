// src/components/Chatbot.jsx
import { useState, useRef, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMinus, faPaperPlane } from '@fortawesome/free-solid-svg-icons';
import { useChatbot } from './ChatbotContext'; // Import the hook
import '../styles/chatbot.css';

function Chatbot() {
  const { isPopupOpen, toggleChatPopup } = useChatbot(); // Use context
  const [messages, setMessages] = useState([
    { text: 'Learning AWS is fun and more interactive now.', isBot: true },
  ]);
  const [userInput, setUserInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [hasUnread, setHasUnread] = useState(false);
  const chatBoxRef = useRef(null);
  const popupRef = useRef(null);
  const beepSound = useRef(new Audio('/chat_notification.mp3'));
  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

  // Remove isPopupOpenRef since context manages isPopupOpen
  useEffect(() => {
    const handleOutsideClick = (event) => {
      if (isPopupOpen && popupRef.current && !popupRef.current.contains(event.target) && !event.target.closest('.chat-icon')) {
        toggleChatPopup();
      }
    };
    document.addEventListener('mousedown', handleOutsideClick);
    return () => document.removeEventListener('mousedown', handleOutsideClick);
  }, [isPopupOpen, toggleChatPopup]);

  // Check and manage session ID with 1-day expiry
  let session = JSON.parse(localStorage.getItem('session_id')) || { id: null, expires: null };
  if (session.expires && Date.now() > session.expires) {
    localStorage.removeItem('session_id');
    session.id = null;
  }
  let sessionId = session.id;

  const getCSRFToken = () => {
    let cookieValue = null;
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      const trimmedCookie = cookie.trim();
      if (trimmedCookie.startsWith('csrftoken=')) {
        cookieValue = trimmedCookie.substring('csrftoken='.length);
        break;
      }
    }
    return cookieValue;
  };

  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  const sendMessage = async () => {
    if (userInput.trim() === '') return;

    const newUserMessage = { text: userInput, isBot: false };
    setMessages((prev) => [...prev, newUserMessage]);
    setUserInput('');
    setIsTyping(true);

    try {
      const response = await fetch(`${BACKEND_URL}/api/chat/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({
          message: userInput,
          session_id: sessionId,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      if (data.session_id) {
        sessionId = data.session_id;
        localStorage.setItem('session_id', JSON.stringify({ id: sessionId, expires: Date.now() + 86400000 }));
      }
      await sleep(2000);

      setIsTyping(false);
      const botResponse = { text: data.message, isBot: true };
      setMessages((prev) => [...prev, botResponse]);
      setHasUnread((prev) => {
        if (!isPopupOpen) {
          beepSound.current.play().catch((err) => console.error('Beep error:', err));
          return true;
        }
        return prev;
      });
    } catch (error) {
      await sleep(2000);
      setIsTyping(false);
      const errorResponse = { text: 'Sorry, something went wrong!', isBot: true };
      setMessages((prev) => [...prev, errorResponse]);
      setHasUnread((prev) => {
        if (!isPopupOpen) {
          beepSound.current.play().catch((err) => console.error('Beep error:', err));
          return true;
        }
        return prev;
      });
    }
  };

  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTo({
        top: chatBoxRef.current.scrollHeight,
        behavior: 'smooth',
      });
    }
  }, [messages, isTyping]);

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  return (
    <>
      <div className="chat-icon" onClick={toggleChatPopup}>
        <img
          src="https://cdn-icons-png.flaticon.com/512/134/134914.png"
          alt="Chat Icon"
        />
        {hasUnread && <span className="unread-dot"></span>}
      </div>
      <div className={`chat-popup ${isPopupOpen ? 'open' : ''}`} ref={popupRef}>
        <div className="chat-header">
          <span>AskNimbus!</span>
          <button className="close-btn" onClick={toggleChatPopup}>
            <FontAwesomeIcon icon={faMinus} />
          </button>
        </div>
        <div className="chat-container">
          <div className="chat-box" ref={chatBoxRef}>
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`chat-message ${msg.isBot ? 'bot-message' : 'user-message'}`}
              >
                {msg.text}
              </div>
            ))}
            {isTyping && (
              <div className="chat-message bot-message typing-indicator">
                <span className="dot"></span>
                <span className="dot"></span>
                <span className="dot"></span>
              </div>
            )}
          </div>
          <div className="user-input-container">
            <input
              type="text"
              className="user-input"
              placeholder="Type your message..."
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              onKeyPress={handleKeyPress}
            />
            <button onClick={sendMessage} className="send-btn">
              <FontAwesomeIcon icon={faPaperPlane} />
            </button>
          </div>
        </div>
      </div>
    </>
  );
}

export default Chatbot;