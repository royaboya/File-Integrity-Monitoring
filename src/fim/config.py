import os
import dotenv
import yaml

dotenv.load_dotenv()

PGSQL_PORT = int(os.getenv("PGSQL_PORT"))
PGSQL_PW = os.getenv("PGSQL_PW")
HOST = os.getenv("HOST")
PGSQL_USER = os.getenv("PGSQL_USER")

SPLUNK_USER = os.getenv("SPLUNK_USER")
SPLUNK_PW = os.getenv("SPLUNK_PW")
SPLUNK_HEC_TOKEN = os.getenv("SPLUNK_HEC_TOKEN")

GMAIL_SMTP = os.getenv("GMAIL_SMTP")
GMAIL_SMTP_TO = os.getenv("GMAIL_SMTP_TO")
GMAIL_SMTP_FROM = os.getenv("GMAIL_SMTP_FROM")

def load_path_config():
    with open("../../config.yaml","rb") as f:
        config = yaml.safe_load(f)
    
    paths_to_scan = config.get("system_paths_to_scan", [])
    return paths_to_scan
