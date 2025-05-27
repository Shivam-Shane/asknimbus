// src/ChatbotContext.js
import { createContext, useContext, useState } from 'react';

const ChatbotContext = createContext();

export const ChatbotProvider = ({ children }) => {
  const [isPopupOpen, setPopupOpen] = useState(false);

  const toggleChatPopup = () => {
    setPopupOpen((prev) => !prev);
  };

  const openChatPopup = () => {
    setPopupOpen(true);
  };

  return (
    <ChatbotContext.Provider value={{ isPopupOpen, toggleChatPopup, openChatPopup }}>
      {children}
    </ChatbotContext.Provider>
  );
};

export const useChatbot = () => useContext(ChatbotContext);