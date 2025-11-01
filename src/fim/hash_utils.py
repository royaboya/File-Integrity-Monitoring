import hashlib

# Generates a sha256 hash of a file given filepath and chunk size
def generate_hash_sha256(filepath, chunk_size=8192):
    # raise exception if given an invalid filepath
    hash = hashlib.new("sha256")
    
    try:
        with open(filepath, "rb") as file:
            while chunk := file.read(chunk_size):
                hash.update(chunk)
    except:
        return "ERROR"            
    return hash.hexdigest()

def verify_file_integrity(filepath, expected_hash, algorithm="sha256"):
    hash = generate_hash_sha256(filepath)
    return hash == expected_hash


def generate_hash_sha512(filepath, chunk_size=8192):
    pass

def generate_hash_blake2b(filepath, chunksize=8192):
    pass
