import smtplib
import ssl
from email.mime.text import MIMEText
from core.utils.logger import CyberLogger

logger = CyberLogger(__name__)

class EmailNotifier:
    def __init__(self, smtp_server: str, smtp_port: int, sender_email: str, sender_password: str):
        self.context = ssl.create_default_context()
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_alert(self, recipient_email: str, subject: str, body: str) -> bool:
        try:
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = recipient_email

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=self.context)
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            return True
        except Exception as e:
            logger.error(f"Email Error: {str(e)}")
            return False