import os
import hashlib
from logger import log

# Example known malware hashes (SHA256)
MALWARE_HASHES = {
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    # Add more known malware hashes here
}

def compute_sha256(file_path):
    """Compute SHA256 hash of a file."""
    try:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        log(f"[HASH ERROR] {file_path} -> {e}")
        return None

def scan_directory(directory="C:\\"):
    """Scan a directory for files and check their SHA256 hash."""
    log(f"[HASH SCANNER] Scanning directory: {directory}")
    infected_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            try:
                file_path = os.path.join(root, file)
                file_hash = compute_sha256(file_path)

                if file_hash in MALWARE_HASHES:
                    log(f"[MALWARE DETECTED] {file_path}")
                    infected_files.append(file_path)

            except Exception as e:
                log(f"[SCAN ERROR] {file_path} -> {e}")

    log(f"[HASH SCANNER] Scan completed. {len(infected_files)} suspicious file(s) found.")
    return infected_files
