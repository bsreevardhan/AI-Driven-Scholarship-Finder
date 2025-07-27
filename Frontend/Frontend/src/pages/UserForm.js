import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Select from 'react-select';
import './UserForm.css';

const stateOptions = [
  { value: 'Andhra Pradesh', label: 'Andhra Pradesh' },
  { value: 'Arunachal Pradesh', label: 'Arunachal Pradesh' },
  { value: 'Assam', label: 'Assam' },
  { value: 'Bihar', label: 'Bihar' },
  { value: 'Chhattisgarh', label: 'Chhattisgarh' },
  { value: 'Goa', label: 'Goa' },
  { value: 'Gujarat', label: 'Gujarat' },
  { value: 'Haryana', label: 'Haryana' },
  { value: 'Himachal Pradesh', label: 'Himachal Pradesh' },
  { value: 'Jharkhand', label: 'Jharkhand' },
  { value: 'Karnataka', label: 'Karnataka' },
  { value: 'Kerala', label: 'Kerala' },
  { value: 'Madhya Pradesh', label: 'Madhya Pradesh' },
  { value: 'Maharashtra', label: 'Maharashtra' },
  { value: 'Manipur', label: 'Manipur' },
  { value: 'Meghalaya', label: 'Meghalaya' },
  { value: 'Mizoram', label: 'Mizoram' },
  { value: 'Nagaland', label: 'Nagaland' },
  { value: 'Odisha', label: 'Odisha' },
  { value: 'Punjab', label: 'Punjab' },
  { value: 'Rajasthan', label: 'Rajasthan' },
  { value: 'Sikkim', label: 'Sikkim' },
  { value: 'Tamil Nadu', label: 'Tamil Nadu' },
  { value: 'Telangana', label: 'Telangana' },
  { value: 'Tripura', label: 'Tripura' },
  { value: 'Uttar Pradesh', label: 'Uttar Pradesh' },
  { value: 'Uttarakhand', label: 'Uttarakhand' },
  { value: 'West Bengal', label: 'West Bengal' },
  { value: 'Other', label: 'Other' },
];

const customStyles = {
  control: (provided) => ({
    ...provided,
    backgroundColor: 'transparent',
    borderColor: '#bb86fc',
    color: '#fff',
    fontSize: '16px',
  }),
  singleValue: (provided) => ({
    ...provided,
    color: '#fff',
  }),
  menu: (provided) => ({
    ...provided,
    backgroundColor: '#000',
  }),
  option: (provided, state) => ({
    ...provided,
    backgroundColor: state.isFocused ? '#8e2de2' : '#000',
    color: '#fff',
    cursor: 'pointer',
  }),
  placeholder: (provided) => ({
    ...provided,
    color: '#ccc',
  }),
  input: (provided) => ({
    ...provided,
    color: '#fff',
  }),
};

