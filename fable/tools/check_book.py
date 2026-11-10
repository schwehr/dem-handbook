#!/usr/bin/env python3
"""Check DEM Handbook chapter/appendix files against STYLE_GUIDE.md.

Usage: python3 tools/check_book.py [--quiet]
Exit code 0 if all files exist and no hard failures; 1 otherwise.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "STYLE_GUIDE.md")

CHAPTER_HEADINGS = [
    "Then & now",
    "Validation & uncertainty",
    "Software",
    "Standards & guides",
    "Pitfalls",
    "Key takeaways",
    "References",
]
WORD_MIN, WORD_MAX = 4500, 7000


def manifest():
    rows = []
    for line in open(MANIFEST, encoding="utf-8"):
        if line.startswith("| ") and ("chapters/" in line or "appendices/" in line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            rows.append((cells[0], cells[1], cells[2]))
    return rows


def count_words(text):
    return len(re.findall(r"\S+", text))


def check_chapter(num, path, title, text, problems, warnings):
    lines = text.splitlines()
    if not lines or not lines[0].startswith(f"# Chapter {num} "):
        problems.append(f"H1 should start with '# Chapter {num} —'")
    h2 = [l[3:].strip() for l in lines if l.startswith("## ")]
    # numbered sections
    numbered = [h for h in h2 if re.match(rf"^{num}\.\d+", h)]
    if len(numbered) < 4:
        problems.append(f"only {len(numbered)} numbered sections")
    # mandatory headings in order
    idx = []
    for h in CHAPTER_HEADINGS:
        if h not in h2:
            problems.append(f"missing heading '## {h}'")
        else:
            idx.append(h2.index(h))
    if idx != sorted(idx):
        problems.append("mandatory headings out of order")
    if "**In this chapter.**" not in text and "**In this chapter**" not in text:
        warnings.append("no 'In this chapter' abstract")
    # pitfalls / takeaways counts
    def bullets_under(heading):
        try:
            start = next(i for i, l in enumerate(lines) if l.strip() == f"## {heading}")
        except StopIteration:
            return 0
        n = 0
        for l in lines[start + 1:]:
            if l.startswith("## "):
                break
            if re.match(r"^\s*[-*]\s+\S", l) or re.match(r"^\s*\d+\.\s+\S", l):
                n += 1
        return n
    p = bullets_under("Pitfalls")
    k = bullets_under("Key takeaways")
    r = bullets_under("References")
    if p < 8:
        warnings.append(f"Pitfalls has {p} bullets (<8)")
    if k < 6:
        warnings.append(f"Key takeaways has {k} bullets (<6)")
    if r < 12:
        warnings.append(f"References has {r} entries (<12)")
    boxes = len(re.findall(r"^> \*\*(Uncertainty budget|Definitions that bite|Case file|Try it|Worked example|Rule of thumb)\.\*\*", text, re.M))
    if boxes < 2:
        warnings.append(f"only {boxes} boxes")
    figs = len(re.findall(r"<!--\s*figure:", text))
    if figs < 2:
        warnings.append(f"only {figs} figure placeholders")
    if re.search(r"\bTODO\b|to be written|lorem ipsum", text, re.I):
        problems.append("placeholder text found (TODO / to be written)")
    return p, k, r, boxes, figs


def check_links(path, text, known, problems):
    d = os.path.dirname(path)
    for m in re.finditer(r"\]\(([^)#\s]+)(#[^)]*)?\)", text):
        target = m.group(1)
        if re.match(r"^[a-z]+://", target) or target.startswith("mailto:"):
            continue
        full = os.path.normpath(os.path.join(d, target))
        if not os.path.exists(full):
            problems.append(f"broken link: {target}")


def main():
    quiet = "--quiet" in sys.argv
    rows = manifest()
    known = {os.path.join(ROOT, r[1]) for r in rows}
    missing, hard = [], 0
    total_words = 0
    print(f"{'#':>3} {'words':>6} {'P':>3} {'K':>3} {'R':>3} {'B':>2} {'F':>2}  file")
    for num, rel, title in rows:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            missing.append(rel)
            continue
        text = open(path, encoding="utf-8").read()
        words = count_words(text)
        total_words += words
        problems, warnings = [], []
        stats = ("", "", "", "", "")
        if num.isdigit():
            stats = check_chapter(num, path, title, text, problems, warnings)
            if words < WORD_MIN:
                warnings.append(f"short ({words} words)")
            elif words > WORD_MAX + 1500:
                warnings.append(f"long ({words} words)")
        else:
            if not text.startswith(f"# Appendix {num}"):
                problems.append(f"H1 should start with '# Appendix {num}'")
        check_links(path, text, known, problems)
        hard += len(problems)
        flag = "FAIL" if problems else ("warn" if warnings else "ok")
        print(f"{num:>3} {words:>6} {stats[0]!s:>3} {stats[1]!s:>3} {stats[2]!s:>3} {stats[3]!s:>2} {stats[4]!s:>2}  {rel}  [{flag}]")
        if not quiet:
            for p in problems:
                print(f"      FAIL: {p}")
            for w in warnings:
                print(f"      warn: {w}")
    print(f"\nfiles present: {len(rows) - len(missing)}/{len(rows)}   total words: {total_words:,}   hard failures: {hard}")
    if missing:
        print("missing:", ", ".join(missing))
    sys.exit(1 if (missing or hard) else 0)


if __name__ == "__main__":
    main()
