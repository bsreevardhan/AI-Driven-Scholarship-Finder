from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import pandas as pd
import os
from eligibility import is_eligible, match_and_rank_scholarships, send_brevo_email
from chatbot import chatbot
app = Flask(__name__)
CORS(app)

# Load CSV once globally
scholarship_data = pd.read_csv('scholarships.csv')

# ----------------- Database Connection -----------------
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='priya',
        database='miniproject'
    )

# ----------------- Signup -----------------
@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        name = data['name']
        email = data['email']
        password = data['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            return jsonify({'status': 'error', 'message': 'User already exists'})

        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# ----------------- Login -----------------
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Invalid credentials'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    
@app.route('/submit-form', methods=['POST', 'OPTIONS'])
def submit_form():
    if request.method == 'OPTIONS':
        # Handle the preflight request
        return jsonify({'status': 'ok'}), 200

    try:
        data = request.get_json()
        if not data:
            print("No JSON received.")
            return jsonify({'status': 'error', 'message': 'No JSON received'}), 400

        print("Received user data:", data)
        top_scholarships = match_and_rank_scholarships(data)
        print("top scholarship1:", top_scholarships)
        return jsonify({'status': 'success', 'matched_scholarships': top_scholarships})

    except Exception as e:
        print("Exception occurred:", str(e))
        return jsonify({'status': 'error', 'message': str(e)}), 500
# ----------------- Chatbot -----------------
# Chatbot API endpoint
@app.route('/chatbot', methods=['POST'])
def chatbot_api():
    try:
        data = request.get_json()
        user_query = data.get('message', '')
        response = chatbot(user_query)
        return jsonify({'reply': response})
    except Exception as e:
        return jsonify({'reply': 'Sorry, something went wrong on the server.'}), 500


# Load your scholarships
scholarships = pd.read_csv('scholarships.csv')
scholarships.columns = scholarships.columns.str.strip()

def match_and_rank_scholarships(user_data, scholarship_file='scholarships.csv'):
    try:
        df = pd.read_csv(scholarship_file)
        df.columns = df.columns.str.strip()

        def check_eligibility(row):
            eligible = is_eligible(user_data, row.to_dict())
            print(f"Checking scholarship '{row['Name']}' eligibility: {eligible}")
            return eligible

        eligible_scholarships = df[df.apply(check_eligibility, axis=1)]

        if 'Award_Amount' in eligible_scholarships.columns:
            eligible_scholarships['Award_Amount'] = pd.to_numeric(
                eligible_scholarships['Award_Amount'], errors='coerce'
            )
            eligible_scholarships = eligible_scholarships.sort_values(by='Award_Amount', ascending=False)

        top_5 = eligible_scholarships.head(5).to_dict(orient='records')
        print(f"Top scholarships: {top_5}")
        return top_5

    except Exception as e:
        print(f"Error in match_and_rank: {str(e)}")
        return []



if __name__ == 'main':
    app.run(debug=True)