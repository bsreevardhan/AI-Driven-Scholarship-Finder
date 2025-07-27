import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

def send_html_email(to_email, username, scholarships):
    from_email = 'bsvminiproject@gmail.com'
    from_password = 'Sree@7848'  # <-- Use your Gmail app password here

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

    # Full HTML content
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

    # Set up email message
    message = MIMEMultipart('alternative')
    message['Subject'] = "Your Top 3 Scholarship Recommendations"
    message['From'] = from_email
    message['To'] = to_email
    message.attach(MIMEText(html_content, 'html'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, from_password)
            server.send_message(message)
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

# ======== USAGE EXAMPLE ========

if __name__ == "__main__":
    scholarships = [
        {'name': 'Scholarship A', 'link': 'https://example.com/a'},
        {'name': 'Scholarship B', 'link': 'https://example.com/b'},
        {'name': 'Scholarship C', 'link': 'https://example.com/c'}
    ]

    send_html_email(
        to_email='2022IT0492@svce.ac.in',  # <-- Put the user’s email here
        username='Sree',               # <-- User’s name
        scholarships=scholarships
    )
