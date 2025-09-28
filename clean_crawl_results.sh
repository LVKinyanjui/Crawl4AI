#!/bin/bash

TARGET_DIR="crawl_results"

echo "WARNING: This will recursively delete ALL non-hidden files in '$TARGET_DIR' and its subdirectories."
read -p "Are you sure you want to continue? (y/N): " confirm

if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "Aborted."
    exit 1
fi

find "$TARGET_DIR" -type f ! -name ".*" -exec rm -v {} +

echo "Cleanup complete. Directory structure and hidden files are preserved."
