# dsmlp-docs.ucsd.edu

Documentation for UC San Diego's Data Science / Machine Learning Platform
(DSMLP) and related ETS services.

Built with [Jekyll](https://jekyllrb.com/) and wrapped in the
[UC San Diego Decorator 5](https://developer.ucsd.edu/design/decorator/index.html)
page shell.

## Local development

```bash
bundle install
bundle exec jekyll serve
```

## Writing documentation

Everything in `docs/` is plain GitHub Flavored Markdown. No front matter,
no Liquid, no HTML — if it renders on GitHub, it renders here. See
[`docs/markdown-reference.md`](docs/markdown-reference.md) for the supported
syntax, and [`AUTHORING.md`](AUTHORING.md) for how the build turns it into
navigation.

Two conventions:

- **One `#` per file, at the top.** It becomes the page title, the
  breadcrumb, and the sidebar entry.
- **Prefix filenames with `NN-` to order them** (`10-accounts.md`,
  `20-launch.md`). The prefix is stripped from the URL. Without it, pages
  sort alphabetically.

`##` and `###` headings are collected into the sidebar automatically. Don't
hand-maintain a table of contents.

## Layout

```
docs/                       content — vanilla GFM, no front matter
_plugins/vanilla_docs.rb    turns docs/ into pages, nav, and per-page TOCs
_data/navigation.yml        top-level navbar (hand-maintained, on purpose)
_includes/decorator/        Decorator CHROME — copied verbatim, do not edit
_includes/                  canvas partials (breadcrumbs, sidebar nav)
_layouts/                   default + one layout per Decorator template
_sass/_canvas.scss          site styles, all scoped under main#main-content
```

## Before you change anything visual

Read [`DECORATOR.md`](DECORATOR.md). Short version:

- Everything inside `main#main-content` is yours.
- The header, drawer, navbar, and footer are not. They come from
  `ucsd-decorator-v5` and are checked by an integrity gate in CI.
- Decorator's own CSS/JS load from `cdn.ucsd.edu` and must stay that way —
  do not vendor or self-compile them for serving.
- Site CSS must be scoped under the canvas selector. An unscoped
  `.btn { }` reaches into the campus chrome.

## Deployment

Pushes to `main` build and deploy via `.github/workflows/pages.yml`.
