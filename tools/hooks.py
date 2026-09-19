"""MkDocs build hooks.

GitHub alert callouts (`> [!NOTE]`) are not native to Python-Markdown, which
renders them as a blockquote with a literal "[!NOTE]" in the body text.

This is harder than the kramdown equivalent for a specific reason worth
recording: Python-Markdown merges consecutive blank-line-separated blockquotes
into ONE <blockquote> with several <p> children, where GitHub and kramdown keep
them separate. So this cannot simply match a blockquote -- it has to split
inside one at every [!TYPE] paragraph, or the second and third callout get
silently swallowed into the first.
"""

import re
import unicodedata

ALERTS = "NOTE|TIP|IMPORTANT|WARNING|CAUTION"
BLOCKQUOTE = re.compile(r"<blockquote>(.*?)</blockquote>", re.S)
MARKER = re.compile(r"<p>\s*\[!(" + ALERTS + r")\]\s*(?:<br\s*/?>)?\s*", re.I)


def _callout(kind: str, inner: str) -> str:
    return (
        f'<div class="docs-note docs-note--{kind.lower()}">'
        f'<p class="docs-note__label">{kind.capitalize()}</p>{inner.strip()}</div>'
    )


def _split_blockquote(match: re.Match) -> str:
    inner = match.group(1)
    hits = list(MARKER.finditer(inner))
    if not hits:
        return match.group(0)

    out = []
    head = inner[: hits[0].start()].strip()
    if head:
        out.append(f"<blockquote>{head}</blockquote>")

    for i, hit in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(inner)
        body = inner[hit.end() : end].strip()
        # The marker consumed the opening <p>, so re-open the first paragraph.
        if body and not body.startswith("<"):
            body = "<p>" + body
        out.append(_callout(hit.group(1), body))
    return "".join(out)


def on_page_content(html: str, page=None, config=None, files=None) -> str:
    return BLOCKQUOTE.sub(_split_blockquote, html)

# --------------------------------------------------------------------------
# GitHub-compatible heading anchors
# --------------------------------------------------------------------------
#
# The docs are authored as vanilla GFM and previewed on GitHub, so in-page
# anchors are written the way GitHub generates them. GitHub and Python-Markdown
# disagree on one rule:
#
#   GitHub DELETES punctuation. Python-Markdown REPLACES it with the separator
#   and collapses runs. For "Peak & Off-Peak Hours":
#
#       GitHub          ->  peak--off-peak-hours
#       Python-Markdown ->  peak-off-peak-hours
#
# Measured on import of the dsmlp-doc-revise content: 34 cross-page anchor
# links were broken by exactly this, every one a heading containing "&" or ",".
#
# Installed from on_config rather than declared in mkdocs.yml, because a
# `!!python/name:` reference would need the project root on PYTHONPATH and
# mkdocs does not add it. Hook modules are loaded by path, so this always works.

_HTML_TAG = re.compile(r"<[!/a-z].*?>", re.I)
_STRIP_PUNCT = re.compile(r"[^\w\s-]", re.UNICODE)


def github_slugify(value, separator="-"):
    """Slugify a heading the way github-slugger does."""
    text = unicodedata.normalize("NFKC", str(value))
    text = _HTML_TAG.sub("", text)
    text = text.strip().lower()
    text = _STRIP_PUNCT.sub("", text)
    return text.replace(" ", separator)


def on_config(config):
    toc = config["mdx_configs"].setdefault("toc", {})
    toc["slugify"] = github_slugify
    return config
