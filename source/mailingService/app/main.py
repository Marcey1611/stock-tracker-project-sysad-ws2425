import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Konfigurationsdetails
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "sysad.stock.tracker@gmail.com"
receiver_email = "sysad.stock.tracker@gmail.com"
app_password = "goczmulgrxsbfesa"

# E-Mail erstellen
subject = "Test-E-Mail mit Anhang"
body = "Diese E-Mail enthält einen Anhang."

# Multipart-Nachricht
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

# Textinhalt hinzufügen
message.attach(MIMEText(body, "plain"))

# Anhang hinzufügen
file = "Test-Anhang.jpg"
with open(file, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Anhang codieren und anhängen
encoders.encode_base64(part)
part.add_header("Content-Disposition", f"attachment; filename={file}")
message.attach(part)

try:
    # Verbindung zum SMTP-Server herstellen
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # TLS aktivieren
        server.login(sender_email, app_password)  # Anmeldung
        server.send_message(message)  # E-Mail senden
        print("E-Mail erfolgreich gesendet!")
except Exception as e:
    print(f"Fehler beim Senden der E-Mail: {e}")

# Alternativ
'''
import yagmail

yag = yagmail.SMTP("sysad.stock.tracker@gmail.com", "faqhiz-Hygtid-4hiqma")
yag.send(
    to="sysad.stock.tracker@gmail.com",
    subject="Hallo von Python",
    contents="Das ist eine Test-E-Mail mit yagmail.",
    attachments="Test-Anhang.jpg"
)
'''