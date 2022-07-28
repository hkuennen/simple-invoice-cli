import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def email_func(number, month, year):
    senderEmail = os.environ.get('USER')
    password = os.environ.get('PASSWORD')
    receiverEmail = ["RECEIVER_EMAIL"] # fill in receiver email address
    ccEmail = ["CC_EMAIL"] # fill in cc email address


    # Create a multipart message and set headers
    msg = MIMEMultipart()
    msg['From'] = "Hinnerk Künnen"
    msg['To'] = ", ".join(receiverEmail)
    msg['Cc'] = ", ".join(ccEmail)
    msg['Subject'] = f"Rechnung Nr. {number}"

    # Create email body
    emailText = f"""
    <p>Sehr geehrte Damen und Herren,</p>
    <p>anbei die Rechnung für <b>{month} {year}</b> mit der Bitte um Begleichung.</p>
    <p>Mit freundlichen Grüßen,
    <br> i. A. Hinnerk Künnen</p>
    """

    # Add body to email
    msg.attach(MIMEText(emailText, 'html'))

    attach_file_name = f"Rechnungs-Nr. {number}.pdf"

    # Open PDF file in binary mode
    with open(attach_file_name, "rb") as f:
        attach = MIMEApplication(f.read(), _subtype="pdf")
    # Add header to attachment
    attach.add_header('Content-Disposition', 'attachment',
                      filename=str(attach_file_name))

    # Add attachment to message
    msg.attach(attach)

    # Create secure connection with server and send email
    try:
        # Create the server connection
        server = smtplib.SMTP("smtp.gmail.com", 587)
        # Switch the connection over to TLS encryption
        server.starttls()
        # Authenticate with the server
        server.login(senderEmail, password)
        text = msg.as_string()
        # Send the message
        server.sendmail(senderEmail,
                        receiverEmail+ccEmail, 
                        text)
        print("Successfully sent email")

    except Exception:
        # Error handling
        print("Error: unable to send email")
        smtplib.SMTPConnectError
    # Disconnect
    server.quit()
