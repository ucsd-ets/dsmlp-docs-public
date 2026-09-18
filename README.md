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

## Layout

```
_data/navigation.yml        site nav (the <li> links only)
_includes/decorator/        Decorator CHROME — copied verbatim, do not edit
_includes/                  canvas partials (breadcrumbs, sidebar nav)
_layouts/                   default + one layout per Decorator template
_sass/_canvas.scss          site styles, all scoped under main#main-content
docs/                       content
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
