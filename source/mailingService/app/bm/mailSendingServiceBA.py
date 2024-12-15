import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
import logging
from string import Template
from jinja2 import Template

from entity.models.MailData import MailData
from entity.exceptions import BadRequestException
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

    def sendMail(self, mailData: MailData):
        subject, body, productPicture = self.setMailData(mailData)
        message = self.configMessage(subject, body, productPicture)
        self.sendingEMail(message)
        
    def setMailData(self, mailData: MailData):
        with open("emailTemplate.html", "r") as emailTemplate:
            templateContent = emailTemplate.read()

        template = Template(templateContent)
        if mailData.action == Action.ADDED:
            body = template.render(
                title = "Successfully Added",
                message = f"Following product was detected and added: ",
                productId = mailData.productId,
                productName = mailData.productName,
                errorMessage = ""
            )
            subject = "Successfully Added"
        elif mailData.action == Action.DELETED:
            body = template.render(
                title = "Successfully Deleted",
                message = f"Following product was detected and deleted: ",
                productId = mailData.productId,
                productName = mailData.productName,
                errorMessage = ""
            )
            subject = "Successfully Deleted"
        elif mailData.action == Action.ERROR:
            body = template.render(
                title = "Something went wrong",
                message = f"Error occured during detecting, adding or deleting the following product: ",
                productId = mailData.productId,
                productName = mailData.productName,
                errorMessage = mailData.errorMessage
            )
            subject = "Something went wrong"
        else:
            self.logger.error(f"Invalid Action: {mailData.action.value}")
            raise BadRequestException()
        productPicture = mailData.productPicture
        return subject, body, productPicture
    
    def configMessage(self, subject: str, body: str, productPicture: str):
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

        with open(productPicture, "rb") as productPictureFile:
            productPicturePart = MIMEImage(productPictureFile.read(), name=productPicture)
        
        productPicturePart.add_header("Content-ID", "<productPicture>")
        productPicturePart.add_header("Content-Disposition", "inline", filename=productPicture)
        message.attach(productPicturePart)

        return message

    def sendingEMail(self, message: MIMEMultipart):
        try:
            with smtplib.SMTP(self.smtpServer, self.smtpPort) as server:
                server.starttls()
                server.login(self.senderEmail, self.password)
                server.send_message(message)     
        except Exception as exception:
            self.logger.error(f"Error: {exception}")
            raise exception
        
    