import smtplib
from email.message import EmailMessage

class NotificationManager:
    """Send flight alerts over SMTP."""
    def __init__(self, from_email: str, password: str, smtp_host: str, smtp_port: int = 587):
        if not all([from_email, password, smtp_host]): raise ValueError("Email configuration is incomplete")
        self.from_email, self.password, self.smtp_host, self.smtp_port = from_email, password, smtp_host, smtp_port

    def send_email(self, subject: str, body: str, to_email: str) -> None:
        message = EmailMessage()
        message["From"], message["To"], message["Subject"] = self.from_email, to_email, subject
        message.set_content(body)
        with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=20) as connection:
            connection.starttls()
            connection.login(self.from_email, self.password)
            connection.send_message(message)
