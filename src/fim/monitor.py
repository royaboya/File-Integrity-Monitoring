from pathlib import Path
import yaml

import alerts
import db
import hash_utils
from logger import logger

unmatched_baselines = []

#TODO: add with open contexts to reduce close calls

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
                    baseline = loaded_baselines[p] # remove this line and get from memory
                except:
                    baseline = "UNKNOWN"
                    
                if hash != baseline:
                    # add to unmatched_baselines?
                    # or build running list in alerts
                    print("alert")
                    alerts.raise_alert("offending message")
                logger.debug(f"{str(p)} : {hash}\n")
            else:
                print("matches, continuing")
                continue
    
def generate_new_baseline():
    db.clear_baseline()
    
    current_config = load_path_config()
   
    for path in current_config:
        converted_path = Path(path)
        for p in converted_path.iterdir():
            if p.is_file():
                hash = hash_filepath(p)
                print(hash)
                
                db.add_entry(str(p), hash)

 
# remove this function
def hash_filepath(path):
    # log hashing filpath?
    
    hash = hash_utils.generate_hash_sha256(filepath=path)
    
    return hash