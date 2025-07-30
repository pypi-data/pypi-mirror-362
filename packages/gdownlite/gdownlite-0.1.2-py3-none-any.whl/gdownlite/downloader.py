import re
import requests
from pathlib import Path
import urllib.parse
import time

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

def _try_multiple_download_methods(session, file_id, quiet=False):
    """Try multiple Google Drive download methods to bypass warnings."""
    
    # Method 1: Standard download URL
    urls_to_try = [
        f"https://drive.google.com/uc?export=download&id={file_id}",
        f"https://drive.google.com/uc?id={file_id}&export=download",
        f"https://docs.google.com/uc?export=download&id={file_id}",
        f"https://drive.google.com/u/0/uc?id={file_id}&export=download",
        f"https://drive.google.com/uc?authuser=0&id={file_id}&export=download"
    ]
    
    for attempt, url in enumerate(urls_to_try):
        try:
            if not quiet and attempt > 0:
                print(f"🔄 Trying alternative method {attempt + 1}...")
            
            response = session.get(url, stream=True, allow_redirects=True)
            
            if response.status_code == 200:
                return response, None
                
        except Exception as e:
            if not quiet:
                print(f"⚠️ Method {attempt + 1} failed: {str(e)[:50]}...")
            continue
    
    raise Exception("❌ All download methods failed")

def _extract_bypass_tokens(content, cookies):
    """Extract various bypass tokens from Google's response."""
    tokens = {}
    
    # Extract confirm token (virus scan bypass)
    confirm_patterns = [
        r'confirm=([a-zA-Z0-9_-]+)',
        r'name="confirm"[^>]*value="([^"]*)"',
        r'"confirm":"([^"]*)"',
        r'&amp;confirm=([^&]*)',
        r'confirm%3D([^%]*)',
    ]
    
    for pattern in confirm_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            tokens['confirm'] = match.group(1)
            break
    
    # Check cookies for download warning tokens
    for key, value in cookies.items():
        if 'download_warning' in key or 'confirm' in key:
            tokens['confirm'] = value
            break
    
    # Extract UUID tokens (sometimes used for large files)
    uuid_match = re.search(r'uuid=([a-f0-9-]+)', content)
    if uuid_match:
        tokens['uuid'] = uuid_match.group(1)
    
    # Extract any other bypass parameters
    bypass_patterns = [
        r'at=([^&"\']*)',
        r'authuser=([^&"\']*)',
        r'usp=([^&"\']*)',
    ]
    
    for pattern in bypass_patterns:
        match = re.search(pattern, content)
        if match:
            param_name = pattern.split('=')[0].strip('r\'')
            tokens[param_name] = match.group(1)
    
    return tokens

def _build_bypass_url(file_id, tokens):
    """Build bypass URL with extracted tokens."""
    base_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    
    params = []
    if 'confirm' in tokens:
        params.append(f"confirm={tokens['confirm']}")
    if 'uuid' in tokens:
        params.append(f"uuid={tokens['uuid']}")
    if 'at' in tokens:
        params.append(f"at={tokens['at']}")
    
    # Add common bypass parameters
    params.extend([
        "authuser=0",
        "usp=drive_web",
        "hl=en"
    ])
    
    if params:
        return f"{base_url}&{'&'.join(params)}"
    return base_url

def _detect_google_warnings(content, response):
    """Detect various Google Drive warning types."""
    warnings = []
    
    warning_indicators = [
        ("virus_scan", ["virus", "scan", "cannot be scanned", "exceeds maximum size"]),
        ("quota_exceeded", ["quota", "download quota", "too many users", "limit exceeded"]),
        ("permission_denied", ["permission denied", "access denied", "not allowed"]),
        ("file_not_found", ["file not found", "does not exist", "been deleted"]),
        ("download_blocked", ["download is not available", "downloading is disabled"]),
    ]
    
    content_lower = content.lower()
    
    for warning_type, keywords in warning_indicators:
        if any(keyword in content_lower for keyword in keywords):
            warnings.append(warning_type)
    
    # Also check response headers
    if 'text/html' in response.headers.get('content-type', ''):
        if len(content) < 1000:  # Likely an error page
            warnings.append("error_page")
    
    return warnings

