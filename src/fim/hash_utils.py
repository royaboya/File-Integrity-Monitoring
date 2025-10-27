# using hashlib, define set of functions that will allow the creation of hashes 
# for specific file paths 
# The behavior should only produce hashtypes or string types of hashes

import hashlib

hasher = hashlib.sha256()

# Generates a sha256 hash of a file given filepath and chunk size
def generate_hash_sha256(filepath, chunk_size=8192):
    # raise exception if given an invalid filepath
    hash = hashlib.new("sha256")
    
    with open(filepath, "rb") as file:
        while chunk := file.read(chunk_size):
            hash.update(chunk)
            
    return hash.hexdigest()

def verify_file_integrity(filepath, expected_hash, algorithm="sha256"):
    hash = generate_hash_sha256(filepath)
    return hash == expected_hash









