#!/usr/bin/env python3
"""Compare SUMMARY.md against chapter/appendix H1 titles and TOC Part headings."""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def h1(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("# "):
                return line[2:].strip()
    return None


def main():
    summary = open(os.path.join(ROOT, "SUMMARY.md"), encoding="utf-8").read()
    toc = open(os.path.join(ROOT, "TABLE_OF_CONTENTS.md"), encoding="utf-8").read()
    problems = 0

    links = re.findall(r"^- \[(.+?)\]\(((?:chapters|appendices)/[^)]+)\)", summary, re.M)
    files = sorted(
        ["chapters/" + f for f in os.listdir(os.path.join(ROOT, "chapters")) if f.endswith(".md")]
        + ["appendices/" + f for f in os.listdir(os.path.join(ROOT, "appendices")) if f.endswith(".md")]
    )
    linked = [p for _, p in links]
    for f in files:
        if f not in linked:
            print(f"MISSING in SUMMARY: {f}")
            problems += 1
    for t, p in links:
        full = os.path.join(ROOT, p)
        if not os.path.exists(full):
            print(f"BROKEN link: {p}")
            problems += 1
            continue
        title = h1(full)
        if title != t:
            print(f"TITLE MISMATCH {p}\n   SUMMARY: {t}\n   H1:      {title}")
            problems += 1
    print(f"SUMMARY links: {len(links)}; files on disk: {len(files)}")

    sum_parts = re.findall(r"^## (.+)$", summary, re.M)
    toc_parts = re.findall(r"^## (Part .+|Appendices)$", toc, re.M)
    if sum_parts != toc_parts:
        print("PART HEADING MISMATCH")
        for a, b in zip(sum_parts, toc_parts):
            if a != b:
                print(f"   SUMMARY: {a}\n   TOC:     {b}")
        if len(sum_parts) != len(toc_parts):
            print(f"   counts: SUMMARY {len(sum_parts)} vs TOC {len(toc_parts)}")
        problems += 1
    else:
        print(f"Part headings match ({len(sum_parts)})")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
