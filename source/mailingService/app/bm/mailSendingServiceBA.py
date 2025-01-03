import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import logging
from string import Template
from jinja2 import Template

from entity.models.MailData import MailData
from entity.exceptions import InternalErrorException
from entity.enums import Action

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

class MailSendingService:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.smtpServer = "smtp.gmail.com"
        self.smtpPort = 587
        self.senderEmail = "sysad.stock.tracker@gmail.com"
        self.receiverEmail = "sysad.stock.tracker@gmail.com"
        self.password = "tihs holh clyi dlai"

    def sendMail(self, mailData, action: Action):
        try:
            if action == Action.ADDED or action == Action.DELETED:
                subject, body = self.setMailData(mailData, action)
            elif action == Action.ERROR:
                subject, body = self.setErrorMailData(mailData)
            else:
                raise InternalErrorException()
            message = self.configMessage(subject, body)
            self.sendingEMail(message)
        except Exception as exception:
            self.logger.error(f"Exception: {exception}")
            raise InternalErrorException()
        
    def setMailData(self, mailDataList: list[MailData], action: Action):
        try:
            productAmountChanged = "productAmountAdded" if action == Action.ADDED else "productAmountDeleted"
            with open("emailTemplate.html", "r") as emailTemplate:
                templateContent = emailTemplate.read()
                template = Template(templateContent)
            
            products = [
                {
                    "productId": mailData.getProductId(),
                    "productName": mailData.getProductName(),
                    productAmountChanged: mailData.getProductAmountChanged(),
                    "productAmountTotal": mailData.getProductAmountTotal(),
                }
                for mailData in mailDataList
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
        
    
    def setErrorMailData(self, errorMessage: str):
        try:
            with open("errorEmailTemplate.html", "r") as emailTemplate:
                templateContent = emailTemplate.read()
                template = Template(templateContent)

                body = template.render(
                    title="Error occured during Detection",
                    message=errorMessage,
                )
                subject = "Error occured during Detection"
            return subject, body
        
        except Exception as exception:
            self.logger.error(f"Error setting mail data: {str(exception)}")
            raise InternalErrorException()
        
    
    
    def configMessage(self, subject: str, body: str):
        try:
            message = MIMEMultipart()
            message["From"] = self.senderEmail
            message["To"] = self.receiverEmail
            message["Subject"] = subject
            message.attach(MIMEText(body, "html"))

            with open("logo.png", "rb") as logo:
                logoPart = MIMEImage(logo.read(), name="logo.png")
            logoPart.add_header("Content-ID", "<logo>")
            logoPart.add_header("Content-Disposition", "inline", filename="logo.png")
            message.attach(logoPart)
            return message
        
        except Exception as exception:
            self.logger.error(f"Error setting message: {str(exception)}")
            raise InternalErrorException()

    def sendingEMail(self, message: MIMEMultipart):
        try:
            with smtplib.SMTP(self.smtpServer, self.smtpPort) as server:
                server.starttls()
                server.login(self.senderEmail, self.password)
                server.send_message(message)   

        except Exception as exception:
            self.logger.error(f"Error sending Mail: {str(exception)}")
            raise InternalErrorException()
        
    