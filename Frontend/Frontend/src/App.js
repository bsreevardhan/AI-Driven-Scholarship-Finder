// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/Home';
import About from './pages/About';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Dashboard from './pages/Dashboard';
import UserForm from './pages/UserForm';
import Results from './pages/Results';
import Chatbot from './pages/Chatbot'; // Import your chatbot
import './App.css';

const App = () => {
    return (
        <Router>
            <div className="app">
                <Header />
                <div className="content">
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/about" element={<About />} />
                        <Route path="/login" element={<Login />} />
                        <Route path="/signup" element={<Signup />} />
                        <Route path="/dashboard" element={<Dashboard />} />
                        <Route path="/userform" element={<UserForm />} />
                        <Route path="/results" element={<Results />} />
                    </Routes>
                </div>
                <Footer />

                {/* 👇 Chatbot visible on all pages */}
                <Chatbot />
            </div>
        </Router>
    );
};

export default App;
