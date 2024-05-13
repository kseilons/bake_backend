
from os import environ


smtp_server = environ.get("SMTP_SERVER", "smtp.gmail.com")
smtp_port  = environ.get("SMTP_PORT", 587)
smtp_username = environ.get("SMTP_USERNAME", 'your_email@gmail.com')
smtp_password = environ.get("SMPT_PASSWORD", 'your_password')