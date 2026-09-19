# dsmlp-docs.ucsd.edu

Documentation for UC San Diego's **Datahub** and **Data Science & Machine
Learning Platform (DSMLP)**.

Built with [MkDocs](https://www.mkdocs.org/) and a bespoke theme carrying the
[UC San Diego Decorator 5](https://developer.ucsd.edu/design/decorator/index.html)
page shell.

> **The content is drafts.** It was imported from
> [`ucsd-ets/dsmlp-doc-revise`](https://github.com/ucsd-ets/dsmlp-doc-revise).
> Every page carries a draft banner, and unpublished figures render as visible
> placeholders. The per-page writer's notes are stripped on import and remain
> upstream — read them there before treating any page as final.

## Local development

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

## Writing documentation

Everything in `docs/` is plain GitHub Flavored Markdown. No front matter, no
template tags, no HTML. If it renders on GitHub, it renders here — heading
anchors included, which is deliberate and is what `tools/hooks.py` exists for.

Two conventions:

- **One `#` per file, at the top.** It becomes the page title, the breadcrumb,
  and the sidebar entry.
- **Link to a section's `README.md`, not to its directory.** Write
  `[Grading](../grading/README.md)`, not `[Grading](../grading/)`. Both work on
  GitHub; only the first survives MkDocs' directory URLs. CI fails on the
  second.

`##` and `###` headings are collected into the sidebar automatically — don't
hand-maintain a table of contents. Page order and section grouping come from
the `nav:` block in `mkdocs.yml`.

See [`AUTHORING.md`](AUTHORING.md) for the full picture.

## Re-importing the drafts

```bash
python3 tools/import-docs.py ../dsmlp-doc-revise/updated-docs
```

Replaces `docs/`, normalizes directory links, and strips the upstream
editorial notes (the leading `> **Draft for review.**` blockquote on each
technical page, plus the README's contributor-facing sections). Re-run it
whenever the upstream drafts move; then update `nav:` in `mkdocs.yml` if pages
were added or renamed.

The site-wide draft banner comes from `extra.draft_banner` in `mkdocs.yml` —
clear that one value to remove it from every page once the content is signed
off.

## Layout

```
docs/                    content — vanilla GFM, no front matter
mkdocs.yml               nav, markdown extensions, link validation
theme/                   the Decorator chrome AS the MkDocs theme
  partials/chrome-*.html   CHROME — copied verbatim, do not edit
  partials/breadcrumbs,sidebar  canvas partials, generated
  css/site.css           site styles, all scoped under main#main-content
tools/hooks.py           GitHub-compatible anchors + alert callouts
tools/import-docs.py     re-import the upstream drafts
tools/check-links.py     dead link/anchor check over the built HTML
```

## Search

Site search is lunr, in the canvas: a box in the sidebar and results on
`/search/`. It is separate from the two Decorator search boxes in the header,
which search all of UC San Diego. Only `/search/` loads the search index, so
it costs nothing on the other pages. See [`AUTHORING.md`](AUTHORING.md#search).

## Before you change anything visual

Read [`DECORATOR.md`](DECORATOR.md). Short version:

- Everything inside `main#main-content` is yours.
- The header, drawer, navbar, and footer are not. They come from
  `ucsd-decorator-v5` and are checked by an integrity gate in CI.
- Decorator's own CSS/JS load from `cdn.ucsd.edu` and must stay that way —
  do not vendor or self-compile them for serving.
- Site CSS must be scoped under `main#main-content`. An unscoped `.btn { }`
  reaches into the campus chrome, and CI fails on it.

## Deployment

Pushes to `main` build and deploy via `.github/workflows/build-and-deploy.yml`.
The build runs `mkdocs build --strict`, so a broken cross-reference fails CI
rather than shipping.

## Why MkDocs

[`SSG-OPTIONS.md`](SSG-OPTIONS.md) compares MkDocs, Jekyll and Docusaurus,
measured with UCSD's own chrome integrity gate.
