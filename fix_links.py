import sys
import re
import os

# Regex to match bare URLs not inside <...>
# Updated to use word boundaries and avoid capturing whitespace
URL_REGEX = re.compile(r'(?<!<)(https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]+\.(?:[a-zA-Z]{2,6})(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*))(?![^<]*>)')
# Regex to match Markdown image embeds ![](url)
IMAGE_EMBED_REGEX = re.compile(r'!\[[^\]]*\]\([^\)]*\)')
# Regex to match Markdown links [text](url)
MD_LINK_REGEX = re.compile(r'\[[^\]]*\]\([^\)]*\)')
# Regex to repair malformed markdown links like [](\<url)> -> [](url)
MALFORMED_MD_LINK_ANGLE = re.compile(r'\[([^\]]*)\]\(<([^)>]+)\)>')


def fix_links_in_text(content):
    """
    Transform bare URLs into <URL> form while preserving Markdown image embeds.

    This function contains the core logic and can be used for testing by
    providing plain strings without touching the filesystem.
    """
    # Repair malformed markdown links with stray '>' after the parenthesis
    content = MALFORMED_MD_LINK_ANGLE.sub(r'[\1](\2)', content)

    # Find all image embeds and replace them with placeholders
    image_embeds = []
    def image_embed_replacer(match):
        image_embeds.append(match.group(0))
        return f"__IMAGE_EMBED_{len(image_embeds)-1}__"
    temp_content = IMAGE_EMBED_REGEX.sub(image_embed_replacer, content)

    # Find all markdown links and replace them with placeholders
    md_links = []
    def md_link_replacer(match):
        md_links.append(match.group(0))
        return f"__MD_LINK_{len(md_links)-1}__"
    temp_content = MD_LINK_REGEX.sub(md_link_replacer, temp_content)

    # Apply URL regex to the rest of the content
    def url_replacer(match):
        url = match.group(1)
        return f'<{url}>'
    new_temp_content = URL_REGEX.sub(url_replacer, temp_content)

    # Restore image embeds
    def restore_image_embed(match):
        idx = int(match.group(1))
        return image_embeds[idx]
    restored_images_content = re.sub(r'__IMAGE_EMBED_(\d+)__', restore_image_embed, new_temp_content)

    # Restore markdown links
    def restore_md_link(match):
        idx = int(match.group(1))
        return md_links[idx]
    final_content = re.sub(r'__MD_LINK_(\d+)__', restore_md_link, restored_images_content)

    return final_content


def fix_links_in_file(filepath, dry_run=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    final_content = fix_links_in_text(content)

    # Safety: never write if placeholders are present in the final content
    if '__IMAGE_EMBED_' in final_content or '__MD_LINK_' in final_content:
        print(f"[WARNING] Skipping write for {filepath} due to leftover placeholder.")
        return

    if final_content != content:
        if dry_run:
            print(f"[DRY-RUN] Would update: {filepath}")
            return
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(final_content)

def _run_internal_asserts():
    def _assert_eq(input_text, expected_text, label):
        actual_text = fix_links_in_text(input_text)
        assert actual_text == expected_text, (
            f"{label} failed.\nExpected:\n{expected_text}\nActual:\n{actual_text}\nInput:\n{input_text}"
        )

    # Bare URL should be wrapped
    _assert_eq("Visit https://example.com for more", "Visit <https://example.com> for more", "bare-url-wrap")

    # Already wrapped URL should remain unchanged
    _assert_eq("See <https://example.com>", "See <https://example.com>", "already-wrapped")

    # Image embeds should be preserved
    md_img_in = "Here is an image ![alt](https://example.com/x.png) and a link https://example.com/page"
    md_img_out = "Here is an image ![alt](https://example.com/x.png) and a link <https://example.com/page>"
    _assert_eq(md_img_in, md_img_out, "image-embed-preserved")

    # No leftover placeholders
    out = fix_links_in_text("![a](https://x/y.png) and https://a.b")
    assert "__IMAGE_EMBED_" not in out, (
        f"leftover-placeholders failed.\nExpected: no placeholders\nActual output:\n{out}"
    )

    # http scheme
    _assert_eq("Plain http http://example.com ok", "Plain http <http://example.com> ok", "http-scheme")

    # complex URL with subdomain, path, query, and fragment
    complex_in = "Go to https://sub.example.co.uk/path/to?p=1&q=two#frag now"
    complex_out = "Go to <https://sub.example.co.uk/path/to?p=1&q=two#frag> now"
    _assert_eq(complex_in, complex_out, "complex-url")

    # www without scheme should not be altered
    _assert_eq("Visit www.example.com/page please", "Visit www.example.com/page please", "www-no-scheme")

    # markdown link target should become angle-wrapped, which is valid CommonMark
    md_link_in = "[site](https://example.com) and text"
    md_link_out = "[site](https://example.com) and text"
    _assert_eq(md_link_in, md_link_out, "markdown-link-target-wrapped")

    # idempotence: applying twice yields same output
    once = fix_links_in_text("url https://idemp.le/test")
    twice = fix_links_in_text(once)
    assert once == twice, (
        f"idempotence failed.\nExpected (once):\n{once}\nActual (twice):\n{twice}"
    )

    # malformed markdown link with angle-bracketed URL should be repaired
    malformed_in = "[](<https://example.com)>"
    repaired_out = "[](https://example.com)"
    _assert_eq(malformed_in, repaired_out, "repair-malformed-md-link-angle")

    print("[SELF-TEST] All assertions passed.")


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "--self-test":
        _run_internal_asserts()
        sys.exit(0)

    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python3 fix_links.py <directory> [--dry-run|-n|--test]")
        print("       python3 fix_links.py --self-test")
        sys.exit(1)
    post_dir = sys.argv[1]
    dry_run = False
    if len(sys.argv) == 3:
        flag = sys.argv[2]
        if flag in ("--dry-run", "-n", "--test"):
            dry_run = True
        else:
            print("Unknown flag:", flag)
            print("Usage: python3 fix_links.py <directory> [--dry-run|-n|--test]")
            sys.exit(1)
    for root, _, files in os.walk(post_dir):
        for file in files:
            if not file.lower().endswith('.md'):
                continue
            filepath = os.path.join(root, file)
            fix_links_in_file(filepath, dry_run=dry_run)

if __name__ == "__main__":
    main() 