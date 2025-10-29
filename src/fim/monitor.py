from pathlib import Path
import yaml

import alerts
import db
import hash_utils
from logger import logger

unmatched_baselines = []

# migrate to config.py in the future
def load_path_config():
    with open("../../config.yaml","rb") as f:
        config = yaml.safe_load(f)
    
    paths_to_scan = config.get("system_paths_to_scan", [])
    return paths_to_scan

# scans entire config and looks for any anomalies
def scan():    
    
    current_config = load_path_config() 
    
    loaded_baselines = db.get_all_baseline_values()
    
    for path in current_config:
        converted_path = Path(path)
        for p in converted_path.iterdir():
            if p.is_file():
                hash = hash_filepath(p) # update
                try:
                    baseline = loaded_baselines[p]
                except:
                    logger.error(f"Unable to hash {str(p)}")
                    baseline = "UNKNOWN"
                    
                if hash != baseline:
                    # add to unmatched_baselines?
                    # or build running list in alerts
                    alerts.raise_alert("offending message")
                else:
                    print("matches, continuing")
            else:
                logger.info(f"Not a directory?: {str(p)}")
                continue
    # alerts.build_alert() # send out
    
def generate_new_baseline():
    db.clear_baseline()
    
    current_config = load_path_config()
    running_records = []
   
   
    for path in current_config:
        # load query for one folder root path at at time
        converted_path = Path(path)
        for p in converted_path.iterdir():
            if p.is_file():
                hash = hash_filepath(p)
                running_records.append((str(p), hash))
                db.add_bulk_entries(running_records)
        running_records.clear()
 
# remove this function
def hash_filepath(path):
    return hash_utils.generate_hash_sha256(filepath=path)
    

# ret t/f
def verify_baseline_integrity():
    # need to create db export dump to hash 
    pass    
    

def validate_config():
    pass