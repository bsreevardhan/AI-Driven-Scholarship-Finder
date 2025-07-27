import React, { useState } from 'react';
import './Chatbot.css';
import chatIcon from '../assets/chatbot-icon.png'; // ✅ use your image path correctly

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [userMessage, setUserMessage] = useState('');
  const [chatMessages, setChatMessages] = useState([]);

  const handleSendMessage = async () => {
    if (!userMessage.trim()) return;

    // Append user message
    const updatedMessages = [...chatMessages, { sender: 'user', text: userMessage }];
    setChatMessages(updatedMessages);
    const messageToSend = userMessage;
    setUserMessage('');

    try {
      // Fetch from Python backend
      const response = await fetch('http://localhost:5000/chatbot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: messageToSend })
      });

      const data = await response.json();
      setChatMessages(prev => [...prev, { sender: 'bot', text: data.reply || 'No reply from bot.' }]);
    } catch (error) {
      console.error('Error fetching bot reply:', error);
      setChatMessages(prev => [...prev, { sender: 'bot', text: 'Sorry, could not reach the server.' }]);
    }
  };

  // Handle Enter key
  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  return (
    <div>
      {/* Chat icon in bottom-right corner */}
      <img
        src={chatIcon}
        alt="Chat Icon"
        className="chatbot-icon"
        onClick={() => setIsOpen(prev => !prev)}
      />

      {/* Chatbot Window */}
      {isOpen && (
        <div className="chatbot-window">
          <div className="chat-header">
            <h3>Scholarship Chatbot</h3>
            <button className="close-btn" onClick={() => setIsOpen(false)}>×</button>
          </div>

          <div className="chat-body">
            {chatMessages.map((msg, i) => (
              <div key={i} className={`message ${msg.sender}`}>
                <p>{msg.text}</p>
              </div>
            ))}
          </div>

          <div className="chat-input">
            <input
              type="text"
              placeholder="Ask something..."
              value={userMessage}
              onChange={(e) => setUserMessage(e.target.value)}
              onKeyDown={handleKeyDown}
            />
            <button onClick={handleSendMessage}>Send</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Chatbot;
