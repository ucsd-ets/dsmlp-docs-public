# Datasets: Shared, Restricted & Licensed

------------------------------------------------------------------------

> **Draft for review.** The mechanism for staging shared data is confirmed; the
> inventory is not, and one published claim about restricted data is wrong and
> should be corrected at its source.
>
> - **Decision needed:** `KB0030470` ("Policies — Sensitive Data") and
>   `KB0030606` both state a flat P3/P4 prohibition **with no review path**.
>   Those articles are the ones that are wrong: P4 is prohibited, but **P3 may be
>   permitted after review**. This is not a cosmetic difference. A researcher who
>   reads either article concludes that they are categorically excluded and never
>   asks, so the failure mode is silence — we never see the request and never
>   learn that the project went elsewhere. Please correct those two articles
>   rather than relying on this page to outrank them.
> - **Decision needed:** the course dataset path convention. Two course sites show
>   two shapes — `/datasets/cs252d-sp22-a00-public/` and, without the prefix,
>   `/ds102-wi22-a00-public/`. This page publishes the first. Someone should
>   confirm whether the second was a separate mount or an error in the assignment.
> - **Missing:** the P3 review itself. No source says who reviews a request, what
>   must be submitted, what an approval permits, or what controls a permitted
>   dataset then sits under. All this page can honestly publish is "ask early, and
>   allow 4-6 weeks or longer".
> - **Missing:** what "restricted to a specific course" means on disk.
>   `KB0030587` says datasets may be published system-wide or restricted to one
>   course, but nothing states whether a restricted tree is enforced by
>   permissions or is merely not advertised. A reader deciding where to put
>   licensed data needs that answer.
> - **Missing:** there is no published list of licensed datasets held on the
>   cluster, and no documented route to be added to one.
> - **Unverified:** the named corpora below come from the Research IT Research
>   Cluster user guide, whose dataset table still lists ImageNet Fall 2011 and
>   similar vintages. The live catalog is the authority, and this page quotes no
>   sizes for that reason.
> - **Unverified:** the Nielsen example — the path `/uss/dsmlp-a/nielsen-dataset/`
>   and the phrase "authorized users" — comes from the same guide. Whether that
>   mount is reachable from a Datahub/DSMLP workspace, and how authorization is
>   granted, is not documented anywhere we can find.
> - **Check before publishing:** that `datahub.ucsd.edu/hub/datasets` is still the
>   catalog, and that it is reachable by students rather than staff only.

Large data belongs in one place that everyone reads, not in a copy per person.
The cluster provides two such places, and which of them holds a dataset
determines what its size counts against. Two further restrictions land on the
same shelf and are separate questions: **classification** is about what the data
*is* — whether the University's protection level permits it here at all — and
**licensing** is about what may be *done* with data the campus has already
acquired.

## Where Shared Data Lives

------------------------------------------------------------------------

**`/datasets` is the cluster-wide tree.** It is present in the container and on
the login node, and holds common training corpora — MNIST, CIFAR-10,
Tiny-ImageNet, ImageNet, Caltech256, ShapeNet and others — alongside data staged
for particular courses. Data is placed there by us, on request, and it sits
outside both the workspace and personal quotas.

