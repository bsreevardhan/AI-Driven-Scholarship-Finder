import React from 'react';
import './About.css';
import Image1 from '../assets/Image8.avif'; 
import ChatbotIcon from '../assets/chatbot-icon.png'; // ✅ Import chatbot icon

const AboutUs = () => {
  return (
    <div className="about-us-container">
      <div className="about-us-content">
        <h1>About Us</h1>

        <section className="mission">
          <h2>Our Mission</h2>
          <p>
            At <strong>Scholarship Finder</strong>, we are dedicated to making education accessible to everyone by connecting students with the right scholarships. We aim to provide a platform where students can easily search and find scholarships that match their qualifications and aspirations.
          </p>
        </section>

        <section className="what-we-do">
          <h2>What We Do</h2>
          <ul>
            <li>Find scholarships based on eligibility criteria.</li>
            <li>Get personalized recommendations to maximize scholarship opportunities.</li>
            <li>Stay updated with the latest scholarship news and deadlines.</li>
          </ul>
          <p>
            Our goal is to simplify the scholarship search process, ensuring that students of all backgrounds and fields of study have equal access to the financial resources they need to pursue their dreams.
          </p>
        </section>

        <section className="why-choose-us">
          <h2>Why Choose Us?</h2>
          <ul>
            <li><strong>Comprehensive Database:</strong> We provide a wide range of scholarships, including local, national, and international options.</li>
            <li><strong>Tailored Suggestions:</strong> Based on your profile, we suggest scholarships you’re most likely to qualify for.</li>
            <li><strong>Easy-to-Use:</strong> With our intuitive interface, you can quickly find and apply for scholarships with ease.</li>
            <li><strong>Reliable Information:</strong> We regularly update our listings to ensure you get the most accurate and current information.</li>
          </ul>
        </section>

        <section className="vision">
          <h2>Our Vision</h2>
          <p>
            Our vision is to become the leading platform that bridges the gap between students and the financial support they need. We believe that every student should have the opportunity to pursue higher education, regardless of their financial background.
          </p>
        </section>

        <section className="contact-us">
          <h2>Contact Us</h2>
          <p>Have questions? We’d love to hear from you!</p>
          <p>Email: <a href="mailto:support@scholarshipfinder.com">support@scholarshipfinder.com</a></p>
          <p>Phone: 1-800-123-4567</p>
          <div className="social-media">
            <p>Follow us on social media:</p>
            <p>
              Facebook: <a href="https://www.facebook.com/ScholarshipFinder" target="_blank" rel="noopener noreferrer">Scholarship Finder</a><br />
              Twitter: <a href="https://twitter.com/ScholarshipFinder" target="_blank" rel="noopener noreferrer">@ScholarshipFinder</a><br />
              Instagram: <a href="https://www.instagram.com/ScholarshipFinder" target="_blank" rel="noopener noreferrer">@ScholarshipFinder</a>
            </p>
          </div>
        </section>
      </div>

      <div className="about-us-image">
        <img src={Image1} alt="About Us" />
      </div>

      {/* ✅ Chatbot Icon */}
      <img src={ChatbotIcon} alt="Chatbot" className="chatbot-icon" />
    </div>
  );
}

export default AboutUs;
