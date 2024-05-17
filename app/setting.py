
from os import environ


smtp_server = environ.get("SMTP_SERVER", "smtp.gmail.com")
smtp_port  = environ.get("SMTP_PORT", 465)
smtp_username = environ.get("SMTP_USERNAME", 'your_email@gmail.com')
smtp_password = environ.get("SMPT_PASSWORD", 'your_password')
confirm_email_url = environ.get("CONFIRM_EMAIL_URL", "http://localhost:80/confirm/")
manager_email = environ.get("MANAGER_EMAIL", "manager@gmail.com")