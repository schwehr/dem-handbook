#!/usr/bin/env python3
"""Fact-checking, structural, math, DOI, and gis-history verification for dem-handbook/fable.

Usage:
    python3 tools/check_facts.py [--check-dois] [--check-history] [files...]

Defaults to all 82 manifest files from STYLE_GUIDE.md if no files are specified.
Exit code: 0 if no hard structural or DOI failures; 1 otherwise.
"""
import argparse
import concurrent.futures
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STYLE_GUIDE = os.path.join(ROOT, "STYLE_GUIDE.md")
TOC_PATH = os.path.join(ROOT, "TABLE_OF_CONTENTS.md")

CHAPTER_HEADINGS = [
    "Then & now",
    "Validation & uncertainty",
    "Software",
    "Standards & guides",
    "Pitfalls",
    "Key takeaways",
    "References",
]
GIS_HISTORY_URL = "https://raw.githubusercontent.com/schwehr/gis-history/main/README.md"
DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+")


def load_manifest():
    """Return list of (id_str, rel_path, title) from STYLE_GUIDE.md §8."""
    rows = []
    with open(STYLE_GUIDE, encoding="utf-8") as f:
        for line in f:
            if line.startswith("| ") and ("chapters/" in line or "appendices/" in line):
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) >= 3:
                    rows.append((cells[0], cells[1], cells[2]))
    return rows


def load_toc_math_chapters():
    """Return set of chapter numbers that have a **Math.** slot in TABLE_OF_CONTENTS.md."""
    if not os.path.exists(TOC_PATH):
        return set()
    txt = open(TOC_PATH, encoding="utf-8").read()
    math_chapters = set()
    matches = list(re.finditer(r"^### Chapter (\d+)\s+—\s+.+$", txt, re.M))
    for idx, m in enumerate(matches):
        ch_num = int(m.group(1))
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(txt)
        block = txt[start:end]
        if re.search(r"^(?:-\s*)?\*\*Math\.?:?\*\*", block, re.M):
            math_chapters.add(ch_num)
    return math_chapters


def clean_doi(raw):
    """Strip trailing punctuation while preserving balanced parentheses/brackets in DOIs."""
    d = raw.rstrip(".,;>")
    while d.endswith(")") and d.count(")") > d.count("("):
        d = d[:-1]
    while d.endswith("]") and d.count("]") > d.count("["):
        d = d[:-1]
    return d.rstrip(".,;>")


def strip_fenced_and_inline_code(lines):
    """Yield (line_num, line_without_inline_code, in_fence) for each line."""
    in_fence = False
    fence_char = ""
    for i, line in enumerate(lines, 1):
        # Handle fenced code blocks inside blockquotes (`> ```bash`) as well as top-level
        unquoted = re.sub(r"^(?:\s*>\s*)*", "", line).lstrip()
        if unquoted.startswith("```") or unquoted.startswith("~~~"):
            ch = unquoted[:3]
            if not in_fence:
                in_fence = True
                fence_char = ch
            elif ch == fence_char:
                in_fence = False
                fence_char = ""
            yield i, "", True
            continue
        if in_fence:
            yield i, "", True
            continue
        # Remove inline code spans (`...` or ``...``)
        cleaned = re.sub(r"``.*?``|`[^`]*`", "", line)
        yield i, cleaned, False


def strip_currency(s):
    """Remove currency tokens like US$100 or '$1.97 million' without touching LaTeX math."""
    # Always strip explicit currency prefixes like US$100, A$50, C$20
    s = re.sub(r"\b(?:US|CA|AU|NZ|HK|SG)\$\d+(?:[.,–-]\d+)*(?:[kMB])?", "", s)
    # Only strip standalone $<number> if the remaining count of '$' on the line is odd
    if s.count("$") % 2 == 1:
        s = re.sub(
            r"(?<![\\A-Za-z0-9])\$\d+(?:[.,–-]\d+)*(?:[kMB])?"
            r"(?=(?:\s+[A-Za-z])|[,;)]|$)",
            "",
            s,
        )
    return s


