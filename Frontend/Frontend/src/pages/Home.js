import React, { useState } from 'react';
import './Home.css';
import Image2 from '../assets/Image7.avif';
import chatbotIcon from '../assets/chatbot-icon.png';

const Home = () => {
  const [showChat, setShowChat] = useState(false);

  const toggleChat = () => {
    setShowChat(!showChat);
  };

  return (
    <div className="home-container">
      <div className="text-section">
        <h1>🎓 Welcome to Scholarship Finder</h1>
        <h2>Discover the right scholarship, effortlessly.</h2>
       
        <h3>🔍 What We Offer:</h3>
        <ul>
          <li>✅ Smart scholarship matching based on your academic and personal details</li>
          <li>✅ Access to national, state, and private scholarship opportunities</li>
          <li>✅ Easy-to-use platform — just fill a form and get recommendations</li>
          <li>✅ Designed for school students, graduates, and postgraduates</li>
        </ul>

        <p>
          Navigating scholarships can be overwhelming — but we make it simple. At Scholarship Finder, we connect students with the most suitable scholarships based on their profile, qualifications, and goals.
        </p>
        <p>💡 Let us help you fund your future — because every dream deserves a chance.</p>
      </div>

      <div className="image-section">
        <img src={Image2} alt="Scholarship Visual" className="main-image" />
        <img
          src={chatbotIcon}
          alt="Chatbot"
          className="chatbot-icon"
          onClick={toggleChat}
        />
        {showChat && (
          <div className="chatbox">
            <h4>Ask me anything!</h4>
            <p>🤖 Hi! How can I help you today?</p>
            {/* You can replace this with real chat later */}
          </div>
        )}
      </div>
    </div>
  );
};

export default Home;
