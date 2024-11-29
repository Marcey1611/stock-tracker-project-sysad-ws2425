import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# config
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "sysad.stock.tracker@gmail.com"
receiver_email = "sysad.stock.tracker@gmail.com"
app_password = "goczmulgrxsbfesa"

# create E-Mail
subject = "Test-E-Mail mit Anhang"
body = "Diese E-Mail enthält einen Anhang."

# multipart-message
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

# add body text
message.attach(MIMEText(body, "plain"))

# add attachement
file = "Test-Anhang.jpg"
with open(file, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# encode attachment and add to mail
encoders.encode_base64(part)
part.add_header("Content-Disposition", f"attachment; filename={file}")
message.attach(part)

try:
    # create connection to smtp-server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # TLS aktivieren
        server.login(sender_email, app_password)  # Anmeldung
        server.send_message(message)  # E-Mail senden
        print("E-Mail erfolgreich gesendet!")
except Exception as e:
    print(f"Fehler beim Senden der E-Mail: {e}")

#from api.boundary.api import app
#import uvicorn

#if __name__ == "__main__":
#    uvicorn.run(app, host="0.0.0.0", port=8000)
