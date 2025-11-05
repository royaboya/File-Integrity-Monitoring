import os
from pathlib import Path

import alerts
import db
import hash_utils
from logger import logger
from config import load_path_config

# scans entire config and looks for any anomalies
def scan():    
    
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
                    print(f"ERROR: {e}")
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
    alerts.send_email_alert("[ALERT] Filepaths modified")
    
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

# remove this function
def hash_filepath(path):
    return hash_utils.generate_hash_sha256(filepath=path)
    

def validate_config():
    # ensure all paths in config.yaml are real/
    # if not, log/add to stored logs 
    config = load_path_config()
    
    for path in config:
        if not(os.path.exists(path)):
            return False
    return True

def generate_report():
    # create from alerts, shouldve had a tracking module
    result = alerts.create_alert_report()
    print(result)
    
    
# ret t/f
def verify_baseline_integrity():
    # need to create db export dump to hash 
    pass
    

if __name__ == "__main__":
    db.clear_baseline()