import csv
import os
import smtplib
import ssl
import time
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from getpass import getpass


host = 'mail.bsc.es'
port = 465
username = input('[From] BSC intranet username: ')
password = getpass()
csv_senders_list = input('[To] CSV file containing senders list: ')
cc = ['krallinger.martin@gmail.com']
context = ssl.create_default_context()

with smtplib.SMTP_SSL(host, port, context=context) as server:
    server.login(username, password)
    with open(csv_senders_list) as file:
        reader = csv.reader(file)
        # senders_number = len(list(reader))
        next(reader)  # Skip header row
        for ann_id, name, email, subject, body, sample_id in reader:
            to = []
            to.append(email)
            
            message = MIMEMultipart("alternative")
            message["Subject"] = Header(subject, 'utf-8')
            message["From"] = "alejandro.asensio@bsc.es"
            message["To"] = ','.join(to)
            message["Cc"] = ','.join(cc)

            # text = open(os.path.join('body', 'mesinesp', body + '.txt'), 'r').read()
            # html = open(os.path.join('body', 'mesinesp', body + '.html'), 'r').read()
            
            with open(os.path.join('body', 'mesinesp', body + '.txt'), 'r') as text_file:
                text = text_file.read()
            part1 = MIMEText(text, "plain")
            message.attach(part1)

            with open(os.path.join('body', 'mesinesp', body + '.html'), 'r') as html_file:
                html = html_file.read()
            part2 = MIMEText(html, "html")
            message.attach(part2)

            # === Attachments ===

            # filename = 'sample-' + sample_id + '.xlsx'
            # attachment = open(filename, "rb")
            # part3 = MIMEBase('application', 'octet-stream')
            # part3.set_payload((attachment).read())
            # encoders.encode_base64(part3)
            # part3.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            # message.attach(part3)

            # filename = 'ejemplo.xlsx'
            # attachment = open(filename, "rb")
            # part4 = MIMEBase('application', 'octet-stream')
            # part4.set_payload((attachment).read())
            # encoders.encode_base64(part4)
            # part4.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            # message.attach(part4)

            # Command line output
            print(f"Sending to '{name}<{email}>'...")
            print(f'Message: {message}')

            # Wait 1 second before send each email to avoid collapsing the mail server
            time.sleep(1)
            # server.sendmail(
            #     message["From"],
            #     (to + cc),
            #     # message.as_string().format(name=name, email=email, sample_id=sample_id).encode('utf-8'),
            #     message.as_string().format(name=name).encode('utf-8'),
            # )
        
        # print(f'Finished OK. {senders_number} have been sent successfully.')
        print(f'Finished OK. The emails have been sent successfully.')
