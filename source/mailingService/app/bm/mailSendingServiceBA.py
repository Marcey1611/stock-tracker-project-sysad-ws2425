import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import logging

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
        message = self.configMessage(subject, body)
        if len(mailData.productPicture) > 0:
            message = self.attachAttachment(message, productPicture)
        self.sendingEMail(message)
        
    def setMailData(self, mailData: MailData):
        subject = "Successfully Detection"
        if mailData.action == Action.ADDED:
            body = f"Following product was detected and added: Product-ID: {mailData.productId}, Product-Name: {mailData.productName}"
        elif mailData.action == Action.DELETED:
            body = f"Following product was detected and deleted: Product-ID: {mailData.productId}, Product-Name: {mailData.productName}"
        elif mailData.action == Action.ERROR:
            body = f"Something went wrong during detecting, adding or deleting the product with the Product-ID: {mailData.productId} and Product-Name: {mailData.productName}. Error-Message: {mailData.errorMessage}"
        else:
            self.logger.error(f"Invalid Action: {mailData.action.value}")
            raise BadRequestException()
        productPicture = mailData.productPicture
        return subject, body, productPicture
    
    def configMessage(self, subject: str, body: str):
        message = MIMEMultipart()
        message["From"] = self.senderEmail
        message["To"] = self.receiverEmail
        message["Subject"] = subject

        message.attach(MIMEText(body, "plain"))
        return message

    def attachAttachment(self, message: MIMEMultipart, productPicture: str):
        with open(productPicture, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={productPicture}")
        message.attach(part)

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
        
    