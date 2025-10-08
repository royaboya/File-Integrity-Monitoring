# import config 

from pathlib import Path
import db
import hash_utils
import yaml
import logging


def load_path_config():
    with open("../../config.yaml","rb") as f:
        config = yaml.safe_load(f)
    
    paths_to_scan = config.get("system_paths_to_scan", [])
    return paths_to_scan


def scan():
    # arr = load_config()
    
    print("Scanning directories for changes")
    
    config = load_path_config()

    for path in config:
        converted_path = Path(path)
        for p in converted_path.iterdir():
            if p.is_file():
                print(hash_filepath(p))
            else:
                continue
        
    #     run hash on file
    #     if hash does not match database entry (path:hash)
    #           # raise alert
    #     else:
    #          # continue
    

def generate_new_baseline():
    pass


# store it too?
def hash_filepath(path):
    hash = hash_utils.generate_hash_sha256(filepath=path)
    
    return hash