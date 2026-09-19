# Reservations

------------------------------------------------------------------------

> **Draft for review.** The reservation model is confirmed and is described
> below. **The surface a member uses to book is not documented anywhere**, and
> neither are most of the calendar's own conventions. This page carries the open
> questions from seven earlier drafts, grouped by subject.
>
> **The booking surface itself.**
>
> - **Missing:** where the reservation calendar actually is. Every source
>   describes "a web interface" and none of them names it, so this page cannot
>   tell a reader how to reach the thing it is about.
>   <!-- FIGURE: the URL of the reservation web interface, and whether it is reached from datahub.ucsd.edu or separately -->
> - **Decision needed:** whether members book for themselves in a course
>   workspace, or whether booking is normally done by the instructor or TA. Both
>   are described as possible; which is expected of a student changes how this
>   page and the student page should read.
> - **Check before publishing:** whether an on-demand launch that cannot be
>   satisfied queues, fails immediately, or waits for a bounded time. Our sources
>   say both "may queue" and that a lease may be denied outright.
>
> **Booking conventions — every one a human must supply.** The internal
> assessment of the reservation-app guides (`RESERVATION-DOCS-ASSESSMENT.md`, §6)
> names these as real behaviours of the shipped system, but no value for any of
> them is confirmed for our deployment, and this page does not guess at one.
>
> - **Granularity.** Whether a window must start and end on a whole hour, or
>   whether shorter units are accepted. *Described as whole hours in the internal
>   assessment; unconfirmed.*
> - **Minimum lead time.** How far before its start a window may be booked. *The
>   assessment names a "15-minute lead"* — **and it is not clear whether that is
>   a distinct rule or a restatement of the 15-minute claim window.** These are
>   two different things and they must not be published as one.
> - **Cross-midnight windows.** Whether one booking may run from one calendar day
>   into the next, or must be split into two.
> - **Timezone.** Which timezone the calendar displays — a fixed site timezone or
>   the viewer's browser locale — and what a member booking from elsewhere sees.
>   Also what happens to a window spanning a daylight-saving change.
> - **Editing.** Whether a booking can be moved, lengthened or shortened after it
>   is made, or only cancelled and rebooked. *If it is cancel-and-rebook, the
>   cancellation penalty applies to an edit, which is consequential and belongs on
>   this page in bold.*
> - **Back-to-back windows.** Whether two adjoining bookings of the same class
>   may be held, and whether a session survives the boundary between them.
> - **Concurrency.** How many bookings, or how many GPUs across bookings, one
>   member may hold at once.
> - **Refusals.** Whether the calendar hides a window the workspace has no quota
>   for at that hour, or accepts the booking and fails later.
> - **Naming.** What the calendar calls each class. Our pages use the label
>   values (`extra-large`); the platform overview writes *X-Large*. One of them
>   should win across the whole set.
>
> **The claim window.**
>
> - **Decision needed:** whether anything warns a member that a claim window is
>   running out — a mail, a message on the calendar, nothing at all. A reader who
>   is told the window is irrevocable will immediately ask whether they get a
>   nudge, and this page cannot answer.
> - **Unverified:** that the 15 minutes is measured from the start of the booked
>   window. Every source states the duration; none states the instant it starts
>   from. A booking claimed at minute 14 and one claimed at minute 16 differ by
>   the whole reservation, so this is worth being sure of.
> - **Check before publishing:** whether a member may cancel a booking during the
>   claim window itself and be treated as an advance cancellation, or whether the
>   window has already committed them.
>
> **Length, the horizon and the caps.**
>
> - **Missing:** the booking horizon itself. The reservation model has a rolling
>   window with a minimum and a maximum number of days ahead, and neither value
>   is published anywhere we can read.
>   <!-- FIGURE: the minimum and maximum days ahead a member may book, and whether either differs for a research workspace -->
> - **Missing:** the cap a course workspace actually uses. The 48-hour member cap
>   is the ceiling on an ordinary member's booking, but course workspaces are
>   described as using "short caps" well below what research workspaces permit,
>   and no figure exists for them.
>   <!-- FIGURE: the per-reservation cap a typical course workspace is configured with -->
> - **Decision needed:** how a window longer than 48 hours is actually obtained.
>   Something reaches up to the 168-hour ceiling, since the ceiling is described
>   as binding on administrators too, but who asks whom, and through what form,
>   is not documented.
> - **Decision needed:** how a multi-day reservation interacts with the 12-hour
>   session runtime limit. Both figures are confirmed and they are limits on
>   different things; whether a reserved window raises the runtime limit, or
>   whether a 48-hour window is expected to hold several consecutive sessions, is
>   the first question any researcher will ask. This page states both and
>   reconciles neither, deliberately.
>
> **Best-effort reservations.** One sentence is confirmed — *run free now, accept
> preemption from the first tick* — and that section is built around it.
>
> - **Missing:** what "free" means. Whether a best-effort session draws no Service
>   Units at all, draws them at a zero or discounted rate, or draws them but does
>   not count against a budget window, is not stated in any source we hold.
>   <!-- FIGURE: the Service Unit treatment of a best-effort session -->
> - **Missing:** how a member asks for one. There is no documented control on the
>   Datahub spawn form and no documented `launch.sh` flag. The reservation
>   controller's own material describes a launch-time pod annotation that sets a
>   session's runtime guarantee to none, and `launch.sh -A key=value` is the flag
>   that would carry an annotation — but the key is prefixed with an internal
>   product codename we do not publish.
>   <!-- FIGURE: the supported way for a user to request a best-effort session -->
> - **Missing:** who may use it. Whether best-effort is offered to every
>   workspace, or only to research workspaces, is unknown — and it matters,
>   because a free route to a GPU sits oddly beside a per-student Service Unit
>   budget.
> - **Check before publishing:** whether preemption of a best-effort session comes
>   with any warning at all. This page states that it may end at any moment, which
>   is the safe reading of "from the first tick" but is not the same as a
>   confirmed "no warning".
>
> **Team mode.**
>
> - **Missing:** the mechanics. How a team is formed, who may join one, whether a
>   team booking draws one member's budget or several, what a teammate may do
>   besides cancel, and whether team mode is offered to course workspaces at all
>   or only to research groups. None of this is confirmed.
> - **Decision needed:** whether the "team" of team mode is the same object as the
>   team behind `launch.sh -G` and the `teams/` directory. The two share a word
>   and, as far as we can confirm, nothing else. If they are the same thing, this
>   page and the storage pages must be reconciled; if they are not, one of the two
>   names should change before either is published, because readers will conflate
>   them on sight.
> - **Check before publishing:** that a teammate's cancellation really cannot be
>   waived by *anyone*, including an administrator. Our fact base says the penalty
>   cannot be waived; it does not distinguish the manager waiver from the
>   administrator pardon, and those are separate controls everywhere else.
>
> **Continue, Extend & Adopt — the whole section is a gap.** These are named
> operations in the reservation system's vocabulary whose mechanics are
> undocumented in every source available to this project. Their names suggest what
> they might do; this page does not act on that suggestion, and neither should a
> reviewer without checking.
>
> - **Missing:** a one-sentence definition of each of the three, from the team
>   that built them.
>   <!-- FIGURE: what Continue does, what Extend does, what Adopt does -->
> - **Missing:** who may invoke each — member, group manager, administrator — and
>   whether a teammate may invoke one against another member's reservation.
> - **Missing:** when each is available. Only during a running session? Only
>   before a window opens? Only while capacity is free?
> - **Missing:** what each costs, and when it is charged. Extending a booking is
>   plainly a Service Unit event; whether the cost is computed up front like the
>   original booking, or accrued, is not stated anywhere.
> - **Missing:** whether the reservation caps bind these operations — whether an
>   extension is measured against the 48/168-hour caps, or is a fresh reservation
>   carrying its own.
> - **Missing:** whether any of the three can fail, and what the reader sees when
>   one does. "The button did nothing" is the ticket this gap generates.
> - **Decision needed:** whether Continue and Extend are two operations or one
>   under two names. `RESERVATION-DOCS-ASSESSMENT.md` §6 lists them as
>   "Continue / Extend" in one breath and Adopt separately, alongside team mode.
> - **Where the answer probably is:** the assessment records that the reservation
>   application's own guide covers Extend in the section that also covers the
>   claim window, the idle re-arm, the runtime guarantee and back-to-back
>   bookings, and marks that section publishable with a light edit. Nobody on this
>   documentation project has read it. That is one afternoon's work for someone
>   with repository access, and it very likely closes several of the gaps above.

