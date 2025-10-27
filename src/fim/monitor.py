from pathlib import Path
import yaml

import alerts
import db
import hash_utils
from logger import logger

unmatched_baselines = []

def load_path_config():
    with open("../../config.yaml","rb") as f:
        config = yaml.safe_load(f)
    
    paths_to_scan = config.get("system_paths_to_scan", [])
    return paths_to_scan


# scans entire config and looks for any anomalies
# needs to handle file not found exceptions
# what if hashes arent able to be made?
# how will those exceptions be handled
def scan():
    print("Scanning directories for changes") # move this to cli.py
    
    config = load_path_config() # config func from db or a config.py module
    for path in config:
        converted_path = Path(path)
        for p in converted_path.iterdir():
            if p.is_file():
                hash = hash_filepath(p)
                baseline = "get baseline func" # baseline func from db? or config.py
                if hash != baseline:
                    alerts.raise_alert("offending message")
                logger.debug(f"{str(p)} : {hash}\n")
            else:
                continue
    
def generate_new_baseline():
    # hash = get hash
    # db.update_entry(filepath, hash)
    pass

 
# remove this function
def hash_filepath(path):
    # log hashing filpath?
    
    hash = hash_utils.generate_hash_sha256(filepath=path)
    
    return hash