import smtplib
import requests
import json
from email.mime.text import MIMEText
from email.message import EmailMessage

from config import SPLUNK_USER, SPLUNK_PW, GMAIL_SMTP, GMAIL_SMTP_TO, GMAIL_SMTP_FROM

import splunklib.client as splunk_client
# splunk/email alerts here

filepaths_of_concern = []


def init_splunk_conn():
    conn = splunk_client.connect(
        host="localhost",
        port="8089",
        username=SPLUNK_USER,
        password=SPLUNK_PW
    )


def add(filepath):
    if not(isinstance(filepath, str)):
        return
    
    # do type checking first
    filepaths_of_concern.append(filepath)


# clear filepaths list?
def send_email_alert(subject, body, sender, offending_file_paths):
    msg = EmailMessage()
    
    msg['From'] = GMAIL_SMTP_FROM
    msg['To'] = GMAIL_SMTP_TO
    msg['Subject'] = subject
    msg.set_content(body)
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_SMTP_FROM, GMAIL_SMTP)
            smtp.send_message(msg)
    except Exception as error:
        print(error)
        
        


def raise_alert(msg):
    pass

if __name__ == "__main__":
    send_email_alert("SUBJECT", "BODY", "NONE", "NONE")