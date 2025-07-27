import pandas as pd
import re
import uuid
import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime
from sentence_transformers import SentenceTransformer, util
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import pytz

# --- Qualification Normalizer ---
def normalize_qualification(text):
    text = str(text).lower().strip()
    if any(f"class {i}" in text for i in range(1, 11)) or "school" in text:
        return 'School'
    if any(x in text for x in ["class 11", "class 12", "hsc", "12th", "plus two", "intermediate"]):
        return '12th'
    if any(x in text for x in ["undergraduate", "ug", "bachelor", "graduation", "stem ug", "degree", "professional"]):
        return 'Undergraduate'
    if any(x in text for x in ["postgraduate", "pg", "masters", "post-graduation"]):
        return 'Postgraduate'
    if any(x in text for x in ["phd", "doctoral", "postdoc"]):
        return 'PhD'
    if any(x in text for x in ["post-matric", "post matric"]):
        return 'Post-Matric'
    if any(x in text for x in ["all levels", "all"]):
        return 'All'
    if any(x in text for x in ["diploma", "polytechnic"]):
        return 'Diploma'
    return 'Unknown'

# --- Income Parser ---
def parse_income(income_str):
    if pd.isna(income_str) or str(income_str).lower().strip() in ["no income limit", "not specified", "na"]:
        return float('inf')
    income_str = str(income_str).lower().replace('inr ', '').replace(',', '').replace('below ', '').replace('up to ', '').strip()
    if 'lakh' in income_str or 'lakhs' in income_str:
        income_str = income_str.replace('lakhs', '').replace('lakh', '').replace('<', '').strip()
        try:
            return float(income_str) * 100000
        except ValueError:
            return float('inf')
    match = re.search(r'\d+(\.\d+)?', income_str)
    if match:
        try:
            return float(match.group())
        except ValueError:
            return float('inf')
    return float('inf')

# --- Minimum Qualification Parser ---
def parse_min_qualification(qual):
    if pd.isna(qual) or str(qual).lower().strip() in ["not specified", ""]:
        return None
    qual = str(qual).lower().strip()
    match = re.search(r"(\d+(\.\d+)?)%\s*in\s*(class\s*(10|12|7)|last\s*qualifying\s*exam)", qual)
    if match:
        return {
            "percentage": float(match.group(1)),
            "level": "12th" if "12" in match.group(3) else "10th" if "10" in match.group(3) else "7th" if "7" in match.group(3) else "last"
        }
    if "1% in 12th" in qual:
        return {"percentage": 99.0, "level": "12th"}
    if "20% in class 12" in qual:
        return {"percentage": 80.0, "level": "12th"}
    return None

def to_scalar(val):
    if isinstance(val, (list, tuple, pd.Series)):
        return val.iloc[0] if len(val) > 0 else ''
    return val

# --- Special Criteria Matcher ---
def match_special_criteria(user_special, user_category, user_gender, sch_special, sch_category):
    user_special = str(user_special).lower().strip() if user_special else ""
    user_category = str(user_category).lower().strip() if user_category else ""
    user_gender = str(user_gender).lower().strip() if user_gender else ""
    sch_special = str(sch_special).lower().strip() if sch_special else "not specified"
    sch_category = str(sch_category).lower().strip() if sch_category else ""

    user_special_list = [s.strip() for s in user_special.split(",") if s.strip()]
    sch_special_list = [s.strip() for s in sch_special.split("/") if s.strip()]

    if sch_special in ["not specified", ""] or "all" in sch_category:
        return True

    matched = False
    for sch_criterion in sch_special_list:
        if "female category" in sch_criterion:
            if user_gender == "female":
                matched = True
        elif "sc/st category" in sch_criterion:
            if user_category in ["sc", "st"]:
                matched = True
        elif "obc category" in sch_criterion:
            if user_category == "obc":
                matched = True
        elif "minority category" in sch_criterion:
            if user_category == "minority" or "minority community" in user_special_list:
                matched = True
        elif "differently abled category" in sch_criterion:
            if "physically challenged" in user_special_list:
                matched = True
        elif "first graduate" in sch_criterion:
            if "first graduate" in user_special_list:
                matched = True
        elif any(uspec in sch_criterion for uspec in user_special_list):
            matched = True
    return matched

