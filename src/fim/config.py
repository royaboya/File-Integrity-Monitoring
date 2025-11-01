import os
import dotenv

dotenv.load_dotenv()

PGSQL_PORT = int(os.getenv("PGSQL_PORT"))
PGSQL_PW = os.getenv("PGSQL_PW")
HOST = os.getenv("HOST")
PGSQL_USER = os.getenv("PGSQL_USER")

SPLUNK_USER = os.getenv("SPLUNK_USER")
SPLUNK_PW = os.getenv("SPLUNK_PW")

GMAIL_SMTP = os.getenv("GMAIL_SMTP")
GMAIL_SMTP_TO = os.getenv("GMAIL_SMTP_TO")
GMAIL_SMTP_FROM = os.getenv("GMAIL_SMTP_FROM")

# add yaml config here
def load_config():
    pass