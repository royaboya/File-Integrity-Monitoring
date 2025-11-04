import hashlib

# Generates a sha256 hash of a file given filepath and chunk size
def generate_hash_sha256(filepath, chunk_size=8192, hashtype="sha256"):
    # raise exception if given an invalid filepath
    if hashtype not in ["sha256", "sha512"]:
        return "ERROR" 
    
    hash = hashlib.new(hashtype)
    
    try:
        with open(filepath, "rb") as file:
            while chunk := file.read(chunk_size):
                hash.update(chunk)
    except PermissionError:
        return "ERROR"            
    
    return hash.hexdigest()

def verify_file_integrity(filepath, expected_hash):
    hash = generate_hash_sha256(filepath)
    return hash == expected_hash