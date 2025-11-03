import smtplib
import requests
import json
from email.mime.text import MIMEText
from email.message import EmailMessage

from config import SPLUNK_USER, SPLUNK_PW, GMAIL_SMTP, GMAIL_SMTP_TO, GMAIL_SMTP_FROM

import splunklib.client as splunk_client

unmatched = {
    "baselines": [],
    "count": 0
}

def init_splunk_conn():
    conn = splunk_client.connect(
        host="localhost",
        port=8089,
        username=SPLUNK_USER,
        password=SPLUNK_PW
    )
    return conn


def add(filepath):
    if not(isinstance(filepath, str)):
        return
    
    
    # do type checking first
    
    unmatched["baselines"].append(filepath)
    unmatched["count"] += 1

# clear filepaths list?
def send_email_alert(subject, offending_file_paths=unmatched):
    msg = EmailMessage()
    
    msg['From'] = GMAIL_SMTP_FROM
    msg['To'] = GMAIL_SMTP_TO
    msg['Subject'] = subject
    
    email_body = "Filepaths with modified hashes are:\n"
    
    for filepath in offending_file_paths["baselines"]:
        email_body += f"\n{filepath}"
    
    msg.set_content(email_body)
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_SMTP_FROM, GMAIL_SMTP)
            smtp.send_message(msg)
    except Exception as error:
        print(error)
        
    

def raise_alert(msg):
    pass

if __name__ == "__main__":
    send_email_alert("SUBJECT", "NONE")