import smtplib
from email.mime.multipart import MIMEMultipart
import logging
import os

from entity.exceptions.internal_error_exception import InternalErrorException

class MailSendingServiceBa:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def send_mail(self, message: MIMEMultipart):
        self.logger.info("Sending email...")
        try:
            with smtplib.SMTP(os.getenv("SMTP_SERVER"), os.getenv("SMTP_PORT")) as server:
                server.starttls()
                server.login(os.getenv("SMTP_MAIL"), os.getenv("SMTP_PASS"))
                server.send_message(message)   
        
        except Exception as exception:
            self.logger.error(f"Error sending mail: {str(exception)}")
            raise InternalErrorException()
        self.logger.info("Successfully sent email!")