import argparse
from .downloader import download_gdrive_file

def main():
    parser = argparse.ArgumentParser(description="Download Google Drive file by shared URL.")
    parser.add_argument("url", help="Google Drive shared link")
    parser.add_argument("-o", "--output", default=".", help="Output directory")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress output")

    args = parser.parse_args()

    try:
        download_gdrive_file(args.url, output_dir=args.output, quiet=args.quiet)
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
