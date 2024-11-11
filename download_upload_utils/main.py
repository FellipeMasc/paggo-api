import os

def save_file_to_s3(file_bytes : bytes, file_name : str) -> None:
    abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../local_s3", file_name))
    with open(abs_path, 'wb') as f:
        f.write(file_bytes)
        
def request_file_from_s3(file_name : str) -> bytes:
    abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../local_s3", file_name))
    with open(abs_path, 'rb') as f:
        return f.read()