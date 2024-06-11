import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.core.config import settings

class EmailSender:
    def __init__(self):
        self.smtp_server = settings.email.SMTP_SERVER
        self.smtp_port = settings.email.SMTP_PORT
        self.smtp_username = settings.email.SMTP_USERNAME
        self.smtp_password = settings.email.SMTP_PASSWORD

    async def send_email(self, email_to: str, subject: str, body: str):
        message = MIMEMultipart()
        message['From'] = self.smtp_username
        message['To'] = email_to
        message['Subject'] = subject
        message.attach(MIMEText(body, 'html'))
        async with aiosmtplib.SMTP(hostname=self.smtp_server, port=self.smtp_port, start_tls=True) as server:
            await server.ehlo()
            await server.login(self.smtp_username, self.smtp_password)
            await server.send_message(message)
            
            
email_sender = EmailSender()