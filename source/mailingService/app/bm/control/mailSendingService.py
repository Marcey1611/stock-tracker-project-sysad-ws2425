import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from bm.entity.Product import Product
from bm.errorHandling.mailSendingException import MailSendingException
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

class MailSendingService:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.smtpServer = "smtp.gmail.com"
        self.smtpPort = 587
        self.senderEmail = "sysad.stock.tracker@gmail.com"
        self.receiverEmail = "sysad.stock.tracker@gmail.com"
        self.password = "tihs holh clyi dlai"
        

    def sendMail(self, product: Product):
        subject, body, productPicture = self.setMailData(product)
        message = self.configMessage(subject, body)
        message = self.attachAttachment(message, productPicture)
        self.sendingEMail(message)

    def sendErrorMail(self, errorMessage: str):
        subject, body = self.setErrorMailData(errorMessage)
        message = self.configMessage(subject, body)
        self.sendingEMail(message)
        
    def setMailData(self, product: Product):
        subject = "Successfully Detection"
        body = f"Following product was detected: Product-ID: {product.productId}, Product-Name: {product.productName}"
        productPicture = product.productPicture
        return subject, body, productPicture
    
    def setErrorMailData(self, errorMessage: str):
        subject = "Product Detection Error"
        body = f"Something went wrong during detect the product. Error-Message: {errorMessage}"
        return subject, body
    
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
        
    