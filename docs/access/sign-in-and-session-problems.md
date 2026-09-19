# Sign-In & Session Problems

------------------------------------------------------------------------

> **Draft for review.** Most of this page is confirmed. The provisioning timings
> are not, and the cause of an unexplained spawn failure is now an open question.
>
> - **Corrected 2026-08-28:** the first cause listed under *Spawn Failed* used to
>   be "the same course environment cannot run from the browser and from a
>   terminal at once". **That restriction does not exist.** A member may run one
>   Datahub session together with any number of shell, VS Code and batch jobs.
>   The entry below has been rewritten to the limit that does exist — one Datahub
>   session — and to the aggregate resource ceiling.
> - **Decision needed:** what actually causes "Spawn failed" when none of the
>   remaining causes applies. The published attribution was to the restriction
>   above, which is not real, so that row is now unexplained. **Nothing here
>   should be treated as the authoritative cause until it is verified against the
>   hub logs.**
>   <!-- FIGURE: the real cause(s) of an unexplained JupyterHub spawn failure -->
> - **Settled 2026-08-28 — the roster timings.** `KB0034559` is correct and the
>   other two sources are not. Rosters are loaded into workspaces **one business
>   day before the start of the term**, and a TSS change is reflected **by 10am
>   the day following the change**. `KB0030470`'s *"allow 1-2 business days"* and
>   our own [Using Datahub in a Course](../student-in-a-course.md)'s *"within a
>   couple of hours"* are both wrong and have been corrected across this set.
> - **Removed 2026-08-28 — "The Address".** This page previously opened with a
>   section saying only `@ucsd.edu` addresses are accepted and that a departmental
>   address such as `@eng.ucsd.edu` produces a silent sign-in loop. **Datahub uses
>   standard UCSD single sign-on**, so there is no Datahub-specific address rule
>   to get wrong. The AD username matters at the *SSH* prompt, and that is
>   documented on [The Login Node](the-login-node.md#connecting-over-ssh). The
>   same claim has been removed from the four other pages that repeated it.
> - **Check before publishing:** the remedies quoted from `KB0030470` —
>   `workspace --list`, `workspace -c`, moving `.local/lib` aside — and the error
>   string *"Spawn failed when starting server"* are reproduced from the published
>   article and have not been checked against the current images.

Nearly every failure to reach [datahub.ucsd.edu](https://datahub.ucsd.edu) is one
of four things, and most of them have a self-service remedy. The sections below
are ordered by how often each turns out to be the cause; please work down them
before filing a ticket.

*Sign-in itself is standard UCSD single sign-on.* An account that cannot get past
the campus sign-in page has a campus credential problem rather than a Datahub
one, and the [ITS Service Desk](https://support.ucsd.edu/) handles it.

## The Course Is Not Listed

------------------------------------------------------------------------

Sign-in succeeds, but the expected course is not there. This is a provisioning
question rather than an access fault.

**Rosters are loaded into workspaces one business day before the start of the
term.** A course that is not listed before then has not been loaded yet.

**A TSS change is reflected in Datahub and DSMLP by 10am the day following the
change** — an add, a drop, a section change. *Please allow until then before
treating a missing course as a fault; beyond that timeframe, report it to*
[datahub@ucsd.edu](mailto:datahub@ucsd.edu).
→ [When Access Starts & Ends](when-access-starts-and-ends.md#students-enrolled-in-a-course)

**The instructor or TA is the first stop for anything course-shaped.** Course
staff can see the roster, which is the fastest way to tell "not enrolled yet"
from "enrolled and not provisioned". Auditors, observers and Extended Studies
students are not on the TSS roster the automatic setup uses, and are added
through Canvas by the instructor.

**Outside a course entirely** — an independent study, a capstone, a personal
project — no roster grants access, and the route in is a request rather than a
wait. → [Projects & Independent Study](../student-project.md)

## "Spawn Failed"

------------------------------------------------------------------------

The account is signed in, an environment has been selected, and it will not
start. Please try these in order.

**1. A Datahub session is already running.** A member may have one Datahub
session at a time, so a session left running — for this course or another one —
has to be stopped before a new one starts. Use **File → Hub Control Panel → Stop
My Server**, or the manual resetter below where the running session cannot be
reached. *This limit is on Datahub only: shell, VS Code and batch jobs are not
part of it.*
→ [One Datahub Session](datahub-in-the-browser.md#one-datahub-session)

**2. The disk quota is full.** A full quota stops a session from starting and
says nothing about why. It is shown at
[datahub.ucsd.edu/hub/spawn](https://datahub.ucsd.edu/hub/spawn) → **Services** →
**disk-quota-service**.
→ [Directories, Quotas & Cleaning Up](../workspaces-and-storage/your-files-and-quotas.md#two-quotas-not-one)

**3. The profile is stale.** A **manual resetter** is provided for exactly this.
From [datahub.ucsd.edu](https://datahub.ucsd.edu), open the **services**
dropdown, choose **manual-resetter**, and click reset. *It stops any running
servers, signs the account out and resets the profile — files are preserved.*

**4. A package installed into `.local` has broken the environment.** Packages
under `.local/lib/python3.x/site-packages` load ahead of the ones the image
provides, and one incompatible package can stop a notebook from starting. Move
them aside from a terminal:

```bash
ssh USERNAME@dsmlp-login.ucsd.edu
workspace --list                  # the workspaces available to the account
workspace -c COURSE_ID            # enter the course workspace
mv .local/lib .local/lib.old      # move the offending packages aside
```

*Please install into a virtual environment rather than into `.local`.*
→ [Customizing an Environment](../environments/customizing-your-environment.md)

**Where none of the four applies, please tell us.** The cause of an otherwise
unexplained spawn failure is not currently documented, and a report with the time
and the course helps us find it.

## Links Clicked Before Sign-In

------------------------------------------------------------------------

Course materials are often distributed by a link that fetches a repository into
the course environment:

```
https://datahub.ucsd.edu/hub/user-redirect/git-pull?repo=<url-encoded>&urlpath=tree%2F<dir>%2F&branch=main
```

**Its commonest failure is being clicked before authentication.** The link needs
a signed-in session to redirect into; without one it fails in a way that looks
like a broken link, and is reasonably reported as one.

*The fix is order of operations.* Sign in at
[datahub.ucsd.edu](https://datahub.ucsd.edu) first, start the course
environment, and then click the link — or simply click it again once signed in.
→ [Grading](../grading/README.md)

## A Launch the Cluster Refuses

------------------------------------------------------------------------

**A GPU already held.** A launch that reports a GPU quota being exceeded means a
pod on the same account already holds the GPU being requested. Usually the old
pod is on its way out and clears within a minute or two; if it does not, stop it
from the login node:

```bash
ssh USERNAME@dsmlp-login.ucsd.edu
kubectl get pods
kubectl delete pod <pod-id>
```

**The total across everything running.** Concurrent sessions are allowed, but
their combined CPU, memory and GPU must fit within the Kubernetes limits on the
namespace and, for GPUs, within the reservation system's limits. A launch that
would take the total past them is refused. *Stopping something no longer in use is
the remedy; there is nothing to request.*
→ [Running Several Jobs at Once](../running-jobs/job-modes-and-limits.md#running-several-jobs-at-once)

**A 504, after a crash.** A notebook that exhausts its memory or spins in an
infinite loop can take the pod down with it, and the hub returns a 504 until it
notices and resets. The same `kubectl delete pod` speeds that up; then run the
manual resetter and start again.
→ [Error Messages](../reference/error-messages.md)

**Signing out stops nothing.** Logging out, closing the tab and closing a laptop
all leave the container running and holding its resources. Use
**File → Hub Control Panel → Stop My Server**.

## When Access Has Ended

------------------------------------------------------------------------

Access is retained for **one additional quarter** beyond the term the course ran
in. After that the course no longer appears, and that is not a fault. *Files
remain retrievable for a period afterwards, and an extension can be requested.*
→ [How Long Access Lasts](when-access-starts-and-ends.md#one-additional-quarter) ·
[Retrieving Work Before Access Ends](../workspaces-and-storage/moving-and-sharing-data.md#retrieving-work-before-access-ends)

## Reporting a Problem

------------------------------------------------------------------------

Please raise anything course-shaped with the instructor or TA first. For
platform matters, email [datahub@ucsd.edu](mailto:datahub@ucsd.edu) or file a
ticket with the [ITS Service Desk](https://support.ucsd.edu/). *Please include
the course, the system in use (Datahub or `dsmlp-login`), the environment name,
the exact command if there was one, and a screenshot.* We aim to resolve
individual user issues within **1-2 business days**.
→ [Getting Help](../reference/getting-help.md)

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