def check_structure_and_hygiene(rel_path, full_path, toc_math_chapters):
    """Check headings, TOC Math, section/figure numbering, LaTeX $, tables, and links."""
    problems = []
    warnings = []
    text = open(full_path, encoding="utf-8").read()
    lines = text.splitlines()

    m_ch = re.match(r"chapters/ch(\d+)-", rel_path)
    m_app = re.match(r"appendices/appendix-([a-i])-", rel_path)
    ch_num = int(m_ch.group(1)) if m_ch else None
    app_letter = m_app.group(1).upper() if m_app else None

    if ch_num is not None:
        if not lines or not lines[0].startswith(f"# Chapter {ch_num} — "):
            problems.append(f"H1 does not start with '# Chapter {ch_num} — '")
        h2 = [l[3:].strip() for l in lines if l.startswith("## ")]
        # Mandatory headings in order
        idx = []
        for h in CHAPTER_HEADINGS:
            if h not in h2:
                problems.append(f"Missing mandatory heading '## {h}'")
            else:
                idx.append(h2.index(h))
        if idx != sorted(idx):
            problems.append("Mandatory headings out of order")
        if ch_num in toc_math_chapters and "Mathematics" not in h2:
            problems.append("TOC specifies Math slot but '## Mathematics' heading is missing")
        if "Mathematics" in h2 and "Then & now" in h2 and "Validation & uncertainty" in h2:
            if not (h2.index("Then & now") < h2.index("Mathematics") < h2.index("Validation & uncertainty")):
                problems.append("'## Mathematics' must appear between '## Then & now' and '## Validation & uncertainty'")

        # Sequential numbered sections ## N.1, ## N.2, ...
        sec_nums = []
        for h in h2:
            sm = re.match(rf"^{ch_num}\.(\d+)\b", h)
            if sm:
                sec_nums.append(int(sm.group(1)))
            elif re.match(r"^\d+\.\d+\b", h):
                problems.append(f"Wrong chapter prefix in H2 section: '## {h}'")
        if sec_nums != list(range(1, len(sec_nums) + 1)):
            problems.append(f"Non-sequential H2 sections: {sec_nums}")
    elif app_letter is not None:
        if not lines or not lines[0].startswith(f"# Appendix {app_letter} — "):
            problems.append(f"H1 does not start with '# Appendix {app_letter} — '")

    # Sequential figure placeholders
    expected_prefix = str(ch_num) if ch_num is not None else app_letter
    if expected_prefix:
        fig_nums = []
        for fm in re.finditer(r"<!--\s*figure:\s*Figure\s+([A-Z]|\d+)\.(\d+)\b", text):
            if fm.group(1) != expected_prefix:
                problems.append(f"Figure prefix mismatch: Figure {fm.group(1)}.{fm.group(2)} in {rel_path}")
            else:
                fig_nums.append(int(fm.group(2)))
        if fig_nums != list(range(1, len(fig_nums) + 1)):
            problems.append(f"Non-sequential figure numbers: {fig_nums}")

    # Relative links and chapter/appendix link-number consistency
    base_dir = os.path.dirname(full_path)
    for lm in re.finditer(r"\]\(([^)#\s]+)(#[^)]*)?\)", text):
        target = lm.group(1)
        if re.match(r"^[a-z]+://", target) or target.startswith("mailto:"):
            continue
        resolved = os.path.normpath(os.path.join(base_dir, target))
        if not os.path.exists(resolved):
            problems.append(f"Broken relative link: {target}")
    for cm in re.finditer(r"\[(?:Chapter|Ch\.)\s*(\d+)[^\]]*\]\((?:\.\./chapters/)?ch(\d\d)-", text):
        if int(cm.group(1)) != int(cm.group(2)):
            problems.append(f"Chapter link number mismatch: {cm.group(0)}")
    for am in re.finditer(r"\[Appendix ([A-I])[^\]]*\]\((?:\.\./appendices/)?appendix-([a-i])-", text):
        if am.group(1).lower() != am.group(2):
            problems.append(f"Appendix link letter mismatch: {am.group(0)}")

    # Balanced LaTeX $ / $$ and GFM pipe tables (outside fenced/inline code)
    in_display_math = False
    table_cols = None
    table_start_line = None
    for lineno, cleaned, in_fence in strip_fenced_and_inline_code(lines):
        if in_fence:
            if table_cols is not None:
                table_cols = None
            continue

        # Table column count check
        s = cleaned.strip()
        if s.startswith("|") and s.endswith("|") and "|" in s[1:-1]:
            # Count unescaped pipes separating columns
            cols = len(re.split(r"(?<!\\)\|", s.strip("|")))
            if cols > 8:
                warnings.append(f"Line {lineno}: table has {cols} columns (> 8)")
            if table_cols is None:
                table_cols = cols
                table_start_line = lineno
            elif cols != table_cols:
                problems.append(f"Line {lineno}: table column count mismatch ({cols} vs {table_cols} from line {table_start_line})")
        else:
            table_cols = None

        # LaTeX $ / $$ check: strip escaped \$ and currency amounts
        no_esc = strip_currency(cleaned.replace(r"\$", ""))
        # Toggle display math on $$
        parts = no_esc.split("$$")
        if len(parts) > 1:
            # Every $$ toggles display math state
            for idx_p, part in enumerate(parts):
                if idx_p > 0:
                    in_display_math = not in_display_math
                # Check single $ in non-display segments
                if not in_display_math and "$" in part:
                    if part.count("$") % 2 != 0:
                        problems.append(f"Line {lineno}: unbalanced inline LaTeX '$'")
        else:
            if not in_display_math and "$" in no_esc:
                if no_esc.count("$") % 2 != 0:
                    problems.append(f"Line {lineno}: unbalanced inline LaTeX '$'")

    if in_display_math:
        problems.append("Unclosed display math '$$' block at end of file")

    return problems, warnings


