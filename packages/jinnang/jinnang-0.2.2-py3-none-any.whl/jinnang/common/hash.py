import hashlib
import functools
import os

def _make_hashable(obj):
    if isinstance(obj, dict):
        return tuple(sorted((k, _make_hashable(v)) for k, v in obj.items()))
    elif isinstance(obj, list):
        return tuple(_make_hashable(elem) for elem in obj)
    else:
        return obj

def stable_hash(obj) -> str:
    """
    Create a stable hash for any object using MD5.
    
    Args:
        obj: The object to hash
        
    Returns:
        str: Hexadecimal representation of the hash
    """
    # Convert the object to a hashable representation
    hashable_obj = _make_hashable(obj)

    # Convert the hashable object to a string in a consistent manner
    obj_str = repr(hashable_obj)

    # Encode the string into bytes
    obj_bytes = obj_str.encode('utf-8')

    # Create an MD5 hash object and update it with the byte-encoded data
    hash_object = hashlib.md5(obj_bytes)

    # Get the hexadecimal representation of the hash
    hash_hex = hash_object.hexdigest()

    return hash_hex

@functools.lru_cache(maxsize=8192)
def md5(path):
    """
    Calculate MD5 hash of a file.
    
    Args:
        path: Path to the file
        
    Returns:
        str: Hexadecimal representation of the hash
    """
    hash_md5 = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def partial_file_hash(path, chunk_size=4096):
    """
    Calculate a partial MD5 hash of a file by reading chunks from the beginning, middle, and end.
    Useful for large files where a full hash would be too slow.
    
    Args:
        path: Path to the file
        chunk_size: Size of chunks to read (default: 4096 bytes)
        
    Returns:
        str: Hexadecimal representation of the hash
    """
    hash_md5 = hashlib.md5()
    file_size = os.path.getsize(path)

    with open(path, "rb") as f:
        if file_size <= chunk_size * 3:
            # If the file is small, read the entire file
            hash_md5.update(f.read())
        else:
            # Read the start, middle, and end of the file
            f.seek(0)
            hash_md5.update(f.read(chunk_size))
            f.seek(file_size // 2)
            hash_md5.update(f.read(chunk_size))
            f.seek(-chunk_size, os.SEEK_END)
            hash_md5.update(f.read(chunk_size))

    return hash_md5.hexdigest()