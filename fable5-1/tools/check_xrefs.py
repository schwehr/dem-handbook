#!/usr/bin/env python3
"""Cross-reference integrity: chapter/appendix mentions vs. TOC numbering."""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
toc = open(os.path.join(ROOT, "TABLE_OF_CONTENTS.md"), encoding="utf-8").read()
titles = {int(n): t.strip() for n, t in re.findall(r"^### Chapter (\d+) — (.+)$", toc, re.M)}
STOP = set("the a an and of to in on for from with its as by or at vs".split())


def words(s):
    return {w for w in re.findall(r"[a-z0-9]+", s.lower()) if w not in STOP and len(w) > 2}


problems = 0
files = sorted(glob.glob(os.path.join(ROOT, "chapters", "*.md")) + glob.glob(os.path.join(ROOT, "appendices", "*.md")))
for f in files:
    rel = os.path.relpath(f, ROOT)
    txt = open(f, encoding="utf-8").read()
    # 1. [Chapter X](chYY-...) link-number agreement
    for m in re.finditer(r"\[(?:Chapter|Ch\.)\s*(\d+)[^\]]*\]\((?:\.\./chapters/)?ch(\d\d)-", txt):
        if int(m.group(1)) != int(m.group(2)):
            print(f"LINK NUMBER MISMATCH {rel}: {m.group(0)}")
            problems += 1
    for m in re.finditer(r"\[Appendix ([A-I])[^\]]*\]\((?:\.\./appendices/)?appendix-([a-i])-", txt):
        if m.group(1).lower() != m.group(2):
            print(f"APPENDIX LINK MISMATCH {rel}: {m.group(0)}")
            problems += 1
    # 2. "Chapter N (title words)" or "Chapter N — title" phrases: check keyword overlap
    for m in re.finditer(r"(?:Chapter|Ch\.)\s*(\d+)\s*(?:\]\([^)]*\))?\s*(?:\(([^)]{6,90})\)|—\s*([^.;:\n]{6,90}))", txt):
        n = int(m.group(1))
        phrase = m.group(2) or m.group(3)
        if n not in titles:
            print(f"UNKNOWN CHAPTER {rel}: {m.group(0)[:100]}")
            problems += 1
            continue
        pw, tw = words(phrase), words(titles[n])
        # skip phrases that are obviously not titles (section refs, years, 'see', etc.)
        if re.match(r"^\s*(§|see|and|e\.g\.|i\.e\.|\d)", phrase):
            continue
        if pw and not (pw & tw):
            print(f"TITLE? {rel}: Chapter {n} '{phrase.strip()[:70]}'  <-> TOC: {titles[n][:70]}")
            problems += 1
print(f"issues: {problems}")
sys.exit(1 if problems else 0)
