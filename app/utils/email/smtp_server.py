import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.setting import smtp_password, smtp_username, smtp_server, smtp_port

class EmailSender:
    def __init__(self):
        # Параметры SMTP сервера по умолчанию
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password

    def send_email(self, email_to: str, subject: str, body: str):
        # Формирование сообщения
        message = MIMEMultipart()
        message['From'] = self.smtp_username
        message['To'] = email_to
        message['Subject'] = subject

        # Добавление текста сообщения
        message.attach(MIMEText(body, 'plain'))

        # Отправка сообщения
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            server.sendmail(self.smtp_username, email_to, message.as_string())