def collect_verify_flags(rel_path, full_path):
    """Return list of (rel_path, line_num, snippet) for (verify) markers."""
    hits = []
    for i, line in enumerate(open(full_path, encoding="utf-8"), 1):
        if "(verify)" in line.lower():
            hits.append((rel_path, i, line.strip()[:140]))
    return hits


def extract_dois(rel_path, full_path):
    """Return list of (doi, rel_path, line_num, line_text)."""
    found = []
    for i, line in enumerate(open(full_path, encoding="utf-8"), 1):
        for m in DOI_RE.finditer(line):
            found.append((clean_doi(m.group(0)), rel_path, i, line.strip()))
    return found


def norm_ascii(s):
    return "".join(
        c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)
    ).lower()


def verify_single_doi(doi):
    """Check DOI via Crossref API (with 429 retry), falling back to doi.org handle API."""
    encoded = urllib.parse.quote(doi, safe="")
    cf_url = f"https://api.crossref.org/works/{encoded}"
    headers = {"User-Agent": "dem-handbook-audit/1.0 (mailto:schwehr@gmail.com)"}
    for attempt in range(4):
        try:
            req = urllib.request.Request(cf_url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                msg = json.loads(resp.read().decode("utf-8"))["message"]
                title = (msg.get("title") or [""])[0]
                authors = [a.get("family", "") for a in msg.get("author", [])[:3] if a.get("family")]
                year = None
                for key in ("published-print", "published-online", "issued", "created"):
                    parts = msg.get(key, {}).get("date-parts") or []
                    if parts and parts[0] and parts[0][0]:
                        year = int(parts[0][0])
                        break
                return ("OK", doi, year, authors, title)
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 3:
                time.sleep(0.8 * (2 ** attempt))
                continue
            if e.code not in (404, 400):
                # Fall through to handle lookup on transient throttling
                break
            break
        except Exception:
            if attempt < 2:
                time.sleep(0.5 * (2 ** attempt))
                continue
            break

    # Fallback: doi.org handle resolution (DataCite, Zenodo, NOAA, USGS, or Crossref 429 fallback)
    hdl_url = f"https://doi.org/api/handles/{encoded}"
    try:
        req2 = urllib.request.Request(hdl_url, headers=headers)
        with urllib.request.urlopen(req2, timeout=10) as resp2:
            h = json.loads(resp2.read().decode("utf-8"))
            if h.get("responseCode") == 1:
                return ("HANDLE_OK", doi, None, [], "")
            return ("FAIL", doi, None, [], f"doi.org responseCode={h.get('responseCode')}")
    except Exception as e2:
        return ("FAIL", doi, None, [], f"DOI lookup failed: {e2}")


def check_history_lines(target_files):
    """Fetch schwehr/gis-history README and compare years on ⟨H⟩ lines."""
    try:
        req = urllib.request.Request(GIS_HISTORY_URL, headers={"User-Agent": "dem-handbook-audit/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            gh_text = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"ERROR fetching {GIS_HISTORY_URL}: {e}", file=sys.stderr)
        return 1

    gh_years = set(re.findall(r"\b(?:1[4-9]\d{2}|20[0-2]\d)\b", gh_text))
    print(f"\n=== gis-history ⟨H⟩ check (fetched {len(gh_text)} bytes, {len(gh_years)} distinct years) ===")
    total_h = 0
    flagged = 0
    for rel_path, full_path in target_files:
        for lineno, line in enumerate(open(full_path, encoding="utf-8"), 1):
            if "⟨H⟩" in line:
                total_h += 1
                yrs = re.findall(r"\b(?:1[4-9]\d{2}|20[0-2]\d)\b", line)
                missing_yrs = [y for y in yrs if y not in gh_years]
                if missing_yrs:
                    flagged += 1
                    print(f"  [YEAR_NOT_IN_GH?] {rel_path}:{lineno} missing={missing_yrs} | {line.strip()[:120]}")
    print(f"⟨H⟩ lines checked: {total_h}; lines with years absent from gis-history README: {flagged}")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Fact-check and audit dem-handbook/fable files.")
    parser.add_argument("--check-dois", action="store_true", help="Verify all DOIs via Crossref/doi.org")
    parser.add_argument("--check-history", action="store_true", help="Cross-check ⟨H⟩ dates against schwehr/gis-history")
    parser.add_argument("--quiet", action="store_true", help="Only print failures/warnings")
    parser.add_argument("files", nargs="*", help="Optional relative or absolute file paths to check")
    args = parser.parse_args()

    manifest = load_manifest()
    toc_math_chapters = load_toc_math_chapters()

    if args.files:
        targets = []
        for f in args.files:
            full = os.path.abspath(f) if os.path.isabs(f) else os.path.normpath(os.path.join(ROOT, f))
            rel = os.path.relpath(full, ROOT)
            if not os.path.exists(full):
                print(f"MISSING FILE: {f}", file=sys.stderr)
                sys.exit(1)
            targets.append((rel, full))
    else:
        targets = [(rel, os.path.join(ROOT, rel)) for _, rel, _ in manifest]

    hard_failures = 0
    verify_hits = []
    doi_map = {}

    for rel, full in targets:
        if not os.path.exists(full):
            print(f"MISSING: {rel}")
            hard_failures += 1
            continue
        problems, warnings = check_structure_and_hygiene(rel, full, toc_math_chapters)
        vhits = collect_verify_flags(rel, full)
        verify_hits.extend(vhits)
        for d, f_rel, ln, ltxt in extract_dois(rel, full):
            doi_map.setdefault(d, []).append((f_rel, ln, ltxt))

        hard_failures += len(problems)
        if problems or warnings or not args.quiet:
            status = "FAIL" if problems else ("warn" if warnings else "ok")
            if problems or warnings:
                print(f"[{status}] {rel} ((verify)={len(vhits)})")
                for p in problems:
                    print(f"    FAIL: {p}")
                for w in warnings:
                    print(f"    warn: {w}")

    print(f"\n=== Structural summary: {len(targets)} files checked, hard failures: {hard_failures}, (verify) flags: {len(verify_hits)} ===")
    if verify_hits and not args.quiet:
        for rel, ln, snip in verify_hits[:40]:
            print(f"  (verify) {rel}:{ln}: {snip}")
        if len(verify_hits) > 40:
            print(f"  ... ({len(verify_hits) - 40} more (verify) lines)")

    doi_failures = 0
    doi_mismatches = 0
    if args.check_dois and doi_map:
        unique_dois = sorted(doi_map.keys())
        print(f"\n=== Checking {len(unique_dois)} unique DOIs ===")
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
            results = list(ex.map(verify_single_doi, unique_dois))
        for status, doi, yr, authors, info in results:
            locs = doi_map[doi]
            first_loc = f"{locs[0][0]}:{locs[0][1]}"
            if status == "FAIL":
                doi_failures += 1
                print(f"  [DOI_FAIL] {doi} at {first_loc}: {info} | {locs[0][2][:110]}")
            elif status == "WARN_NET":
                print(f"  [DOI_NET_WARN] {doi} at {first_loc}: {info}")
            elif status == "OK":
                line_norm = norm_ascii(locs[0][2])
                # Check if citation line looks like a bibliography entry with a year
                yr_match = re.findall(r"\b(19\d{2}|20[0-2]\d)\b", locs[0][2])
                if authors:
                    author_hit = any(norm_ascii(a) in line_norm for a in authors if len(a) >= 3)
                    if not author_hit and not re.search(r"https?://", locs[0][2].split("doi")[0]):
                        doi_mismatches += 1
                        print(f"  [AUTHOR_MISMATCH?] {doi} at {first_loc}: Crossref={authors} ({yr}) '{info[:50]}' | line: {locs[0][2][:105]}")
                if yr and yr_match:
                    line_yrs = [int(y) for y in yr_match]
                    if all(abs(ly - yr) > 2 for ly in line_yrs):
                        doi_mismatches += 1
                        print(f"  [YEAR_MISMATCH?] {doi} at {first_loc}: Crossref={yr} vs line={line_yrs} '{info[:50]}' | line: {locs[0][2][:105]}")
        print(f"DOIs checked: {len(unique_dois)}, failures: {doi_failures}, potential author/year mismatches: {doi_mismatches}")

    if args.check_history:
        check_history_lines(targets)

    sys.exit(1 if (hard_failures or doi_failures) else 0)


if __name__ == "__main__":
    main()
