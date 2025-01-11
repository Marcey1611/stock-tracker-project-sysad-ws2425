import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import logging
from jinja2 import Template

from entity.models.mail_data import MailData
from entity.exceptions.internal_error_exception import InternalErrorException
from entity.enums.action import Action

class MailSendingServiceBa:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "sysad.stock.tracker@gmail.com"
        self.receiver_email = "sysad.stock.tracker@gmail.com"
        self.password = "tihs holh clyi dlai"

    def send_mail(self, mail_data, action: Action):
        try:
            if action == Action.ADDED or action == Action.DELETED:
                subject, body = self.set_mail_data(mail_data, action)
            elif action == Action.ERROR:
                subject, body = self.set_error_mail_data(mail_data)
            else:
                raise InternalErrorException()
            message = self.config_message(subject, body)
            self.send_email(message)
        except Exception as exception:
            self.logger.error(f"Exception: {exception}")
            raise InternalErrorException()
        
    def set_mail_data(self, mail_data_list: list[MailData], action: Action):
        try:
            product_amount_changed = "productAmountAdded" if action == Action.ADDED else "productAmountDeleted"
            with open("email_template.html", "r") as email_template:
                template_content = email_template.read()
                template = Template(template_content)
            
            products = [
                {
                    "productId": mail_data.get_product_id(),
                    "productName": mail_data.get_product_name(),
                    product_amount_changed: mail_data.get_product_amount_changed(),
                    "productAmountTotal": mail_data.get_product_amount_total(),
                }
                for mail_data in mail_data_list
            ]

            if action == Action.ADDED:
                body = template.render(
                    title="Products Successfully Added",
                    message="The following products were detected and added:",
                    products=products,
                )
                subject = "Products Successfully Added" 

            elif action == Action.DELETED:
                body = template.render(
                    title="Products Successfully Deleted",
                    message="The following products were detected and deleted:",
                    products=products,
                )
                subject = "Products Successfully Deleted" 

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
        
    def config_message(self, subject: str, body: str):
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

    def send_email(self, message: MIMEMultipart):
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.password)
                server.send_message(message)   

        except Exception as exception:
            self.logger.error(f"Error sending mail: {str(exception)}")
            raise InternalErrorException()