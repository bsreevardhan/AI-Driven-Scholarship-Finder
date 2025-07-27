# AI-Driven Scholarship Finder

## Overview  
AI-Driven Scholarship Finder is an intelligent hybrid recommendation platform that revolutionizes how students identify suitable scholarships. By combining **heuristic rule-based filtering** with **advanced AI-powered semantic matching**, it delivers highly accurate and personalized scholarship recommendations that go beyond traditional keyword searches. This system processes complex user profiles and diverse scholarship criteria to provide relevant matches, along with a Q&A chatbot and proactive email notifications to support user engagement and timely application.

## Table of Contents  
1. Introduction  
2. Key Features  
3. System Architecture  
4. Implementation Details  
5. Detailed Workflow

## 1. Introduction  
Finding the right scholarships is traditionally a tedious and imprecise effort, often hindered by static filtering and keyword matching. The AI-Driven Scholarship Finder solves these problems by:

- Applying **deterministic heuristic rules** for initial strict filtering based on eligibility (e.g., GPA thresholds, nationality, income bracket).  
- Leveraging **sentence transformer models** to embed both user queries and scholarship descriptions for contextual semantic matching, enabling relevance beyond exact keyword overlaps.  
- Enhancing the platform experience with **real-time chatbot assistance** and **deadline-driven email notifications** to empower students to take timely action.

## 2. Key Features  

- **Comprehensive User Profile Acquisition:** Collects detailed academic, financial, demographic, and special criteria data through intuitive forms to build rich user profiles.  

- **Robust Data Preprocessing & Structuring:** Automates cleaning and normalization of diverse scholarship listings, extracting eligibility criteria using regex and keyword-based logic.  

- **Heuristic Rule-Based Filtering Engine:** Implements strict, interpretable eligibility rules to eliminate scholarships that do not meet fundamental criteria.  

- **Semantic Matching & Ranking Module:** Generates dense, context-aware embeddings with a Sentence Transformer model and ranks scholarships by cosine similarity to user preferences for nuanced matching.  

- **AI-Powered Q&A Chatbot:** Provides instant, interactive assistance, answering user questions about scholarships, eligibility, and next steps.  

- **Automated Notification System:** Sends personalized email alerts highlighting the top three scholarship matches ahead of deadlines, improving users’ chances to apply on time.  

## 3. System Architecture  

The platform consists of modular components integrated into a seamless pipeline:

1. **Data Ingestion:** Crawls and scrapes scholarship data from multiple reliable web sources, ensuring up-to-date listings.  
2. **Preprocessing Pipeline:** Normalizes diverse eligibility fields such as income ranges and education levels, structuring unstructured data for effective filtering.  
3. **Filtering Engine:** Applies deterministic heuristics to exclude scholarships failing hard criteria filters.  
4. **Embedding & Semantic Ranking:** Encodes relevant texts into 768-dimensional vectors using Sentence-BERT and ranks by cosine similarity to user queries.  
5. **Recommendation & Notification:** Prepares personalized top scholarship recommendations and triggers email alerts.  
6. **Chatbot Interface:** Employs natural language understanding models for real-time interactive support.

<img width="617" height="384" alt="image" src="https://github.com/user-attachments/assets/dd3190e8-2c54-49f8-bdab-58440f00d3db" />


## 4. Implementation Details  

- **Languages & Frameworks:**  
  - Backend: Python 3.x with Flask API  
  - Frontend: React.js  
  - Database: PostgreSQL  

- **Core Libraries:**  
  - `sentence-transformers` for embedding generation using pretrained Sentence-BERT models  
  - NumPy for similarity computation  
  - Regex & pandas for data preprocessing  
  - Celery & SMTP for scheduled email notifications  
  - Rasa or similar NLP toolkit for chatbot development  

- **Deployment Considerations:** Environment variables secure credentials; database migration handled by Flask-Migrate.

## 6. Detailed Workflow

1. **User Registration & Profile Creation:**  
 Students sign up and fill out comprehensive forms capturing their academic qualifications, financial background, nationality, special circumstances, and scholarship preferences.

2. **Scholarship Data Collection & Preprocessing:**  
 The system automatically scrapes current scholarship listings from selected websites nightly. Raw data is cleansed, normalized, and eligibility criteria are extracted using regular expressions and keyword logic, structuring semi-structured texts into standardized actionable fields.

3. **Rule-Based Eligibility Filtering:**  
 Using deterministic heuristics, scholarships that do not meet *mandatory* eligibility rules (e.g., minimum GPA, specific nationality, income brackets) are excluded, drastically reducing the pool to only valid options.

4. **Semantic Embedding & Relevance Scoring:**  
 Descriptions of the remaining scholarships and user input queries are encoded into semantic vectors via a Sentence Transformer. The system computes cosine similarity scores, ranking scholarships to surface the most contextually aligned opportunities.

5. **Recommendation Presentation:**  
 The top-ranked scholarships are displayed to the user in an intuitive interface, along with detailed eligibility information.

6. **Real-Time Chatbot Assistance:**  
 Users can interact with the AI-powered chatbot to clarify doubts about eligibility, deadlines, application procedures, or request personalized guidance.

7. **Notification & Alerts:**  
 Ahead of scholarship deadlines, the system automatically sends personalized emails featuring the top three recommended scholarships, encouraging timely applications.

This hybrid system significantly improves scholarship recommendation accuracy by blending deterministic logic with AI-based semantic understanding, enhancing student access to equitable educational funding.

For more detailed technical insights, visit the `/docs` directory or explore the source code in `/src`.



