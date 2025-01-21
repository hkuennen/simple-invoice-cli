import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def email_func(number, month, year):
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = [os.getenv("RECEIVER_EMAIL")]
    cc_email = [os.getenv("CC_EMAIL")]
    password = os.getenv("PWD")
    sender_name = os.getenv("SENDER_NAME")
    receiver_name = os.getenv("RECEIVER_NAME")

    # Create a multipart message and set headers
    msg = MIMEMultipart()
    msg["From"] = sender_name
    msg["To"] = ", ".join(receiver_email)
    msg["Cc"] = ", ".join(cc_email)
    msg["Subject"] = f"Rechnung Nr. {number}"

    # Create email body
    emailText = f"""
    <p>Hallo {receiver_name},</p>
    <p>anbei die Rechnung für <b>{month} {year}</b> mit der Bitte um Begleichung.</p>
    <p>Mit freundlichen Grüßen,
    <br> {sender_name}</p>
    """

    # Add body to email
    msg.attach(MIMEText(emailText, "html"))

    invoice_name = f"Rechnungs-Nr. {number}.pdf"

    # Open PDF file in binary mode
    with open(f"_output/{invoice_name}", "rb") as f:
        attach = MIMEApplication(f.read(), _subtype="pdf")
    # Add header to attachment
    attach.add_header("Content-Disposition", "attachment", filename=str(invoice_name))

    # Add attachment to message
    msg.attach(attach)

    # Create secure connection with server and send email
    try:
        # Create the server connection
        server = smtplib.SMTP("smtp.gmail.com", 587)
        # Switch the connection over to TLS encryption
        server.starttls()
        # Authenticate with the server
        server.login(sender_email, password)
        text = msg.as_string()
        # Send the message
        server.sendmail(sender_email, receiver_email + cc_email, text)
        print("Successfully sent email")

    except Exception:
        # Error handling
        print("Error: unable to send email")
        smtplib.SMTPConnectError
    # Disconnect
    server.quit()
