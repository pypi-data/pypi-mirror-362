import re
import requests
from pathlib import Path

def extract_file_id(url: str) -> str:
    match = re.search(r"(?:file/d/|open\?id=)([a-zA-Z0-9_-]+)", url)
    if match:
        return match.group(1)
    raise ValueError("❌ Invalid Google Drive URL")

def download_gdrive_file(gdrive_url: str, output_dir: str = ".", quiet: bool = False) -> str:
    file_id = extract_file_id(gdrive_url)
    session = requests.Session()

    response = session.get(f"https://drive.google.com/uc?export=download&id={file_id}", stream=True)
    confirm_token = None

    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            confirm_token = value
            break

    if confirm_token:
        response = session.get(
            f"https://drive.google.com/uc?export=download&confirm={confirm_token}&id={file_id}",
            stream=True,
        )

    disposition = response.headers.get("Content-Disposition", "")
    filename_match = re.search(r'filename="(.+)"', disposition)
    filename = filename_match.group(1) if filename_match else f"{file_id}.file"

    output_path = Path(output_dir) / filename

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)

    if not quiet:
        print(f"✅ Downloaded: {output_path}")

    return str(output_path)
