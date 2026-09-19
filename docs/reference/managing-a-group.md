# Managing a Group: Privilege Tiers & Reports

------------------------------------------------------------------------

> **Draft for review.** The four tiers, the manager's three powers, and what the
> reports cover are confirmed. How tiers are *assigned*, what the auditor tier can
> see, and where the reports live are not.
>
> - **Decision needed:** what we call the second tier in public. Our source names
>   it **group manager**; every other page in this set, and the workspace
>   terminology decision behind them, says **workspace manager**. This page uses
>   "workspace manager" for consistency and notes the other spelling once. One
>   term should win across the corpus.
> - **Decision needed:** whether cluster-wide report visibility is intended, and
>   whether we describe it plainly or hold that section until it is narrowed. A
>   manager opening a report and finding other departments' bookings in it is a
>   privacy-shaped surprise, and it is better met in documentation than in
>   discovery. This draft describes it plainly.
> - **Missing:** how a manager becomes one. Course rosters auto-populate from
>   TritonLink/TSS and Canvas, so a TA presumably acquires the tier with the
>   Canvas role — but nothing published says so, and nothing says how a PI or a
>   lab member is designated. A course adding a TA in week 3 needs the answer.
> - **Missing:** what an auditor sees. "Read-only staff" is the whole of what is
>   confirmed. Whether an auditor can see a member's usage, a group's calendar, or
>   nothing but reports is undocumented.
> - **Missing:** whether a member can see which tier they hold, anywhere in the
>   interface.
> - **Missing:** which reports are group-scoped and which are cluster-wide. Our
>   source says "some", not which, so this page has to warn about all four. A
>   reviewer with access to the running system can settle it in a minute.
>   <!-- FIGURE: for each of the four reports, whether it is scoped to the manager's own group -->
> - **Missing:** where the reports are. The reservation interface is not named in
>   any source we hold, so this page cannot tell a manager how to reach the thing
>   it describes. The same gap blocks
>   [Reservations](../gpu-access/reservations.md).
> - **Missing:** whether the reports break down by individual member, whether they
>   can be exported, and how current they are. All three change how a manager
>   would use them, and none is documented.
> - **Unverified:** what a manager can see of a member's bookings. The reservation
>   system's own documentation, as assessed for this project, states that the
>   notes attached to a booking are visible to course staff, and that in
>   researcher mode a member's username and notes are visible to the whole group.
>   Neither is confirmed for DSMLP, and both should be settled before members are
>   told anything about privacy.
> - **Check before publishing:** against `KB0034559`, which remains the published
>   scope-of-support article for instruction and does not mention reporting at
>   all.

Four tiers exist in the reservation and workspace system, and the boundary that
matters in practice is not the one between member and manager — it is the one
between what a manager may do and what only an administrator may do.

## The Four Tiers

------------------------------------------------------------------------

| Tier | Who holds it | What it is for |
|---|---|---|
| **Member** | A student in a course, a member of a lab | Doing the work: launching sessions, and booking windows against their own budget |
| **Workspace manager** | An instructor, a TA, a PI | Running the workspace on behalf of its members |
| **Auditor** | Read-only staff | Seeing what is happening without changing it |
| **Administrator** | Cluster administrators, in ITS | Everything the platform can do |

*Our source calls the second tier a "group manager"; this documentation says
**workspace manager**.*
→ [What a Workspace Is](../workspaces-and-storage/what-a-workspace-is.md)

## What a Manager May Do

------------------------------------------------------------------------

Three powers are confirmed.

**View the group calendar.** A manager sees the whole workspace's bookings, not
only their own.

**Book on a member's behalf.** The booking takes effect immediately and **does not
draw that member's Service Unit budget**.
→ [Service Units & Budgets](../gpu-access/service-units-and-budgets.md)

