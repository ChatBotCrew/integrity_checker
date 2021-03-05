import smtplib
import sys
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders
from os.path import basename

missing_variables = []
try:
    fromaddr = os.environ["FROM_ADDR"]
except KeyError:
    missing_variables.append("FROM_ADDR")

try:
    email_pw = os.environ["FROM_ADDR_PW"]
except KeyError:
    missing_variables.append("FROM_ADDR_PW")

try:
    smtp_server = os.environ["SMTP_SERVER"]
except KeyError:
    missing_variables.append("SMTP_SERVER")

try:
    smtp_port = os.environ["SMTP_SERVER_PORT"]
except KeyError:
    missing_variables.append("SMTP_SERVER_PORT")

try:
    recipients = os.environ["RECIPIENTS"].split()
except KeyError:
    missing_variables.append("RECIPIENTS")

if missing_variables:
    print("[ERR] Missing the following environmental variables to be able to send emails:")
    for key in missing_variables:
      print("  - " + key)
    sys.exit(1)

def send_mail(TABLE_DISABLED, message):

    print("[INFO]: Sending email ...")
    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = "Integrity Check Codebeamer"

    body = "Moin,\nDiese Email enthält die automatisch generierten Checks für liquidebleiben.codebeamer.com.\
    Im Anhang befindet sich eine Tabelle(xlsx) mit einer Auflistung aller Tracker.\nViel Spaß!\n\n\
    Mit freundlichen Grüßen,\n   der Integritätschecker\n\n\n\n"
    body += message

    msg.attach(MIMEText(body, 'plain'))
    if TABLE_DISABLED == 'false':
        print("[INFO]: Attaching xlsx file ...")
        filename = "table.xlsx"

        with open(filename, "rb") as fil: 
            ext = filename.split('.')[-1:]
            attachedfile = MIMEApplication(fil.read(), _subtype = ext)
            attachedfile.add_header(
                'content-disposition', 'attachment', filename=basename(filename) )
        msg.attach(attachedfile)


    server = smtplib.SMTP(host=smtp_server, port=smtp_port)
    server.ehlo()
    server.starttls()
    server.login('lucas@humfeldt.de', email_pw)
    text = msg.as_string()

    for recipient in recipients:
        server.sendmail(fromaddr, recipient, text)
    server.quit()
    print("[INFO]: Email sent ...")
