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
EMAIL_PASSWORD = "zomn ccws nrxl zgrb"

def get_volunteers():
    """Fetch all registered volunteers' emails from Supabase"""
    response = supabase.table("volunteers").select("email").execute()
    return [v["email"] for v in response.data if "email" in v]

def get_published_events(id):
    """Fetch all published events from Supabase"""
    response = supabase.table("events").select("title, location, status").eq("id", id).execute()
    return response.data  # List of events

def send_email(to_email, event_name, location):
    """Send an email notification about an event to a volunteer"""
    subject = f"📢 Upcoming Event: {event_name} 🚀"
    
    # HTML Email Content
    html_content = f"""
    <html>
    <body>
        <h2>📢 <span style="color: #007bff;">Upcoming Event: {event_name}</span> 🚀</h2>
        <p>Dear Volunteer,</p>
        <p>We are excited to invite you to our upcoming event:</p>
        
        <table border="1" cellspacing="0" cellpadding="5">
            <tr>
                <td>📍 <b>Location:</b></td>
                <td>{location}</td>
            </tr>
            <tr>
                <td>📅 <b>Status:</b></td>
                <td>Published</td>
            </tr>
        </table>


        <p>Looking forward to seeing you there!</p>

        <p>Best Regards,<br><b>Samarthanam Team</b></p>
    </body>
    </html>
    """

    # Email Setup
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_content, "html"))

    # Send Email
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        print(f"✅ Email sent to {to_email} for event '{event_name}'")
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")

def notify_volunteers(id):
    """Send email notifications for all published events to all volunteers"""
    volunteers = get_volunteers()
    events = get_published_events(id)

    if not events:
        print("⚠️ No published events found.")
        return

    for event in events:
        event_name = event["title"]
        location = event["location"]
        
        for email in volunteers:
            send_email(email, event_name, location)

# Run the script
if __name__ == "__main__":
    notify_volunteers(id)
