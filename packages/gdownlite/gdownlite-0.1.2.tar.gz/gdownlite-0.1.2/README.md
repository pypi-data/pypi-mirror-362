# gdownlite

A simple, lightweight Google Drive downloader that preserves original filenames.

## Features

- Download files from Google Drive shared links
- Preserves original filename from Google Drive
- Simple command-line interface
- Can be used as a Python library
- Handles large files with confirmation tokens
- Lightweight with minimal dependencies

## Installation

```bash
pip install gdownlite
```

Or install from source:

```bash
git clone https://github.com/ceejay06s/gdownlite.git
cd gdownlite
pip install .
```

## Usage

### Command Line

Download a file to the current directory:
```bash
gdownlite "https://drive.google.com/file/d/YOUR_FILE_ID/view?usp=sharing"
```

Download to a specific directory:
```bash
gdownlite "https://drive.google.com/file/d/YOUR_FILE_ID/view?usp=sharing" -o /path/to/download/folder
```

Quiet mode (suppress output):
```bash
gdownlite "https://drive.google.com/file/d/YOUR_FILE_ID/view?usp=sharing" -q
```

### As a Python Library

```python
from gdownlite import download_gdrive_file

# Download file
file_path = download_gdrive_file(
    "https://drive.google.com/file/d/YOUR_FILE_ID/view?usp=sharing",
    output_dir="./downloads",
    quiet=False
)
print(f"Downloaded to: {file_path}")
```

## Supported URL Formats

The tool supports various Google Drive URL formats:
- `https://drive.google.com/file/d/FILE_ID/view?usp=sharing`
- `https://drive.google.com/open?id=FILE_ID`
- Any URL containing a valid Google Drive file ID

## Requirements

- Python 3.6+
- requests

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Christian**  
Email: christianbalais06@gmail.com  
GitHub: [@ceejay06s](https://github.com/ceejay06s) 