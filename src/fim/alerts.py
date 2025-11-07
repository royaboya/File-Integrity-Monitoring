import smtplib
import requests
import json
from email.mime.text import MIMEText
from email.message import EmailMessage

from config import SPLUNK_USER, SPLUNK_PW, GMAIL_SMTP, GMAIL_SMTP_TO, GMAIL_SMTP_FROM, SPLUNK_HEC_TOKEN

import splunklib.client as splunk_client

unmatched = {
    "baselines": [],
    "count": 0,
    "errors": 0
}


def init_splunk_conn():
    conn = splunk_client.connect(
        host="localhost",
        port=8089,
        username=SPLUNK_USER,
        password=SPLUNK_PW
    )
    return conn

def create_splunk_alert():
    url = "https://localhost:8088/services/collector"
    
    event_data = {
        "event": "FIM violation in ___",
        "sourcetype": "fim_alert",
        "index": "main",
        "host": "localhost" 
    }
    
    response = requests.post(url, 
                             headers={"Authorization":f"Splunk {SPLUNK_HEC_TOKEN}",
                                      "Content-Type": "application/json"},
                             data=json.dumps(event_data),
                             verify=False # verify true later
                             )
    

def add(filepath):
    if not(isinstance(filepath, str)):
        return
    
    unmatched["baselines"].append(filepath)
    unmatched["count"] += 1

def inc_err_count():
    unmatched["errors"] += 1

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
        
def get_counts():
    return unmatched        

def create_alert_report():
    msg = """"""
    
    ERROR_COUNT = unmatched["errors"]
    MISMATCH_COUNT = unmatched["count"]
    # DIR_AFFECTED = func() -> unmatched["baselines"]
    msg += f"Errors encountered while scanning: {ERROR_COUNT}\n"
    msg += f"Baseline mismatches: {MISMATCH_COUNT}\n"
    msg += f"Directories Affected: [DIRS]"
    
    return msg
    
if __name__ == "__main__":
    create_splunk_alert()