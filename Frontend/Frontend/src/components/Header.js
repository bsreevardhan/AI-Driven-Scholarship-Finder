// src/components/Header.js
import React from 'react';
import './Header.css';
import logo from '../assets/logo.png'; // Ensure this path is correct

const Header = () => {
  return (
    <header className="header">
      {/* Logo and Title Section */}
      <div className="logo-container">
        <img src={logo} alt="Logo" className="logo" />
        <h1 className="title">🎓Scholarship Finder</h1>
      </div>

      {/* Search and Navbar Section */}
      <div className="navbar-search-container">
        {/* Search Bar */}
        <form className="search-form">
          <input
            type="text"
            placeholder="🔍 Search..."
            className="search-input"
          />
        </form>

        {/* Navigation Links */}
        <nav className="navbar">
          <ul>
          <li><a href="/">Home</a></li>
            <li><a href="/about">About Us</a></li>
            <li><a href="/login">Login</a></li>
            <li><a href="/signup">Signup</a></li>
            <li><a href="/dashboard">Dashboard</a></li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;
