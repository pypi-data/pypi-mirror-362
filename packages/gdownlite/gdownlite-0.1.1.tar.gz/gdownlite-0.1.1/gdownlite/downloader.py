import re
import requests
from pathlib import Path
import urllib.parse

def extract_file_id(url: str) -> str:
    """Extract Google Drive file ID from various URL formats."""
    # Handle different Google Drive URL formats
    patterns = [
        r"(?:file/d/|open\?id=|id=)([a-zA-Z0-9_-]+)",
        r"drive\.google\.com/file/d/([a-zA-Z0-9_-]+)",
        r"drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)",
        r"docs\.google\.com/.*[?&]id=([a-zA-Z0-9_-]+)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    raise ValueError("❌ Invalid Google Drive URL - Could not extract file ID")

def download_gdrive_file(gdrive_url: str, output_dir: str = ".", quiet: bool = False) -> str:
    """Download a file from Google Drive with proper error handling."""
    file_id = extract_file_id(gdrive_url)
    session = requests.Session()
    
    # Set proper headers to mimic a real browser
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    })
    
    # First attempt to download
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    
    if not quiet:
        print(f"🔄 Attempting to download file ID: {file_id}")
    
    response = session.get(download_url, stream=True)
    
    # Check for errors
    if response.status_code != 200:
        raise Exception(f"❌ HTTP {response.status_code}: Failed to access Google Drive file")
    
    # Check if we got a virus scan warning (for large files)
    confirm_token = None
    if 'download_warning' in response.cookies:
        # Extract the confirm token from cookies
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                confirm_token = value
                break
    
    # Check response content for virus scan warning
    if confirm_token is None and 'text/html' in response.headers.get('content-type', ''):
        # For large files, Google shows a confirmation page
        content = response.text
        confirm_match = re.search(r'confirm=([a-zA-Z0-9_-]+)', content)
        if confirm_match:
            confirm_token = confirm_match.group(1)
        else:
            # Try to find the confirm token in form data
            form_match = re.search(r'name="confirm"[^>]*value="([^"]*)"', content)
            if form_match:
                confirm_token = form_match.group(1)
    
    # If we found a confirm token, make the confirmed request
    if confirm_token:
        if not quiet:
            print("🔄 Large file detected, confirming download...")
        
        confirmed_url = f"https://drive.google.com/uc?export=download&confirm={confirm_token}&id={file_id}"
        response = session.get(confirmed_url, stream=True)
        
        if response.status_code != 200:
            raise Exception(f"❌ HTTP {response.status_code}: Failed to confirm download")
    
    # Check if we actually got a file (not an error page)
    content_type = response.headers.get('content-type', '')
    if 'text/html' in content_type and not confirm_token:
        # We might have gotten an error page
        raise Exception("❌ File may not be publicly accessible or URL is invalid")
    
    # Extract filename from Content-Disposition header
    filename = None
    disposition = response.headers.get('Content-Disposition', '')
    
    if disposition:
        # Handle both quoted and unquoted filenames, including UTF-8 encoding
        filename_patterns = [
            r'filename\*=UTF-8\'\'([^;]+)',  # RFC 5987 UTF-8 encoding
            r'filename="([^"]+)"',           # Quoted filename
            r'filename=([^;]+)',             # Unquoted filename
        ]
        
        for pattern in filename_patterns:
            match = re.search(pattern, disposition, re.IGNORECASE)
            if match:
                filename = match.group(1)
                # Decode URL-encoded filenames
                if pattern.startswith('filename\\*'):
                    filename = urllib.parse.unquote(filename)
                break
    
    # Fallback filename
    if not filename:
        filename = f"gdrive_file_{file_id}"
        # Try to guess extension from content-type
        if 'application/pdf' in content_type:
            filename += '.pdf'
        elif 'image/' in content_type:
            filename += '.jpg'
        elif 'video/' in content_type:
            filename += '.mp4'
        elif 'text/' in content_type:
            filename += '.txt'
        else:
            filename += '.file'
    
    # Sanitize filename for filesystem
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Create output path
    output_path = Path(output_dir) / filename
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Download the file with progress indication
    if not quiet:
        file_size = response.headers.get('content-length')
        if file_size:
            print(f"📁 Downloading: {filename} ({int(file_size)//1024//1024} MB)")
        else:
            print(f"📁 Downloading: {filename}")
    
    total_downloaded = 0
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                total_downloaded += len(chunk)
    
    # Verify we actually downloaded something
    if total_downloaded == 0:
        output_path.unlink()  # Remove empty file
        raise Exception("❌ Downloaded file is empty - the file may not be accessible")
    
    if not quiet:
        size_mb = total_downloaded / (1024 * 1024)
        print(f"✅ Downloaded: {output_path} ({size_mb:.2f} MB)")
    
    return str(output_path)
