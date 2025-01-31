import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import logging
from jinja2 import Template

from entity.exceptions.internal_error_exception import InternalErrorException

class MailSendingServiceBa:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "sysad.stock.tracker@gmail.com"
        self.receiver_email = "sysad.project.ws2425@gmail.com"
        self.password = "tihs holh clyi dlai"

    def send_mail(self, message: MIMEMultipart):
        self.logger.info("Sending email...")
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.password)
                server.send_message(message)   
        
        except Exception as exception:
            self.logger.error(f"Error sending mail: {str(exception)}")
            raise InternalErrorException()
        self.logger.info("Successfully sent email!")