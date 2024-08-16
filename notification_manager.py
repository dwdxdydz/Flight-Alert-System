import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class NotificationManager:
    def __init__(self, from_email: str, password: str, smtp: str):
        self.from_email = from_email
        self.password = password
        self.smtp = smtp

    def send_email(self, subject: str, body: str, to_email: str):
        """Send an email with the given subject and body to the specified recipient."""
        # Create a MIMEText object to represent the email
        message = MIMEMultipart()
        message['From'] = self.from_email
        message['To'] = to_email
        message['Subject'] = subject

        # Attach the email body to the MIMEText object
        message.attach(MIMEText(body, 'plain'))

        try:
            # Connect to the SMTP server and send the email
            with smtplib.SMTP(self.smtp, port=587) as connection:
                connection.starttls()
                connection.login(user=self.from_email, password=self.password)
                connection.sendmail(
                    from_addr=self.from_email,
                    to_addrs=to_email,
                    msg=message.as_string()
                )
            print("Email sent successfully.")
        except smtplib.SMTPException as e:
            print(f"Failed to send email: {e}")

