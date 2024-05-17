import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.setting import smtp_password, smtp_username, smtp_server, smtp_port

class EmailSender:
    def __init__(self):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password

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