const UserForm = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    Name: '',
    Email: '',
    Age: '',
    Gender: '',
    Income: 0,
    State: '',
    CGPA: '',
    tenth_Percent: '',
    twelveth_Percent: '',
    Category: '',
    Religion: '',
    Special_Criteria: [],
    scholarship_type_preference: '',
    Qualification: '',
    current_program: '',
    current_year_of_study: 0,
    criteria: [], // Initialize criteria as an empty array
  });

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
      Username: name === 'Name' ? value : prevData.Username, // auto-set Username = Name
    }));
  };

  const handleStateChange = (selectedOption) => {
    setFormData({ ...formData, State: selectedOption ? selectedOption.value : '' }); // Fix key to match 'State'
  };

  const handleReligionChange = (e) => {
    const updatedReligion = e.target.value;
    const minorityReligions = ['Muslim', 'Christian', 'Sikh', 'Buddhist', 'Jain', 'Parsi'];

    setFormData((prevData) => {
      const isMinority = minorityReligions.includes(updatedReligion);
      const updatedCriteria = isMinority
        ? prevData.criteria.includes('Minority Community')
          ? prevData.criteria
          : [...prevData.criteria, 'Minority Community']
        : prevData.criteria.filter((item) => item !== 'Minority Community');

      return {
        ...prevData,
        Religion: updatedReligion, // Fix key to match formData
        criteria: updatedCriteria,
      };
    });
  };

  const handleSpecialCriteriaChange = (e) => {
    const { value, checked } = e.target;
    setFormData((prevData) => {
      const updatedSpecialCriteria = checked
        ? [...prevData.Special_Criteria, value]
        : prevData.Special_Criteria.filter((item) => item !== value);

      return {
        ...prevData,
        Special_Criteria: updatedSpecialCriteria,
      };
    });
  };

  const handleSubmit = async (e) => {
  e.preventDefault();
  try {
    const response = await fetch('http://localhost:5000/submit-form', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    });

    const result = await response.json();

    if (result.status === 'success') {
      alert('Form submitted successfully!an email has been sent to you');
      navigate('/dashboard', { state: formData });
    } else {
      alert('Error: ' + result.message);
    }
  } catch (error) {
    console.error('Submission error:', error);
    alert('An error occurred while submitting the form.');
  }
};
  return (
    <div className="form-background">
      <div className="form-overlay">
        <div className="form-box">
          <h2>Check Your Scholarship Eligibility</h2>
          <form onSubmit={handleSubmit}>
            <label>Name:</label>
            <input type="text" name="Name" value={formData.Name} onChange={handleChange} required />

            <label>Email:</label>
            <input type="Email" name="Email" value={formData.Email} onChange={handleChange} required />

            <label>Age:</label>
            <input type="number" name="Age" value={formData.Age} onChange={handleChange} min="10" max="30" required />

            <label>Gender:</label>
            <select name="Gender" value={formData.Gender} onChange={handleChange} required>
              <option value="">Select</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
            </select>

            <label>Annual Income:</label>
            <input type="number" name="Income" value={formData.Income} onChange={handleChange} min="0" max="1000000" required />

            <label>State:</label>
            <Select
              options={stateOptions}
              onChange={handleStateChange}
              value={stateOptions.find((option) => option.value === formData.State)} // Ensure it matches 'State'
              placeholder="Enter your state"
              isSearchable
              styles={customStyles}
            />

            <label>Current Education Level:</label>
            <select
              name="Qualification"
              value={formData.Qualification}
              onChange={handleChange}
              required
            >
              <option value="">Select</option>
              <option>High School</option>
              <option>UG</option>
              <option>PG</option>
              <option>Doctorate</option>
              <option>Diploma</option>
              <option>Associate Degree</option>
            </select>

            <label>Current Programming:</label>
            <input
              type="text"
              name="current_program"
              value={formData.current_program}
              onChange={handleChange}
              required
            />

            <label>Current Year of Study:</label>
            <input
              type="text"
              name="current_year_of_study"
              value={formData.current_year_of_study}
              onChange={handleChange}
              required
            />

            <label>CGPA:</label>
            <input type="number" name="CGPA" value={formData.CGPA} step="0.01" onChange={handleChange} />

            <label>10th Percentage:</label>
            <input type="number" name="tenth_Percent" value={formData.tenth_Percent} step="0.01" onChange={handleChange} required />

            <label>12th Percentage:</label>
            <input type="number" name="twelveth_Percent" value={formData.twelveth_Percent} step="0.01" onChange={handleChange} required />

            <label>Category:</label>
            <select name="Category" value={formData.Category} onChange={handleChange} required>
              <option value="">Select</option>
              <option>General</option>
              <option>OBC</option>
              <option>SC</option>
              <option>ST</option>
              <option>EWS</option>
              <option>Minority</option>
            </select>

            <label>Religion:</label>
            <select name="Religion" value={formData.Religion} onChange={handleReligionChange} required>
              <option value="">Select</option>
              <option value="Hindu">Hindu</option>
              <option value="Muslim">Muslim</option>
              <option value="Christian">Christian</option>
              <option value="Sikh">Sikh</option>
              <option value="Buddhist">Buddhist</option>
              <option value="Jain">Jain</option>
              <option value="Parsi">Parsi</option>
              <option value="Other">Other</option>
            </select>

            <label>Special Criteria:</label>
            <div>
              {['Armed Force Family', 'First Graduate', 'Female Student', 'Minority Community', 'Physically challenged'].map((option) => (
                <label key={option}>
                  <input
                    type="checkbox"
                    value={option}
                    checked={formData.Special_Criteria.includes(option)}
                    onChange={handleSpecialCriteriaChange}
                  />
                  {option}
                </label>
              ))}
            </div>

            <button type="submit">Recommended Scholarships</button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default UserForm;
