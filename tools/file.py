from uuid import uuid4
from pathlib import Path
from fastapi import UploadFile

UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


async def save_file(file: UploadFile, prefix: str = ''):
    ext = file.filename.split(".")[-1]
    file_name = f"{f'{prefix}-' if prefix else ''}{uuid4()}.{ext}"
    file_path = f"{UPLOAD_DIR}/{file_name}"

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
        
    return file_name


def file_is_exist(file_name: str):
    try:
        file_path = Path(f"{UPLOAD_DIR}/{file_name}")
        if file_path.is_file(): True
        else: False
    except FileNotFoundError:
        return False