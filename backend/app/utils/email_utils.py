import smtplib
from email.message import EmailMessage


def send_email(
    smtp_host: str,
    smtp_port: int,
    from_email: str,
    from_password: str,
    to_email: str,
    subject: str,
    message: str
):
    """
    Send an email using the given SMTP credentials and message content.
    """
    # Create the email message
    email = EmailMessage()
    email["From"] = from_email
    email["To"] = to_email
    email["Subject"] = subject
    email.set_content(message)

    # Connect and send email
    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(from_email, from_password)
            server.send_message(email)
            print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")
