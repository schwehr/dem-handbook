#!/usr/bin/env python3
"""Validate DEM survey planning & execution checklists under checklists/.

Modeled on fable/tools/check_book.py.

Usage:
  python3 checklists/tools/check_checklists.py [--phase0-only | --dir checklists/<modality>] [--quiet] [--self-test]

Exit code 0 if all target files exist and have zero hard failures; 1 otherwise.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from urllib.parse import unquote

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHECKLISTS_DIR = os.path.join(ROOT, "checklists")

PLAN_DOCS_DIR = "plans/01-checklists"
PLAN_DOCS = (
    f"{PLAN_DOCS_DIR}/PRD.md",
    f"{PLAN_DOCS_DIR}/PLAN.md",
    f"{PLAN_DOCS_DIR}/TASKS.md",
)

SHARED_FILES = (
    "template-project-header.md",
    "template-error-budget.md",
    "template-cost-ledger.md",
    "template-insurance-coi.md",
    "template-accident-card.md",
    "template-aar-retrospective.md",
    "multimodal-white-ribbon.md",
)

MODALITIES = (
    "underwater-auv",
    "autonomous-surface-vessel",
    "unols-research-cruise",
    "coastal-bathylidar",
    "land-drone-lidar-imagery",
    "land-aircraft-lidar-imagery",
    "satellite-elevation",
)

MODALITY_FILES = (
    "00-README-and-signoff.md",
    "01-requirements-and-preplanning.md",
    "02-permits-safety-insurance-cost.md",
    "03-platform-sensor-prep-and-support.md",
    "04-mission-or-flight-planning.md",
    "05-underway-qc-and-field-processing.md",
    "06-accidents-and-emergencies.md",
    "07-demob-processing-and-validation.md",
    "08-error-budget-and-retrospective.md",
    "09-resources-and-templates.md",
)

PLANNED_MODALITY_PATHS = frozenset(
    os.path.abspath(os.path.join(CHECKLISTS_DIR, m, f))
    for m in MODALITIES
    for f in MODALITY_FILES
)

WORD_MIN_PHASE0 = 350
WORD_MIN_MODALITY = 600
MIN_GATES_PER_FILE = 5
MIN_TAGGED_PER_FILE = 12

PLACEHOLDER_RE = re.compile(
    r"\bTODO\b|\bTBD\b|lorem\s+ipsum|to\s+be\s+written|\(verify\)",
    re.IGNORECASE,
)

# Matches Markdown link targets inside [...](target#frag) or [...](target "title")
LINK_RE = re.compile(
    r"\]\((?:<([^>#\n]*)(?:#([^>\n]*))?>|([^)#\s\n]*)(?:#([^)\s\n]*))?)"
    r"(?:\s+(?:\"[^\"]*\"|'[^']*'))?\)"
)
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*$")
HTML_ANCHOR_RE = re.compile(
    r"<a\s+[^>]*(?:id|name)\s*=\s*[\"']([^\"']+)[\"'][^>]*>",
    re.IGNORECASE,
)

CHECKBOX_RE = re.compile(r"^\s*[-*]\s+\[([ xX])\]\s*(.*)$")
ESCAPED_CHECKBOX_RE = re.compile(r"^\s*[-*]\s+`\[[ xX]\]`")
TAG_RE = re.compile(r"\*\*\[(GATE|REC|COND)\]\*\*")

PM_NUM_RE = re.compile(r"(?:±|\\pm|\+/-)\s*(?:\\[,;!]|[$~≈])*\s*\d")
STAT_LABEL_RE = re.compile(
    r"RMSE|1\s*σ|2\s*σ|3\s*σ|sigma|\\sigma|95\s*%|90\s*%|"
    r"LE95|LE90|CE90|CE95|TVU|THU|NVA|VVA|NMAD|P95|"
    r"tolerance|bound|envelope|half-width|leveling|levelling",
    re.IGNORECASE,
)

FT_RE = re.compile(r"\b(feet|ft)\b", re.IGNORECASE)
STATUTORY_FT_LINE_RE = re.compile(
    r"14\s*CFR|Part\s*107|91\.211|91\.509|400\s*ft|12,?500\s*ft|14,?000\s*ft|"
    r"15,?000\s*ft|(?:U\.?S\.?\s*)?Survey\s+F(?:oot|eet)|"
    r"International\s+F(?:oot|eet)|USACE",
    re.IGNORECASE,
)
SI_LEN_RE = re.compile(
    r"(?:\b\d[\d.,]*\s*(?:mm|cm|m|km)\b|\d[\d.,]*\s*\\text\{\s*(?:mm|cm|m|km)\s*\})",
    re.IGNORECASE,
)
MI2_RE = re.compile(r"(?:\bmi\s*(?:²|\^2\b)|\bsq\.?\s*mi\b)", re.IGNORECASE)
SI_AREA_RE = re.compile(
    r"(?:\b\d[\d.,]*\s*(?:mm²|mm\^2\b|cm²|cm\^2\b|m²|m\^2\b|km²|km\^2\b|ha\b)|"
    r"\b\d[\d.,]*\s*(?:mm|cm|m|km)\s*²|"
    r"\d[\d.,]*\s*\\text\{\s*(?:m\^2|km\^2|km²|m²|ha)\s*\}|"
    r"(?:/|\bper\s+)km\s*(?:²|\^2\b))",
    re.IGNORECASE,
)

FENCE_OPEN_RE = re.compile(r"^\s*(?:>\s*)?((`{3,})(?=[^`]*$)|~{3,})")


def count_words(text: str) -> int:
    return len(re.findall(r"\S+", text))


def strip_fenced_code_lines(lines: list[str]) -> list[str]:
    """Return lines with fenced code block contents replaced by empty strings (1:1 line indices)."""
    out: list[str] = []
    in_fence = False
    fence_char = ""
    fence_len = 0
    for line in lines:
        if not in_fence:
            m = FENCE_OPEN_RE.match(line)
            if m:
                seq = m.group(1)
                fence_char = seq[0]
                fence_len = len(seq)
                in_fence = True
                out.append("")
            else:
                out.append(line)
        else:
            out.append("")
            close_re = re.compile(
                rf"^\s*(?:>\s*)?{re.escape(fence_char)}{{{fence_len},}}\s*$"
            )
            if close_re.match(line):
                in_fence = False
                fence_char = ""
                fence_len = 0
    return out


def strip_inline_code(line: str) -> str:
    """Strip CommonMark inline backtick spans from a single line, preserving spacing."""
    res: list[str] = []
    i = 0
    n = len(line)
    while i < n:
        if line[i] != "`":
            res.append(line[i])
            i += 1
            continue
        j = i
        while j < n and line[j] == "`":
            j += 1
        tick_len = j - i
        # Search forward for matching closing backtick run of exact length tick_len
        k = j
        found = -1
        while k < n:
            if line[k] == "`":
                m = k
                while m < n and line[m] == "`":
                    m += 1
                if m - k == tick_len:
                    found = m
                    break
                k = m
            else:
                k += 1
        if found != -1:
            res.append(" ")
            i = found
        else:
            res.append(line[i:j])
            i = j
    return "".join(res)


def github_slugify(heading: str) -> str:
    """Convert a Markdown ATX heading to a GitHub-Flavored Markdown anchor slug."""
    text = re.sub(r"\s+#+\s*$", "", heading.strip())
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("`", "").lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    return text.replace(" ", "-")


def extract_anchors(text: str) -> frozenset[str]:
    """Return valid GitHub heading slugs and explicit HTML anchor IDs from Markdown."""
    nofence = strip_fenced_code_lines(text.splitlines())
    anchors: set[str] = set()
    seen_counts: dict[str, int] = {}
    for line in nofence:
        m = HEADING_RE.match(line)
        if m:
            base = github_slugify(m.group(1))
            if base:
                cnt = seen_counts.get(base, 0)
                slug = base if cnt == 0 else f"{base}-{cnt}"
                seen_counts[base] = cnt + 1
                anchors.add(slug)
        for hm in HTML_ANCHOR_RE.finditer(line):
            anchors.add(hm.group(1).strip().lower())
    return frozenset(anchors)


def check_links_and_placeholders(
    path: str,
    nocode_lines: list[str],
    failures: list[str],
    *,
    allow_planned_modality_links: bool = False,
    root_dir: str = ROOT,
    anchor_cache: dict[str, frozenset[str]] | None = None,
) -> tuple[int, int, int, int]:
    """Check relative links, #anchors, and placeholders on fence+inline-code-stripped lines.

    Returns (valid_fable_links, valid_gemini4_links, valid_shared_links, pending_modality_links).
    """
    parent = os.path.dirname(path)
    abs_root = os.path.abspath(root_dir)
    fable_dir = os.path.join(abs_root, "fable") + os.sep
    gemini4_dir = os.path.join(abs_root, "gemini4") + os.sep
    shared_dir = os.path.join(abs_root, "checklists", "_shared") + os.sep
    cache = anchor_cache if anchor_cache is not None else {}

    def get_anchors(file_path: str) -> frozenset[str]:
        if file_path not in cache:
            with open(file_path, encoding="utf-8") as afh:
                cache[file_path] = extract_anchors(afh.read())
        return cache[file_path]

    fable_links = 0
    gemini4_links = 0
    shared_links = 0
    pending_modality_links = 0

    for lineno, line in enumerate(nocode_lines, 1):
        ph = PLACEHOLDER_RE.search(line)
        if ph:
            failures.append(f"line {lineno}: placeholder '{ph.group(0)}' found")

        for m in LINK_RE.finditer(line):
            if m.group(1) is not None or m.group(2) is not None:
                target = m.group(1) or ""
                fragment = m.group(2)
            else:
                target = m.group(3) or ""
                fragment = m.group(4)

            if SCHEME_RE.match(target):
                continue
            if target.startswith("/"):
                failures.append(
                    f"line {lineno}: absolute path link '{target}' forbidden (use relative path)"
                )
                continue
            if not target and fragment is None:
                continue
            if not target and fragment is not None:
                frag_norm = unquote(fragment).strip().lower()
                if not frag_norm or frag_norm not in get_anchors(os.path.abspath(path)):
                    failures.append(
                        f"line {lineno}: broken intra-file #anchor '#{fragment}'"
                    )
                continue

            resolved = os.path.normpath(os.path.join(parent, target))
            abs_resolved = os.path.abspath(resolved)
            if abs_resolved != abs_root and not abs_resolved.startswith(abs_root + os.sep):
                failures.append(
                    f"line {lineno}: link '{target}' escapes repository root"
                )
                continue
            if not os.path.isfile(resolved):
                if allow_planned_modality_links and abs_resolved in PLANNED_MODALITY_PATHS:
                    pending_modality_links += 1
                    continue
                failures.append(f"line {lineno}: broken link '{target}'")
                continue
            if fragment is not None:
                frag_norm = unquote(fragment).strip().lower()
                if not frag_norm or frag_norm not in get_anchors(abs_resolved):
                    failures.append(
                        f"line {lineno}: broken #anchor '#{fragment}' in '{target}'"
                    )
                    continue
            if abs_resolved.startswith(fable_dir) or target.startswith("../../fable/"):
                fable_links += 1
            elif abs_resolved.startswith(gemini4_dir) or target.startswith("../../gemini4/"):
                gemini4_links += 1
            elif abs_resolved.startswith(shared_dir) or target.startswith("../_shared/"):
                shared_links += 1

    return fable_links, gemini4_links, shared_links, pending_modality_links


def check_warnings(
    nofence_lines: list[str],
    nocode_lines: list[str],
    warnings: list[str],
    *,
    warn_escaped_checkbox: bool = False,
) -> None:
    """Check unqualified ±/\\pm/+/- (incl. inline code) and bare ft/mi² without SI units."""
    for lineno, (nf_line, nc_line) in enumerate(zip(nofence_lines, nocode_lines), 1):
        if PM_NUM_RE.search(nf_line) and not STAT_LABEL_RE.search(nf_line):
            warnings.append(
                f"line {lineno}: unqualified '±' without statistic/confidence label"
            )
        if warn_escaped_checkbox and ESCAPED_CHECKBOX_RE.match(nf_line):
            warnings.append(
                f"line {lineno}: backtick-escaped checkbox '- `[ ]`' will not render"
            )
        for m in FT_RE.finditer(nc_line):
            if STATUTORY_FT_LINE_RE.search(nc_line):
                continue
            prefix = nc_line[: m.start()]
            if SI_LEN_RE.search(prefix):
                continue
            warnings.append(
                f"line {lineno}: bare '{m.group(0)}' without SI primary unit"
            )
        for m in MI2_RE.finditer(nc_line):
            if re.search(r"\bUSACE\b", nc_line):
                continue
            prefix = nc_line[: m.start()]
            if SI_AREA_RE.search(prefix):
                continue
            warnings.append(
                f"line {lineno}: bare '{m.group(0)}' without SI primary area unit"
            )


def check_mandatory_header(lines: list[str], failures: list[str]) -> None:
    """Verify PLAN.md §2.1 mandatory '# ' H1 and '> ' blockquote header on modality 01..08."""
    if not lines or not lines[0].startswith("# "):
        failures.append("missing H1 heading starting with '# ' on line 1")
        return

    idx = 1
    while idx < len(lines) and not lines[idx].strip():
        idx += 1

    bq_lines: list[str] = []
    while idx < len(lines) and lines[idx].lstrip().startswith(">"):
        bq_lines.append(lines[idx])
        idx += 1

    if not bq_lines:
        failures.append("missing mandatory '> ' blockquote header block after H1")
        return

    bq = "\n".join(bq_lines)
    required_patterns = (
        ("Project / Cruise / Sortie ID", r"Project\s*/\s*Cruise\s*/\s*Sortie\s+ID"),
        ("Modality", r"\bModality\b"),
        ("Horizontal CRS / Epoch", r"Horizontal\s+CRS\s*/\s*Epoch"),
        ("Vertical Datum", r"Vertical\s+Datum"),
        ("Sign Convention", r"Sign\s+Convention"),
    )
    for label, pat in required_patterns:
        if not re.search(pat, bq, re.IGNORECASE):
            failures.append(f"header blockquote missing '{label}'")

    if "Elevation (+z" not in bq:
        failures.append("header blockquote missing 'Elevation (+z'")
    if "Depth (+d" not in bq:
        failures.append("header blockquote missing 'Depth (+d'")


def check_checkboxes(nofence_lines: list[str], failures: list[str]) -> tuple[int, int]:
    """Verify all checkboxes in modality 01..08 carry [GATE]/[REC]/[COND] and meet counts."""
    gate_count = 0
    tagged_count = 0
    for lineno, line in enumerate(nofence_lines, 1):
        if ESCAPED_CHECKBOX_RE.match(line):
            failures.append(
                f"line {lineno}: backtick-escaped checkbox '- `[ ]`' bypasses tag enforcement"
            )
            continue
        m = CHECKBOX_RE.match(line)
        if not m:
            continue
        tag_m = TAG_RE.search(line)
        if not tag_m:
            failures.append(
                f"line {lineno}: checkbox missing **[GATE]**, **[REC]**, or **[COND]**"
            )
            continue
        tagged_count += 1
        if tag_m.group(1) == "GATE":
            gate_count += 1

    if gate_count < MIN_GATES_PER_FILE:
        failures.append(f"only {gate_count} [GATE] items (<{MIN_GATES_PER_FILE})")
    if tagged_count < MIN_TAGGED_PER_FILE:
        failures.append(f"only {tagged_count} tagged items (<{MIN_TAGGED_PER_FILE})")
    return gate_count, tagged_count


def validate_file(
    rel_path: str,
    kind: str,
    *,
    phase0_only: bool = False,
) -> dict[str, object]:
    """Validate a single Markdown file and return structured metrics/findings."""
    full_path = os.path.join(ROOT, rel_path)
    failures: list[str] = []
    warnings: list[str] = []
    stats: dict[str, object] = {
        "rel_path": rel_path,
        "kind": kind,
        "exists": False,
        "words": 0,
        "gates": "-",
        "tagged": "-",
        "fable_links": 0,
        "gemini4_links": 0,
        "shared_links": 0,
        "pending_modality_links": 0,
        "failures": failures,
        "warnings": warnings,
    }

    if not os.path.isfile(full_path):
        failures.append("missing file")
        return stats

    stats["exists"] = True
    with open(full_path, encoding="utf-8") as fh:
        text = fh.read()

    words = count_words(text)
    stats["words"] = words
    lines = text.splitlines()
    nofence_lines = strip_fenced_code_lines(lines)
    nocode_lines = [strip_inline_code(l) for l in nofence_lines]

    if kind in ("readme", "shared"):
        if words < WORD_MIN_PHASE0:
            failures.append(f"stub file ({words} words < {WORD_MIN_PHASE0})")
    elif kind.startswith("modality_"):
        if words < WORD_MIN_MODALITY:
            failures.append(f"stub file ({words} words < {WORD_MIN_MODALITY})")

    fable_links, gemini4_links, shared_links, pending_links = check_links_and_placeholders(
        full_path,
        nocode_lines,
        failures,
        allow_planned_modality_links=phase0_only,
    )
    stats["fable_links"] = fable_links
    stats["gemini4_links"] = gemini4_links
    stats["shared_links"] = shared_links
    stats["pending_modality_links"] = pending_links

    if kind != "plan_doc":
        check_warnings(
            nofence_lines,
            nocode_lines,
            warnings,
            warn_escaped_checkbox=kind in ("readme", "shared", "modality_00", "modality_09"),
        )

    if kind == "modality_01_08":
        check_mandatory_header(lines, failures)
        gates, tagged = check_checkboxes(nofence_lines, failures)
        stats["gates"] = gates
        stats["tagged"] = tagged

    if kind in ("shared", "modality_00", "modality_01_08", "modality_09"):
        if fable_links < 1:
            failures.append("missing valid fable/ cross-link (>=1 required)")
        if gemini4_links < 1:
            failures.append("missing valid gemini4/ cross-link (>=1 required)")

    return stats


def resolve_modality_dir(raw_dir: str) -> str:
    """Normalize --dir argument to one of the 7 modality slugs."""
    norm = os.path.normpath(raw_dir).replace("\\", "/")
    if norm.startswith("./"):
        norm = norm[2:]
    if norm.startswith("checklists/"):
        slug = norm[len("checklists/") :]
    else:
        abs_in = os.path.abspath(raw_dir)
        prefix = os.path.abspath(CHECKLISTS_DIR) + os.sep
        if abs_in.startswith(prefix):
            slug = abs_in[len(prefix) :].replace("\\", "/")
        else:
            slug = norm
    slug = slug.strip("/")
    if slug not in MODALITIES:
        valid = ", ".join(f"checklists/{m}" for m in MODALITIES)
        raise ValueError(f"Unknown modality directory '{raw_dir}'. Expected one of: {valid}")
    return slug


def run_self_tests() -> tuple[bool, int]:
    """Run deterministic in-memory and temporary-directory unit tests for the validator."""
    checks = 0

    # 1. Fence and inline code stripping
    fenced = strip_fenced_code_lines(["ok", "```python", "TODO", "```", "~~~", "TBD", "~~~", "after"])
    assert fenced == ["ok", "", "", "", "", "", "", "after"], fenced
    checks += 1
    assert "TODO" not in strip_inline_code("see `TODO` and `` `±5 m` `` end")
    checks += 1

    # 2. GitHub heading slugify + duplicate heading deduplication
    anchors = extract_anchors(
        "# Title One & Two\n## Repeat\n## Repeat\n<a id='custom-id'></a>\n```md\n# Ignored\n```"
    )
    assert anchors == frozenset({"title-one--two", "repeat", "repeat-1", "custom-id"}), anchors
    checks += 1

    # 3. Warnings: inline ±, \pm\,, ±$, bare draft/bias vs labeled, ft and mi²
    nf = [
        "Inline `±0.05 m` unlabeled",
        r"LaTeX $\pm\,0.05\text{ m}$",
        "Dollar ±$0.05$ m",
        "Vessel draft ±0.10 m without stat",
        "Line bias ±0.10 m without stat",
        "Tolerance ±0.10 m (RMSE)",
        "Ceiling 5000 ft unlabeled",
        "Ceiling 122 m (400 ft) AGL",
        "Cost $1,000/mi² alone",
        "Cost ~$385+/km² (~$1,000+/mi²)",
        "- `[ ]` Escaped box",
    ]
    nc = [strip_inline_code(l) for l in nf]
    w: list[str] = []
    check_warnings(nf, nc, w, warn_escaped_checkbox=True)
    warn_lines = [int(msg.split()[1].rstrip(":")) for msg in w]
    assert warn_lines == [1, 2, 3, 4, 5, 7, 9, 11], f"unexpected warnings: {w}"
    checks += 1

    # 4. Escaped checkbox hard failure + mandatory header checks
    cb_fail: list[str] = []
    check_checkboxes(["- `[ ]` **[GATE]** sneaky"], cb_fail)
    assert len(cb_fail) == 3, cb_fail  # escaped checkbox + <5 GATE + <12 tagged
    checks += 1

    hdr_ok: list[str] = []
    check_mandatory_header(
        [
            "# Modality — Phase",
            "",
            "> **Project / Cruise / Sortie ID:** `P1` | **Modality:** `auv`",
            "> **Horizontal CRS / Epoch:** `ITRF2020` | **Vertical Datum / Geoid or SEP:** `MLLW`",
            "> **Sign Convention:** `[ ] Elevation (+z ↑, m)` `[ ] Depth (+d ↓, m)` | **Phase Lead:** `x`",
        ],
        hdr_ok,
    )
    assert not hdr_ok, hdr_ok
    checks += 1

    # 5. Relative, absolute, escaping, and #anchor links in a temp repo
    with tempfile.TemporaryDirectory() as tmpdir:
        sub = os.path.join(tmpdir, "checklists", "auv")
        fable_ch = os.path.join(tmpdir, "fable", "chapters")
        g4_sec = os.path.join(tmpdir, "gemini4", "book", "ch-01")
        os.makedirs(sub, exist_ok=True)
        os.makedirs(fable_ch, exist_ok=True)
        os.makedirs(g4_sec, exist_ok=True)
        mod_file = os.path.join(sub, "01.md")
        with open(os.path.join(fable_ch, "ch01.md"), "w", encoding="utf-8") as fh:
            fh.write("# Chapter One\n## Sub Section\n")
        with open(os.path.join(g4_sec, "sec-01-01.md"), "w", encoding="utf-8") as fh:
            fh.write("# Intro\n")
        with open(mod_file, "w", encoding="utf-8") as fh:
            fh.write("# Self\n## Local Sec\n")

        link_fails: list[str] = []
        test_lines = [
            "[ok](../../fable/chapters/ch01.md#sub-section)",
            "[g4](../../gemini4/book/ch-01/sec-01-01.md)",
            "[intra](#local-sec)",
            "[bad_intra](#nope)",
            "[bad_cross](../../fable/chapters/ch01.md#missing)",
            "[abs](/etc/passwd)",
            "[escape](../../../outside.md)",
            "[dir](../../fable/chapters)",
        ]
        fl, gl, sl, pl = check_links_and_placeholders(
            mod_file, test_lines, link_fails, root_dir=tmpdir
        )
        assert (fl, gl, sl, pl) == (1, 1, 0, 0), (fl, gl, sl, pl)
        assert len(link_fails) == 5, link_fails
        checks += 1

    return True, checks


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate DEM survey checklists, shared templates, and planning docs."
    )
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument(
        "--phase0-only",
        action="store_true",
        help="Validate plans/01-checklists/{PRD,PLAN,TASKS}.md, checklists/README.md, and checklists/_shared/*.md.",
    )
    scope.add_argument(
        "--dir",
        metavar="PATH",
        help="Validate 00..09.md inside one modality directory (e.g., checklists/underwater-auv).",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Print summary plus files with failures/warnings only.",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run built-in unit self-tests (standalone if no --phase0-only/--dir is given).",
    )
    args = parser.parse_args()

    if args.self_test:
        try:
            ok, n_checks = run_self_tests()
        except AssertionError as exc:
            print(f"[self-test] FAIL: {exc}", file=sys.stderr)
            return 1
        print(f"[self-test] PASS ({n_checks}/{n_checks} test groups passed)")
        if not args.phase0_only and not args.dir:
            return 0 if ok else 1

    targets: list[tuple[str, str]] = []
    modalities_to_check: tuple[str, ...] = ()

    if args.dir:
        try:
            slug = resolve_modality_dir(args.dir)
        except ValueError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
        modalities_to_check = (slug,)
    elif args.phase0_only:
        for fn in PLAN_DOCS:
            targets.append((fn, "plan_doc"))
        targets.append(("checklists/README.md", "readme"))
        for fn in SHARED_FILES:
            targets.append((f"checklists/_shared/{fn}", "shared"))
    else:
        for fn in PLAN_DOCS:
            targets.append((fn, "plan_doc"))
        targets.append(("checklists/README.md", "readme"))
        for fn in SHARED_FILES:
            targets.append((f"checklists/_shared/{fn}", "shared"))
        modalities_to_check = MODALITIES

    for slug in modalities_to_check:
        for fn in MODALITY_FILES:
            if fn.startswith("00-"):
                kind = "modality_00"
            elif fn.startswith("09-"):
                kind = "modality_09"
            else:
                kind = "modality_01_08"
            targets.append((f"checklists/{slug}/{fn}", kind))

    results = [
        validate_file(rel_path, kind, phase0_only=args.phase0_only)
        for rel_path, kind in targets
    ]

    # Enforce per-modality valid ../_shared/ links requirement across 00..09.md
    for slug in modalities_to_check:
        mod_prefix = f"checklists/{slug}/"
        mod_results = [r for r in results if str(r["rel_path"]).startswith(mod_prefix)]
        total_shared = sum(int(r["shared_links"]) for r in mod_results)
        if total_shared < 1 and mod_results:
            mod_results[0]["failures"].append(  # type: ignore[union-attr]
                f"modality '{slug}' has 0 valid ../_shared/ links across 00..09.md (>=1 required)"
            )

    total_files = len(results)
    present_files = sum(1 for r in results if r["exists"])
    total_words = sum(int(r["words"]) for r in results)
    total_failures = sum(len(r["failures"]) for r in results)  # type: ignore[arg-type]
    total_warnings = sum(len(r["warnings"]) for r in results)  # type: ignore[arg-type]
    total_pending = sum(int(r["pending_modality_links"]) for r in results)

    if not args.quiet:
        print(f"{'words':>6} {'G':>3} {'T':>3} {'F':>2} {'G4':>2} {'S':>2}  {'file':<58} status")
    for r in results:
        failures: list[str] = r["failures"]  # type: ignore[assignment]
        warnings: list[str] = r["warnings"]  # type: ignore[assignment]
        status = "FAIL" if failures else ("warn" if warnings else "ok")
        if args.quiet and status == "ok":
            continue
        print(
            f"{r['words']:>6} {str(r['gates']):>3} {str(r['tagged']):>3} "
            f"{r['fable_links']:>2} {r['gemini4_links']:>2} {r['shared_links']:>2}  "
            f"{str(r['rel_path']):<58} [{status}]"
        )
        for msg in failures:
            print(f"       FAIL: {msg}")
        for msg in warnings:
            print(f"       warn: {msg}")

    pending_note = (
        f"   pending Phase 1-7 links: {total_pending}" if total_pending else ""
    )
    print(
        f"\nfiles present: {present_files}/{total_files}   "
        f"total words: {total_words:,}   "
        f"hard failures: {total_failures}   "
        f"warnings: {total_warnings}{pending_note}"
    )
    return 1 if (present_files < total_files or total_failures > 0) else 0


if __name__ == "__main__":
    sys.exit(main())
