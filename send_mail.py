import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders
from os.path import basename

def send_mail(message):
    fromaddr = ""
    email_pw = ""
    smtp_server = ""
    smtp_port = ""
    recipients = [
        ""
    ]

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = "Subject"

    body = "Moin,\nDiese Email enthält alle zurzeitig laufenden checks für liquidebleiben.codebeamer.com.\
    Zusätzlich ist im Anhang ein Tabellen-Datei(xlsx) mit einer Auflistung aller Tracker.\nViel Spaß!\n\n\
    Mit freundlichen Grüßen,\n  der Integritätschecker\n\n\n\n"
    body += message

    msg.attach(MIMEText(body, 'plain'))

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
