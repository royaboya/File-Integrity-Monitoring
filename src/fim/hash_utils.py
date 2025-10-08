# using hashlib, define set of functions that will allow the creation of hashes 
# for specific file paths 
# The behavior should only produce hashtypes or string types of hashes

import hashlib

hasher = hashlib.sha256()

# Generates a sha256 hash of a file given filepath and chunk size
def generate_hash_sha256(filepath, chunk_size=8192):
    hash = hashlib.new("sha256")
    
    with open(filepath, "rb") as file:
        while chunk := file.read(chunk_size):
            hash.update(chunk)
            
    return hash.hexdigest()
    









