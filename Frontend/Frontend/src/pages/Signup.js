import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Signup.css';

const Signup = () => {
  const [form, setForm] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });

  const navigate = useNavigate();

  // Handle input changes
  const handleChange = (e) => {
    setForm({ ...form, [e.target.id]: e.target.value });
  };

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();

    if (form.password !== form.confirmPassword) {
      alert('Passwords do not match!');
      return;
    }

    // Send data to Flask backend
    fetch('http://localhost:5000/signup', {  // Update URL to match backend port (5000)
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(form)  // Send form data as JSON
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === 'success') {
          alert('Signup successful!');
          navigate('/login');  // Redirect to login page
        } else {
          alert(data.message);  // Show error message
        }
      })
      .catch((error) => {
        console.error('Error:', error);
        alert('An error occurred while signing up!');
      });
  };

  return (
    <div className="signup-background">
      <div className="signup-overlay">
        <form onSubmit={handleSubmit} className="signup-box">
          <h2>Sign Up</h2>

          <input
            type="text"
            id="name"
            value={form.name}
            onChange={handleChange}
            placeholder="Enter your full name"
            required
          />

          <input
            type="email"
            id="email"
            value={form.email}
            onChange={handleChange}
            placeholder="Enter your email address"
            required
          />

          <input
            type="password"
            id="password"
            value={form.password}
            onChange={handleChange}
            placeholder="Enter a password"
            required
          />

          <input
            type="password"
            id="confirmPassword"
            value={form.confirmPassword}
            onChange={handleChange}
            placeholder="Confirm your password"
            required
          />

          <button type="submit">Sign Up</button>

          <p>Already have an account? <a href="/login">Login</a></p>
        </form>
      </div>
    </div>
  );
};

export default Signup;
