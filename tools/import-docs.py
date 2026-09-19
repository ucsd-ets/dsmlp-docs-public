#!/usr/bin/env python3
"""Import the authored drafts from ucsd-ets/dsmlp-doc-revise into docs/.

Usage:
    python3 tools/import-docs.py ../dsmlp-doc-revise/updated-docs

The source is vanilla GFM with no front matter and is authored to be read on
GitHub. One transform is needed to make it build correctly here, and it is
applied on every import so a re-import never regresses:

  Directory links.  The drafts link to a section as `](../grading/)`, which is
  correct on GitHub -- it renders that directory's README.md. MkDocs publishes
  pages at directory URLs (reference/glossary.md -> /reference/glossary/), so a
  link it does not recognise as a document is passed through untouched and then
  resolves RELATIVE TO THE PAGE: from /reference/glossary/, `../grading/`
  resolves to /reference/grading/, which is a 404.

  Rewriting to `](../grading/README.md)` fixes it and still works on GitHub,
  because MkDocs then knows it is a document and rewrites the href correctly.

Anything else is left exactly as written. Heading anchors are NOT rewritten --
tools/hooks.py makes MkDocs generate GitHub-compatible ids instead, so the
drafts' own `#peak--off-peak-hours` style links resolve without editing them.
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

# ](some-dir/) or ](../some-dir/) -- a bare directory link, no file, no anchor.
DIR_LINK = re.compile(r"\]\((\.{0,2}/?(?:[\w.-]+/)*[\w-]+/)\)")

DEST = Path(__file__).resolve().parent.parent / "docs"


def normalize(text: str) -> tuple[str, int]:
    count = 0

    def sub(m: re.Match) -> str:
        nonlocal count
        count += 1
        return f"]({m.group(1)}README.md)"

    return DIR_LINK.sub(sub, text), count


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2

    src = Path(argv[1]).resolve()
    if not src.is_dir():
        print(f"error: {src} is not a directory")
        return 1

    if DEST.exists():
        shutil.rmtree(DEST)
    shutil.copytree(src, DEST)

    total_links = 0
    touched = 0
    for md in sorted(DEST.rglob("*.md")):
        original = md.read_text(encoding="utf-8")
        rewritten, n = normalize(original)
        if n:
            md.write_text(rewritten, encoding="utf-8")
            total_links += n
            touched += 1

    pages = sum(1 for _ in DEST.rglob("*.md"))
    print(f"imported {pages} pages from {src}")
    print(f"normalized {total_links} directory links across {touched} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
