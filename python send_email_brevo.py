import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from datetime import datetime

def send_brevo_email(to_email, username, scholarships):
    configuration = sib_api_v3_sdk.Configuration()
    
    # 🟡 STEP 1 → Replace with your FULL Brevo API key
    configuration.api_key['api-key'] = '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'

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    # Current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Build HTML table rows
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
        <p>Hi, {username}</p>
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

    # 🟡 STEP 2 → Replace with your verified sender email
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": to_email}],
        sender={"email": "bsvminiproject@gmail.com", "name": "Scholarship Bot"},
        subject="Your Top 3 Scholarship Recommendations",
        html_content=html_content
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(f"✅ Email sent! Full response: {api_response}")
    except ApiException as e:
        print(f"❌ Error sending email: {e}")

# ======== USAGE EXAMPLE ========

if __name__ == "__main__":
    scholarships = [
        {'name': 'Scholarship A', 'link': 'https://example.com/a'},
        {'name': 'Scholarship B', 'link': 'https://example.com/b'},
        {'name': 'Scholarship C', 'link': 'https://example.com/c'}
    ]

    # 🟡 STEP 3 → Replace with the recipient’s email and name
    send_brevo_email(
        to_email='2022it0219@svce.ac.in',
        username='Priya',
        scholarships=scholarships
    )
