import sys
import re
import os

LIST_ITEM_RE = re.compile(r'^[ \t]*(?:[-*+]|\d+[.)]) ')
HEADING_RE = re.compile(r'^#{1,6} ')
FENCE_RE = re.compile(r'^(`{3,}|~{3,})')


def fix_list_headers_in_text(content):
    """
    Ensure a blank line separates a list from a following heading.

    Kramdown can indent a heading into a list if there is no blank line
    between the last list item (or its continuation) and the heading,
    producing ugly indented output.  This function inserts the missing
    blank line while leaving everything else untouched.
    """
    lines = content.split('\n')
    result = []
    in_frontmatter = False
    in_code_fence = False
    in_list = False

    for i, line in enumerate(lines):
        # ── frontmatter ──────────────────────────────────────────────────
        if i == 0 and line.strip() == '---':
            in_frontmatter = True
            result.append(line)
            continue
        if in_frontmatter:
            if line.strip() == '---':
                in_frontmatter = False
            result.append(line)
            continue

        # ── blank line ───────────────────────────────────────────────────
        if not line.strip():
            in_list = False
            result.append(line)
            continue

        # ── code fence toggle ─────────────────────────────────────────────
        if FENCE_RE.match(line):
            in_code_fence = not in_code_fence
            in_list = False
            result.append(line)
            continue

        if in_code_fence:
            result.append(line)
            continue

        # ── heading: insert blank line if still inside a list ─────────────
        if HEADING_RE.match(line) and in_list:
            result.append('')
            in_list = False

        # ── update list state for this line ───────────────────────────────
        if LIST_ITEM_RE.match(line):
            in_list = True
        elif line[:1] in (' ', '\t') and in_list:
            pass  # indented list continuation — stay in list
        else:
            in_list = False

        result.append(line)

    return '\n'.join(result)


def fix_list_headers_in_file(filepath, dry_run=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    fixed = fix_list_headers_in_text(content)

    if fixed != content:
        if dry_run:
            print(f"[DRY-RUN] Would update: {filepath}")
            return
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed)


def _run_internal_asserts():
    def _assert_eq(label, input_text, expected):
        actual = fix_list_headers_in_text(input_text)
        assert actual == expected, (
            f"{label} failed.\nExpected:\n{expected!r}\nActual:\n{actual!r}"
        )

    # Basic: heading directly after list item gets a blank line
    _assert_eq(
        "basic-bullet",
        "- item one\n- item two\n## Heading",
        "- item one\n- item two\n\n## Heading",
    )

    # Ordered list
    _assert_eq(
        "ordered-list",
        "1. first\n2. second\n## Heading",
        "1. first\n2. second\n\n## Heading",
    )

    # Already has blank line — must not add a second one
    _assert_eq(
        "already-blank",
        "- item\n\n## Heading",
        "- item\n\n## Heading",
    )

    # Heading not after list — must not be changed
    _assert_eq(
        "no-list",
        "Some text\n## Heading",
        "Some text\n## Heading",
    )

    # List continuation (indented) before heading
    _assert_eq(
        "list-continuation",
        "- item one that spans\n  multiple lines\n## Heading",
        "- item one that spans\n  multiple lines\n\n## Heading",
    )

    # Inside a code fence — must not be modified
    _assert_eq(
        "code-fence",
        "```\n- item\n## not a heading\n```\n## Real heading",
        "```\n- item\n## not a heading\n```\n## Real heading",
    )

    # Frontmatter — must not be modified
    _assert_eq(
        "frontmatter",
        "---\nlayout: post\n---\n- item\n## Heading",
        "---\nlayout: post\n---\n- item\n\n## Heading",
    )

    # Idempotence
    once = fix_list_headers_in_text("- a\n## H")
    twice = fix_list_headers_in_text(once)
    assert once == twice, f"idempotence failed.\nOnce:\n{once!r}\nTwice:\n{twice!r}"

    # All heading levels
    for level in range(1, 7):
        hashes = '#' * level
        _assert_eq(
            f"h{level}",
            f"- item\n{hashes} Heading",
            f"- item\n\n{hashes} Heading",
        )

    print("[SELF-TEST] All assertions passed.")


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "--self-test":
        _run_internal_asserts()
        sys.exit(0)

    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python3 fix_list_headers.py <directory> [--dry-run|-n|--test]")
        print("       python3 fix_list_headers.py --self-test")
        sys.exit(1)

    post_dir = sys.argv[1]
    dry_run = False
    if len(sys.argv) == 3:
        flag = sys.argv[2]
        if flag in ("--dry-run", "-n", "--test"):
            dry_run = True
        else:
            print("Unknown flag:", flag)
            print("Usage: python3 fix_list_headers.py <directory> [--dry-run|-n|--test]")
            sys.exit(1)

    for root, _, files in os.walk(post_dir):
        for file in files:
            if not file.lower().endswith('.md'):
                continue
            fix_list_headers_in_file(os.path.join(root, file), dry_run=dry_run)


if __name__ == "__main__":
    main()
