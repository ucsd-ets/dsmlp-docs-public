# What Ends a Session

------------------------------------------------------------------------

> **Draft for review.** Idle culling and both maintenance regimes are confirmed
> from source. The end of a reservation window is confirmed in shape and missing
> every figure. This page carries the open questions from three earlier drafts.
>
> **Idle culling.**
>
> - **Missing:** what "the re-arm" is. The subject index names it, and no source
>   we hold defines it. The section below says only what is confirmed — that a
>   booked window survives the session that was culled from it — which is almost
>   certainly not the whole of it.
>   <!-- FIGURE: a one-line definition of the re-arm — specifically, whether the 15-minute claim window restarts after an idle cull inside a booked window, and what happens if nothing relaunches -->
> - **Decision needed:** how the warning actually reaches a member. The daemon
>   records status on the pod, which a student in a browser will never see. If
>   there is a banner, a mail or a notebook message, this page should describe it;
>   if there is not, "the user is warned before it happens" is too strong.
> - **Check before publishing:** every timing here is a packaged default in the
>   culler's chart and is overridable at deployment. Please confirm the deployed
>   values — these are the numbers users will hold us to.
> - **Check before publishing:** the class scope. Covering all five classes was a
>   decision, and the packaged default covers only some.
>
> **The end of a window, overstay and preemption.**
>
> - **Missing:** what overstay actually costs. Whether it draws Service Units at
>   the ordinary rate, at a premium, or is accounted for some other way is stated
>   in none of the sources we hold, and it is the first question a reader will
>   ask.
>   <!-- FIGURE: the Service Unit treatment of time run past a reservation window -->
> - **Missing:** how much warning the countdown gives.
>   `RESERVATION-DOCS-ASSESSMENT.md` §3 records a 30-minute warning and a
>   15-minute lead before capacity is taken back, read from the reservation
>   repositories; **neither figure is in the confirmed fact base**, so neither
>   appears below. A reviewer with `SCHEDULING.md` in front of them settles both
>   in a minute.
>   <!-- FIGURE: the warning interval, and the interval between warning and reclaim -->
> - **Unverified:** that capacity is reclaimed only when another booking needs it,
>   rather than on a timer. Same source, same status.
> - **Decision needed:** what a background or batch job sees. A countdown that
>   appears "in session" has nowhere to show itself in a `-B` job, and unattended
>   work is exactly the work most likely to overstay.
> - **Check before publishing:** that an on-demand lease behaves like a booked
>   window here. This page assumes the guarantee works the same way whichever
>   created it — likely, but not confirmed.
>
> **Maintenance.**
>
> - **Missing:** how a planned closure is presented in the reservation calendar. A
>   withdrawn node reduces a GPU class's capacity for those dates, and a class can
>   read zero as a result — but whether the interface labels that as maintenance,
>   or simply shows nothing available, is undocumented. The difference decides
>   whether a user files a ticket.
>   <!-- FIGURE: how a maintenance capacity override appears to someone trying to book -->
> - **Missing:** what happens to a reservation already booked across a closure
>   announced afterwards. The Research Cluster window is announced about 7 days
>   ahead, and multi-day research reservations can be booked further out than
>   that.
> - **Unverified:** the timing detail in the maintenance section — a reminder
>   shortly before the day, and deliberate avoidance of quarter boundaries,
>   midterms and known conference deadlines — together with the statement that
>   worker nodes are patched on demand year-round. Both come from the internal
>   maintenance record summarised in `CONFLUENCE-FINDINGS.md` §2 rather than from
>   any published statement, and describe consistent past practice rather than a
>   commitment.
> - **Correcting a published article:** `KB0030470` gives the instructional
>   maintenance window as **Wednesdays** 6-8 AM. It is Tuesdays, and has been for
>   as long as the internal patching schedule records. Anyone reusing that
>   article's text should not inherit the day.

A session can end for five different reasons, and they are commonly confused with
one another. **None of them is a crash, and none of them loses saved work.**

