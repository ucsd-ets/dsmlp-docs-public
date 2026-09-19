#!/usr/bin/env python3
"""Import the authored drafts from ucsd-ets/dsmlp-doc-revise into docs/.

Usage:
    python3 tools/import-docs.py ../dsmlp-doc-revise/updated-docs

The source is vanilla GFM with no front matter, authored to be read on GitHub.
Three transforms are applied on every import, so a re-import never regresses.

1. DIRECTORY LINKS.  The drafts link to a section as `](../grading/)`, correct
   on GitHub, where it renders that directory's README.md. MkDocs publishes
   pages at directory URLs (reference/glossary.md -> /reference/glossary/), so a
   link it does not recognise as a document is passed through untouched and
   then resolves RELATIVE TO THE PAGE: from /reference/glossary/, `../grading/`
   lands on /reference/grading/, a 404. Rewriting to `](../grading/README.md)`
   fixes it and still works on GitHub.

2. LEADING INTERNAL NOTES.  Each technical page opens with a
   `> **Draft for review.**` blockquote addressed to the writing team --
   unverified claims, decisions awaiting a person, figures that do not exist.
   That is editorial apparatus, not reader documentation, so it is dropped here.
   It stays in the upstream repository, which is where it is worked on.

   Measured on the first import: exactly one blockquote per noted page, always
   in the same position, and no page anywhere in the set uses a blockquote for
   anything else -- so this cannot swallow real content. The importer asserts
   that invariant and fails loudly if a future import breaks it.

3. CONTRIBUTOR-FACING README SECTIONS.  The root README's "Status of This
   Documentation" and "Conventions" sections address editors, not readers, and
   the first becomes actively false once (2) has run -- it tells the reader that
   every technical page opens with a note.

What is NOT touched: heading anchors (tools/hooks.py makes MkDocs generate
GitHub-compatible ids instead) and the `<!-- FIGURE: ... -->` markers in page
bodies, which tools/hooks.py renders as a visible placeholder so a missing
number reads as missing rather than as a blank cell.
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

DEST = Path(__file__).resolve().parent.parent / "docs"

# ](some-dir/) or ](../some-dir/) -- a bare directory link, no file, no anchor.
DIR_LINK = re.compile(r"\]\((\.{0,2}/?(?:[\w.-]+/)*[\w-]+/)\)")

NOTE_OPENER = "> **Draft for review.**"
RULE = re.compile(r"^-{3,}\s*$")

# Sections of the root README that address editors rather than readers.
DROP_README_SECTIONS = ("Status of This Documentation", "Conventions")


def normalize_dir_links(text: str) -> tuple[str, int]:
    count = 0

    def sub(m: re.Match) -> str:
        nonlocal count
        count += 1
        return f"]({m.group(1)}README.md)"

    return DIR_LINK.sub(sub, text), count


def strip_leading_note(text: str) -> tuple[str, bool]:
    """Drop a leading `> **Draft for review.**` blockquote, and the horizontal
    rule that separates it from the title."""
    lines = text.split("\n")
    start = next((i for i, l in enumerate(lines) if l.startswith(NOTE_OPENER)), None)
    if start is None:
        return text, False

    # Everything above the note must be the H1, blank lines and at most one rule.
    # If real prose sits above it, this is not the leading note; leave it alone.
    rule_at = None
    for i, line in enumerate(lines[:start]):
        s = line.strip()
        if not s or line.startswith("# "):
            continue
        if RULE.match(s) and rule_at is None:
            rule_at = i
            continue
        return text, False

    end = start
    while end < len(lines) and (lines[end].startswith(">") or lines[end].strip() == ">"):
        end += 1
    while end < len(lines) and not lines[end].strip():
        end += 1

    keep = lines[:start] + lines[end:]
    if rule_at is not None:
        del keep[rule_at]
    # Collapse the blank run left behind under the title.
    out = "\n".join(keep)
    return re.sub(r"(^# [^\n]*\n)\n{2,}", r"\1\n", out), True


def strip_sections(text: str, titles: tuple[str, ...]) -> tuple[str, int]:
    """Remove `## <title>` through to the next heading of the same level."""
    removed = 0
    for title in titles:
        pattern = re.compile(
            r"^##[ \t]+" + re.escape(title) + r"[ \t]*$.*?(?=^##[ \t]|\Z)",
            re.M | re.S,
        )
        text, n = pattern.subn("", text)
        removed += n
    return re.sub(r"\n{3,}", "\n\n", text).rstrip() + "\n", removed


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2

    src = Path(argv[1]).resolve()
    if not src.is_dir():
        print(f"error: {src} is not a directory")
        return 1

    # Invariant check against the source, before anything is written: a page
    # must not use a blockquote for anything but its leading note.
    offenders = []
    for md in sorted(src.rglob("*.md")):
        lines = md.read_text(encoding="utf-8").split("\n")
        blocks = [
            i
            for i, l in enumerate(lines)
            if l.startswith("> ") and (i == 0 or not lines[i - 1].startswith(">"))
        ]
        if len(blocks) > 1:
            offenders.append(f"{md.relative_to(src)} has {len(blocks)} blockquotes")
    if offenders:
        print("refusing to import: blockquotes are no longer note-only, so")
        print("stripping the leading note could remove real content.")
        for o in offenders:
            print(f"  {o}")
        print("\nreview these pages and update strip_leading_note() before retrying.")
        return 1

    if DEST.exists():
        shutil.rmtree(DEST)
    shutil.copytree(src, DEST)

    links = notes = sections = 0
    for md in sorted(DEST.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        original = text

        text, n = normalize_dir_links(text)
        links += n

        text, stripped = strip_leading_note(text)
        notes += 1 if stripped else 0

        if md.name == "README.md" and md.parent == DEST:
            text, n = strip_sections(text, DROP_README_SECTIONS)
            sections += n

        if text != original:
            md.write_text(text, encoding="utf-8")

    pages = sum(1 for _ in DEST.rglob("*.md"))
    print(f"imported {pages} pages from {src}")
    print(f"  normalized {links} directory links")
    print(f"  stripped {notes} leading 'Draft for review' notes")
    print(f"  stripped {sections} contributor-facing README sections")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