# --- Eligibility Check ---
def is_eligible(user, scholarship):
    try:
        user_state = str(user.get('State', '')).lower()
        sch_state = str(scholarship.get('State', '')).lower()
        if not any([sch_state == 'all india', user_state == sch_state]):
            return False
        
        scholarship_categories = set([c.strip().lower() for c in str(scholarship.get('Category', '')).split('/')])
        user_category = str(user.get('Category', '')).lower().strip()

        if not any(cat in scholarship_categories for cat in ['all', 'all categories']):
            if not any(user_category == cat or cat == 'general' for cat in scholarship_categories):
                return False
        
        user_income = float(user.get('Income', 0))
        scholarship_income = parse_income(scholarship.get('Income Eligibility'))
        if user_income > scholarship_income:
            return False

        qualification_order = {
            'school': 1, '12th': 2, 'post-matric': 2, 'diploma': 2.5,
            'undergraduate': 3, 'postgraduate': 4, 'phd': 5, 'all': 0, 'unknown': 0
        }
        user_qual = normalize_qualification(user.get('Qualification', '')).lower()
        sch_qual = normalize_qualification(scholarship.get('Qualification', '')).lower()
        user_qual_level = qualification_order.get(user_qual, 0)
        sch_qual_level = qualification_order.get(sch_qual, 0)

        if sch_qual_level != 0 and user_qual_level == 0:
            return False
        if sch_qual_level != 0 and user_qual_level < sch_qual_level:
            return False

        sch_qual_raw = str(scholarship.get('Qualification', '')).lower()
        if "1st-year ug" in sch_qual_raw or "1st-year ug (tech)" in sch_qual_raw:
            if str(user.get('Current Year of Study', '')).lower() != "1st year":
                return False

        if sch_qual == 'unknown':
            for program in ['engineering', 'pharmacy', 'agriculture']:
                if program in sch_qual_raw and program not in str(user.get('Current Program', '')).lower():
                    return False

        if not match_special_criteria(
            user.get('Special_Criteria', ''),
            user.get('Category', ''),
            user.get('Gender', ''),
            scholarship.get('Special Criteria', ''),
            scholarship.get('Category', '')
        ):
            return False

        min_qual = parse_min_qualification(scholarship.get('Minimum Qualification'))
        if min_qual:
            if min_qual["level"] == "12th":
                if float(user.get('12th_Percent', 0)) < min_qual["percentage"]:
                    return False
            elif min_qual["level"] == "10th":
                if float(user.get('10th_Percent', 0)) < min_qual["percentage"]:
                    return False
            elif min_qual["level"] == "7th":
                if float(user.get('10th_Percent', 0)) < min_qual["percentage"]:
                    return False
            elif min_qual["level"] == "last":
                cgpa_percent = float(user.get('CGPA', 0)) * 9.5 if user.get('CGPA') else 0
                max_percent = max(
                    float(user.get('10th_Percent', 0)),
                    float(user.get('12th_Percent', 0)),
                    cgpa_percent
                )
                if max_percent < min_qual["percentage"]:
                    return False

        return True
    except Exception as e:
        print("Eligibility check error:", e)
        return False

