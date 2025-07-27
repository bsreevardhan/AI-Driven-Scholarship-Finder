import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import './Dashboard.css';

const Dashboard = () => {
  const location = useLocation();
  const userData = location.state;

  const [scholarships, setScholarships] = useState([]);
  const [loading, setLoading] = useState(true);
  const [alert, setAlert] = useState(null); // 👈 Alert state

  useEffect(() => {
    if (!userData) {
      setLoading(false);
      setAlert('No form data found. Please submit the form first.'); // 👈 Set alert
      return;
    }

    const fetchScholarships = async () => {
      try {
        const response = await fetch('http://localhost:5000/submit-form', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(userData),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        console.log("Received response:", result);

        if (result.status === 'success' && Array.isArray(result.matched_scholarships)) {
          setScholarships(result.matched_scholarships.slice(0, 3));
          setAlert('Scholarships successfully fetched! 🎉'); // 👈 Success alert
        } else {
          setAlert('No scholarships matched your profile.');
        }
      } catch (err) {
        console.error("Error fetching scholarships:", err);
        setAlert('Failed to fetch scholarships. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchScholarships();
  }, [userData]);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="dashboard">
      {/* 🔔 Alert Box */}
      {alert && <div className="alert">{alert}</div>}

      <h2>Top 3 Scholarships For You!!!.....</h2>
      <ul>
        {scholarships.map((scholarship) => (
          <li key={scholarship.ID} className="scholarship-item">
            <p><span className="label">ID:</span><span className="detail">{scholarship.ID}</span></p>
            <p><span className="label">Name:</span><span className="detail">{scholarship.Name}</span></p>
            <p><span className="label">State:</span><span className="detail">{scholarship.State}</span></p>
            <p><span className="label">Award Amount:</span><span className="detail">{scholarship['Award Amount']}</span></p>
            <p><span className="label">Duration:</span><span className="detail">{scholarship.Duration}</span></p>
            <p><span className="label">Application Deadline:</span><span className="detail">{scholarship['Application Deadline']}</span></p>
            <p>
              <span className="label">Registration Link:</span>
              <a href={scholarship['Registration Link']} className="detail" target="_blank" rel="noopener noreferrer">
                {scholarship['Registration Link']}
              </a>
            </p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Dashboard;
