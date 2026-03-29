import os
import shutil

# Absolute paths
BASE_DIR = r'c:\Projects\racing_league_tools_documentation'
SRC_DIR = os.path.join(BASE_DIR, 'downloaded_content')
DEST_DIR = os.path.join(BASE_DIR, 'docs', 'penalty-system', 'images')

def copy_images():
    print(f"Copying images from {SRC_DIR} to {DEST_DIR}")
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR, exist_ok=True)
        print(f"Created {DEST_DIR}")
    
    count = 0
    for filename in os.listdir(SRC_DIR):
        if filename.endswith('.png'):
            src_path = os.path.join(SRC_DIR, filename)
            dest_path = os.path.join(DEST_DIR, filename)
            shutil.copy2(src_path, dest_path)
            count += 1
    
    print(f"Copied {count} images")

if __name__ == "__main__":
    copy_images()
