from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import logging
from jinja2 import Template
import os
import threading

from entity.models.mail_data import MailUpdateData
from entity.exceptions.internal_error_exception import InternalErrorException
from entity.enums.action import Action
from bm.mail_sending_service_ba import MailSendingServiceBa

class MailPreparingServiceBa:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.mail_data_list = []
        self.mail_sending_service_ba = MailSendingServiceBa()
        self.mail_sending_timer = None
        self.start_scheduled_mail_sending()

    def start_scheduled_mail_sending(self):
        if self.mail_sending_timer:
            self.mail_sending_timer.cancel()
        self.mail_sending_timer = threading.Timer(120, self.send_scheduled_mail)
        self.mail_sending_timer.start()

    def send_scheduled_mail(self):
        if self.mail_data_list:
            subject, body = self.set_mail_data(self.mail_data_list, Action.CHANGED)
            self.mail_sending_service_ba.send_mail(self.config_message(subject, body))
            self.mail_data_list.clear()
        self.start_scheduled_mail_sending()

    def prepare_mail(self, new_mail_data_list, action: Action):
        self.logger.info(f"Preparing mail data...")
        try:
            if action == Action.CHANGED:
                for new_mail_data in new_mail_data_list:
                    existent = False
                    for mail_data in self.mail_data_list:

                        if mail_data.id == new_mail_data.id:
                            mail_data.changed_amount += new_mail_data.changed_amount
                            mail_data.amount = new_mail_data.amount
                            existent = True
                            break

                    if not existent:
                        self.mail_data_list.append(new_mail_data)

            elif action == Action.ERROR:
                subject, body = self.set_error_mail_data(new_mail_data_list)
                self.mail_sending_service_ba.send_mail(self.config_message(subject, body))
            else:
                raise InternalErrorException()
    
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
                    "id": mail_data.id,
                    "name": mail_data.name,
                    "changed_amount": mail_data.changed_amount,
                    "amount": mail_data.amount,
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
            message["From"] = os.getenv("SMTP_MAIL")
            message["To"] = os.getenv("RECV_MAIL")
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