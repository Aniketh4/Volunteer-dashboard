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
    """Fetch all published events that have not had emails sent yet"""
    response = supabase.table("events").select("id, title, location, start_date, end_date, registration_deadline, email_sent").eq("status", "published").eq("email_sent", False).execute()
    return response.data  # List of events

def mark_email_sent(event_id):
    """Update event to mark that emails have been sent"""
    supabase.table("events").update({"email_sent": True}).eq("id", event_id).execute()

def send_email(to_email, event_title, location, start_date, end_date, registration_deadline):
    """Send an email notification about an event to a volunteer"""
    subject = f"📢 Upcoming Event: {event_title} 🚀"

    html_content = f"""
    <html>
    <body>
        <h2>📢 <span style="color: #007bff;">Upcoming Event: {event_title}</span> 🚀</h2>
        <p>Dear Volunteer,</p>
        <p>We are excited to invite you to our upcoming event:</p>

        <table border="1" cellspacing="0" cellpadding="5">
            <tr>
                <td>📍 <b>Location:</b></td>
                <td>{location}</td>
            </tr>
            <tr>
                <td>📅 <b>Start Date:</b></td>
                <td>{start_date}</td>
            </tr>
            <tr>
                <td>📅 <b>End Date:</b></td>
                <td>{end_date}</td>
            </tr>
            <tr>
                <td style="background-color: #ffcccc;"><b>⏳ Deadline:</b></td>
                <td style="background-color: #ffcccc;"><b>{registration_deadline}</b></td>
            </tr>
        </table>

        <p>Looking forward to seeing you there!</p>

        <p>Best Regards,<br><b>Samarthanam Team</b></p>
    </body>
    </html>
    """

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        print(f"✅ Email sent to {to_email} for event '{event_title}'")
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")

def notify_volunteers():
    """Send email notifications for new published events to all volunteers"""
    volunteers = get_volunteers()
    events = get_unsent_published_events()

    if not events:
        print("⚠️ No new published events found.")
        return

    for event in events:
        event_id = event["id"]
        event_title = event["title"]
        location = event["location"]
        start_date = event["start_date"]
        end_date = event["end_date"]
        registration_deadline = event["registration_deadline"]

        for email in volunteers:
            send_email(email, event_title, location, start_date, end_date, registration_deadline)

        # Mark event as email sent in the database
        mark_email_sent(event_id)

# Run the script
if __name__ == "__main__":
    notify_volunteers()
