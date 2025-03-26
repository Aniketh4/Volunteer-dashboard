import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from supabase import create_client

# Supabase Credentials
SUPABASE_URL = "https://nstgxvfpostirynqhqhl.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5zdGd4dmZwb3N0aXJ5bnFocWhsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDI1NzgyNTAsImV4cCI6MjA1ODE1NDI1MH0.ygNv7-9SKWOpfFXHo2oNHgS0nw5FYdBavR7S6NovZFo"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Email Credentials
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "saanvi.22210135@viit.ac.in"
EMAIL_PASSWORD = "zomn ccws nrxl zgrb"  # Use environment variables instead for security

def get_volunteers():
    """Fetch all registered volunteers' emails from Supabase"""
    response = supabase.table("volunteers").select("email").execute()
    return [v["email"] for v in response.data if "email" in v]

def get_unsent_published_events():
    """Fetch all events where email_sent is False and status is 'Published'"""
    response = supabase.table("events").select("id, title, location, start_date, end_date, registration_deadline").eq("status", "published").eq("email_sent", False).execute()
    return response.data

def send_email(to_email, event_title, location, start_date, end_date, deadline):
    """Send an email notification about an event to a volunteer"""
    subject = f"📢 Upcoming Event: {event_title} - Join Us for an Exciting Event!"

    # HTML Email Content
    email_html = f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            padding: 20px;
        }}
        .container {{
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            max-width: 600px;
            margin: auto;
        }}
        h2 {{
            color: #007bff;
        }}
        .details {{
            padding: 10px;
            border-left: 4px solid #007bff;
            background: #f9f9f9;
            margin: 20px 0;
        }}
        .details p {{
            margin: 5px 0;
        }}
        .register-button {{
            display: inline-block;
            background-color: #ff0000;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            font-size: 14px;
            font-weight: bold;
        }}
        .highlight {{
            color: #2c3e50;
            font-weight: bold;
        }}
    </style>
</head>
<body>

<div class="container">
    <h2>🚀 {event_title} 🚀</h2>
    
    <p>Dear Volunteer,</p>
    <p>We are excited to invite you to our upcoming event:</p>

    <div class="details">
        <p>📍 <strong>Location:</strong> {location}</p>
        <p>📅 <strong>Start Date:</strong> {start_date}</p>
        <p>🏁 <strong>End Date:</strong> {end_date}</p>
        <p>⏳ <strong style="color: red;">Registration Deadline:</strong> {deadline}</p>
    </div>

    <p class="highlight" style="color: #007bff;">Don't miss out! Register now!</p>

    <a href="#" class="register-button" style="color: #FFFFFF;">Register Now</a>

    <p>Best Regards,<br><strong>Samarthanam Team</strong></p>
</div>

</body>
</html>
"""

   

    # Email Setup
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(email_html, "html"))

    # Send Email
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        print(f"✅ Email sent to {to_email} for event '{event_title}'")
        return True
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")
        return False

def notify_volunteers():
    """Send email notifications for all unpublished events and update their status"""
    volunteers = get_volunteers()
    events = get_unsent_published_events()

    if not events:
        print("⚠️ No unpublished events found.")
        return

    for event in events:
        event_id = event["id"]
        event_title = event["title"]
        location = event["location"]
        start_date = event["start_date"]
        end_date = event["end_date"]
        deadline = event["registration_deadline"]

        emails_sent = 0
        for email in volunteers:
            if send_email(email, event_title, location, start_date, end_date, deadline):
                emails_sent += 1

        if emails_sent > 0:
            # Update the event status to mark emails as sent
            supabase.table("events").update({"email_sent": True}).eq("id", event_id).execute()
            print(f"✅ Updated event {event_id}: Emails marked as sent")

# Run the script
if __name__ == "__main__":
    notify_volunteers()
