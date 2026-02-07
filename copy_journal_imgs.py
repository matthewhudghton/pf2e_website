#!/usr/bin/en
#!/usr/bin/env python3
import os
import json
import re
import shutil
import argparse
from urllib.parse import unquote


def extract_image_paths(json_file):
    """Extract all image src paths from text.content fields in the JSON."""
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    html_content = "".join(
        page.get("text", {}).get("content", "") for page in data.get("pages", [])
    )
    return re.findall(r'src="([^"]+)"', html_content)


def copy_images(image_paths, src_root, dest_root):
    """Copy images from src_root to dest_root, preserving relative paths."""
    for path in image_paths:
        decoded_path = unquote(path)  # Decode URL-encoded characters
        src_path = os.path.join(src_root, decoded_path)
        dest_path = os.path.join(dest_root, decoded_path)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        try:
            shutil.copy(src_path, dest_path)
            print(f"Copied: {src_path} -> {dest_path}")
        except FileNotFoundError:
            print(f"Warning: File not found: {src_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Copy images referenced in JSON content."
    )
    parser.add_argument("json_file", help="Path to the JSON file")
    parser.add_argument("asset_src", help="Root folder where source assets live")
    parser.add_argument("dest", help="Destination folder to copy images into")
    args = parser.parse_args()

    image_paths = extract_image_paths(args.json_file)
    copy_images(image_paths, args.asset_src, args.dest)


if __name__ == "__main__":
    main()