# --- Email Sender Function ---
def send_brevo_email(to_emails, username, scholarships):
    configuration = sib_api_v3_sdk.Configuration()
    
    configuration.api_key = os.getenv("SENDINBLUE_API_KEY")
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    india_tz = pytz.timezone('Asia/Kolkata')
    timestamp = datetime.now(india_tz).strftime('%Y-%m-%d %H:%M:%S IST')

    table_rows = ''
    for i, sch in enumerate(scholarships, start=1):
        table_rows += f"""
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd;">{i}</td>
            <td style="padding: 8px; border: 1px solid #ddd;">{sch['name']}</td>
            <td style="padding: 8px; border: 1px solid #ddd;"><a href="{sch['link']}">View</a></td>
        </tr>
        """

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <p>Hi {username},</p>
        <p>Your personalized top 3 scholarships are here:</p>
        <table style="border-collapse: collapse; width: 100%;">
            <thead>
                <tr style="background-color: #f2f2f2;">
                    <th style="padding: 8px; border: 1px solid #ddd;">No.</th>
                    <th style="padding: 8px; border: 1px solid #ddd;">Scholarship Name</th>
                    <th style="padding: 8px; border: 1px solid #ddd;">Link</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
        <p style="margin-top: 20px;">Timestamp: {timestamp}</p>
        <p>Thank you!</p>
    </body>
    </html>
    """

    # Ensure to_emails is a list
    if isinstance(to_emails, str):
        to_emails = [to_emails]
    to_list = [{"email": email} for email in to_emails if email]

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to_list,
        sender={"email": "bsvminiproject@gmail.com", "name": "Scholarship Bot"},
        subject="Your Top 3 Scholarship Recommendations",
        html_content=html_content
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(f"✅ Email sent to {to_emails}! Response: {api_response}")
        return True
    except ApiException as e:
        print(f"❌ Error sending email to {to_emails}: {e}")
        return False

# --- Create User and Scholarship Text ---
def create_user_text(user):
    return f"{user.get('Qualification', '')} {user.get('Current Program', '')} {user.get('Special_Criteria', '')}"

def create_scholarship_text(scholarship):
    return f"{scholarship.get('Qualification', '')} {scholarship.get('Special Criteria', '')} {scholarship.get('Description', '')}"

# --- Main Matching and Ranking Logic ---
def match_and_rank_scholarships(user_data, scholarship_file):
    user = pd.Series(user_data)

    try:
        scholarships_df = pd.read_csv(scholarship_file)
    except FileNotFoundError:
        print(f"File not found: {scholarship_file}")
        return

    scholarships_df.columns = (
        scholarships_df.columns
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
        .str.encode('ascii', 'ignore')
        .str.decode('ascii')
    )

    scholarships_df = scholarships_df.drop_duplicates(subset=['Name'], keep='first')

    output_columns = [
        'ID', 'State', 'Name', 'Category', 'Income Eligibility', 'Qualification',
        'Special Criteria', 'Minimum Qualification', 'Description', 'Type',
        'Award Amount', 'Duration', 'Application Deadline', 'Registration Link'
    ]

    print(f"\n🔍 Matching for user: {user['Name']}")

    eligible = []
    for _, scholarship in scholarships_df.iterrows():
        if is_eligible(user, scholarship):
            eligible.append(scholarship)

    user_name = user['Name'].replace(' ', '_')
    output_filename = f"{user_name}_eligible_scholarships.csv"
    if eligible:
        eligible_df = pd.DataFrame(eligible)
        for col in output_columns:
            if col not in eligible_df.columns:
                eligible_df[col] = pd.NA
        eligible_df = eligible_df[output_columns]
        eligible_df.to_csv(output_filename, index=False)
        print(f"📁 Eligible scholarships saved to: {output_filename}")
    else:
        pd.DataFrame(columns=output_columns).to_csv(output_filename, index=False)
        print("❗ No eligible scholarships found.")
        return

    try:
        model = SentenceTransformer('all-MiniLM-L6-v2')
    except Exception as e:
        print(f"Model error: {e}")
        return

    user_text = create_user_text(user)
    scholarship_texts = eligible_df.apply(create_scholarship_text, axis=1).tolist()

    try:
        user_embedding = model.encode(user_text, convert_to_tensor=True)
        scholarship_embeddings = model.encode(scholarship_texts, convert_to_tensor=True)
        cosine_scores = util.cos_sim(user_embedding, scholarship_embeddings)[0]
    except Exception as e:
        print(f"Embedding error: {e}")
        return

    results = pd.DataFrame({
        'Scholarship_Name': eligible_df['Name'],
        'Similarity_Score': cosine_scores.cpu().numpy()
    })

    top_n = min(len(eligible), 3)
    top_scholarships = results.sort_values(by='Similarity_Score', ascending=False).head(top_n)

    top_3 = []
    for _, row in top_scholarships.iterrows():
        name = row['Scholarship_Name']
        matched = eligible_df[eligible_df['Name'] == name]
        if not matched.empty:
            top_3.append({
                'name': name,
                'link': matched.iloc[0]['Registration Link']
            })

    if top_3:
        email = user.get('Email', '2022it0492@svce.ac.in').strip()
        # Simple email validation
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(email):
            print(f"❌ Invalid email provided: {email}. Using default email.")
            email = '2022it0492@svce.ac.in'
        
        print(f"📧 Attempting to send email to: {email}")
        success = send_brevo_email(
            to_emails=[email],
            username=user['Name'],
            scholarships=top_3
        )
        
        if not success and email != '2022it0492@svce.ac.in':
            print(f"❌ Failed to send email to {email}. Trying default email: 2022it0492@svce.ac.in")
            send_brevo_email(
                to_emails=['2022it0492@svce.ac.in'],
                username=user['Name'],
                scholarships=top_3
            )
    else:
        print("❗ No top scholarships to send via email.")

# --- Get User Data ---
def get_user_data():
    print("Please enter your details:")
    user_data = {
        'Name': input("Name: "),
        'State': input("State: "),
        'Income': float(input("Annual Income: ")),
        'Qualification': input("Qualification (e.g., UG, PG): "),
        'Gender': input("Gender (M/F/Other): "),
        'Category': input("Category: "),
        'Special_Criteria': input("Special Criteria (e.g., Disabled, Gender-based, etc.): "),
        '10th_Percent': float(input("10th Percentage: ")),
        '12th_Percent': float(input("12th Percentage: ")),
        'CGPA': float(input("CGPA: ")),
        'Current Year of Study': input("Current Year of Study: "),
        'Current Program': input("Current Program: "),
        'Email': input("Email: ")
    }
    return user_data

# --- Run ---
if __name__ == "__main__":
    try:
        user_data = get_user_data()
        scholarship_file = 'scholarships.csv'
        match_and_rank_scholarships(user_data, scholarship_file)
    except Exception as e:
        print(f"Error: {str(e)}")