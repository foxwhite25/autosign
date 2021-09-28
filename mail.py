import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import email_config
from fancy import rootLogger


class Mail(object):
    def __init__(self):
        self.user, self.password = email_config
        self.session = smtplib.SMTP('smtp.gmail.com', 587)  # 不是gmail请修改smtp

    def send(self, to: list, subject: str, body: str):
        message = MIMEMultipart()
        message['From'] = self.user
        message['To'] = ", ".join(to)
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        self.session.starttls()
        self.session.login(self.user, self.password)
        self.session.sendmail(self.user, to, message.as_string())
        rootLogger.info("Email sent successfully!")

