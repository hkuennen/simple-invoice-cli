import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Email:
    def __init__(self, number, month, year):
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.receiver_email = [os.getenv("RECEIVER_EMAIL")]
        self.cc_email = [os.getenv("CC_EMAIL")]
        self.password = os.getenv("PWD")
        self.number = number

        sender_name = os.getenv("SENDER_NAME")
        receiver_name = os.getenv("RECEIVER_NAME")

        # Create a multipart message to attach files and set email data
        self.msg = MIMEMultipart()
        self.msg["From"] = sender_name
        self.msg["To"] = ", ".join(self.receiver_email)
        self.msg["Cc"] = ", ".join(self.cc_email)
        self.msg["Subject"] = f"Rechnung Nr. {self.number}"

        # Set email body
        emailText = f"""
        <p>Hallo {receiver_name},</p>
        <p>anbei die Rechnung für <b>{month} {year}</b> mit der Bitte um Begleichung.</p>
        <p>Mit freundlichen Grüßen,
        <br> {sender_name}</p>
        """

        # Add email body
        self.msg.attach(MIMEText(emailText, "html"))

    def add_attachment(self):
        invoice_name = f"Rechnungs-Nr. {self.number}.pdf"

        # Read in attaching PDF file
        with open(f"_output/{invoice_name}", "rb") as f:
            attach = MIMEApplication(f.read(), _subtype="pdf")
        # Add file name to attachment
        attach.add_header(
            "Content-Disposition", "attachment", filename=str(invoice_name)
        )

        # Add attachment to email
        self.msg.attach(attach)

    def send(self):
        try:
            # Create the server connection
            server = smtplib.SMTP("smtp.gmail.com", 587)
            # Switch the connection to TLS encryption
            server.starttls()
            # Authenticate with email provider
            server.login(self.sender_email, self.password)
            text = self.msg.as_string()
            server.sendmail(
                self.sender_email, self.receiver_email + self.cc_email, text
            )
            print("Email sent successfully")

        except Exception:
            # Error handling if email cannot be sent successfully. This might be due to wrong password, network issues, or email provider restrictions.
            print("Error: unable to send email")
            smtplib.SMTPConnectError
        # Disconnect
        server.quit()
