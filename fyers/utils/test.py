import hashlib


data = "E42ZG96H6Q-100:BYFQCGWO5W"
sha256_hash = hashlib.sha256()

# Update the hash object with the bytes of the string
sha256_hash.update(data.encode('utf-8'))

# Get the hexadecimal representation of the hash
hex_digest = sha256_hash.hexdigest()
print(f"SHA-256 Hash: {hex_digest}")
