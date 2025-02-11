import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import logging
from jinja2 import Template

from entity.models.mail_data import MailUpdateData
from entity.exceptions.internal_error_exception import InternalErrorException
from entity.enums.action import Action
from bm.mail_sending_service_ba import MailSendingServiceBa

class MailPreparingServiceBa:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.sender_email = "sysad.stock.tracker@gmail.com"
        self.receiver_email = "sysad.project.ws2425@gmail.com"

    def prepare_mail(self, mail_data, action: Action):
        self.logger.info(f"Preparing email...")
        try:
            if action == Action.CHANGED:
                subject, body = self.set_mail_data(mail_data, action)
            elif action == Action.ERROR:
                subject, body = self.set_error_mail_data(mail_data)
            else:
                raise InternalErrorException()
            mail_sending_service_ba = MailSendingServiceBa()
            mail_sending_service_ba.send_mail(self.config_message(subject, body))
        
        except Exception as exception:
            self.logger.error(f"Exception: {exception}")
            raise InternalErrorException()
        
        
    def set_mail_data(self, mail_data_list: list[MailUpdateData], action: Action):
        try:
            with open("email_template.html", "r") as email_template:
                template_content = email_template.read()
                template = Template(template_content)
            
            products = [
                {
                    "product_id": mail_data.id,
                    "product_name": mail_data.name,
                    "product_amount_changed": mail_data.changed_amount,
                    "product_amount_total": mail_data.amount,
                }
                for mail_data in mail_data_list
            ]

            if action == Action.CHANGED:
                body = template.render(
                    title="Products Successfully Added/Deleted",
                    message="The following products were detected and added or deleted:",
                    products=products,
                )
                subject = "Products Successfully Added/Deleted" 

            else:
                self.logger.error("Unexpected action!")
                raise InternalErrorException()
            return subject, body
        
        except Exception as e:
            self.logger.error(f"Error setting mail data: {str(e)}")
            raise InternalErrorException()
        
    def set_error_mail_data(self, error_message: str):
        try:
            with open("error_email_template.html", "r") as email_template:
                template_content = email_template.read()
                template = Template(template_content)

                body = template.render(
                    title="Error occurred during Detection",
                    message=error_message,
                )
                subject = "Error occurred during Detection"
            return subject, body
        
        except Exception as exception:
            self.logger.error(f"Error setting mail data: {str(exception)}")
            raise InternalErrorException()
        
    def config_message(self, subject: str, body: str) -> MIMEMultipart:
        try:
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = self.receiver_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "html"))

            with open("logo.png", "rb") as logo:
                logo_part = MIMEImage(logo.read(), name="logo.png")
            logo_part.add_header("Content-ID", "<logo>")
            logo_part.add_header("Content-Disposition", "inline", filename="logo.png")
            message.attach(logo_part)
            return message
        
        except Exception as exception:
            self.logger.error(f"Error setting message: {str(exception)}")
            raise InternalErrorException()