**Waive a cancellation charge.** Where a penalty was assessed and the
circumstances warrant relief, the manager can waive it. **A manager's waiver
zeroes the member's share of the charge**; a full pardon is an administrator
action.
→ [Having a Charge Waived](../gpu-access/service-units-and-budgets.md#having-a-charge-waived)

## What a Manager May Not Do

------------------------------------------------------------------------

**A manager may not edit Service Unit budgets.** Not a member's, and not the
workspace's own. Budgets are set administratively — for a course, cluster
administrators calculate the per-student figure so that it evenly divides the
course's weekly peak evening GPU allocation.

**A manager may not edit group limits or quotas.** How many GPUs of each class the
workspace may hold at once is likewise a platform-side setting.

**Both are changeable by request.** A manager may raise a ticket to
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) asking for either, and should say what
the work is and the dates it matters on.
→ [The Six Requests](getting-help.md#the-six-requests) ·
[Asking for More](../gpu-access/quotas-and-availability.md#asking-for-more)

## One Penalty Nobody Can Waive

------------------------------------------------------------------------

**Where a teammate cancels another member's booking in team mode, the resulting
charge stands.** Not the manager's waiver, not an administrator's pardon. It is
the only cancellation charge in the system with no route of appeal.
→ [Team Mode](../gpu-access/reservations.md#team-mode)

## What the Reports Cover

------------------------------------------------------------------------

**Instructors, TAs and PIs can see how the GPU capacity attached to their
workspace is being used.**

| Report | The question it answers |
|---|---|
| **Reservations by group** | Which groups hold which bookings, and when they fall |
| **Peak simultaneous use by class** | The most GPUs of a class held at once — the number that shows whether a limit is actually binding |
| **Reserved hours** | How much time has been committed over a span, as against how much was available |
| **Effective limits** | What a group's limit *is right now*, after any date-ranged change has been applied |

**"Effective" is the operative word in the last of these.** Quotas are date-aware:
a course's share may be raised for exactly the span of a project deadline and
revert on its own afterwards, so the limit in force this week is not necessarily
the one quoted at provisioning.
→ [Quotas Move with the Calendar](../gpu-access/quotas-and-availability.md#quotas-move-with-the-calendar)

## Cluster-Wide Scope

------------------------------------------------------------------------

**Some of these reports display cluster-wide data, not only the manager's own
workspace.** Two things follow from that.

**The figures have to be read with their scope in mind.** A total that includes
every group on the cluster is not a total for one course, and a peak drawn from
the whole cluster is not evidence about one roster. *Please establish what a
report is scoped to before quoting a figure from it in a ticket or a syllabus.*

**Other groups' data warrants discretion.** Another department's booking pattern
is not a manager's to circulate, and a manager's own group is visible to others on
the same terms. **The reports are a planning tool, not a public record.**

## What Managers Do With Them

------------------------------------------------------------------------

**Requesting a limit change with evidence.** Peak simultaneous use by class and
reserved hours are exactly what a request needs behind it: *"we peaked at our
ceiling every evening of week 7, and the project is due in week 9."* A survey of
student deadlines a few weeks ahead is what lets us raise a quota in advance
rather than discover the surge as it happens.
→ [The Six Requests](getting-help.md#the-six-requests)

**Booking on a member's behalf.** This takes effect at once and does not draw that
member's Service Unit budget.

**Waiving a cancellation charge** where a missed window was not the member's
fault.

**Steering a course off the peak.** Where reserved hours cluster in the evenings,
the cheapest intervention available to a manager is telling students that off-peak
time is discounted and generally obtainable.
→ [Peak & Off-Peak Hours](../gpu-access/service-units-and-budgets.md#peak--off-peak-hours)

## What the Reports Are Not

------------------------------------------------------------------------

**They are not a bill.** Compute on DSMLP is not chargeable, and Service Units
divide capacity rather than costing money. *Storage above 1 TB is a separate matter
and is chargeable.*

**They are not a live availability view.** The status page carries what the cluster
is holding right now.
→ [The Status Page](../gpu-access/quotas-and-availability.md#the-status-page)

**They are not controls.** The three powers above are the whole set; everything
else is administrative and requested by ticket.

**A report explains contention; it does not resolve it.** A course whose quota
never fits its roster is a provisioning problem rather than a scheduling one, and
we would rather hear about it during the term than after it.
→ [Teaching with Datahub & DSMLP](../instructor-or-ta.md) ·
[Setting Up a Research Lab](../faculty-research-lab.md)

**Zero availability in a class is not an outage**, and a cohort can be fully drawn
while an individual group still has headroom on paper.
→ [Cohorts](../gpu-access/quotas-and-availability.md#cohorts)

## Three Things That Are Not Privilege Tiers

------------------------------------------------------------------------

**The shared grader account** is an account, not a tier. Each course receives one
for nbgrader and formgrader, and it holds write permission on the workspace's
`public/` directory. An instructor's own account does not inherit its powers.
→ [The Notebook Grading Workflow](../grading/notebook-grading-workflow.md)

**A team is a Unix group, not a role.** `launch.sh -G list` prints the teams an
account belongs to and `-G <teamid>` launches with that team's data visible.
Membership of a team changes which files are readable; it does not change what a
member may do.
→ [Team Directories](../workspaces-and-storage/your-files-and-quotas.md#team-directories)

**A Technical Point of Contact is a designation, not a permission.** A TPOC is the
person a course nominates to lead its customization work, and the designation
determines who we work with rather than what they can do in the interface. TPOCs
may book [1:1 Consultation](https://ucsd-datahub.youcanbook.me/) appointments
alongside instructors and TAs.
→ [Teaching with Datahub & DSMLP](../instructor-or-ta.md)

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