def download_gdrive_file(gdrive_url: str, output_dir: str = ".", quiet: bool = False) -> str:
    """Download a file from Google Drive with aggressive warning bypass."""
    file_id = extract_file_id(gdrive_url)
    session = requests.Session()
    
    # Set more aggressive headers to mimic various browsers
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    })
    
    if not quiet:
        print(f"🔄 Attempting to download file ID: {file_id}")
    
    max_retries = 3
    for retry in range(max_retries):
        try:
            # Try multiple download methods
            response, initial_error = _try_multiple_download_methods(session, file_id, quiet)
            
            # Check if we got actual file content
            content_type = response.headers.get('content-type', '')
            
            # If we got HTML, we likely hit a warning page
            if 'text/html' in content_type:
                content = response.text
                warnings = _detect_google_warnings(content, response)
                
                if warnings and not quiet:
                    print(f"⚠️ Detected warnings: {', '.join(warnings)}")
                    print("🔄 Attempting to bypass warnings...")
                
                # Extract bypass tokens
                tokens = _extract_bypass_tokens(content, response.cookies)
                
                if tokens:
                    if not quiet:
                        print(f"🔧 Found bypass tokens: {list(tokens.keys())}")
                    
                    # Build bypass URL and retry
                    bypass_url = _build_bypass_url(file_id, tokens)
                    
                    # Wait a bit to avoid rate limiting
                    time.sleep(1)
                    
                    response = session.get(bypass_url, stream=True, allow_redirects=True)
                    
                    # Check if bypass worked
                    if response.status_code == 200:
                        new_content_type = response.headers.get('content-type', '')
                        if 'text/html' not in new_content_type:
                            if not quiet:
                                print("✅ Successfully bypassed warnings!")
                        else:
                            # Still got HTML, try more aggressive bypass
                            if not quiet:
                                print("🔄 Attempting aggressive bypass...")
                            
                            # Try direct file stream URL
                            stream_url = f"https://docs.google.com/uc?export=download&id={file_id}&confirm=t"
                            response = session.get(stream_url, stream=True)
            
            # Final check - if still HTML and small content, likely failed
            final_content_type = response.headers.get('content-type', '')
            if 'text/html' in final_content_type:
                content_length = int(response.headers.get('content-length', 0))
                if content_length < 10000:  # Less than 10KB HTML is likely an error
                    if retry < max_retries - 1:
                        if not quiet:
                            print(f"🔄 Retry {retry + 1}/{max_retries} - waiting 2 seconds...")
                        time.sleep(2)
                        continue
                    else:
                        raise Exception("❌ File may not be publicly accessible or has persistent download restrictions")
            
            # If we got here, we should have the file
            break
            
        except Exception as e:
            if retry < max_retries - 1:
                if not quiet:
                    print(f"⚠️ Attempt {retry + 1} failed: {str(e)[:50]}... retrying...")
                time.sleep(2)
            else:
                raise e
    
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
    
    # Fallback filename with better extension detection
    if not filename:
        filename = f"gdrive_file_{file_id}"
        content_type = response.headers.get('content-type', '')
        
        # More comprehensive extension mapping
        extension_map = {
            'application/pdf': '.pdf',
            'application/zip': '.zip',
            'application/x-zip-compressed': '.zip',
            'application/msword': '.doc',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
            'application/vnd.ms-excel': '.xls',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
            'application/vnd.ms-powerpoint': '.ppt',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation': '.pptx',
            'image/jpeg': '.jpg',
            'image/png': '.png',
            'image/gif': '.gif',
            'image/bmp': '.bmp',
            'video/mp4': '.mp4',
            'video/avi': '.avi',
            'video/quicktime': '.mov',
            'audio/mpeg': '.mp3',
            'audio/wav': '.wav',
            'text/plain': '.txt',
            'text/csv': '.csv',
            'application/json': '.json',
            'application/xml': '.xml',
        }
        
        for mime_type, ext in extension_map.items():
            if mime_type in content_type:
                filename += ext
                break
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
