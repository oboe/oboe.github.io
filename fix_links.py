import sys
import re
import os
from urllib.parse import urlparse

# Regex to match bare URLs not inside <...>
URL_REGEX = re.compile(r'(?<!<)(https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]+\.(?:[a-zA-Z]{2,6})(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*))(?![^<\n]*>)')
# Regex to match angle-bracket auto-links <https://...>
ANGLE_URL_REGEX = re.compile(r'<(https?://[^>]+)>')
# Regex to match Markdown image embeds ![](url)
IMAGE_EMBED_REGEX = re.compile(r'!\[[^\]]*\]\([^\)]*\)')
# Regex to match Markdown links [text](url)
MD_LINK_REGEX = re.compile(r'\[([^\]]*)\]\(([^\)]*)\)')
# Regex to repair malformed markdown links like [](\<url)> -> [](url)
MALFORMED_MD_LINK_ANGLE = re.compile(r'\[([^\]]*)\]\(<([^)>]+)\)>')


def _domain(url):
    parsed = urlparse(url)
    netloc = parsed.netloc[4:] if parsed.netloc.startswith('www.') else parsed.netloc
    path = re.sub(r'\.(html?|php|aspx?)$', '', parsed.path.rstrip('/'))
    return netloc + path if path else netloc


def fix_links_in_text(content):
    """
    Normalise all URLs in markdown content to [domain](full-url) form.

    Handles: bare URLs, <url> angle-bracket auto-links, and markdown links
    where the display text is itself a raw URL. Preserves image embeds and
    markdown links that already have meaningful display text.
    """
    # Repair malformed markdown links with stray '>' after the parenthesis
    content = MALFORMED_MD_LINK_ANGLE.sub(r'[\1](\2)', content)

    # Convert angle-bracket auto-links <url> to [domain](url)
    content = ANGLE_URL_REGEX.sub(lambda m: f'[{_domain(m.group(1))}]({m.group(1)})', content)

    # Find all image embeds and replace them with placeholders
    image_embeds = []
    def image_embed_replacer(match):
        image_embeds.append(match.group(0))
        return f"__IMAGE_EMBED_{len(image_embeds)-1}__"
    temp_content = IMAGE_EMBED_REGEX.sub(image_embed_replacer, content)

    # Find all markdown links and replace them with placeholders.
    # Normalise if display text is a raw URL or is just the bare domain (missing path).
    md_links = []
    def md_link_replacer(match):
        text, url = match.group(1).strip(), match.group(2)
        parsed = urlparse(url)
        bare_domain = parsed.netloc[4:] if parsed.netloc.startswith('www.') else parsed.netloc
        is_raw_url = bool(re.match(r'https?://', text))
        is_domain_only = text == bare_domain and parsed.path.rstrip('/')
        if is_raw_url or is_domain_only:
            result = f'[{_domain(url)}]({url})'
        else:
            result = match.group(0)
        md_links.append(result)
        return f"__MD_LINK_{len(md_links)-1}__"
    temp_content = MD_LINK_REGEX.sub(md_link_replacer, temp_content)

    # Apply URL regex to the rest of the content
    def url_replacer(match):
        url = match.group(1)
        return f'[{_domain(url)}]({url})'
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

    # Bare URL should be replaced with [domain/path](url)
    _assert_eq("Visit https://example.com for more", "Visit [example.com](https://example.com) for more", "bare-url-wrap")

    # Bare URL with path
    _assert_eq(
        "Visit https://example.com/some/page for more",
        "Visit [example.com/some/page](https://example.com/some/page) for more",
        "bare-url-with-path"
    )

    # Angle-bracket auto-link should be converted
    _assert_eq("See <https://example.com>", "See [example.com](https://example.com)", "angle-bracket-url")

    # Angle-bracket with path (real post: tribe-capital-kapital.md)
    _assert_eq(
        "<https://tribecap.co/kapital-thriving-in-a-desert/>",
        "[tribecap.co/kapital-thriving-in-a-desert](https://tribecap.co/kapital-thriving-in-a-desert/)",
        "angle-bracket-real-tribecap"
    )

    # Angle-bracket with www stripped and nested path (real post: startup-strategy-precision.md)
    _assert_eq(
        "<https://www.battery.com/blog/strategic-coherence>",
        "[battery.com/blog/strategic-coherence](https://www.battery.com/blog/strategic-coherence)",
        "angle-bracket-www-stripped"
    )

    # Angle-bracket with .html extension stripped (real post: brooker)
    _assert_eq(
        "<https://brooker.co.za/blog/2026/02/07/you-are-here.html>",
        "[brooker.co.za/blog/2026/02/07/you-are-here](https://brooker.co.za/blog/2026/02/07/you-are-here.html)",
        "angle-bracket-html-stripped"
    )

    # Angle-bracket with query params — path shown, query string omitted (real post: system-jitter.md)
    _assert_eq(
        "<https://www.youtube.com/watch?v=I_TtMk5z0O0&ab_channel=JaneStreet>",
        "[youtube.com/watch](https://www.youtube.com/watch?v=I_TtMk5z0O0&ab_channel=JaneStreet)",
        "angle-bracket-query-params"
    )

    # Markdown link where display text is domain-only — add the path
    _assert_eq(
        "[randsinrepose.com](https://randsinrepose.com/archives/bored-people-quit/)",
        "[randsinrepose.com/archives/bored-people-quit](https://randsinrepose.com/archives/bored-people-quit/)",
        "domain-only-gets-path-added"
    )

    # Markdown link with meaningful display text — leave it alone
    _assert_eq(
        "[Rands in Repose](https://randsinrepose.com/archives/bored-people-quit/)",
        "[Rands in Repose](https://randsinrepose.com/archives/bored-people-quit/)",
        "meaningful-link-text-preserved"
    )

    # Domain-only link where URL has no path — leave it alone
    _assert_eq(
        "[example.com](https://example.com)",
        "[example.com](https://example.com)",
        "domain-only-no-path-unchanged"
    )

    # Markdown link where display text is a raw URL — normalise it
    _assert_eq(
        "[https://example.com/page](https://example.com/page)",
        "[example.com/page](https://example.com/page)",
        "md-link-url-text-normalised"
    )

    # Image embeds should be preserved
    md_img_in = "Here is an image ![alt](https://example.com/x.png) and a link https://example.com/page"
    md_img_out = "Here is an image ![alt](https://example.com/x.png) and a link [example.com/page](https://example.com/page)"
    _assert_eq(md_img_in, md_img_out, "image-embed-preserved")

    # No leftover placeholders
    out = fix_links_in_text("![a](https://x/y.png) and https://a.b")
    assert "__IMAGE_EMBED_" not in out, (
        f"leftover-placeholders failed.\nExpected: no placeholders\nActual output:\n{out}"
    )

    # http scheme
    _assert_eq("Plain http http://example.com ok", "Plain http [example.com](http://example.com) ok", "http-scheme")

    # complex URL with subdomain, path, query, and fragment
    complex_in = "Go to https://sub.example.co.uk/path/to?p=1&q=two#frag now"
    complex_out = "Go to [sub.example.co.uk/path/to](https://sub.example.co.uk/path/to?p=1&q=two#frag) now"
    _assert_eq(complex_in, complex_out, "complex-url")

    # www without scheme should not be altered
    _assert_eq("Visit www.example.com/page please", "Visit www.example.com/page please", "www-no-scheme")

    # bare URL followed by > on a later line should still be transformed
    _assert_eq(
        "https://example.com/page\n\nA > B",
        "[example.com/page](https://example.com/page)\n\nA > B",
        "url-with-gt-on-later-line"
    )

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