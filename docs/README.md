# Datahub & DSMLP Documentation

------------------------------------------------------------------------

This is the documentation set for UC San Diego's **Datahub** and **Data Science
& Machine Learning Platform (DSMLP)**. It is organized by audience and task, with
the technical detail written once and linked from everywhere it is needed.

Please reach out to our team with any questions or feedback regarding these
guidelines or Datahub/DSMLP as a whole.

- Email: [datahub@ucsd.edu](mailto:datahub@ucsd.edu)
- 1:1 Consultation: <https://ucsd-datahub.youcanbook.me/>

## Start Here

------------------------------------------------------------------------

Each page states its assumptions in its opening lines.

| Page | Intended for | Assumes |
|---|---|---|
| [Overview](overview.md) | Everyone; routes to the appropriate page | Nothing |
| [Using Datahub in a Course](student-in-a-course.md) | Students enrolled in a course that uses Datahub | A web browser |
| [Working from the Command Line](working-from-the-command-line.md) | The same students, when a course requires a terminal | A terminal and `ssh` |
| [Teaching with Datahub & DSMLP](instructor-or-ta.md) | Instructors and TAs | A browser; a shell for customization |
| [Projects & Independent Study](student-project.md) | Student projects, independent study, capstones, clubs and teams | Familiarity with a shell |
| [Research on DSMLP](individual-researcher.md) | Researchers working without a lab workspace | Familiarity with a shell |
| [Setting Up a Research Lab](faculty-research-lab.md) | Faculty provisioning access for a group | Some steps are performed by our staff |

## Technical Documentation

------------------------------------------------------------------------

Detail that applies to more than one audience is documented once, in the subject
area it belongs to, and linked from the audience pages.

| Subject | Covers |
|---|---|
| [Access](access/README.md) | The browser, the login node, remote editors, sign-in problems, and when access starts and ends |
| [Workspaces & Storage](workspaces-and-storage/README.md) | The unit that governs rosters, storage, images, GPU access and quotas — and where files live, how they move, and datasets |
| [Running Jobs](running-jobs/README.md) | `launch.sh`, job modes and runtime limits, watching a job, checkpointing, and Kubernetes |
| [GPU Access](gpu-access/README.md) | GPU classes, reservations, Service Units, quotas and availability, and what ends a session |
| [Environments](environments/README.md) | Standard images and pinning, customization, and building a custom image |
| [Grading](grading/README.md) | Grading tools and interfaces, the notebook workflow through to Canvas, and recovery |
| [Reference](reference/README.md) | Error messages, support routing, the glossary, HPC vocabulary, group management, policy and software |

## Status of This Documentation

------------------------------------------------------------------------

**Audience pages are drafted. The technical set is 32 pages, consolidated from
an earlier 71.** Every technical page opens with a note naming what its writer
could not settle — a decision only a person can make, a claim we could not verify
against a source, or a figure that does not exist anywhere yet. Please read those
notes before treating any page as final. *A merged page carries the notes of
every page it absorbed, grouped by subject, so several of them are long.*

*Figures relating to the Fall 2026 GPU reservation system — Service Unit rates,
per-student budgets, off-peak discounts, borrowing horizons — are not published
anywhere. Where a page needs one it carries a `<!-- FIGURE: ... -->` marker and
says so in its note. Nothing in this set invents a number to fill such a gap.*

## Conventions

------------------------------------------------------------------------

**One fact, one anchor.** A flag table, a quota figure, or a retention policy is
documented in exactly one place, under one heading, and everything else links to
that heading. Where an audience page appears to duplicate a technical page, that
duplication is deliberate and is noted on the page.

**Headings are load-bearing.** Inbound links target `##` anchors, so renaming a
heading breaks them. `tools/check-links.py` validates every internal link and
every anchor; please run it after any edit that moves or renames a section.

**Pages over roughly 2,500 words open with a contents list.**

**Every page states its assumptions.** A page written for a browser does not
quietly require a terminal three sections in.

**Markdown, with inline images.** Images live in [`images/`](images/README.md) and are
referenced by relative path.
