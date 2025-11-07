import os
from pathlib import Path
from socket import gethostname

import alerts
import db
import hash_utils
from logger import logger
from config import load_path_config

# scans entire config and looks for any anomalies
def scan():    
    
    hostname = gethostname()
    current_config = load_path_config() 
    loaded_baselines = db.get_all_baseline_values()
    
    for path in current_config:
        converted_path = Path(path)
        for p in converted_path.iterdir():
            if p.is_file():
                hash = hash_filepath(p)
                try:
                    baseline = loaded_baselines[str(p)]
                except Exception as e:
                    print(f"ERROR: Could not hash {str(p)}")
                    logger.error(f"Unable to hash {str(p)}")
                    alerts.inc_err_count()
                    baseline = "UNKNOWN"
                    
                if hash != baseline:
                    print(f"MISTMATCH FOUND: {str(p)}")
                    alerts.add(str(p))
                else:
                    continue
            else:
                logger.info(f"Not a directory?: {str(p)}")
                continue
    alerts.send_email_alert(f"[ALERT] Filepaths modified for host {hostname}")
    
def generate_new_baseline():
    db.clear_baseline()
    
    current_config = load_path_config()
    running_records = []
   
    for path in current_config:
        converted_path = Path(path)
        for p in converted_path.iterdir():
            if p.is_file():
                hash = hash_filepath(p)
                running_records.append((str(p), hash))
    print("adding")
    db.add_bulk_entries(running_records)

# TODO: remove this feature 
def hash_filepath(path):
    return hash_utils.generate_hash_sha256(filepath=path)
    

def validate_config(): 
    config = load_path_config()
    
    for path in config:
        if not(os.path.exists(path)):
            # logger.log(path does not exist)
            return False
        
    return True

def generate_report():
    result = alerts.create_alert_report()
    print(result)
    
    return result
    
def verify_baseline_integrity() -> bool:
    # need to create db export dump to hash 
    pass
    

if __name__ == "__main__":
    db.clear_baseline()