**From Fall 2026, every GPU session on DSMLP sits on a reservation.** There are
two ways to come by one: book a window ahead of time, or launch and have one
created on the spot. **Both draw on a member's Service Unit budget.** The
difference between them is certainty, not cost.

**Contents**

- [The Three Ways a Session Gets a GPU](#the-three-ways-a-session-gets-a-gpu)
- [Booking Ahead](#booking-ahead)
- [Launching Without a Booking](#launching-without-a-booking)
- [Which One to Use](#which-one-to-use)
- [What a Booking Names](#what-a-booking-names)
- [The Timings That Are Fixed](#the-timings-that-are-fixed)
- [The Claim Window](#the-claim-window)
- [Reservation Length Caps](#reservation-length-caps)
- [Length Is Not Runtime](#length-is-not-runtime)
- [The Booking Horizon](#the-booking-horizon)
- [Planning a Long Window](#planning-a-long-window)
- [Best-Effort Reservations](#best-effort-reservations)
- [Team Mode](#team-mode)
- [Continue, Extend & Adopt](#continue-extend--adopt)
- [Routes to More Time](#routes-to-more-time)
- [What Governs How Much Is Held](#what-governs-how-much-is-held)

## The Three Ways a Session Gets a GPU

------------------------------------------------------------------------

| | When it starts | What it costs | What protects it |
|---|---|---|---|
| **A booked window** | At the reserved window, claimed within 15 minutes | Service Units, computed up front | A runtime guarantee for the length of the window |
| **An on-demand lease** | Now, if capacity is idle | Service Units, exactly as a booked window would | It is a real reservation, and is treated as one |
| **Best-effort** | Now | Free <!-- FIGURE: what "free" means here --> | Nothing |

## Booking Ahead

------------------------------------------------------------------------

**A reservation is a booking of a GPU class for a window of time** — for example,
*"Tuesday 9am-7pm: 4× extra-large"*. During that window the capacity is held, and
a session launched into it is admitted ahead of the walk-up queue.

**A reservation is a guarantee of access, not a running job.** Nothing starts by
itself at 9am. A notebook, a shell session or a batch job is launched exactly as
it would be otherwise, and it lands on the capacity being held.
→ [From Reservation to Running Session](gpu-classes.md#from-reservation-to-running-session)

*This is the part readers most often get wrong.* A booked window with no launch
in it is a window nobody used, and it is charged — see
[The Claim Window](#the-claim-window), which is the expensive version of the same
mistake.

## Launching Without a Booking

------------------------------------------------------------------------

**Launching a GPU session with no reservation creates one.** It draws from
whatever capacity is idle at that moment, and it charges the member's budget
exactly as a booked window would. *Launching an eligible session is what
authorizes that spend; there is no free exploratory launch.*
→ [On-Demand Leases Charge Budget](service-units-and-budgets.md#on-demand-leases-charge-budget)

**Off-peak, this is close to instantaneous** and it is how most day-to-day work
gets done. **On a busy deadline evening it is the weaker position**: reserved
users are admitted first, and an on-demand request may wait or be refused. A
session that never started because the lease was denied reports itself as
`OnDemandLeaseDenied`.
→ [When the Cluster Is Full](quotas-and-availability.md#when-the-cluster-is-full) ·
[Kubernetes Events](../running-jobs/kubernetes.md#reservation-events)

**The first 2 hours of an on-demand lease are penalty-free on cancellation.** A
lease started and stopped inside that window is charged for the time used and
nothing more.
→ [The Cancellation Penalty](service-units-and-budgets.md#the-cancellation-penalty)

## Which One to Use

------------------------------------------------------------------------

| Situation | Please |
|---|---|
| A GPU is needed on Thursday evening | Book it. Evening capacity during a deadline week is what the calendar exists to allocate |
| A twenty-minute experiment, now, at 11am | Launch. Daytime capacity is generally idle, and the first 2 hours carry no cancellation penalty |
| A run that will take two days | Book it, and check the length caps first → [Reservation Length Caps](#reservation-length-caps) |
| Work whose answer is not needed today, done cheaply | Move the work off-peak → [Off-Peak Discounts](service-units-and-budgets.md#peak--off-peak-hours) |
| Work that can start now and accept being interrupted | Consider a best-effort reservation → [Best-Effort Reservations](#best-effort-reservations) |

## What a Booking Names

------------------------------------------------------------------------

**A booking names a GPU class, a number of GPUs, and a window of time** — for
example, *"Tuesday 9am-7pm: 4× `extra-large`"*. It is made through the
reservation web interface, and it holds that capacity until the window ends.
→ [GPU Classes](gpu-classes.md)

**Until the conventions listed in the note above are settled, the booking form is
the authority.** It refuses a window it cannot accept. *Please report any of its
rules that this page does not cover.*

## The Timings That Are Fixed

------------------------------------------------------------------------

These belong to the reservation model rather than to the calendar's form, and
they are confirmed.

| Timing | What it governs |
|---|---|
| **15 minutes** | The claim window. Launch inside it or the reservation is cancelled as a no-show → [The Claim Window](#the-claim-window) |
| **First 2 hours** | Of an on-demand lease, penalty-free on cancellation → [The Cancellation Penalty](service-units-and-budgets.md#the-cancellation-penalty) |
| **Roughly 12 hours ahead** | The boundary below which work may borrow idle capacity beyond its workspace's quota → [Borrowing Beyond Quota](quotas-and-availability.md#borrowing-beyond-quota) |
| **48 hours / 168 hours** | The member cap on one reservation, and the absolute ceiling nobody exceeds → [Reservation Length Caps](#reservation-length-caps) |

*The 15-minute claim window is not a lead time.* It is measured at the start of a
window already held, and it has nothing to do with how far ahead a booking may be
made.

## The Claim Window

------------------------------------------------------------------------

**A booked window must be claimed within 15 minutes of its start.** A reservation
holds capacity; claiming it means actually starting a session on that capacity.
If nothing launches inside those 15 minutes, the reservation is treated as a
no-show: it is cancelled, the capacity returns to the pool, and the window is
gone for the rest of its length.

**Claiming is launching.** There is no separate confirmation step: a notebook, a
shell session or a batch job starts in the usual way, and the reservation is
claimed by the session landing on it.

*The clock runs during the launch itself.* Pulling a large custom image, or a
first launch of the term, is not instant. A window cannot be claimed before it
starts.

**A no-show is charged.** What it costs, and how to have the charge waived, is
documented with the other charges.
→ [The Cancellation Penalty](service-units-and-budgets.md#the-cancellation-penalty)

## Reservation Length Caps

------------------------------------------------------------------------

**Two ceilings apply to how long one reservation may be.**

| Cap | Applies to |
|---|---|
| **48 hours** | An ordinary member's reservation |
| **168 hours** | An absolute ceiling. Nobody exceeds it, administrators included |

**A workspace's own cap may be shorter than either.** Each workspace sets one,
matched to the work it was provisioned for: course workspaces use short caps,
while research workspaces can permit multi-day windows well beyond them. A
booking refused for its length has met a workspace setting rather than a platform
limit, and the PI or instructor is the person to ask.
→ [What a Workspace Is](../workspaces-and-storage/what-a-workspace-is.md)

## Length Is Not Runtime

------------------------------------------------------------------------

**A reservation's length and a session's runtime are different limits**, and a
long booking does not by itself grant a long-running pod.

- **A reservation** holds GPU capacity for a window of time. A 48-hour booking
  means the hardware is held across those 48 hours.
- **A session** — the pod a launch creates — runs for **6 hours** by default,
  and **up to 12 hours** where that is set at launch. Beyond 12 hours, please
  write to [datahub@ucsd.edu](mailto:datahub@ucsd.edu).
  → [The Runtime Limit](../running-jobs/job-modes-and-limits.md#the-runtime-limit)

**Checkpointing is what makes a long booking usable.** A run that writes its
progress somewhere durable at affordable intervals can be picked up again; a
single uninterruptible process cannot.
→ [Checkpointing & Logging](../running-jobs/checkpointing.md)

**A session is also subject to idle culling for the whole of its life**, however
long the window behind it. A reserved GPU that stops being used is reclaimed like
any other. → [What Ends a Session](what-ends-a-session.md)

## The Booking Horizon

------------------------------------------------------------------------

**Bookings are accepted inside a rolling window, not arbitrarily far ahead.**
The calendar takes bookings no nearer than some minimum and no further than some
maximum, and that window moves forward with the date.
<!-- FIGURE: the minimum and maximum days ahead a member may book -->

*Neither bound is published, and this page will state them once they are.* Until
then, the booking form is the authority on how far out a window may be placed.

**One horizon is confirmed.** Work starting within roughly the next **12 hours**
may borrow idle capacity beyond its workspace's quota — so a last-minute job has
a route to hardware that a booking made a week out does not. Course workspaces
always borrow senior.
→ [Borrowing Beyond Quota](quotas-and-availability.md#borrowing-beyond-quota)

## Planning a Long Window

------------------------------------------------------------------------

**Please book the class the work needs rather than the largest one available.**
A 48-hour `extra-large` booking is a substantial draw on a budget and a
substantial hold on scarce hardware.
→ [GPU Classes](gpu-classes.md) ·
[Service Units & Budgets](service-units-and-budgets.md)

**Unused time can be handed back.** Releasing the tail of a finished booking
carries no cancellation penalty — the charge is for the time actually used, and
the rest returns to the pool.
→ [Cancelling in Advance](service-units-and-budgets.md#cancelling-in-advance)

## Best-Effort Reservations

------------------------------------------------------------------------

**A best-effort reservation trades the guarantee for an immediate start.** An
ordinary reservation holds capacity and protects the session for the length of the
window. A best-effort one holds nothing: it runs on capacity that is genuinely
spare, and hands that capacity back the moment somebody with a claim on it turns
up.

**Launching without a booking is not the same as launching best-effort.** An
ordinary on-demand launch creates a reservation on the member's behalf and spends
that member's budget on it; that is the default behaviour. Best-effort is a
deliberate choice to run without the guarantee.

**A best-effort session can end at any point in its life, including immediately.**
There is no protected initial period and no point after which the session is safe.
A best-effort session that has been running for four hours is exactly as liable to
be reclaimed as one that started a minute ago.

**Saved work survives; unsaved work does not.** A preemption arrives without a
signal the running code can catch and without an opportunity to write state out on
the way past. Everything that matters has to be on disk already.
→ [Checkpointing & Logging](../running-jobs/checkpointing.md)

The session records the ending as a `Preempted` Kubernetes event, which
distinguishes the cluster taking the card back from a program that crashed.
→ [Kubernetes Events](../running-jobs/kubernetes.md#reservation-events)

**What best-effort is good for:**

- **Work that checkpoints.** A training run that resumes from disk loses minutes
  to a preemption rather than hours.
- **Attended work.** Debugging, a first pass over a dataset, checking that a model
  builds and a batch runs — short interactive work where losing the container
  costs a re-launch and nothing else.
- **Capacity that would otherwise go unused.** Capacity that is spare at eleven in
  the morning is capacity nobody has booked.

What it is not good for is anything with a deadline attached to it. *A reservation
is the only thing on this platform that promises a GPU at a particular time.*

**Best-effort is not a route around a budget.** Where a member's Service Unit
budget is not enough for the work, a workspace manager — an instructor, TA or
PI — can book on that member's behalf without drawing the member's budget, and can
request an increase.
→ [When a Budget Runs Out](service-units-and-budgets.md#when-a-budget-runs-out)

*Idle culling, the runtime limit and the workspace's GPU class grants all apply to
a best-effort session exactly as they do to any other.*

## Team Mode

------------------------------------------------------------------------

**Team mode lets members of a team act on one another's reservations.** That is
very nearly the whole of what we can confirm about it, and this section is short
for that reason.

**A teammate can cancel another member's booking, and that penalty cannot be
waived.** *This is the only cancellation charge in the system with no route of
appeal.* Elsewhere, a workspace manager may waive a charge where it is warranted
and an administrator may pardon one outright; here, neither applies.
→ [Having a Charge Waived](service-units-and-budgets.md#having-a-charge-waived)

**Everything else about team mode is unsettled** at the time of writing. *Please
write to us at [datahub@ucsd.edu](mailto:datahub@ucsd.edu) before planning work
that depends on it.*

**`launch.sh -G` is about data, not reservations.** `-G list` prints the teams an
account belongs to and `-G <teamid>` launches with that team's data visible under
`teams/`. That mechanism scopes which files are visible. It is not known to be
connected to team mode in the reservation system.
→ [Sections, Teams and Group Data](../workspaces-and-storage/what-a-workspace-is.md#sections-teams-and-group-data)

*Note also that `-g` and `-G` are different flags entirely: `-g 1` asks for one
GPU, `-G 1` does not.*

## Continue, Extend & Adopt

------------------------------------------------------------------------

**Continue, Extend and Adopt belong to the reservation system's own vocabulary.**
They name operations on a reservation already held, and members will meet the
three words before this page can define them. Their mechanics are undocumented in
every source available to this project, and this page states that rather than
guessing at which is which.

**The rules that bound every reservation bound these too.** Whatever the three
turn out to do, none of them escapes the following, all of which are confirmed:

- **No reservation exceeds 168 hours.** That ceiling is absolute. Ordinary
  members cap at 48 hours per reservation.
- **GPU time draws Service Units.** There is no free route to more hours; a longer
  booking is a larger charge, however the extra time is arranged.
- **Cancelling in advance carries no penalty.** The charge is for the time
  actually used, and the remainder returns to the pool.
- **In team mode, a teammate can cancel another member's booking**, and that
  particular penalty cannot be waived. If Adopt turns out to be a team operation,
  this is the neighbourhood it lives in.

## Routes to More Time

------------------------------------------------------------------------

Until the three operations above are documented, these are the routes we can
describe honestly.

**Booking the required time up front.** A window released early costs nothing
beyond the hours actually used.

**Running past the window.** There is no hard kill when a window closes, and
there is an in-session countdown — but the time is no longer guaranteed, the
session has no protection once the capacity is wanted, and overstay has a cost we
cannot yet state.
→ [Overstay](what-ends-a-session.md#overstay)

**A booking made by a group manager.** An instructor, TA or PI can book on a
member's behalf, and that booking does not draw the member's budget. For a project
that has genuinely outgrown its budget, a manager can request a change by ticket.
→ [Managing a Group](../reference/managing-a-group.md)

**Checkpointing.** A run that resumes from disk turns a window that ended into an
inconvenience rather than a lost day.
→ [Checkpointing & Logging](../running-jobs/checkpointing.md)

## What Governs How Much Is Held

------------------------------------------------------------------------

**A workspace has a quota per GPU class** — the most of that class the whole
workspace may hold at once — and, separately, **each member has a Service Unit
budget** which meters their own share of it. The quota is about capacity; the
budget is about fairness within the workspace.
→ [Quotas, Cohorts & Availability](quotas-and-availability.md) ·
[Service Units & Budgets](service-units-and-budgets.md)

*Quotas are not hard ceilings.* Work starting within roughly the next 12 hours
may borrow idle capacity beyond the workspace's quota, and course workspaces
always borrow senior. *Availability can also read zero while a workspace still
has headroom on paper* — that is the cohort mechanism.
→ [Cohorts](quotas-and-availability.md#cohorts)

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
