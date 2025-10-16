from pathlib import Path
import db
import hash_utils
import yaml
from logger import logger
import json


def load_path_config():
    with open("../../config.yaml","rb") as f:
        config = yaml.safe_load(f)
    
    paths_to_scan = config.get("system_paths_to_scan", [])
    return paths_to_scan



def scan():

    print("Scanning directories for changes")
    
    
    config = load_path_config()
    with open("../../logs/test.log", "w") as logfile:    
        for path in config:
            converted_path = Path(path)
            for p in converted_path.iterdir():
                if p.is_file():
                    hash = hash_filepath(p)
                    # check hash here with baseline
                    logfile.write(f"{str(p)} : {hash}\n")
                    logger.debug(f"{str(p)} : {hash}\n")
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
    # log hashing filpath
    
    hash = hash_utils.generate_hash_sha256(filepath=path)
    
    return hash