import os

def remove_empty_files(root_dir):
    removed = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.isfile(file_path) and os.path.getsize(file_path) == 0:
                os.remove(file_path)
                removed.append(file_path)
                print(f"Removed empty file: {file_path}")
    if not removed:
        print("No empty files found.")
    else:
        print(f"Total removed: {len(removed)}")

if __name__ == "__main__":
    remove_empty_files("crawl_results")