**`public/` is the workspace's own shared area.** Course datasets most often
live here, staged by the instructor or the course grader account, readable by
every member of the workspace.
→ [The Shared Workspace Area](your-files-and-quotas.md#the-shared-workspace-area)

*Which of the two a course uses is the instructor's choice.* Data that several
courses want, or that is too large to sit in a workspace, tends to be staged
under `/datasets`; data specific to one course tends to sit in `public/`.

## Finding What Is Available

------------------------------------------------------------------------

The catalog of cluster-wide datasets is published at
[datahub.ucsd.edu/hub/datasets](https://datahub.ucsd.edu/hub/datasets). From a
running environment or from the login node, the tree itself is browsable:

```bash
cd /datasets
ls
```

Course data staged under `/datasets` follows the workspace ID —
`/datasets/<workspace-id>-public/` — so a course's own material is findable
without a catalog entry.

## Read It Where It Is

------------------------------------------------------------------------

**Please do not copy a shared dataset into a home directory.** It is the fastest
way to exhaust a quota, and the copy is no closer to the job than the original:
the same filesystem is visible from the container and from the login node.
→ [What Usually Fills a Quota](your-files-and-quotas.md#what-usually-fills-a-quota)

**Code points at the shared path instead.** Notebooks written against a local
machine usually need one edit — the dataset path — and nothing else.

Where a run genuinely needs a derived subset, the subset — not the source
corpus — is what belongs in a home directory.

## Asking for a Dataset to Be Staged

------------------------------------------------------------------------

**Where a dataset is large and several people need it, please ask us to stage
it** rather than downloading it into each home directory. Email
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) with what the data is, roughly how
large it is, and who needs to read it.

- **Course dataset distribution up to 500 GB** is accommodated as a matter of
  course; larger corpora are accepted on a space-available basis.
- **Datasets may be published cluster-wide or scoped to one course.** Say which
  in the request.
- **Research datasets** are handled by Research IT, at
  [rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu).

*Please raise anything confidential, licensed, or subject to a data use agreement
before it is uploaded*, not after.

**Small downloads need no request.** `wget` and `curl` are available on the
login node and in the container; for anything substantial, please see
[Moving & Sharing Data](moving-and-sharing-data.md).

## Restricted & Licensed Datasets

------------------------------------------------------------------------

**P4 data is prohibited on Datahub and DSMLP** — highly-sensitive information
such as clinical records or export-controlled material. There is no review path
and no exception.

**P3 data may be permitted after review.** Legally or contractually protected
information is not categorically excluded; it requires a conversation before any
of it reaches the cluster. *Vetting may take 4-6 weeks or longer.*

**Where either may apply, please raise it with us early.** For instruction and
coursework, email [datahub@ucsd.edu](mailto:datahub@ucsd.edu); for research,
Research IT at [rcd-support@ucsd.edu](mailto:rcd-support@ucsd.edu).
→ [Policy](../reference/policy.md#data-classification)

## What Falls into These Categories

------------------------------------------------------------------------

The University's [classification
levels](https://security.ucop.edu/policies/institutional-information-and-it-resource-classification.html)
are the authority. The examples our own documentation gives are:

| Kind of data | Examples |
|---|---|
| Government classified or controlled | CUI, CTI, ITAR, FISMA |
| Health and personal information | PHI/HIPAA, IRB-controlled data, statutory PII |
| Student records | Other students' grades or academic records (FERPA) |
| Contractually protected | Information subject to certain Data Use Agreements |

**The student-records line catches more people than it looks like it will.** A TA
or grader working with identifiable grades is handling protected data, and the
grading tools are built to hold that material.
→ [Grading](../grading/README.md)

## Licensed and Subscription Data

------------------------------------------------------------------------

**Some data on the cluster is licensed rather than open**, acquired under terms
that limit who may read it and what may be done with the results. Such corpora
are staged read-only and released to an authorized group rather than to everyone
— the Nielsen subscription datasets held for the Chicago Booth Kilts Center are
the standing example, mounted read-only outside the general `/datasets` tree.
→ [Mounting External Storage](your-files-and-quotas.md#mounting-external-storage)

For licensed data, the terms usually mean:

- **Read it in place.** Duplicating it into a home directory makes a second copy
  under the same terms, and consumes quota.
- **Do not pass it on.** Access is granted to an individual, not to that
  person's collaborators, and moving the data into a shared or outward-facing
  location is a licensing decision, not a file operation.
  → [Sharing with People Who Have No Cluster Account](moving-and-sharing-data.md#sharing-with-people-who-have-no-cluster-account)
- **Delete what is no longer needed.** Derived subsets and intermediate files
  accumulate, and they inherit the terms of their source.

**Datasets may be published cluster-wide or scoped to a single course.** Where a
course or lab has acquired data under terms, please say so in the request to have
it staged, so that it is scoped correctly from the start rather than moved
afterwards.

## Two Practical Consequences

------------------------------------------------------------------------

**Restricted data does not travel to the end of the course by default.** Large
datasets cannot be archived when a course environment is purged; a corpus that
has to be kept is a conversation to have before the term ends.
→ [Archiving on Request](../access/when-access-starts-and-ends.md#archiving-on-request)

**Datahub and DSMLP are not a place to publish restricted data outward.** The
platform is not for externally-available services or applications except as
required for coursework or projects, and that limit applies with particular force
to anything held under terms.

------------------------------------------------------------------------

If you still have questions or need additional assistance, email us at
[datahub@ucsd.edu](mailto:datahub@ucsd.edu) or submit a ticket to the
[ITS Service Desk](https://support.ucsd.edu/).
