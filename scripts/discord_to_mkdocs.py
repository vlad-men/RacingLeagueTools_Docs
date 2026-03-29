import json
import os
from datetime import datetime

# Paths
JSON_FILE = 'downloaded_content/messages_2026-03-29_manual.json'
OUTPUT_DIR = 'docs/penalty-system'
DOCS_IMAGES_DIR = 'docs/penalty-system/images'
IMAGE_REL_PATH = 'images'

def convert_json_to_markdown():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    if not os.path.exists(DOCS_IMAGES_DIR):
        os.makedirs(DOCS_IMAGES_DIR)

    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        messages = json.load(f)

    # Sort messages by timestamp (oldest first)
    messages.sort(key=lambda x: x['timestamp'])

    markdown_content = "# Penalty System (Help)\n\nThis page contains archived messages from the Discord help channel.\n\n"

    for msg in messages:
        author = msg.get('author', 'Unknown')
        content = msg.get('content', '')
        timestamp = msg.get('timestamp', '')
        dt_object = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        formatted_time = dt_object.strftime("%Y-%m-%d %H:%M")

        markdown_content += f"### {author} - {formatted_time}\n\n"
        
        if content:
            markdown_content += f"{content}\n\n"

        for attachment in msg.get('attachments', []):
            local_path = attachment.get('local_path')
            if local_path:
                filename = os.path.basename(local_path)
                # Copy image to docs directory if it doesn't exist
                src_path = os.path.join(os.getcwd(), local_path)
                dest_path = os.path.join(DOCS_IMAGES_DIR, filename)
                
                if os.path.exists(src_path):
                    import shutil
                    shutil.copy2(src_path, dest_path)
                    markdown_content += f"![{filename}]({IMAGE_REL_PATH}/{filename})\n\n"
                else:
                    markdown_content += f"*[Missing image: {filename}]*\n\n"

        markdown_content += "---\n\n"

    output_file = os.path.join(OUTPUT_DIR, 'help-channel.md')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print(f"Generated {output_file}")

if __name__ == "__main__":
    convert_json_to_markdown()
