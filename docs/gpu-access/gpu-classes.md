# GPU Classes & Getting One Attached

------------------------------------------------------------------------

> **Draft for review.** The class table, the label, the taint failure and the
> confirmation commands are confirmed. What a class *costs* is not, and **half of
> the reservation-to-session path does not exist in any source** — the half most
> readers need.
>
> - **Missing, and blocking:** how a member with a booked window launches into it
>   from the Datahub spawn form. Is there a control? Does launching during a
>   booked window attach to it automatically? If several bookings overlap, which
>   one is used? This is undocumented in every source this project has — the
>   platform overview, the published articles, the internal Confluence space, and
>   the reservation system's own guides. **A booked window is unusable without
>   it.**
>   <!-- FIGURE: the Datahub spawn-form path from a booked window to a running session -->
> - **Missing:** the same question for the command line. `launch.sh` has no
>   documented flag naming a reservation. The reservation controller's material
>   describes a launch-time pod annotation naming the **workspace** (under the
>   application's own name for it) and states it is *required* for on-demand
>   eligibility. `launch.sh -A key=value` is the flag that would carry an
>   annotation, and the key itself is prefixed with an internal product codename
>   we do not publish. Both the publishable key, and whether `-W` already
>   satisfies this, need deciding.
>   <!-- FIGURE: what a command-line launch must carry to be matched to a reservation -->
> - **Missing:** what happens on a mismatch. If a member books X-Large and
>   launches a Medium profile, or launches into the wrong workspace, does that
>   claim the window, leave it unclaimed, or count as a no-show? The claim window
>   is 15 minutes and a no-show is charged up to 50%, so the answer has money
>   attached to it.
> - **Decision needed:** the maximum number of GPUs a single job may request.
>   Our default tiers give 1 GPU per pod and 1 across a member's namespace; the
>   platform overview says "up to 4 GPU per job"; the reservation system has no
>   such fixed limit and binds on the group's ceiling instead. This page states
>   the defaults and says larger requests are a conversation, which is true under
>   all three readings, but a reader planning multi-GPU work needs a real answer.
> - **Missing:** the per-class SU rate. "A larger class costs more" is the only
>   honest form available, and it is weak next to a number.
>   <!-- FIGURE: hourly SU rate per GPU class, for the Rates page and for this page's guidance on choosing the smallest class -->
> - **Missing, by decision:** the multi-GPU paragraph below stops at "please
>   write to us". The capstone course material that many students arrive holding
>   teaches a specific flag pair for requesting several GPUs, which we have
>   decided not to document; readers who have seen it will find this page silent
>   on something they believe they already know how to do.
> - **Unverified, and self-contradictory in its own source:** the internal page
>   that supplies the class label also states that **Small needs no flag**, while
>   stating that omitting the label on a GPU request fails with
>   `0/5 nodes available`. Both cannot be plainly true. This page follows the
>   confirmed fact base and tells readers to always pass the label.
> - **Check before publishing:** that `-l gpu-class=` is the current selector.
>   `-v <model>` still exists and is still taught in course material, and no
>   source states which of the two is authoritative going forward.
> - **Check before publishing:** the memory figures. They are approximate by
>   design, because ITS reconfigures the hardware behind a class during the term,
>   but a reader will size a model against them.

**A GPU class is a size band, not a hardware model.** A request names the amount
of GPU memory the work needs, and the platform decides which physical card
provides it. This page covers the five classes, choosing between them, asking for
one, and confirming what was actually attached.

## The Five Classes

------------------------------------------------------------------------

| Class | Memory | Typically backed by |
|---|---|---|
| `extra-small` | ~6 GB | A slice of an A30 |
| `small` | ~12 GB | RTX 2080Ti, or a slice of an A30 or H100 |
| `medium` | ~24 GB | A30, A5000, or a slice of an H100 or RTX 6000 |
| `large` | ~48 GB | L40S, or a slice of an H100 or RTX 6000 |
| `extra-large` | ~96 GB | A full H100 or RTX PRO 6000 Blackwell |

**The memory column is the one to plan against**, and the hardware column is
context. *Both are approximate and both change.* A class is a promise about
roughly how much GPU memory a session has, not a promise about which card it
lands on — two sessions in the same class on the same afternoon may sit on
different hardware.

**Each workspace is granted access to one or more classes**, chosen when the
workspace was provisioned to match the work it was expected to do. An
introductory course may see `small` or `medium`; a lab fine-tuning large models
may see `extra-large`. *A class the workspace was not granted is refused* — that
is a request for the instructor or PI to make, not a fault to report.
→ [What a Workspace Is](../workspaces-and-storage/what-a-workspace-is.md)

## Choosing a Class

------------------------------------------------------------------------

**Please request the smallest class the work fits within.** A larger class is
not faster for a model that already fits in a smaller one. It is scarcer, so the
wait for it is longer, and it draws more heavily on the Service Unit budget for
every hour it is held.
→ [Service Units & Budgets](service-units-and-budgets.md)

*The figure that decides the class is memory, not speed.* A model's parameters,
its optimizer state, and the activations for one batch all have to sit on the
card at once. A run that fails with a CUDA out-of-memory error has two usual
remedies, a smaller batch size or the next class up, in that order — a smaller
batch costs nothing and is available immediately.

**One GPU is the normal case.** Single-GPU work is mostly a matter of moving a
model and its batches onto the device; using several GPUs at once is a code
change rather than a launch flag, and a substantial one — in PyTorch,
`nn.parallel.DistributedDataParallel` or a library such as Hugging Face
Accelerate.

**The defaults are one GPU per pod and one GPU across a namespace at any one
time.** More than that is available by arrangement; please write to us and say
what the work is.
→ [Defaults & The Three Resource Tiers](../running-jobs/launch-sh-reference.md#defaults--the-three-resource-tiers)

## Requesting a Class

------------------------------------------------------------------------

A GPU session asks for two things: how many GPUs, and which class of GPU.

```bash
launch-scipy-ml.sh -g 1 -l gpu-class=medium
```

**`-g` is the count and `-l gpu-class=` is the size band.** The five literal
values are `extra-small`, `small`, `medium`, `large` and `extra-large`.

**Always pass the class label on a GPU request.** Medium and above sit behind
`NoSchedule` taints, so a pod that asks for a GPU without naming a class has
nowhere to be scheduled.

**The workspace is what grants class access.** Each workspace is given one or
more classes matching the work it was provisioned for, and a class the workspace
was not granted is refused however idle the hardware is. For a member who belongs
to several workspaces, `-W` chooses which one the launch goes into — and it is
the workspace that carries the class grant and the Service Unit budget.
→ [Belonging to Several Workspaces](../workspaces-and-storage/what-a-workspace-is.md#belonging-to-several-workspaces)

**`-g` is GPU and `-G` is group.** The lower-case flag asks for a card. The
upper-case one does something else entirely, and the error that follows is not
obviously about capitalization.
→ [`launch.sh` Reference](../running-jobs/launch-sh-reference.md)

**`-v` is a different mechanism at a different layer.** It names a specific GPU
model rather than a size band. Both work; workspace grants, reservations and
quotas are all expressed in classes, so `-l gpu-class=` is the usual form and
`-v` is for pinning the hardware.

**For Slurm users**, `--partition` is not a scheduling partition here — it is
forwarded as a `gpu-class` label, so `--partition medium` asks for the `medium`
class.
→ [Coming from HPC](../reference/coming-from-hpc.md#option-mapping)

## On Datahub, the Class Is Preset

------------------------------------------------------------------------

**From the browser there is no GPU class to choose.** The class is set on the
environment a workspace publishes, so it arrives baked into whichever profile is
selected from the spawn menu. There is no control to change it and nothing to
type.

**Which means the menu is the decision.** Where a course offers both a CPU option
and a GPU option, choosing the GPU option is choosing its class as well. Work that
needs a different class from the one a course publishes is a conversation with the
instructor or TA, not a setting.

*Where a course does not publish a GPU environment at all, the command line is the
same access used differently.*
→ [Working from the Command Line](../working-from-the-command-line.md)

## When the Label Is Missing

------------------------------------------------------------------------

**`medium` and above sit behind `NoSchedule` taints.** A GPU request with no
`gpu-class` label, or with the label misspelled, has nowhere to land: the pod
stays pending and eventually fails with `0/5 nodes available`.

*This is the single commonest GPU launch failure, and the message does not
mention the label.* The spelling of `gpu-class` and of the class name is the
first thing to check against it, ahead of concluding that the cluster is full.
→ [When the Cluster Is Full](quotas-and-availability.md#when-the-cluster-is-full) ·
[Error Messages](../reference/error-messages.md)

## Confirming the Allocation

------------------------------------------------------------------------

Inside the running container, two commands settle what was actually allocated:

```bash
python -c "import torch; print(torch.cuda.get_device_name(0));"
nvidia-smi
```

**The first is the one to run when code reports no device found**, which is
much more often an environment problem than a scheduling one — an image without
CUDA tooling, for instance, cannot see a card that is genuinely attached. The
`rstudio-notebook` image derives from the CPU image and is not GPU-enabled at all.
→ [Standard Images](../environments/standard-images.md)

**The second names the model and how much memory it has**, which is how a session
is confirmed to be on the expected class rather than one adjacent to it. It also
reports what is currently using the card — the practical way to tell whether a
training run is actually on the GPU rather than quietly on the CPU.

*Please check this once at the start of a long run.* A job that never touches the
GPU is also a job the idle culler will reclaim the card from.
→ [What Ends a Session](what-ends-a-session.md#what-counts-as-idle)

**To see what the cluster currently holds**, the status page lists the GPU models
present on each node and how many are free.
→ [The Status Page](quotas-and-availability.md#the-status-page)

## From Reservation to Running Session

------------------------------------------------------------------------

**A reservation is a guarantee of access, not a running job.** Booking a window
does not start anything. When the window opens, a session is launched the usual
way, and what the booking buys is that the capacity is there and that the session
is admitted ahead of the walk-up queue.

**The claim window is 15 minutes.** A window that is not claimed inside it is
cancelled, the capacity returns to the pool, and the window is gone for the rest
of its length.
→ [The Claim Window](reservations.md#the-claim-window)

**How a booked window is selected on the Datahub spawn form is not documented
anywhere.** We are stating that plainly rather than describing a plausible
interface. *A member who has booked a window and cannot see how to use it has met
this gap rather than made a mistake.* Please
[write to us](mailto:datahub@ucsd.edu) and we will walk through it — and the
answer will be published here.

## Caveats & Limitations

------------------------------------------------------------------------

**Launching without a booking is not free.** It creates a reservation on the
member's behalf and draws Service Units, exactly as a booked window would. There
is no exploratory launch.
→ [On-Demand Leases Charge Budget](service-units-and-budgets.md#on-demand-leases-charge-budget)

**The runtime asked for is the runtime charged.** Please request the time the work
needs rather than the maximum permitted. A session must be stopped explicitly;
logging out does not stop it.
→ [The Runtime Limit](../running-jobs/job-modes-and-limits.md#the-runtime-limit)

**A GPU that is not in use is reclaimed.** Idle culling applies to every class,
reservation or no reservation.
→ [What Ends a Session](what-ends-a-session.md)

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
