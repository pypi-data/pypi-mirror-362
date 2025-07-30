import hashlib
import base64

def calculate_md5_base64(file_path: str) -> str:
    with open(file_path, "rb") as file:
        md5_hash = hashlib.md5(file.read()).digest()
        return base64.b64encode(md5_hash).decode()