'''
Script to send personalized mails using TXT and HTML template files.

Author: Aitor González <aitor.gonzalez@bsc.es>
Refactored by: Alejandro Asensio <alejandro.asensio@bsc.es>
'''

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


# Hardcoded variables
KEYWORD = input('Template KEYWORD: ')
senders_list = os.path.join(f'{KEYWORD}.csv')
body = {
    'plain': os.path.join('body', 'cantemist', f'{KEYWORD}.txt'),
    'html': os.path.join('body', 'cantemist', f'{KEYWORD}.html'),
}
visual_from_addr = 'antonio.miranda@bsc.es'
cc = ['']

# BSC corporate mail credentials
host = 'mail.bsc.es'
port = 465
username = input('BSC intranet username [From]: ')
password = getpass()

# Stablish mailing server connection
context = ssl.create_default_context()
with smtplib.SMTP_SSL(host, port, context=context) as server:
    server.login(username, password)

    senders_length = 0
    with open(senders_list) as csv_file:
        reader = csv.reader(csv_file)

        next(reader)  # Skip header row
        # for fullname, email, password, subject in reader:
        for fullname, email, subject in reader:
        #for email, subject in reader:
            senders_length += 1

            message = MIMEMultipart("alternative")
            message['From'] = visual_from_addr
            to = []
            to.append(email)
            message['To'] = ','.join(to)
            message['Cc'] = ','.join(cc)
            message['Subject'] = Header(subject, 'utf-8')

            with open(body['plain']) as text_file:
                plain = text_file.read()
            part1 = MIMEText(plain, 'plain')
            message.attach(part1)

            with open(body['html']) as html_file:
                html = html_file.read()
            part2 = MIMEText(html, 'html')
            message.attach(part2)

            # ===== Attachments =====

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

            # ===== END Attachments =====

            # Command line output
            print(f"Sending email to '{fullname}<{email}>'...")
            #print(f"Sending email to '<{email}>'...")
            # print(f'Message: {message}')

            # Wait 1 second before send each email to avoid collapsing the mail server
            time.sleep(1)

            # Finally send the email
            server.sendmail(
                message['From'],
                (to + cc),
                message.as_string().format(
                    fullname=fullname,
                    email=email,
                    # password=password
                ).encode('utf-8')
            )

    print(f'Finished OK. {senders_length} email(s) have been sent successfully.')
