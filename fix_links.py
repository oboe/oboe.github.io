import sys
import re
import os

# Regex to match bare URLs not inside <...>
# Updated to use word boundaries and avoid capturing whitespace
URL_REGEX = re.compile(r'(?<!<)(https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]+\.(?:[a-zA-Z]{2,6})(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*))(?![^<]*>)')
# Regex to match Markdown image embeds ![](url)
IMAGE_EMBED_REGEX = re.compile(r'!\[[^\]]*\]\([^\)]*\)')


def fix_links_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all image embeds and replace them with placeholders
    image_embeds = []
    def image_embed_replacer(match):
        image_embeds.append(match.group(0))
        return f"__IMAGE_EMBED_{len(image_embeds)-1}__"
    temp_content = IMAGE_EMBED_REGEX.sub(image_embed_replacer, content)

    # Apply URL regex to the rest of the content
    # Use a function to handle the replacement more carefully
    def url_replacer(match):
        url = match.group(1)
        return f'<{url}>'
    
    new_temp_content = URL_REGEX.sub(url_replacer, temp_content)

    # Restore image embeds
    def restore_image_embed(match):
        idx = int(match.group(1))
        return image_embeds[idx]
    final_content = re.sub(r'__IMAGE_EMBED_(\d+)__', restore_image_embed, new_temp_content)

    # Safety: never write if '__IMAGE_EMBED_' is present in the final content
    if '__IMAGE_EMBED_' in final_content:
        print(f"[WARNING] Skipping write for {filepath} due to leftover IMAGE_EMBED placeholder.")
        return

    if final_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(final_content)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 fix_links.py <directory>")
        sys.exit(1)
    post_dir = sys.argv[1]
    for root, _, files in os.walk(post_dir):
        for file in files:
            if not file.lower().endswith('.md'):
                continue
            filepath = os.path.join(root, file)
            fix_links_in_file(filepath)

if __name__ == "__main__":
    main() 