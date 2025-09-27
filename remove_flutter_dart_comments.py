#!/usr/bin/env python3
"""
Remove // and /* */ comments from all .dart files under the workspace.
This script tries to preserve string literals and character escapes.

USAGE:
  python tools/remove_dart_comments.py

Back up your repo before running this 
"""
import os
import sys


def remove_comments(src: str) -> str:
    out = []
    i = 0
    n = len(src)
    in_single = False
    in_double = False
    in_triple_single = False
    in_triple_double = False
    in_block_comment = False
    in_line_comment = False
    while i < n:
        ch = src[i]


        if in_block_comment:
            if ch == '*' and i + 1 < n and src[i+1] == '/':
                in_block_comment = False
                i += 2
                continue
            else:
                i += 1
                continue

        if in_line_comment:
            if ch == '\n':
                in_line_comment = False
                out.append(ch)
            i += 1
            continue

        if in_triple_single:
            if ch == "'" and src[i:i+3] == "'''":
                out.append("'''")
                i += 3
                in_triple_single = False
                continue
            else:
                out.append(ch)
                i += 1
                continue

        if in_triple_double:
            if ch == '"' and src[i:i+3] == '"""':
                out.append('"""')
                i += 3
                in_triple_double = False
                continue
            else:
                out.append(ch)
                i += 1
                continue

        if in_single:
            if ch == "\\":

                if i + 1 < n:
                    out.append(ch)
                    out.append(src[i+1])
                    i += 2
                    continue
                else:
                    out.append(ch)
                    i += 1
                    continue
            if ch == "'":
                out.append(ch)
                in_single = False
                i += 1
                continue
            out.append(ch)
            i += 1
            continue

        if in_double:
            if ch == "\\":
                if i + 1 < n:
                    out.append(ch)
                    out.append(src[i+1])
                    i += 2
                    continue
                else:
                    out.append(ch)
                    i += 1
                    continue
            if ch == '"':
                out.append(ch)
                in_double = False
                i += 1
                continue
            out.append(ch)
            i += 1
            continue

        if ch == '/' and i + 1 < n:
            nxt = src[i+1]
            if nxt == '/':
                in_line_comment = True
                i += 2
                continue
            if nxt == '*':
                in_block_comment = True
                i += 2
                continue


        if ch == "'":
            if src[i:i+3] == "'''":
                in_triple_single = True
                out.append("'''")
                i += 3
                continue
            in_single = True
            out.append(ch)
            i += 1
            continue

        if ch == '"':
            if src[i:i+3] == '"""':
                in_triple_double = True
                out.append('"""')
                i += 3
                continue
            in_double = True
            out.append(ch)
            i += 1
            continue

        out.append(ch)
        i += 1

    return ''.join(out)


def process_file(path: str):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"[ERROR] Failed to read {path}: {e}")
        return False

    cleaned = remove_comments(content)
    if cleaned == content:
        return True

    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        print(f"[OK] Cleaned: {path}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to write {path}: {e}")
        return False


def main(root: str):
    dart_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        for name in filenames:
            if name.endswith('.dart'):
                dart_files.append(os.path.join(dirpath, name))

    if not dart_files:
        print('No .dart files found.')
        return 0

    failures = []
    for p in dart_files:
        ok = process_file(p)
        if not ok:
            failures.append(p)

    if failures:
        print('\nSome files failed to process:')
        for f in failures:
            print('  -', f)
        return 2

    print('\nAll done.')
    return 0


if __name__ == '__main__':
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.exit(main(root))
