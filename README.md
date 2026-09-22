# dsmlp-docs.ucsd.edu

Documentation for UC San Diego's **Datahub** and **Data Science & Machine
Learning Platform (DSMLP)**.

**Read it at <https://dsmlp-docs.ucsd.edu/>.**

## This repository is a published snapshot

The pages here are generated automatically from a privately maintained source
repository. Nobody commits to this repository by hand, and anything committed
here directly is overwritten by the next publish.

### Found a problem? Want something changed?

**[Open an issue](../../issues/new/choose).** That is the fastest route and the
one we watch. Wrong instructions, a dead link, a page that assumes knowledge you
do not have, a missing topic — all of it is worth telling us about.

Pull requests are welcome and we read every one, but we cannot merge them here.
A maintainer ports the change into the source repository, credits you in the
commit, and then closes the PR with a link to the live page.

For help with **your own account, course, or job** — not the documentation —
email <datahub@ucsd.edu> rather than filing an issue here.

## Built with

[MkDocs](https://www.mkdocs.org/) and a bespoke theme carrying the
[UC San Diego Decorator 5](https://developer.ucsd.edu/design/decorator/index.html)
page shell. Content in `docs/` is plain GitHub Flavored Markdown.

```
docs/               content
mkdocs.yml          nav, markdown extensions, link validation
theme/              the Decorator chrome as the MkDocs theme
tools/hooks.py      GitHub-compatible heading anchors, alert callouts
tools/check-links.py  dead link and anchor check over the built HTML
```

To build it locally:

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

See [CONTRIBUTING.md](CONTRIBUTING.md).