| What ended it | The signal |
|---|---|
| **Idle culling** | The GPU stopped being used for about 30 minutes |
| **The runtime limit** | The pod reached 6 hours, or 12 where that was set at launch → [The Runtime Limit](../running-jobs/job-modes-and-limits.md#the-runtime-limit) |
| **Preemption** | The capacity was needed for somebody's booking |
| **Maintenance** | A node was drained, or the quarterly window opened |
| **Overstay, then preemption** | The window closed, the session ran on, and the capacity came due |

**Contents**

- [What Counts as Idle](#what-counts-as-idle)
- [The Timings](#the-timings)
- [Warnings & Pod Status](#warnings--pod-status)
- [A Cull Is Not an Error](#a-cull-is-not-an-error)
- [Backgrounding Does Not Exempt a Job](#backgrounding-does-not-exempt-a-job)
- [Inside a Booked Window](#inside-a-booked-window)
- [Not the Same as a Browser Timeout](#not-the-same-as-a-browser-timeout)
- [The End of a Window Is Not a Kill](#the-end-of-a-window-is-not-a-kill)
- [The Countdown](#the-countdown)
- [Overstay](#overstay)
- [Preemption](#preemption)
- [Maintenance Closures](#maintenance-closures)
- [A Class That Reads Zero](#a-class-that-reads-zero)
- [Jobs Ending Outside Any Window](#jobs-ending-outside-any-window)

## What Counts as Idle

------------------------------------------------------------------------

**A session that holds a GPU and stops using it has the GPU taken back.** No GPU
memory in use and essentially no CPU, for about **30 minutes**, and the session is
shut down. When the cluster is quiet the figure is up to **6 hours** instead.
Nothing is culled in its first **45 minutes**, and a session that has been working
hard gets a grace of up to an hour after the GPU goes quiet before the clock
starts.

**This applies to every GPU class.** *CPU-only sessions are not culled by this
mechanism at all.*

All of these have to be true at once. Any one of them failing means the session
is busy as far as the culler is concerned.

| Signal | Idle means |
|---|---|
| GPU memory | No more than about **150 MiB** in use, on every GPU the session holds |
| GPU memory, changing | **Any** change since the last check counts as activity and restarts the clock |
| CPU | At most about **0.1 cores**, taken as the maximum over the last hour |
| Age | The session is at least **45 minutes** old. Nothing younger is ever considered idle |

A model sitting loaded on the card is not idle: it is holding framebuffer. A
session that finished training an hour ago and has been at a shell prompt since
is idle, because nothing is holding anything.

*The CPU test looks at the last hour, not at this instant.* A job that does a
burst of work every forty minutes will not be culled between bursts.

## The Timings

------------------------------------------------------------------------

| Stage | How long |
|---|---|
| **First 45 minutes** | Never culled, whatever the session is doing |
| **Grace after the GPU goes quiet** | **15 to 60 minutes** before the quiet time counts as idle at all, scaling with how much GPU work the session has already done. A session with two hours or more of GPU activity behind it gets the full hour |
| **Normal cull** | **30 minutes** of idleness |
| **When the class is underloaded** | **6 hours** of idleness |
| **How often it is checked** | Every **5 minutes** |

**The 6-hour case is a property of the class, not of the session.** It applies
when every node behind that GPU class is under 75% allocated on CPU, memory *and*
GPU at once. On a quiet evening the same work gets six hours; in week 10 the same
work gets thirty minutes. *The longer figure is not something to plan around.*

## Warnings & Pod Status

------------------------------------------------------------------------

**A session is warned before it is culled** — the warning starts when there are
30 minutes of runway left.

**The status is recorded on the pod itself**, and is readable from the command
line:

```bash
kubectl get pods
kubectl describe pod <pod-id>
```

Under `Annotations`, `dsmlp/idle-gpu-status` reads `ok`, `idle` or `warning`, and
`dsmlp/idle-gpu-cull-deadline` gives the time the session would be culled if
nothing changes.

*Two cautions about reading those.* The deadline is a projection, not a
countdown — it is recalculated on every pass and moves as conditions change, and
it disappears entirely as soon as the session does some GPU work again.
**A missing annotation does not mean everything is fine**; it means the session
is out of scope, not yet swept, or already culled, so a blank reads as "unknown"
rather than as "healthy".

*On a busy cluster `idle` does not appear at all.* With a 30-minute threshold
and a 30-minute warning lead, a session goes straight from `ok` to `warning`.
Plain `idle` shows during the 6-hour window on a quiet cluster.

## A Cull Is Not an Error

------------------------------------------------------------------------

**A cull is not a crash, and it is not a fault in the code.** The session is
stopped deliberately, and there is nothing to report and nothing to fix.

**Files survive.** The container is deleted; the home directory, the `private/`
area and the workspace's shared directories are not.
→ [Directories, Quotas & Cleaning Up](../workspaces-and-storage/your-files-and-quotas.md#where-files-live)

**Anything that lived only in the session's memory is gone** — a notebook
kernel's variables, a model that had trained for two hours and had not been
saved. *Please checkpoint long runs.*
→ [Checkpointing & Logging](../running-jobs/checkpointing.md)

A culled session leaves nothing behind that needs clearing up before a relaunch.

## Backgrounding Does Not Exempt a Job

------------------------------------------------------------------------

**The test is whether the GPU is doing anything, not whether a session is
attached to it.** A background pod (`-b`) disconnected from three hours ago, a
batch job whose Python process has already exited, a `nohup`-ed script that is now
waiting on a download — all of them look exactly like an idle session, because
that is what they are.

*A job that is genuinely computing on the GPU is never culled, however long it
runs and whether or not anyone is watching it.* Backgrounding a real training run
is entirely safe. What is not safe is holding a card open for later.
→ [Interactive, Background & Batch Modes](../running-jobs/job-modes-and-limits.md#the-three-modes)

## Inside a Booked Window

------------------------------------------------------------------------

**A cull does not cancel the reservation.** The booked window stands for its
remaining length, and a session may be launched into it again.

*What is not yet documented is whether relaunching is time-limited.* If the claim
window re-arms after a cull — 15 minutes to start something new before the
reservation is treated as unclaimed — that is consequential, and this page will
say so once it is settled. Until then, please treat a cull inside a booked window
as something to respond to promptly.
→ [The Claim Window](reservations.md#the-claim-window)

## Not the Same as a Browser Timeout

------------------------------------------------------------------------

**Third-party course material gives Datahub an inactivity timeout of 20 minutes,
or of 30.** *Neither figure is ours, and neither describes this mechanism.* Idle
culling is about a GPU sitting unused, not about a browser tab sitting untouched.

**A disconnection is not a shutdown.** Logging out or closing a laptop leaves the
session running and still holding its GPU — and still drawing on the budget. Stop
it with **File → Hub Control Panel → Stop My Server**.
→ [On-Demand Leases Charge Budget](service-units-and-budgets.md#on-demand-leases-charge-budget)

## The End of a Window Is Not a Kill

------------------------------------------------------------------------

**Nothing stops a container at the stroke of the hour.** A reservation window
closing does not terminate the session running inside it. Where the capacity is
not needed by anybody else, the session keeps running.

**The window still matters.** It is what was charged for, it is what is
guaranteed, and once it has passed the session is running on someone else's
terms.

## The Countdown

------------------------------------------------------------------------

**A session reports how long its guarantee has left.** The countdown appears in
the session itself rather than by email.

<!-- FIGURE: how far ahead the countdown begins, and how it is presented -->

**A checkpoint written before the window closes is what survives it.** Stopping,
extending and running on are the three outcomes available from that point.
→ [Checkpointing & Logging](../running-jobs/checkpointing.md)

## Overstay

------------------------------------------------------------------------

**Running past a guaranteed window is called overstay, and it has a cost.** The
session is not stopped, nothing warns it off, and nothing in the interface
prevents it. What changes is that the time is no longer covered by what was
booked.

<!-- FIGURE: what overstay costs, in Service Units or otherwise -->

**The figure is not yet published.** It appears in none of the sources this
documentation set draws on, and a placeholder here would be worse than the gap.

**An overstaying session has no protection.** It runs on capacity that is no
longer guaranteed to it, so when that capacity is needed back — for somebody
else's booked window — the overstaying session is the one that yields.

*A longer window arranged in advance is the alternative to running over.*
→ [Routes to More Time](reservations.md#routes-to-more-time)

**Handing time back early costs nothing.** Releasing the tail of a window that has
mostly been used carries no cancellation penalty — the charge is for the time
actually used, and the remainder returns to the pool.
→ [Cancelling in Advance](service-units-and-budgets.md#cancelling-in-advance)

## Preemption

------------------------------------------------------------------------

**Preemption is a session ending because the capacity was needed for a booking.**
It is a capacity outcome, not a fault.

Two situations lead to it:

- **An overstaying session**, where a reservation comes due for the capacity it
  is still holding.
- **A best-effort session**, which accepts preemption from its first tick in
  exchange for running now.
  → [Best-Effort Reservations](reservations.md#best-effort-reservations)

**Saved work survives; anything held only in memory does not.** There is no
signal to catch and no chance to write things out on the way past.

The session records what happened as a Kubernetes event — `Preempted`, or
`OverstayRelinked` where an overstay was involved. Reading those directly assumes
more Kubernetes than most readers want.
→ [Kubernetes Events](../running-jobs/kubernetes.md#reservation-events)

## Maintenance Closures

------------------------------------------------------------------------

**Two different maintenance regimes apply to this platform.** One is weekly,
routine, and usually invisible. The other happens four times a year and ends every
job that is running.

**Instructional maintenance: Tuesdays, 6-8 AM.** Tuesday morning is a window in
which we may patch, not a scheduled outage. Campus policy requires prompt patching
of servers, and 6-8 AM Pacific on Tuesdays is the period set aside for it on the
instruction side. *Most Tuesdays, most users notice nothing at all.*

In practice this usually means a subset of worker nodes. Scheduling policy tries
to place jobs on nodes that will not be touched, so running work is generally
unaffected. During the window the platform may operate at reduced capacity, and —
depending on what is being fixed — the cluster as a whole can be briefly
inaccessible. **A running job can still be terminated**, since some updates
require a node to be drained.

*Patching is deferred where possible during 10th week and Finals week*, unless
the nature of a vulnerability requires immediate action. Critical updates
occasionally force work outside the window, in which case we notify instructors
and TAs as far in advance as we can.

**Research Cluster maintenance: quarterly, and everything stops.** The window
falls in the break between terms, roughly once a quarter, with about **7 days'
notice** — and **all running jobs are terminated**. Not drained, not migrated, not
deferred to another node: terminated. A multi-day training run started the day
before is lost at the point the window opens, and everything not written to disk
is gone with it.

Windows are placed to avoid the start and end of a quarter, midterm periods, and
known conference deadlines, and the notice is followed by a reminder shortly
before the day. *That is consistent past practice rather than a published
commitment; the notice that is sent governs, not the pattern.*

**Research Cluster notices come from
[rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu)**, which is also where to ask
about one.

**Please do not start a 12-hour run into an announced maintenance window.**

## A Class That Reads Zero

------------------------------------------------------------------------

**Withdrawn hardware is withdrawn capacity.** When nodes are taken out of service
for planned work, the GPU classes they back have fewer cards — or none — for the
duration. A class can therefore show nothing available on particular dates even
though nobody has booked it.

**There is no way to tell those two situations apart from the outside:** a class
reading zero on a date might be fully booked, might be closed for maintenance, and
looks identical either way.
→ [When the Cluster Is Full](quotas-and-availability.md#when-the-cluster-is-full)

*Please ask us where a class in regular use is unavailable across a specific span
of days and no notice has been sent, rather than assuming demand.*

## Jobs Ending Outside Any Window

------------------------------------------------------------------------

**Worker nodes are patched on demand, year-round, and without user notification.**
Only the JupyterHub, login and file-server components are held to the notified
schedule; the nodes containers actually run on are maintained as need arises.

This accounts for a class of incident that otherwise looks inexplicable — a job
that ended cleanly, at no particular time, with no error of its own and no
maintenance announcement anywhere. It is not the common case, and it cannot be
scheduled around.

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
