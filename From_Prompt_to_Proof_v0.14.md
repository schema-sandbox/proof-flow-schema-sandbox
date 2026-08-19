---
title: "From Prompt to Proof: The Anatomy of AI-Assisted Mathematical Discovery in 2026"
author: Tengjiao Liu (psi@psi.run, psi.run)
date: "Version 0.14 — Corpus evidence snapshot: 3 August 2026; C17 repository resnapshot and branch-merge audit: 3 August 2026"
abstract: |-
  Reports of frontier language models resolving or refuting open
  mathematical problems multiplied in 2026. The public record, however,
  mixes unlike forms of evidence: an X thread, a shared conversation, an
  executable checker, a compiled Lean theorem, an expert review, and a
  later human proof do not support the same claim.

  We apply a preliminary single-analyst coding protocol to public evidence
  visible through 1 August 2026. The corpus contains seventeen workflow
  episodes covering more than thirty-six mathematical target families.
  Episodes, rather than posts or files, are the unit of analysis; batch
  campaigns may contain nested task-level subepisodes or result families,
  and a superseded intermediate result may remain causally important as a
  bridge to a stronger result. The newly added OpenAI campaign is counted as
  one workflow episode. Its ten public result families, twelve
  `formalization.yaml` main-result entries and Comparator configuration
  bundles, thirty-eight named theorem declarations, and four explicitly
  bound definitions remain nested analytical units rather than independent
  workflow episodes. Each
  episode is assessed along six dimensions: process provenance, artifact
  availability, deterministic verification, independent review, novelty,
  and autonomy or attribution. We also record a conservative lower-bound
  tier for visible human labor.

  The more credible episodes show that target selection, semantic binding,
  search topology, persistent state, accepted research-state transitions,
  continuation control, adversarial falsification, formalization, repair,
  cross-model handoff, trace derivation, trusted-challenge binding,
  Comparator-coverage accounting, artifact-correlation accounting, human
  judgment, and post-solution maturation jointly determine what can
  reasonably be claimed. We describe these episodes through nine workflow components
  and four operational configurations. Four recurring mechanisms are
  formulated as testable hypotheses, and nine recurrent cross-case failure
  modes delimit the evidence. Mathematics makes these distinctions unusually
  observable; transfer to industrial research would additionally require
  validated physical models, manufacturability, qualified test systems,
  configuration control, and field feedback.

  Version 0.14 reconciles two synchronized Version 0.14 branches: a
  primary-source C17 audit and a research-state/continuation-control
  extension inspired by LoopX. The C17 re-audit retains the episode-level
  coding but corrects the formal-target hierarchy, updates the repository
  snapshot from an earlier zero-parent root commit to the current distinct
  zero-parent root, distinguishes solution `sorry_count` from intentional
  challenge placeholders, records nanoda as configured rather than executed
  by this audit, and identifies a concrete Comparator-coverage gap between
  the permanent headline and the named formula-only challenge bundle.
---

# Introduction

During 2026, public reports of AI-assisted mathematics began to expose more
than final answers. Some threads documented how problems were screened,
how targets were specified, how parallel routes were managed, how proofs
were attacked, and how formal or executable feedback changed the argument.
That additional visibility is valuable, but it also makes the evidence
harder to read. A root post, a shared chat, a repository, a successful Lean
build, and a human-written proof answer different questions.

The study is therefore concerned with process and evidential scope rather
than headline counts. For each episode, it asks how a candidate result was
selected, produced, challenged, repaired, checked, attributed, and later
matured; which artifacts remain unavailable; and what each available
artifact actually warrants. The corpus consists of seventeen public workflow
episodes. It includes several campaigns with multiple nested targets, multiple Erdős
problem formalization episodes, an exact-checker-repair episode, the unit-
distance research trace and its later maturation, two minimal-prompt or
finite-certificate cases, a Devin-orchestrated pipeline, a documented
candidate resolution of Erdős Problem #477, the von-Mangoldt-chain solution
and maturation of Erdős #1196, a reported 180,000-line personal Lean
formalization of Erdős #870, an OpenAI internal-model campaign later digested
into a three-result human paper, and a computational-social-choice episode in
which a five-voter bridge reduction, failed cross-model notes, a stronger
three-voter reduction, and two Lean repositories formed one continuous
support path. The corpus also includes an OpenAI Astra campaign released as
ten result families, a 249-page manuscript, a 62-page derived process
narrative, and twelve Comparator-bound Lean targets.

Four questions organize the study:

1. Which workflow components recur across independently organized
   AI-mathematics episodes?
2. Where do substantive errors enter, and which mechanisms remove or
   merely relocate them?
3. How is labor divided among language models, proof assistants, exact
   programs, human mathematicians, and public reviewers?
4. Which observations plausibly transfer to scientific and industrial
   research, and which depend on mathematics-specific affordances?

What the evidence does support is a process-level observation:

> **In the most credible public cases, the strength of an AI-assisted
> mathematical claim depends on the surrounding research system—target
> selection, verification, repair, and review—rather than on the base
> model or prompt alone.**

The system includes target selection, semantic binding, search budget,
state continuity, transition acceptance, continuation admission,
adversarial review, deterministic verification, repair lineage, human
intervention, and an external maturation pipeline. A trajectory becomes
durable research state only when the record makes visible what changed, why
it changed, what evidence was accepted, which obligations remain open, and
what authorizes the next bounded turn.

Figure 1 in the cross-case synthesis maps the operational
configuration of each episode against the strongest visible public
evidence tier. The axes are deliberately orthogonal: a compact finite
counterexample from an O1 session may be more auditable than an O4
pipeline whose repository, formal target, or build cannot be pinned.
Conversely, an elaborate workflow may be methodologically informative
while remaining evidentially immature.

## Contributions

Six elements define the contribution.

1. It reconstructs seventeen public workflow episodes covering more than
   thirty-six mathematical target families using a six-dimensional evidence card.
2. It introduces two orthogonal descriptive views: nine workflow
   components and a map from four operational configurations to the
   strongest visible public evidence tier.
3. It adds conservative lower-bound coding of visible human labor, making
   hidden curation and maturation work harder to erase behind a global
   “fully autonomous” label.
4. It freezes an explicit coding manual, reports descriptive corpus
   statistics and a per-case mechanism-signal matrix, and formulates four
   mechanisms as controlled, equal-budget hypotheses rather than causal
   conclusions.
5. It adds a research-state transition lens that distinguishes operational,
   epistemic, claim, and artifact states; separates observations and
   proposals from accepted transitions; and decomposes state management into
   trajectory retention, transition acceptance, and continuation or handoff
   control.
6. It identifies nine recurrent cross-case failure modes with concrete
   controls, instantiates a machine-readable JSON evidence ledger, and adds
   single-campaign audit distinctions for derived traces, correlated artifact
   triangulation, trusted challenge roots, Comparator coverage, repository
   snapshot lineage, cost boundaries, and benchmark completeness without
   converting them into population-level claims.

## Claim boundaries and threats to validity

The sample is selected for public process visibility and is therefore subject to survivor and reporting biases. The descriptive findings below should not be read as population-level success rates or causal claims.

Coding in Version 0.14 remains single-analyst. A frozen codebook, JSON
Schema validation, and automated cross-field checks reduce clerical drift
but do not establish interpretive reliability. No Cohen's $\kappa$,
weighted $\kappa$, or Krippendorff's $\alpha$ is reported. The
frequency counts and mechanism matrix below are therefore descriptive of
this frozen corpus and coding pass, not population estimates. These limitations directly constrain how the descriptive counts should be read.

## Related work: controlled benchmarks and wild observational evidence

Controlled studies and formal benchmarks answer different questions
from this case series. The Gödel Test examined a fixed set of conjectures
under a specified prompting regime and reported both near-solutions and
failure modes (Feldman and Karbasi 2025). A Gemini-based study processed
700 open-labeled Erdős problems, used automated filtering, and relied on
expert assessment for correctness and novelty (Feng et al. 2026).
Formal Conjectures provides a large and evolving Lean benchmark of
research-level statements, making statement fidelity and formal target
selection measurable (Firsching et al. 2026). Automated Conjecture
Resolution, LEAP, and large-scale formal proof search evaluate systems in
which informal reasoning is coupled to Lean feedback (Ju et al. 2026;
Kung et al. 2026; Tsoukalas et al. 2026).

### Perspective-guided question generation and collaborative knowledge curation

STORM addresses a different stage of the research process: before long-form
writing, it discovers perspectives, simulates retrieval-grounded
writer--expert conversations, asks follow-up questions, and constructs a
hierarchical outline. In a NAACL 2024 evaluation, experienced Wikipedia
editors judged its articles more organized and broader than an
outline-driven retrieval baseline, while also identifying source-bias
transfer and over-association of unrelated facts as unresolved risks
(Shao et al. 2024). Co-STORM adds multiple grounded LM experts, a moderator,
human steering, and a dynamic mind map intended to expose "unknown
unknowns" and reduce the cognitive burden of extended discourse. In the
reported human evaluation, participants preferred Co-STORM to both a
search engine and a RAG chatbot on the studied information-seeking tasks
(Jiang et al. 2024).

These systems are relevant as **controlled pre-search and pre-writing
scaffolds**, not as mathematical-discovery episodes. They do not generate
proof-kernel evidence, establish theorem novelty, or validate the seventeen
public workflows studied here. Their value for this paper is narrower:
they make the question agenda, perspective portfolio, human steering, and
shared conceptual map explicit—variables that the current public
AI-mathematics record usually leaves hidden. The open-source STORM
implementation is modular across language models and retrievers and can
also operate over user-provided corpora, making it a practical candidate
for future controlled AI4Math experiments (Stanford OVAL 2026).

Those projects are controlled benchmarks, system evaluations, or formal
proof-search studies. The present work is a **wild observational case
series**: independently organized episodes whose evidence is distributed
across social-media reply chains, shared conversations, manuscripts,
repositories, corrections, community problem pages, and later human
papers. Its contribution is process forensics and comparative workflow
analysis.

### Long-running agent control planes and LoopX

LoopX is an open-source local control plane for long-running AI agent work
(Huang and contributors 2026). It is not a mathematical-discovery system and
does not enter the seventeen-episode corpus. Its relevance is methodological.
The project keeps lifetime goals, concrete user gates, executable todos,
peer claims and leases, evidence, quota, and handoffs outside ephemeral chat
memory while external runtimes execute bounded turns. Its architecture
separates the execution path—agent to capability to provider—from the control
path, in which provider observations are normalized into typed transition
proposals and committed by a durable kernel. It explicitly states that an
observation is not a transition and that automatic spend should follow
validated writeback rather than a timer or model self-report.

This engineering vocabulary sharpens a distinction already implicit in this
paper's **M: state and trajectory management** component. Persistent history is
not the same as accepted state. A model can remember a failed route without
recording why it was closed; a tool can produce a result without changing the
epistemic state; and a handoff can transfer text without transferring scope,
artifacts, open obligations, or the next acceptance predicate. LoopX therefore
motivates additional coding fields and controlled experiments. It does not
validate any mathematical mechanism, establish that the public cases used a
similar control plane, or justify reconstructing missing state histories from
final papers.

# Method

## Corpus and case selection

Episodes were included when at least two of the following were visible:
a continuation thread, a public conversation or prompt, a manuscript or
technical report, code or a proof-assistant artifact, an explicit repair
or correction, an external review, or an unusually detailed route
history. Table 1 summarizes the seventeen episode-level units. “Reported”
means that the process fact is author-reported but the full underlying
artifact was not independently captured.

Controlled benchmark studies, large formal-search evaluations, and
general-purpose knowledge-curation systems such as STORM/Co-STORM were not
counted as corpus episodes. They appear in Related Work because their target
sets, evaluation procedures, or information-seeking regimes are designed in
advance, whereas this corpus concerns independently organized public
mathematical-discovery episodes. STORM is not C17: it does not
report the resolution of an open mathematical target and is used only as an
adjacent design comparison. Other
public claims were screened out when only a root announcement was available,
the mathematical target could not be identified, or no process, artifact,
repair, or review evidence could be recovered. The exclusions are methodological,
not judgments about whether the underlying mathematics is true.

**Visible human-labor tiers.** `L0` denotes minimal visible
intervention (typically no more than a short prompt/start-and-release
sequence); `L1` denotes bounded curation, cleanup, checking, or
single-researcher coordination; `L2` denotes sustained multi-day or team
work involving reconstruction, formalization, or maturation; `L?` means
that public evidence is insufficient. These are conservative lower
bounds on *visible* human effort, not total labor estimates, and they
exclude model runtime.

**Table 1. Core workflow episodes and strongest visible public evidence.**

| ID | Episode and target | Model or system | Human labor | Strongest visible public evidence |
|---|---|---|:---:|---|
| **C1** | Shouqiao Wang, six Erdős targets | GPT-5.6 Sol, Codex, selected Lean | **L2** | Several manuscripts and selected Lean/CI artifacts; evidence maturity is uneven across targets |
| **C2** | Adam Holter, ten-candidate campaign | GPT-5.6 Pro, same-model audits | **L?** | Ten public Pro sessions and selected exact checks; unrefereed, correlated audit |
| **C3** | David Turturean et al., Erdős #330 | ChatGPT-5.5 Pro, scaffold, Lean | **L1** | Public Lean package and community PROVED (LEAN) state; full chat unavailable |
| **C4** | Liam Price et al., Erdős #635 | GPT-5.2 Pro, Aristotle | **L1** | Lean artifact for one subproblem and a public downgrade of the broader claim |
| **C5** | Pietro Monticone et al., Erdős #650 | GPT-5.4 Pro, Aristotle, Lean | **L2** | Lean proof and human-written arXiv paper; a defective prose step was replaced |
| **C6** | Acer et al., Erdős #728 | GPT-5.2 Pro, Aristotle | **L2** | Lean proof, human write-up, and public discussion after target reconstruction |
| **C7** | Adam Holter, fixed-perimeter Conjecture 1.2 | GPT-5.6 Pro, exact Python checker | **L1** | Destructive audit, repaired proof, and millions of finite checks; no proof-kernel artifact |
| **C8** | OpenAI unit-distance disproof | Internal model, AI grading, human editors | **L2** | Public proof, rewritten trace, nine-author human proof, and later strengthening |
| **C9** | Dmitry Rybin, Dinitz–Garg–Goemans counterexample | GPT-5.6 Pro | **L2** | Concrete finite graph and reported independent checks; full session and verifier incomplete |
| **C10** | Anirudh Chakravarthy, two minimal-prompt targets | GPT-5.6 Sol Pro | **L0** | Technical reports are reported, but captured verification remains limited |
| **C11** | Jared Zoneraich/Devin, graph-conjecture batch | Devin, Fable, GPT-5.6 Sol, Lean | **L?** | Repository/video and no-`sorry` Lean builds reported; target-to-build mapping not pinned |
| **C12** | Patrick White/MathDyad, Erdős #477 | GPT-5.6 Sol; Claude source checks | **L1** | Auditable candidate trail and bounded review; no Lean proof or complete expert validation |
| **C13** | Liam Price, Jared Duker Lichtman et al., Erdős #1196 | GPT-5.4 Pro; later human paper and Lean formalization | **L2** | Multi-author proof, public formalization, and expert/curator maturation |
| **C14** | David Turturean, Erdős #870 | ChatGPT-5.5 Pro, Codex, Claude Opus 4.8, Lean 4 | **L2** | Approximately 180,000-line sorry-free/axiom-free project reported; clean rebuild not pinned |
| **C15** | Alexeev, Putterman, Sawhney, Sellke, and Valiant, three Erdős questions | Internal OpenAI model; later GPT-5.4 Pro recreation attempts | **L2** | Six-page human paper and partial public-model recreation; internal trace unavailable |
| **C16** | Dominik Peters, Kemeny rank aggregation for three voters | GPT-5.6 Sol Ultra, Claude Fable 5, Lean 4 | **L2** | arXiv proof and two public Lean repositories; independent review and clean rebuild remain pending |
| **C17** | OpenAI, ten advances in mathematics and theoretical computer science | Internal Astra, human/model manuscript preparation, Lean 4, Comparator | **L2** | Public manuscript, derived walkthroughs, current and prior root snapshots, twelve trusted challenge/configuration bundles, and Comparator instructions; external review pending |

Material human roles, status qualifications, and principal limitations are retained in Appendix C rather than compressed into this table.

## Unit of analysis and coding rule

The unit is a **research workflow episode**:

> one operator or coordinated team + one bounded time window + one shared
> orchestration and support path.

A root post, shared conversation, manuscript, repository, correction,
and later review are evidence objects inside the same episode when they
support the same run. Distinct theorem targets inside a batch campaign
are coded as **nested subepisodes** for within-campaign comparison, not
as statistically independent workflows. This is why Holter’s ten public
Pro sessions count as one campaign-level episode and ten task-level
subepisodes. Conversely, Holter’s fixed-perimeter run is separate because
it has a distinct target, prompt sequence, repair history, and support
path. The same rule applies to C17: the OpenAI release is
one campaign episode, not ten statistically independent workflows. Its ten
public result families, twelve main-result/configuration bundles, thirty-eight
named theorem declarations, and four bound definitions are nested units used
to study dependency, formal binding, coverage, and release topology.

Features are coded as clearly observed, partially visible or
author-reported, or not established. Absence of public evidence is not
coded as evidence of absence.

## Coding manual and reliability status

Version 0.14 uses `coding_manual_2026_v0.3.md`. Every non-missing code
must cite at least one evidence object in the episode record. For the
workflow and mechanism matrices, `[Y]` means direct, claim-specific
support in the frozen public evidence; `[P]` means partial visibility,
author report, indirect support, or unresolved source binding; and `[-]`
means that the frozen corpus does not establish the feature. `[-]` is not
an assertion that the activity did not occur. Ordinal O, E, and L labels
use the lowest defensible tier when the public record is uneven.

The codebook also separates the **presence** of a mechanism from its
**outcome**. For example, a destructive audit may be visible even when it
finds no material defect, and a formalizer may be present without
rewriting the proof. This prevents a mechanism from being coded only in
successful episodes.

The present release has one analyst. Machine validation checks allowed
vocabularies, tier ranges, required evidence fields, and selected
cross-field consistency rules; it cannot measure interpretive agreement.
A confirmatory release should give a second coder the same frozen source
pack and codebook without the first coder's labels, report raw agreement
and field-level reliability (weighted $\kappa$ for ordinal tiers and
Cohen's $\kappa$ or Krippendorff's $\alpha$ for nominal fields), and
publish the pre-adjudication labels plus a disagreement log. Until that
step is completed, no inter-coder reliability claim is made.

## Six-dimensional evidence card

A single “verified” flag collapses non-equivalent claims. Each episode is
therefore coded along six dimensions.

| Dimension | Audit question | Typical non-implication |
|---|---|---|
| **Process provenance** | Are prompts, timing, branches, interventions, and repairs visible, attested, or missing? | A public result does not imply a complete process trace |
| **Artifact availability** | Are manuscripts, code, formal targets, logs, and data inspectable and versioned? | File existence does not imply successful execution |
| **Deterministic verification** | Did a proof kernel accept an exact theorem, or did a fail-closed program check its declared domain? | A kernel/checker does not establish source binding or novelty |
| **Independent review** | Did a distinct reviewer inspect the relevant claim, and is the review scope stated? | Same-model repetition does not create independence by count |
| **Novelty and prior art** | What theorem, proof, or method was searched against which corpus as of what date? | “No match found” does not prove global novelty or training independence |
| **Autonomy and attribution** | Which steps were performed by model, operator, formalizer, exact tool, or later mathematicians? | One global “AI-only” label erases material intervention |

An artifact-access ladder used for compact evidence cards is defined in
Appendix A. It is not a second correctness score.

## Terminology

To avoid role confusion, this paper uses three terms consistently:

- **formalizer**: a proof-assistant-mediated system that translates,
  completes, repairs, or replaces part of an argument in a formal
  environment, such as Aristotle coupled to Lean;
- **checker**: an exact executable program over a declared finite or
  symbolic domain;
- **verifier**: the umbrella term for any deterministic proof kernel,
  formalizer output check, or exact checker.

A formalizer may be a research contributor; a checker may have a narrow
epistemic ceiling; a verifier is not automatically an independent
reviewer.

## Model-label normalization

Model and product names are recorded exactly as reported by the episode
authors. They are provenance labels, not normalized experimental
conditions: web products, API snapshots, long-running modes, and agent
wrappers may differ even when their names share a version number.

| Author-reported label | Episodes | Reported access or role | Treatment in this paper |
|---|---|---|---|
| **GPT-5.2 Pro** | C4, C6 | ChatGPT Pro sessions reported by operators | Not assumed equivalent to later Pro or Sol modes |
| **GPT-5.4 Pro** | C5, C13, C15 | ChatGPT Pro generation, public recreation, or expert-maturation workflows | Recorded separately from internal models, formalizers, and later human derivations |
| **ChatGPT-5.5 Pro** | C3, C14 | Web sessions embedded in custom scaffolds and long formalization loops | Product label retained; exact serving snapshot and tool context unavailable |
| **GPT-5.6 Pro** | C2, C7, C9 | Public or reported Pro sessions | Same label does not establish identical prompts, tools, or backend state |
| **GPT-5.6 Sol / Sol Pro** | C1, C10, C11, C12 | Long-running or agent-mediated search mode, as author-reported | Sol and Sol Pro are not collapsed into one controlled condition |
| **GPT-5.6 Sol Ultra** | C16 | Multi-subagent mode in the Codex product, as described by Peters | Treated as a distinct orchestration condition rather than another name for a standard Pro session |
| **Codex** | C1, C14, C16 | Coding, artifact, formalization, or multi-subagent orchestration assistance | Tool/model role coded separately from the main reasoner |
| **Aristotle** | C4–C6 | Formalization and, in C5, proof repair | Treated as a formalizer, not merely a base-model label |
| **Devin / Fable** | C11 | Controller and specialist-agent stack | Treated as orchestration infrastructure pending commit-pinned reconstruction |
| **Claude** | C12, C14, C16 | Primary-source spot checks, compiler-driving assistance, reduction simplification, and failed-route notes | Not treated as a complete independent proof verifier; failed outputs may still become handoff artifacts |
| **Internal OpenAI model** | C8, C15 | Internal research runs later exposed through papers or reports | Exact public serving identifier unavailable; no equivalence to public labels is assumed |
| **Internal Astra** | C17 | Internal research campaign, later manuscript preparation and formalization | Recorded as an internal model identity; private serving snapshot, prompts, route history, and denominator remain unavailable |

## Source collection, archival, and missing evidence

Each social-media thread was treated as an event stream: root post,
author replies, linked conversations, attachments, repositories,
corrections, and current problem-page status. The evidence snapshot is
3 August 2026. Source URLs and captured artifacts are stored in a
content-addressed local case library with per-file SHA-256 manifests.
Mutable pages are tagged as full capture, partial capture, or URL-only.
Unless another date is stated, mutable web sources in the references were
last accessed on 3 August 2026; per-source capture state and hashes live in
the companion ledger. A public immutable deposit is required before
arXiv v1; until then the manuscript does not claim that inaccessible
sessions have been fully archived.

The newly added #1196 and short-proofs papers are pinned by arXiv identifiers
`2605.00301` and `2603.29961`. The #870 process thread is public, but
the repository URL, commit, dependency lock, and clean rebuild have not yet
been independently captured in the frozen archive; its 180,000-line claim is
therefore coded as reported. The Erdős #477 repository is pinned to commit `8440d59`
(23 July 2026). Its public record is unusually explicit about what was
and was not checked, but the complete model sessions are not public and
the repository itself states that no working number theorist has
completed a full proof review and that no Lean proof exists (White and
Claude 2026).

C17's primary sources were captured from the OpenAI announcement, the
249-page manuscript, the 62-page model-authored reasoning walkthroughs, and
two observed `openai/ten-proofs` root snapshots. The earlier audit pinned
`29362184c2b698c1b279bc85b3957ee813646c63`; the 3 August resnapshot pinned
current `main` at `94bc0feb6a9ff12c7d31d6de640a725c9d43d2b6`.
Both are zero-parent roots, and GitHub showed one current branch commit.
The repository declares Lean 4.32.0, locked dependencies, twelve
`formalization.yaml` main results and Comparator configurations, permitted
axioms `propext`, `Classical.choice`, and `Quot.sound`, and an
`agent-reviewed` status. Version 0.14 inspected the public artifacts,
configuration files, challenge protocol, and coverage hierarchy but did not
independently rebuild all solution modules or execute and archive all
Comparator/nanoda runs.

The Kemeny episode is pinned by arXiv identifier `2607.25540`. Two public
repositories, `DominikPeters/KemenyHardnessLean` and
`DominikPeters/HardnessReductionsLean`, expose the formalized reduction and
a broader library of certified hardness reductions. At the snapshot date
their public pages reported active histories and CI infrastructure, but
this audit had not yet completed an independent clean rebuild or frozen an
exact commit pair. The episode is therefore coded as E3 provisional rather
than as independently reviewed mathematics.


## No success-rate claim

Public campaigns are selected after the fact. Problem age, ambiguity,
certificate cost, and publication incentives alter which episodes are
visible. We therefore report no population-level success percentage. A
future benchmark should disclose a preregistered target set and compute

$$
\mathrm{SR}(\tau) = \frac{|S(\tau)|}{|A|}
$$

where $S(\tau)$ is the set of all preregistered episodes satisfying evidence threshold $\tau$, and $A$ is the set of all preregistered attempted episodes, with the threshold, duplicate policy, withdrawals, and failed attempts
specified before evaluation. Here an **attempted episode** means a
preregistered target that received at least one substantive generation,
search, proof, or counterexample action intended to resolve or refute it.
Abandoned, timed-out, duplicated-after-detection, invalidly scoped, and
withdrawn attempts remain in the denominator. Predeclared infrastructure
dry runs may be excluded only by a rule fixed before results are seen.

Here $\tau$ denotes a preregistered minimum evidence predicate. It may include an
E0–E5 artifact-access floor, but access alone is insufficient: the predicate
should also specify claim-specific requirements for exact checking, source
binding, review, and novelty.

## Research-state transition lens

Version 0.14 distinguishes four state planes.

| State plane | Operational question | Typical evidence |
|---|---|---|
| **Operational state** | Who owns the next bounded action, what is blocked, and may another turn run? | todos, gates, claims or leases, scheduler decisions, human instructions |
| **Epistemic state** | What is now known, excluded, retained, uncertain, or reformulated? | counterexamples, route obstructions, bridge results, prior-art updates |
| **Claim state** | What maturity and verdict is warranted for an exact proposition? | proof, checker, formal target, review, correction |
| **Artifact state** | Is a proof, script, repository, or report draft, broken, repaired, superseded, or released? | commits, build logs, formalizer deltas, release metadata |

The distinction prevents several false implications. A Lean build may change
the formal coordinate of Claim State without settling natural-language target
binding. A failed experiment may produce an accepted Epistemic State change
without proving a theorem. A human may change Operational State by redirecting
a route without making the new route correct. A polished paper may change
Artifact State while leaving the original discovery trace inaccessible.

A coded transition has the following provisional structure:

```yaml
ResearchStateTransition:
  episodeId: ...
  fromState:
    operational: ...
    epistemic: ...
    claim: ...
    artifact: ...
  triggerClass:
    HUMAN_INSIGHT | MODEL_PROPOSAL | COUNTEREXAMPLE |
    TOOL_OR_CHECKER_RESULT | FORMALIZATION_FAILURE |
    SOURCE_OR_PRIOR_ART_UPDATE | REPRESENTATION_SHIFT |
    EXTERNAL_REVIEW | RESOURCE_OR_CAPABILITY_CHANGE |
    PUBLIC_CORRECTION
  triggerEvidenceRefs: [...]
  proposalActorRef: ...
  acceptanceActorOrMechanismRef: ...
  acceptedDelta:
    operational: [...]
    epistemic: [...]
    claim: [...]
    artifact: [...]
  rejectedOrUnacceptedComponents: [...]
  nextObligationRefs: [...]
  handoffRefs: [...]
  visibility:
    DIRECTLY_OBSERVED | DERIVED_FROM_PUBLIC_TRACE |
    AUTHOR_REPORTED | NOT_ESTABLISHED
```

The unit is an **accepted delta**, not a private chain of thought. A model
statement that it found an error is a proposal; an exact counterexample, proof
kernel, scoped human decision, or public correction may support acceptance.
Where the public record does not expose the acceptance basis, the transition
is coded as reported or not established.

### Refinement of component M

The original nine-component framework is retained. Component M is decomposed
for selected deep dives:

- **M1 — Trajectory retention:** failed routes, open obligations, scripts,
  counterexamples, and prior attempts are preserved.
- **M2 — Transition acceptance:** the record shows what evidence or authority
  accepted the state change.
- **M3 — Continuation and handoff control:** the next actor receives scope,
  artifacts, unresolved obligations, and a basis for the next turn.

The full seventeen-case statistics are not recomputed in Version 0.14. Public
evidence is usually sufficient for M1 but often incomplete for M2 and M3;
forcing a complete recoding would create false precision.

# Case Reconstructions: Six Mechanistic Deep Dives and Eleven Compact Notes

Six episodes receive extended treatment because each isolates a distinct process mechanism: C5 (proof-assistant repair), C7 (destructive critique and checker risk), C8 (route replacement), C12 (transparent but bounded candidate review), C16 (bridge results and cross-model handoff), and C17 (correlated release triangulation and trusted-challenge verification). The remaining eleven are summarized in Table 2a and Table 2b; full notes are in Appendix F.

**Table 2a. Compact notes for episodes C1 to C9.**

| Episode and workflow signal | Current evidence boundary | Key process inference |
|---|---|---|
| **C1 — Contracted parallel search**: Problem screening, contract-like target specification, and parallel incompatible routes. | Maturity was uneven across outputs; public scope correction and prior-art issues block a campaign-level success-rate claim. | The separation between which problems to attack and how to manage routes within one problem is worth preserving. |
| **C2 — High-throughput nested cohort**: Ten task-level Pro sessions under a comparatively stable operator and audit style. | Same-model audits found real defects but remain correlated; the campaign denominator and independent review are incomplete. | Treat the campaign as one episode with nested subepisodes, not ten independent successes. |
| **C3 — End-to-end formalization**: A custom scaffold, semantic choices, manuscript production, and a public Lean support path for Erdős #330. | Kernel acceptance applies to the encoded theorem; complete chat provenance and source-to-target equivalence remain separate. | Formalization begins with semantic binding, not with the first Lean token. |
| **C4 — Public downgrade**: A two-part Erdős claim was corrected after expert review: one subproblem remained open. | The correction narrows the compound claim rather than erasing the supported subresult. | A mature system must permit partial results and dependency-scoped downgrades. |
| **C6 — Target reconstruction**: Humans and models reconstructed a meaningful target for an ambiguous Erdős problem, then formalized and humanized it. | Autonomy and novelty are mixed because steering, exposition, and related prior work materially affect the contribution. | Goal reconstruction is a contribution only when the semantic delta is explicit. |
| **C9 — Finite certificate asymmetry**: A concrete graph counterexample was reported after weeks of prior human work and one GPT-5.6 Pro conversation. | The finite certificate form is favorable, but the complete chat, public exact-checking program, and mature paper were not fully captured. | Prompt simplicity matters less than the cost and inspectability of the certificate. |

**Table 2b. Compact notes for episodes C10 to C15.**

| Episode and workflow signal | Current evidence boundary | Key process inference |
|---|---|---|
| **C10 — Minimal-prompt target discovery**: A one-sentence instruction reportedly delegated target selection, search, and exposition for two combinatorial problems. | The linked reports and full thread were incompletely captured; the episode remains a process hypothesis rather than mature theorem-level evidence. | Minimal prompting does not establish that mathematical expertise or later verification is unnecessary. |
| **C11 — Controller-mediated batch research**: Devin reportedly coordinated problem discovery, parallel agents, Lean translation, and adversarial checking. | The frozen corpus lacks a commit-pinned repository, theorem-to-build map, and clean independent rebuild. | A sophisticated pipeline does not automatically produce auditable evidence. |
| **C13 — Representation escape and expert maturation**: GPT-5.4 Pro introduced a von-Mangoldt-weight route for Erdős #1196 that departed from decades of standard probabilistic openings. | A multi-author paper, curator state, and formalization support the theorem, but the original full session and transformation chronology remain incomplete. | Models may add value by escaping inherited representation conventions; experts remain essential for interpretation, generalization, and durable exposition. |
| **C14 — Formalization at extreme scale**: Turturean reported a 180,000-line Lean project driven by Codex, Claude, ChatGPT Pro, and a custom compiler loop. | The public process description is unusually detailed, but this audit has not yet pinned the exact repository, commit, dependencies, or clean rebuild. | At research scale, autoformalization becomes a software-engineering and state-management problem, not merely theorem proving. |
| **C15 — Internal generation and human digestion**: An internal OpenAI model produced three short proofs later published by five human mathematicians; public GPT-5.4 Pro recreated two targets imperfectly. | The paper is inspectable and explicit about human roles, but the internal model trace and complete attempt denominator are unavailable. | Publication-quality mathematical knowledge may require substantial human digestion even when the core proof is attributed entirely to a model. |

## C5. The formalizer as co-author: when Aristotle rewrites the proof

The Erdős #650 collaboration involved human mathematicians, GPT-5.4 Pro,
Aristotle, and Lean. GPT-5.4 Pro supplied an informal argument, but the
human team found that a claimed injection was false. The defect was not a
missing line of routine algebra; it broke the stated support path.

Aristotle's contribution was therefore more than transcription. In the
course of formalization, the system produced a different injection that
avoided the failed step. The mathematicians then read the Lean term,
reconstructed the new argument, and wrote a natural-language proof
(Monticone 2026; Doorn, Li, and Tang 2026; Doorn and collaborators 2026).
The kernel accepted the encoded theorem, while the original prose route
was rejected and replaced.

This distinction matters for both evidence and credit. A formal artifact
can support the theorem without validating the submitted informal proof.
When the formalizer changes a load-bearing argument, the repair belongs in
the proof lineage and the formalizer is a research contributor, not merely
a final checker.

### State-transition reconstruction

The publicly visible sequence is conservative:

```text
informal candidate
→ formalization exposes a defective step
→ Aristotle proposes a different injection
→ the replacement is accepted in the Lean development
→ the human paper presents the repaired support path
```

The compiler or formalizer error is an observation; the new injection is a
transition proposal; kernel acceptance changes Artifact and Claim State for
the encoded theorem. Whether the resulting human exposition is a transcription,
a reformulation, or an independently reviewed proof remains a separate
maturation question.

## C7. Adversarial self-repair and exact-checker risk: fixed-perimeter Conjecture 1.2

Adam Holter first asked GPT-5.6 Pro to select and solve an open conjecture
from Gray et al. (2025), then instructed it to try to kill its own proof.
The second pass found a boundary defect in the initial argument. The model
discarded the faulty step, rewrote the approximation, and produced a
Python program that checked millions of finite instances.

The repair strengthened the candidate, but it also showed that the first
"complete proof" was not complete. A useful record therefore includes the
defect, the range in which it appears, the rejected artifact, and the
replacement argument. Keeping only the final draft would erase the most
informative transition in the episode.

The executable checker introduced a separate problem. Its proof-critical
tests used Python `assert` statements, which disappear under
`python -O`; the program could then reach a success message without
executing those checks. The public record supports discovery of this
failure mode and motivates a fail-closed refactor, an executed-check
manifest, environment capture, and negative mutations. This paper does
not treat those hardening steps as completed unless the repaired checker
and its mutation logs are available. Millions of test cases add evidence
only when the harness itself can be made to fail.

## C8. Route replacement, not local patch: the unit-distance episode

The unit-distance episode has the broadest public maturation path in the
corpus. An internal OpenAI model produced a disproof of the
$n^{1+o(1)}$ conjectural upper bound. OpenAI released the proof and a
125-page rewritten research trace. Nine mathematicians later produced a
shorter human proof, and Sawin obtained an explicit exponent exceeding
1.014.

These artifacts support different claims. The later papers give the
theorem strong external mathematical support. The 125-page document is a
rewritten trajectory summary, not a raw chronological command log, so its
detail should not be confused with completeness. Its value lies in the
sequence of failed routes, tests, and changes of representation that it
preserves.

**Reconstructed route timeline:**

```text
incidence / Fourier / additive-combinatorial routes
    → number-field and relative-unit constructions
    → almost-totally-real route rejected (height and lattice-shape costs)
    → CM sign-ideal and cut-and-project kernel retained
    → cyclic-cubic pro-3 tower replaces the upstream existence mechanism
    → human re-derivation, compression, and explicit strengthening
```

The decisive change was a route replacement rather than a local repair.
The upstream arithmetic mechanism was abandoned while a downstream
geometric kernel was retained and rechecked. The failed routes had
lasting value because they identified the height, denominator, and
lattice-shape costs that any successor had to pay. The episode therefore
supports treating negative results and route history as research assets,
without treating the rewritten trace as a complete record of private
deliberation.

### State-transition reconstruction

C8 exposes a partial order rather than a complete raw event stream:

```text
candidate routes and cost estimates
→ productive vetoes and route obstructions
→ upstream mechanism replacement
→ retained downstream combinatorial kernel
→ final model construction
→ human digestion, independent re-derivation, and strengthening
```

The 125-page document supports a derived transition narrative, not a complete
chronological ledger. Version 0.14 therefore marks route ordering and retained
kernels as visible while leaving the original acceptance events, exact branch
denominator, and some timestamps unestablished.

## C12. Auditable candidate trail with bounded review: Patrick White, GPT-5.6 Sol, and Claude on Erdős #477

**This episode is included as an example of process transparency, not as
an established mathematical breakthrough.**

The `pw/erdos477-cubic` repository claims an affirmative answer to Erdős
Problem #477. GPT-5.6 Sol supplied the core construction. Separate runs
from the same model family produced case splits and adversarial passes,
while Claude checked source statements, elementary algebra, and selected
exponents.

The audit record contains real corrections. One pass repaired a citation
mismatch; another found an incorrect genus-drop formula for even $K$.
The repository argues that this error is not load-bearing because the
main route uses absolute irreducibility rather than the genus calculation.
That impact analysis is useful even though it does not amount to a full
proof review.

The evidence ceiling remains limited. The complete model sessions are not
public, the main audits share model ancestry, Claude's checks cover only
parts of the proof, and no Lean proof or complete review by a number
theorist was available at the snapshot date. A related source-binding
issue also remains: the natural-language problem ranges over integers,
whereas a cited formal target restricts inputs to positive integers and
contains placeholders. C12 is therefore coded as an auditable candidate
trail, not as a verified resolution.

## C16. Bridge results and cross-model handoffs: Kemeny hardness for three voters

Dominik Peters's preprint gives an NP-hardness reduction for Kemeny rank
aggregation with three input rankings, a question open since Dwork et al.
posed it in 2001. The final reduction is from a restricted form of SIMPLE
MAX CUT. The process account is unusually specific about how the result
emerged (Peters 2026a, 2026b).

Peters had previously asked models to attack the five-voter case and
concluded that repeatedly trying to induce the existing Conitzer
reduction was unproductive. He placed that negative instruction in a new
prompt together with the relevant papers. GPT-5.6 Sol Ultra then worked
for about six hours and forty-five minutes and produced a complicated
five-voter reduction. Subsequent simplification passes used both GPT-5.6
and Claude Fable 5. Claude did not solve the three-voter case, but left
notes and scripts. Peters supplied the five-voter construction and those
failed-attempt artifacts to a new GPT-5.6 Sol Ultra run, which reported a
three-voter reduction after roughly four hours.

```text
repeated attempts at an old reduction
    → dead-end warning recorded in the prompt
    → complex five-voter bridge result
    → cross-model simplification attempts
    → Claude notes and scripts retained despite failure
    → stronger three-voter reduction
    → human simplification and exposition
    → Kemeny-specific Lean proof and general hardness-reduction library
```

The five-voter result was superseded in the final theorem, but it was not
research waste: it carried structure into the successful run. Likewise,
Claude's unsuccessful attempt became a handoff artifact rather than a
discarded transcript. Peters's own contribution was concentrated in
simplification, including the long-even-edge restriction, and in writing
the paper; he explicitly notes that current models did not explain the
complex reduction well enough for publication.

The arXiv paper and two public Lean repositories make the mathematical
artifacts inspectable. The Kemeny repository presents a Lean formalization
of the reduction, while the broader library separates combinatorial
correctness from a certificate language for polynomial-cost maps and
states the remaining machine-model bridge explicitly. This audit had not
completed a clean, commit-pinned rebuild or obtained independent peer
review by the snapshot date. C16 is therefore coded O4, E3 provisional,
and L2. Its main methodological contribution is the visibility of bridge
results, cross-model failure handoffs, and proof simplification as
separate stages of discovery.

### State-transition reconstruction

The episode is the clearest public approximation to an evidence-backed
handoff:

```text
known dead-end constraint
→ complex five-voter bridge reduction
→ simplification attempts
→ failed three-voter notes and scripts
→ cross-model transfer
→ three-voter reduction
→ human conceptual simplification and exposition
→ formalization and reusable reduction infrastructure
```

The bridge result is later superseded but remains epistemically active. The
handoff is stronger than a free-form summary because the receiving run obtained
notes and scripts, although the complete session packet, exact acceptance
criteria, and raw transition log remain unavailable.

## C17. A campaign release stack: Astra, derived process narratives, and Comparator-bound Lean certificates

OpenAI's 1 August release is not one additional theorem and should not be
counted as ten independent workflow episodes. It is one internal research
campaign presented as ten public result families. The release hierarchy is
more precise than the earlier phrase “twelve formal targets” suggested.

| Analytical layer | Count | Meaning |
|---|---:|---|
| Workflow episode | **1** | One Astra campaign and release process |
| Public result families | **10** | The ten headings used by the announcement and manuscript |
| `formalization.yaml` main results | **12** | Twelve declared main-result records, each mapped to a Comparator configuration |
| Comparator configuration bundles | **12** | Separate challenge/solution bindings for sphere packing; binary codes; spherical codes; permanent formulas; non-sofic groups; Connes rigidity; Ehrhart; quantum repetition; GapCVP; Ramsey; compactness; and two-degenerate graphs |
| Named theorem declarations in the twelve configurations | **38** | The exact Lean theorem names requested by Comparator |
| Explicitly bound definition names | **4** | Four GapCVP promise definitions checked in addition to theorem names |

The counts are nested, not additive evidence units. Binary and spherical
codes share a result family but use separate configurations; compactness and
two-degenerate graphs share the tenth public heading but also use separate
configurations. Conversely, one configuration can bind several theorem
declarations around one main result.

OpenAI attributes the mathematical arguments to an internal version of Astra.
It reports that the discovery tokens would cost roughly USD 2,000 at Sol API
rates, that humans prepared the manuscripts with the same model, and that the
model subsequently formalized every argument in Lean. The public attribution
statement is unusually explicit: human participants accept responsibility for
correctness and release while declining to claim authorship of arguments
generated by the system, a separation the announcement connects to the Leiden
Declaration on AI and Mathematics (OpenAI 2026d; Leiden Declaration 2026).

The public package has several evidential layers:

```text
private original trajectories
    → 62-page model-written retrospective walkthrough
    → 249-page mathematical manuscript
    → Lean solution modules
    → twelve trusted challenge/configuration bundles
    → Comparator same-statement, axiom-ceiling, and kernel checks
    → nanoda replay configured in every bundle
    → mutable public repository snapshot
```

### Trace provenance and retrospective reconstruction

The walkthrough says that an AI model read the original chains of thought
together with the resulting papers and writeups and reconstructed the ideas,
obstacles, changes of perspective, and decisive steps. It is therefore richer
than a final-only paper but weaker than a raw event stream. Its table of
contents and chapter narratives preserve several substantial failures:
the incorrect first binary recurrence, loss of control in a Newton-volume
route, an impossible quantum reduction, a long signed-histogram detour, a
useful but incomplete harmonic-symmetrization route, and stalled natural
reductions in extremal graph theory (OpenAI 2026f).

This is meaningful negative-knowledge evidence. It is also outcome-conditioned
evidence. The narrator had access to both private trajectories and final
papers, so the public story may compress uncertainty, branch competition,
luck, and abandoned work into a cleaner progression. Version 0.14 therefore
retains **retrospective-narrative laundering** as a recurrent risk visible in
C8 and C17. The walkthrough is coded
`MODEL_RECONSTRUCTION_FROM_PRIVATE_TRACE`, not as a public raw trace or a
complete attempt denominator.

### Formal release and trusted-challenge boundary

The repository uses Lean 4.32.0, mathlib, and Lake and exposes a top-level
`All` build. Its current `formalization.yaml` is version `v0.3`. It reports
zero `sorry`s in the solution formalizations and zero in solution definitions;
permits only `propext`, `Classical.choice`, and `Quot.sound`; records twelve
main-result entries; cites two Sphere-Packing-Lean repositories as prior work;
describes the automation as Astra orchestrated through Codex with about one
week of wall-clock formalization time; and labels review status
`agent-reviewed` (OpenAI 2026g, 2026h).

The zero-`sorry` metadata must not be misread as saying that trusted challenge
files contain no placeholders. Comparator challenge modules intentionally state
the trusted theorems with `sorry` proofs; the solution modules supply the
candidate proofs. Comparator then checks statement equality, the permitted
axiom ceiling, and kernel acceptance relative to the trusted challenge.
This challenge/solution distinction is part of the protocol, not a
contradiction in the metadata (Lean FRO 2026).

All twelve current configuration files set `enable_nanoda` to `true`. This
means a second-kernel replay is configured. Version 0.14 did not execute and
archive all twelve Comparator/nanoda runs, so it does not describe nanoda
checking as independently completed.

The configuration-level coverage is:

| Bundle | Named theorems | Bound definitions | nanoda configured |
|---|---:|---:|:---:|
| A Sphere packing | 4 | 0 | Yes |
| B Binary codes | 6 | 0 | Yes |
| B Spherical codes | 4 | 0 | Yes |
| C Permanent formula lower bounds | 2 | 0 | Yes |
| D Non-sofic group | 1 | 0 | Yes |
| E Connes rigidity | 2 | 0 | Yes |
| F Ehrhart volume inequality | 4 | 0 | Yes |
| G Quantum parallel repetition | 2 | 0 | Yes |
| H GapCVP | 4 | 4 | Yes |
| I Multicolor Ramsey | 4 | 0 | Yes |
| J Compactness conjecture | 3 | 0 | Yes |
| J Two-degenerate graphs | 2 | 0 | Yes |
| **Total** | **38** | **4** | **12/12** |

This finer audit identifies a concrete coverage boundary. The public headline
for arithmetic circuit complexity includes lower bounds for both circuits and
formulas. `Permanent.lean` contains the circuit theorem
`PermanentRollout.permanent_circuit_loglog_lower_bound` and related
superquadratic results. However, the published permanent Comparator
configuration names only the two formula lower-bound theorems. Thus the circuit
subclaim may be present in the Lean solution repository and top-level build
without belonging to the named Comparator same-statement target set. Repository
coverage, kernel-build coverage, `formalization.yaml` main-result coverage, and
Comparator coverage are not interchangeable.

The audit did not construct a complete headline-to-configuration matrix for
every subclaim in the 249-page manuscript. Natural-language-to-trusted-challenge
binding and configuration coverage therefore remain claim-specific open
obligations even when every named Lean declaration is accepted.

### Repository snapshot succession

The repository is publicly inspectable but its branch history is not a stable
development trace. The first C17 audit pinned zero-parent root commit
`29362184c2b698c1b279bc85b3957ee813646c63`, whose GitHub diff statistic
reported 43 files and 477,114 additions. On 3 August, `main` instead pointed
to distinct zero-parent root commit
`94bc0feb6a9ff12c7d31d6de640a725c9d43d2b6`, with 43 files and 550,770
additions, while GitHub showed one commit on the branch. The reason for the
pointer change is not established by the public record.

The addition counts are GitHub commit statistics across the whole repository,
not pure Lean lines of code. Version 0.14 records both hashes and treats the
later root as the current public snapshot and the former as a superseded audit
snapshot. This is an Artifact State transition. No mathematical correction,
Claim State downgrade, or theorem change is inferred merely from the changed
root and line statistic.

### Inter-result dependency and process lessons

The public headings are not ten independent mathematical mechanisms. Binary
and spherical codes share a moving-subspace construction, the spherical
certificates recover the sphere-packing exponent, and the permanent circuit
and formula results concern distinct computational models around one target
polynomial. The campaign therefore needs an inter-result dependency graph in
addition to a headline count.

The reconstructed processes expose several reusable failure and repair
patterns. A small \(n=8,\ k=1\) counterexample invalidated an attractive
binary recurrence before asymptotic development. The coding-theory work
distinguishes improving one classical bound from beating the fully optimized
benchmark. Other chapters preserve long failed routes that changed the
representation or the question. The Ehrhart walkthrough separates the proved
volume inequality from an equality-classification direction that remains
unproved. The sphere-packing work pairs a constructive witness with a positive
dual obstruction. These observations support micro-falsification, benchmark
completeness, scoped nonclaims, primal/dual certificate planning, and route
replacement as first-class research objects.

### Evidence classification and remaining gaps

The public evidence remains correlated. Astra generated the arguments; the
same model family assisted manuscript preparation; the system performed the
formalization; and a model reconstruction narrates the private process.
Different artifact types therefore provide complementary triangulation but
not independent review by count. The release is `agent-reviewed`, and mature
external full-proof review was not established at the snapshot date.

C17 remains coded **O4, E3 provisional, and L2**. The E3 ceiling reflects not
only the absence of mature external mathematical review and an independently
archived clean rebuild, but also the absence of a complete public Comparator
execution log, a full headline-to-config coverage audit, and independent
natural-language-to-trusted-challenge adjudication. The release nevertheless
provides the strongest same-day formal-artifact stack in the corpus.

The announcement presents a selected set of ten results and reports the
discovery-token equivalent, but it does not disclose the upstream candidate
pool, failed attempts, duplicate policy, or complete denominator. The
missing-attempt-denominator failure mode therefore remains applicable without
assuming an unsupported selection rule.

### State-transition reconstruction

C17 is best described as artifact-rich and transition-incomplete:

```text
private internal campaign
→ model-derived retrospective walkthrough
→ 249-page result-family manuscript
→ solution formalization
→ trusted challenge/configuration packaging
→ current public root snapshot
```

The accepted state transitions inside the private campaign are not public.
The walkthrough is a derived narrative; the repository is a release artifact,
not an event ledger. The later root replacement is visible as an Artifact
State change, but the evidence does not show a corresponding Epistemic or Claim
State change. Version 0.14 therefore codes release transitions and trace
derivation while refusing to infer a complete discovery state machine.

# Cross-Case Synthesis

## Nine workflow components

The cases are better described by component vectors than by mutually
exclusive paradigms.

| Code | Component | Operational question |
|---|---|---|
| **P** | Problem portfolio management | How are targets screened for importance, tractability, ambiguity, prior art, and certificate cost? |
| **G** | Goal binding and specification | Are definitions, quantifiers, claim atoms, and forbidden shortcuts explicit? |
| **T** | Search topology | Is search sequential, parallel, batch, or controller-mediated? |
| **M** | State and trajectory management | Are failed routes and obligations preserved (**M1**), is the acceptance basis for state changes visible (**M2**), and can the next actor recover scope, artifacts, open obligations, and continuation conditions (**M3**)? |
| **F** | Falsification topology | Who or what tries to refute the candidate, and how independent is that path? |
| **V** | Formal or executable verification | What exact theorem or finite domain is checked, in which environment? |
| **R** | Repair semantics | Was the proof transcribed, completed, locally repaired, replaced, or retargeted? |
| **H** | Human semantic and domain intervention | Where did humans select, steer, bind, interpret, or approve? |
| **E** | External maturation | Was there prior-art adjudication, independent re-derivation, correction, simplification, or strengthening? |

## Four operational configurations

Operational scale is orthogonal to evidence maturity.

| Level | Configuration | Distinguishing feature | Illustrative cases |
|---|---|---|---|
| **O1 — Minimal/direct** | One prompt or one visible session | Target discovery or a proof/certificate inside one interaction | C9, C10, C13 |
| **O2 — Self-adversarial** | Generate, then explicitly attack the candidate | Local objective switches from completion to defect discovery | C2, C7, C12 |
| **O3 — Scaffolded extended** | Contracted target, persistent state, multiple routes, long run, or internal research campaign | Search management, maturation, or route memory become explicit | C1, C4, C6, C8, C15 |
| **O4 — Orchestrated formal** | Controller or specialist pipeline with formalization/checking | Artifacts move through generation, critique, handoff, formalization, and release stages | C3, C5, C11, C14, C16, C17 |

## Two-axis map: operational complexity versus public evidence

![Figure 1. Operational configuration (O1–O4) versus strongest visible
public evidence tier (E0–E5).](operational_evidence_map_v0.14.png)

**Figure 1. Operational configuration versus strongest visible public evidence tier.** Higher workflow complexity does not automatically yield stronger mathematical evidence. For instance, the O4 Devin campaign (C11) remains at the E2–E3 levels due to unpinned repositories, whereas the O3 unit-distance trace (C8) has matured to E5 through external human digestion. C17 is likewise coded O4 but E3 provisional: despite an integrated artifact stack, the verification chain remains within a single institution and model family, and external full mathematical review and an independent clean rebuild have not yet occurred—again demonstrating that the two axes are orthogonal.

A text-accessible rendering of the same coordinates is:

| Operational configuration | Episodes and public-access ranges |
|---|---|
| **O1** | C9: E2–E3; C10: E1–E2; C13: E5 |
| **O2** | C2: E2–E3; C7: E3; C12: E2 |
| **O3** | C1: E3–E4; C4: E3–E4; C6: E4; C8: E5; C15: E4 |
| **O4** | C3: E3–E4; C5: E4; C11: E2–E3 reported; C14: E3–E4 reported; C16: E3 provisional; C17: E3 provisional |

The plotted coordinates are also present in the JSON ledger, so the
figure is not the sole carrier of the data.

## Descriptive statistics of the coded corpus

The following counts describe the seventeen selected episodes under the
Version 0.14 codebook. They are not estimates of unseen AI-mathematics
workflows.

| Workflow component | Clear `[Y]` | Partial/reported `[P]` | Not established `[-]` |
|---|---:|---:|---:|
| Problem portfolio management (**P**) | 6 | 4 | 7 |
| Goal binding and specification (**G**) | 12 | 5 | 0 |
| Search topology (**T**) | 6 | 7 | 4 |
| State and trajectory management (**M**) | 8 | 9 | 0 |
| Falsification topology (**F**) | 11 | 6 | 0 |
| Formal or executable verification (**V**) | 9 | 8 | 0 |
| Repair semantics (**R**) | 13 | 4 | 0 |
| Human semantic/domain intervention (**H**) | 16 | 1 | 0 |
| External maturation (**E**) | 6 | 8 | 3 |

The M count retains the previous coding boundary and primarily reflects
trajectory visibility. It must not be read as evidence that transition
acceptance or continuation control was present in all seventeen episodes.
Version 0.14 reports M1–M3 only for selected deep dives and treats missing
control-plane evidence as unknown.

Human intervention and some form of falsification are the most visible
components in this deliberately process-rich corpus. Portfolio selection
and external maturation are less uniformly documented. These frequencies
partly reflect the inclusion rule and should not be read as prevalence in
the underlying population.

**Illustrative summary only; the small cells and ordinal evidence tiers preclude inference.**

| Configuration | $n$ | Visible evidence range |
|---|---:|---|
| O1 | 3 | E1–E5 |
| O2 | 3 | E2–E3 |
| O3 | 5 | E3–E5 |
| O4 | 6 | E2–E4 |

The ranges do not support a monotonic complexity–maturity claim. C11 is an
O4 workflow with only E2–E3 reported evidence, whereas C8 reaches E5 at
O3. The table is included to show dispersion, not to summarize an ordinal
scale with pseudo-precision.

Visible human labor is coded as L0: 1 episode, L1: 4, L2: 10, and L?: 2.
The mature C5, C6, C8, C13, and C15 support paths all contain L2 visible
human work, but C9 is also L2 with only E2–E3 evidence. Because labor is a visible
lower bound and the sample is selected, this pattern is descriptive, not
causal.

## Workflow fingerprints

**Table 3. Visible workflow components.** `[Y]` = clearly present in
the accessible evidence; `[P]` = partial or author-reported; `[-]` = not
established. Plain-text codes are used for reliable Pandoc/LaTeX
rendering. The table is not a quality score.

| Case | P | G | T | M | F | V | R | H | E |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| C1 Wang | [Y] | [Y] | [Y] | [Y] | [Y] | [P] | [Y] | [Y] | [P] |
| C2 Holter campaign | [Y] | [P] | [Y] | [P] | [Y] | [P] | [Y] | [Y] | [-] |
| C3 #330 | [-] | [Y] | [P] | [Y] | [Y] | [Y] | [P] | [Y] | [P] |
| C4 #635 | [-] | [P] | [-] | [P] | [Y] | [Y] | [Y] | [Y] | [Y] |
| C5 #650 | [-] | [Y] | [P] | [P] | [Y] | [Y] | [Y] | [Y] | [Y] |
| C6 #728 | [-] | [Y] | [P] | [P] | [Y] | [Y] | [Y] | [Y] | [Y] |
| C7 fixed perimeter | [Y] | [P] | [-] | [Y] | [Y] | [Y] | [Y] | [P] | [-] |
| C8 unit distance | [P] | [Y] | [P] | [Y] | [Y] | [P] | [Y] | [Y] | [Y] |
| C9 Rybin | [-] | [P] | [-] | [P] | [P] | [P] | [P] | [Y] | [P] |
| C10 Chakravarthy | [Y] | [P] | [P] | [P] | [P] | [P] | [P] | [Y] | [P] |
| C11 Devin | [Y] | [Y] | [Y] | [Y] | [Y] | [P] | [P] | [Y] | [P] |
| C12 #477 | [-] | [Y] | [P] | [Y] | [Y] | [P] | [Y] | [Y] | [-] |
| C13 #1196 | [P] | [Y] | [-] | [P] | [P] | [Y] | [Y] | [Y] | [Y] |
| C14 #870 | [-] | [Y] | [Y] | [Y] | [Y] | [Y] | [Y] | [Y] | [P] |
| C15 OpenAI short proofs | [Y] | [Y] | [P] | [P] | [P] | [P] | [Y] | [Y] | [Y] |
| C16 Kemeny three voters | [P] | [Y] | [Y] | [Y] | [P] | [Y] | [Y] | [Y] | [P] |
| C17 OpenAI ten advances | [P] | [Y] | [Y] | [P] | [P] | [Y] | [Y] | [Y] | [P] |

## Common lifecycle

```text
Select and screen target
    → Bind source, definitions, quantifiers, and claim atoms
    → Generate non-equivalent routes and, where useful, bridge targets
    → Preserve state, obligations, failed notes, scripts, and duplicate fingerprints
    → Observe a tool, model, source, repository, or human intervention
    → Propose and accept a scoped operational/epistemic/claim/artifact delta
    → Hand off scope, artifacts, rejected routes, and open obligations
    → Decide whether the next bounded turn should run, wait, redirect, or stop
    → Falsify with counterexamples, destructive critique, or exact tests
    → Repair locally, simplify, or replace an upstream route
    → Formalize or check the exact claimed domain
    → Seek independent review and prior-art adjudication
    → Publish, correct, simplify, strengthen, resnapshot, or reopen
```

Formalization, source checking, or expert review may reopen goal binding
and proof search rather than merely approving the current artifact.

## Paired comparisons

Several pairs look similar at first glance but differ sharply in what their evidence supports.

| Pair | Shared surface | Decisive difference | Process inference |
|---|---|---|---|
| **C3 #330 vs C5 #650** | Both end in Lean-backed support paths | C3 foregrounds semantic choices and end-to-end formalization; in C5 Aristotle replaces a defective informal step with a different injection | “Formalized” must be decomposed into target binding and proof relation: transcription, completion, repair, or replacement |
| **C9 Rybin vs C10 Chakravarthy** | Both are O1/minimal public stories | C9 exposes a concrete finite graph plus substantial prior human engagement; C10 exposes an extreme minimal prompt but incompletely captured reports | Prompt minimality does not determine evidence maturity; certificate form and artifact capture do |
| **C4 #635 vs C8 unit distance** | Both undergo post-release scrutiny | C4 matures by narrowing a compound claim; C8 matures through route replacement, independent human re-derivation, and strengthening | Maturation can downgrade, preserve, or strengthen different claim atoms rather than simply “confirm” a headline |
| **C2 Holter campaign vs C11 Devin** | Both operate across multiple targets | C2 has public task-level sessions but correlated same-model audits; C11 reports controller-mediated Lean pipelines but lacks a pinned target-to-build reconstruction | Batch throughput and orchestration complexity solve different problems and neither substitutes for evidence completeness |
| **C3 #330 vs C14 #870** | Both are Turturean-led Lean formalization episodes | #330 used a comparatively bounded handoff to Codex/Lean; #870 reportedly required a custom multi-model compiler loop, roughly 180,000 Lean lines, and orders of magnitude more tokens | Formalization difficulty is an engineering-scale variable: durable state, dependency management, and repair orchestration can dominate proof search |
| **C13 #1196 vs C15 OpenAI short proofs** | Both attribute core mathematical ideas to OpenAI models and later rely on expert human papers | C13 exposes a new representation choice that experts generalized across a theory; C15 exposes three concise proofs but with an unavailable internal trace and only partial public recreation | Human digestion may serve different roles—extracting a new research programme versus converting terse model proofs into publishable mathematics |
| **C8 unit distance vs C16 Kemeny** | Both preserve failed routes and later produce formal or human-readable artifacts | C8 replaces an upstream mechanism inside a long research trajectory; C16 uses a superseded five-voter result and another model's failed notes as inputs to a stronger three-voter result | A failed route and a superseded intermediate theorem can be causal assets when their scope and handoff are recorded |
| **C8 unit distance vs C17 ten advances** | Both originate in internal OpenAI research and release process narratives | C8 has one rewritten long trace followed by external human re-derivation and strengthening; C17 has a broad model-written reconstruction plus twelve configuration bundles and thirty-eight named theorem declarations but no external maturation yet | Process visibility, formal-certificate depth, and independent maturation are distinct evidence coordinates |
| **C15 short proofs vs C17 ten advances** | Both attribute core arguments to internal OpenAI models and involve human manuscript preparation | C15 exposes concise human digestion and partial public-model recreation; C17 adds derived process narratives, trusted challenge modules, Comparator, and a large pinned formal repository | A richer release bundle improves auditability but same-lineage artifacts still require correlation accounting |

## Question agendas as an uncoded precursor to route search

The nine-component matrix starts once a target and at least one route are
visible. It does not separately code how a research system decided which
questions to ask before those routes appeared. The public episodes rarely
expose that stage with enough detail for reliable retrospective coding.
STORM and Co-STORM show that it can be made explicit through perspective-
guided question asking, retrieval-grounded follow-up, a human-steerable
discourse, and a dynamic concept map (Shao et al. 2024; Jiang et al. 2024).

This paper therefore does **not** add a tenth workflow component or revise
the seventeen-case statistics. Instead, it identifies the question agenda as
an external design hypothesis for future experiments. A question should
receive process credit only when it changes a route, surfaces a previously
unarticulated constraint, produces a discriminating test, identifies a
source or counterexample, or is retained as an explicit unresolved
obligation. Raw question volume, persona count, discourse length, or
mind-map density are not measures of mathematical progress. Synthetic
perspectives may broaden search but do not constitute independent review.

# Mechanism Signals and Testable Hypotheses

The workflow-component matrix records broad process features. Table 4 asks a narrower question and summarizes **mechanism–outcome contingencies**. The outcome is a clearly reported material defect, falsification, correction, or route elimination. `[P]` outcomes remain partial rather than being converted to successes. Because the corpus is selected and single-coded, the table is descriptive and cannot support causal or population-level inference.

**Table 4. Mechanism–outcome contingencies in the seventeen selected episodes.**

Each cell reports outcome counts as `[Y]/[P]/[-]`: clearly reported
material change, partial or ambiguous change, and no established change.

| Proposed mechanism | Clearly present | Partial presence | Not established |
|---|:---:|:---:|:---:|
| **Certificate asymmetry** | 3/0/0 | 2/1/1 | 5/3/1 |
| **Destructive critique** | 5/0/0 | 5/3/2 | 0/1/0 |
| **Proof-assistant or exact-checker feedback** | 3/0/0 | 2/3/1 | 5/1/1 |
| **Compute headroom plus persistent state** | 4/2/0 | 5/1/2 | 1/1/0 |

The clearest descriptive pattern concerns destructive critique: every episode
coded `[Y]` on that mechanism also disclosed a material change. The sample was
selected partly for process visibility, however, so the table cannot estimate a
counterfactual effect or a population rate. Formal feedback and compact
certificates improve auditability in several episodes, but material corrections
also arise through ordinary source checking and expert review.

The detailed per-case mechanism matrix is retained in Appendix G. Accordingly, the mechanisms remain hypotheses. The proposed experiments indicate how they could be tested without treating the present case series as causal evidence.

| Mechanism | Equal-budget controlled test | Primary outcomes |
|---|---|---|
| **Certificate asymmetry** | Hold model and budget fixed; randomize whether the workflow estimates verification cost before target selection | Independently checkable-result rate, human review time, false-complete rate, certificate size |
| **Destructive critique** | Compare generic polish, same-model destructive critique, and different-lineage critique on the same candidate proofs | Fatal-gap recall, valid-repair rate, residual false-complete rate, correlation-adjusted review value |
| **Proof-assistant or exact-checker feedback** | Compare prose-only review, exact-checker feedback, and proof-assistant/formalizer feedback with frozen source targets | Gap detection, repair success, target fidelity, repaired-versus-replaced argument rate, exact-checker false-pass rate |
| **Compute headroom plus persistent state** | Equalize total tokens and tool time; compare stateless retries with structured trajectory memory and reserved checking capacity | Verified yield, duplicate-route rate, reopened obligations, verification debt, useful negative knowledge |

Certificate asymmetry is a property of task and evidence structure, not an unsupported theory of language-model internals. Destructive critique separates cheap internal filtering from independent review. Formal or checker feedback requires logging a delta when the accepted support path changes. The compute-plus-state hypothesis predicts that elapsed time alone is insufficient: additional generation without trajectory memory and checking capacity increases backlog rather than knowledge.

## External design hypothesis: perspective-guided question agendas

STORM's evidence does not support adding a fifth corpus-derived mechanism,
because it was evaluated on knowledge curation rather than open mathematics.
It does support a controlled experiment that the present case series cannot
run retrospectively:

| Experimental factor | Equal-budget comparison | Primary outcomes | Failure controls |
|---|---|---|---|
| **Question-elicitation scaffold** | Direct proof prompt vs generic decomposition vs perspective-guided, retrieval-grounded question agenda with optional human steering | Non-equivalent route yield, goal-relevant question depth, useful bridge results, source coverage, fatal-gap discovery, human review time | Source-bias transfer, over-association, synthetic-perspective correlation, outline lock-in, question-volume gaming |

The agenda should be frozen only provisionally and reopened when a
contradiction, new source, failed route, or human intervention changes the
problem representation. The experiment should retain question lineage and
measure downstream state changes rather than reward articulate but unused
questions.

## External design hypothesis: accepted transitions and continuation control

LoopX motivates a second external hypothesis. In equal-budget research
workflows, separating observation, transition proposal, validation, accepted
writeback, and continuation admission may reduce repeated routes, state drift,
handoff loss, and false completion. The hypothesis is not evaluated by the
current observational corpus.

A controlled study should compare:

| Condition | State supplied to the next turn |
|---|---|
| **A Stateless** | Original problem only |
| **B Transcript memory** | Full or compacted prior conversation |
| **C Structured trajectory** | Routes, failures, artifacts, and obligations |
| **D Dynamic control plane** | C plus bounded todos, gates, ownership, accepted writeback, and a typed continuation decision |

Hold model, total tokens, wall-time accounting, tools, verifier access, problem
set, and human-review allowance fixed. Measure duplicate-route rate,
goal-binding accuracy, stale-state conflicts, accepted handoff recovery,
verified epistemic advance per token, false-complete rate, human attention
minutes, and control-plane overhead. A lower turn count is not itself a better
result: the system must preserve exploratory diversity and outcome neutrality.

The principal risks are over-structuring, premature no-action decisions, gate
fatigue, hidden scheduler capture, and a misleading projection that diverges
from canonical evidence.

# Failure Modes and Controls

**Table 5. Recurrent failure modes, observations, and controls.**

| Failure mode | Observed manifestation | Control | Where visible |
|---|---|---|---|
| **Forced resolution** | “Full solution only” wording pressures partial evidence toward closure | Separate aggressive search persistence from outcome-neutral claim disposition | C1, C4, C7, C10 |
| **Target or scope drift** | One subproblem, variant, or positive-only formalization is mistaken for the source claim | Independent source reconstruction; claim atoms; formal-to-natural round trip | C3, C4, C6, C12 |
| **Correlated self-audit** | Same model family generates and attacks a proof, sharing the same citations and blind spots; the verification chain stays within a single institution | Different-lineage critic, deterministic evidence, blinded expert review | C2, C7, C12, C17 |
| **Formalization laundering** | Kernel acceptance is described as verification of the original prose or source problem | Exact theorem binding, axiom audit, formalizer delta, granular attribution | C3, C5, C6, C11, C14, C17 |
| **Exact-checker execution gap** | Assertions, timeouts, dead branches, or unconditional success messages prevent critical checks from running | Fail-closed logic, executed-check manifest, negative mutations, environment capture | C7 |
| **Missing attempt denominator** | Public successes omit abandoned, duplicated, or unpublished attempts | Preregistered target set, all-attempt ledger, fixed evidence threshold | C1, C2, C10, C11, C15, C16, C17 |
| **Prior-art drift or rediscovery** | A valid argument is later found to be known, related, or differently scoped | Time-stamped search dossier; separate theorem, proof, method, and operational novelty | C1, C2, C6, large Erdős scans |
| **Route and narrative amnesia** | Failed routes repeat; bridge results, failed notes, or replaced proofs disappear from the public account | Global claim registry, handoff artifacts, obligation reopening, repair lineage, narrative-compression audit | C2, C5, C8, C12, C13, C14, C16, C17 |
| **Retrospective narrative laundering** | A post-hoc narrative written by the same author or model after seeing the outcome smooths trial and error, jitter, and luck into a coherent heroic arc, or hides outcome leakage | Lock the chronology and provenance of final papers versus trajectories or narratives; independently record failed routes; cross-check narratives against raw event streams | C8, C17 |

The table remains restricted to failure modes observed or materially
coded in the seventeen-case corpus. STORM's expert evaluation identifies two
additional **external curation risks**—source-bias transfer and the
over-association of unrelated facts. Co-STORM also makes moderator and
turn-policy effects relevant. These are candidates for future AI4Math
experiments, not retrospectively asserted properties of the present cases.
A concept map or outline should therefore be treated as a navigational
artifact whose relations remain source-bound and revisable, not as a
validated theorem graph.

The fixed-perimeter case yields a concrete exact-checker lesson:

```python
assert proof_critical_condition()  # removed by Python under -O
print("success")                   # may still execute
```

```bash
python -O checker.py
```

A hardened checker replaces removable assertions with explicit
fail-closed branches, records the identifiers of checks that actually
executed, captures runtime flags and dependencies, and includes negative
mutations that must fail. A finite checker also declares the exact domain
it establishes; it cannot silently inherit an asymptotic claim.

C17 also motivates eight **single-campaign audit hazards** that are not
reclassified as recurrent cross-case failures until further cases exist:
result-family counting, cross-result independence, retrospective-coherence
from reconstructed traces, correlated artifact triangulation, trusted-
challenge statement laundering, discovery-cost compression, mutable-root
snapshot drift, and Comparator-coverage compression. Additional technical
subrisks include definition-hole gaming, conflating solution `sorry_count`
with challenge placeholders, mistaking a configured second kernel for an
executed independent replay, comparing against a weaker endpoint, and treating
a one-shot release root as a development trace.

## Future control-plane hazards

The following are design hypotheses for future coding, not additional recurrent
failure counts. LoopX is not a mathematical episode, and the present corpus
rarely exposes enough runtime state to estimate their prevalence.

| Hazard | Description | Minimum control |
|---|---|---|
| **State amnesia** | A failed route or decision exists only in chat and is repeated after compaction or handoff | protected trajectory and duplicate detection |
| **Unaccepted writeback** | A model summary or provider receipt changes durable state without validation | observation/proposal/acceptance separation |
| **Phantom progress** | More turns, files, or tokens are narrated as progress without a state or evidence delta | typed accepted delta and no-change accounting |
| **Handoff loss** | The next actor lacks scope, artifacts, failed routes, open obligations, or acceptance criteria | evidence-backed handoff receipt |
| **Gate bypass by side work** | Safe fallback work conceals that the primary route still needs human judgment | scoped gate and non-bypass projection |
| **Quota spend without epistemic delta** | Automatic compute continues after no useful transition remains | typed continuation decision and spend-after-writeback |
| **Projection drift** | Dashboard, paper narrative, or final report diverges from canonical event and artifact state | source-revision-bound read-only projection |
| **Stale-state race** | Concurrent agents overwrite each other's proof, route, or evidence updates | revision checks, idempotency, and scoped task leases |
| **Ownership laundering** | Responsibility for a todo is presented as mathematical verification or publication authority | ownership/authority separation |

These hazards should enter the main failure-mode taxonomy only after a larger
corpus or controlled experiment establishes recurrence and coding reliability.

# Cross-Case Findings

## Credibility accumulates through pipelines, not prompts

Minimal prompting can produce valuable finite certificates, but the
strongest public evidence states involve additional machinery—semantic
binding, exact verification, correction, human re-derivation, or external
strengthening—well beyond the prompt itself. C13 is particularly instructive: an initially compact O1 session
reached E5 only through expert interpretation, formalization, a multi-author
paper, and generalization beyond the original target.

## Human labor is redistributed, not removed

The lower-bound coding in Table 1 assigns one episode to `L0`, four to
`L1`, ten to `L2`, and leaves two as `L?`. These counts are not estimates
of total labor; they record only what the public evidence makes visible.
Even under that conservative rule, the most mature support paths are
usually associated with sustained human work in target selection,
semantic binding, formalization interpretation, source and prior-art
review, verifier design, public correction, independent re-derivation,
or release.

Domain-naive operators can trigger useful search, but “one prompt” does
not imply a labor-free research system. The emerging unit is a mixed
research organization in which some local derivation moves to models
while human labor concentrates around intent, evidence, integration, and
maturation.

## Question formulation may precede the visible search topology

Several episodes report routes and repairs but provide little evidence
about the questions that generated those routes. STORM and Co-STORM make
that hidden stage inspectable: perspectives seed questions, answers produce
follow-ups, humans redirect attention, and a concept map preserves the
emerging structure. This is compatible with the paper's system-level
claim, but it is not evidence that STORM-style curation improves theorem
solving. The proper next step is an equal-budget intervention study, not a
retrospective recoding of the current corpus.

## Verification economics shapes apparent capability

Models may appear unusually strong on targets with compact falsifying
certificates. Comparative studies should stratify by certificate cost,
not only by field, age, or perceived difficulty.

## Formalization is a discovery operator and a scaling problem

C5 shows formalization changing a load-bearing proof step rather than
merely checking it. C14 shows the same interface at repository scale,
where compiler orchestration, dependency management, context continuity,
and human integration may dominate the work. C16 adds a third pattern:
the formal artifact can outgrow the immediate theorem into a reusable
library of reductions and certificates.

These cases should not be collapsed into a single "Lean verified" label.
The relevant questions are which target was encoded, whether the accepted
argument transcribed or replaced the prose proof, which parts of the
complexity claim were formalized, and whether the repository was rebuilt
under a pinned environment.

## Representation escape can create a new research programme

C13 supplies a distinct contribution type. The model did not merely shorten a
known proof; it selected von Mangoldt weights at the opening move, avoiding a
probabilistic route that had become conventional in the field. The later paper
used that representation to solve #1196 and #1217, reprove #164, and address a
revised Banks–Martin statement. The case motivates a testable hypothesis about
representation diversity, not a general claim that models are free of bias.

## Bridge results and failed handoffs can carry discovery forward

C16 makes visible a category that final papers often erase. The
five-voter reduction was superseded by the three-voter theorem, yet it
served as a bridge object for the later search. Claude's unsuccessful
three-voter attempt also left notes and scripts that became inputs to the
next GPT run. A result can therefore be unnecessary in the final proof
and still be causally important to discovery.

This suggests recording a bridge result separately from a final claim,
and treating failed-route notes, scripts, source maps, and open
obligations as typed handoff artifacts. Their value should be judged by
what they enable downstream, not by whether the producing run closed the
main theorem.

## Negative knowledge is reusable capital

C8 shows that a rejected route can reveal the exact denominator,
embedding, or uniformity cost that a successor must pay. C12 records a
non-load-bearing bug rather than hiding it. C16 preserves a superseded
intermediate reduction and another model's failed notes as inputs to a
stronger result. Bare rejection destroys this
capital; productive veto preserves failure witness, scope, salvageable
kernel, and reactivation conditions.

## Claim status is temporal and vector-valued

A result can be correct but not novel; formally checked but poorly bound;
autonomous at generation but dependent on human target choice; or
publicly discussed while still awaiting expert review. “Solved” is a
presentation shorthand, not an adequate stored state.

## Release bundles improve auditability only when correlation is visible

C17 exposes a release architecture not previously visible at this scale:
process narrative, mathematical manuscript, formal repository, trusted
challenge modules, and adversarial checking instructions. The bundle is more
informative than any single artifact, but the artifacts share generator,
editorial, and formalization lineage. Triangulation must therefore be
correlation-aware rather than counted by file type.

## The trusted challenge is part of the proof boundary

Comparator can establish same-statement, axiom-ceiling, and kernel acceptance
relative to a trusted Lean challenge. That is a substantial advance over a
plain build. It does not settle whether the challenge faithfully encodes the
source theorem or whether an open definition has been filled in the intended
way. Formal target design is an assurance operation, not a clerical prelude.

## Small counterexamples and complete benchmarks should precede scale

The ten-advances walkthroughs include a small exact example that invalidated
an attractive recurrence and a separate warning that beating one classical
bound does not beat the strongest optimized benchmark. These episodes suggest
a practical order: run cheap local falsification, freeze the true comparison
baseline and parameter regime, and only then spend heavily on asymptotic or
formal development.

## Persistent trajectory is not yet accepted state

The public cases show that retaining failed routes, scripts, and intermediate
artifacts is valuable. They do not show that any stored item should
automatically change the research state. A provider observation, model
self-correction, compiler error, human preference, proof-kernel acceptance, and
public correction affect different state planes. Durable progress requires an
explicit basis for accepting the relevant delta while leaving unsupported
coordinates unchanged.

This distinction is most visible in C5, where a formalizer repair changes the
encoded proof; C16, where failed notes become a causal handoff asset; and C17,
where a rich release stack does not expose the private campaign's accepted
transition history.

## Repository snapshots are part of the evidence state

A commit hash is not clerical metadata. C17 moved between two distinct
zero-parent root snapshots during the audit window. Both remain addressable,
but only the later root was current on 3 August. A reproducible dossier must
therefore store the branch or tag, the resolved commit, the observation time,
any prior audited root, and whether the new snapshot is a descendant,
replacement, or relationship-unknown object. A change in repository state is
not automatically a change in mathematical claim state.

## Comparator coverage is narrower than repository existence

A top-level Lean module may contain more theorems than a Comparator
configuration names. C17's permanent module formalizes a circuit lower bound
as well as formula lower bounds, while the public Comparator bundle names only
the two formula theorems. Consequently, “the repository contains a proof,”
“`lake build All` succeeds,” “`formalization.yaml` lists a main result,” and
“Comparator checks the named declaration” are four different evidence claims.
Future releases should publish a headline-to-manuscript-to-Lean-to-config
coverage matrix rather than one global “formally verified” label.

## Discovery-token cost is not lifecycle cost

The reported roughly USD 2,000 equivalence concerns tokens used to find the
selected solutions at a stated price reference. C17's `formalization.yaml`
confirms the separation directly: the repository records a wall-clock cost of
roughly one week for formalization and Comparator configuration, independent
of the discovery tokens. The figure excludes the unseen target
pool, failed attempts, human labor, manuscript preparation, formalization,
checking, infrastructure, and external review. Cost claims should be stored as
vectors with explicit exclusions, not as a single campaign price.

# Boundaries of Generalization: A Hypothesis

The controls identified here—fail-closed checks, explicit goal binding, repair lineage, independent attack, and configuration control—may be necessary for transfer to industrial research, but sufficiency cannot be assessed from a purely mathematical corpus. The following are observational warnings and testable design hypotheses, not validated industrial principles.

Five candidate invariants plausibly survive domain transfer: preserve the original objective while versioning reformulations; maintain non-equivalent routes and their failure conditions; separate proposer, adversary, checker or proof kernel, and release authority; preserve negative knowledge and reopen invalidated obligations; and maintain one lineage across claims, artifacts, repairs, reviews, and configurations.

Mathematics nonetheless has unusually decisive affordances. A finite counterexample can refute a universal statement, and a small trusted proof kernel can validate an exact formal theorem. Physical and industrial systems usually add model discrepancy, measurement uncertainty, manufacturing variation, configuration drift, and field degradation. Any transfer study must therefore add at least the following evidence layers:

| Additional industrial requirement | Question that mathematics usually avoids |
|---|---|
| **Model credibility** | In which physical regimes are simulations, surrogates, simplifications, and uncertainty bounds trustworthy? |
| **Manufacturability and supply** | Can the design be fabricated, inspected, sourced, assembled, repaired, and produced at acceptable yield? |
| **Qualified test systems** | Can the rig, sensor, compiler, benchmark, or metrology chain reliably make a bad design fail? |
| **Configuration control** | Which requirement, CAD, material, software, process, and test versions support the released claim? |
| **Field feedback** | Do telemetry, degradation, maintenance, incidents, and operator observations update the model and next design generation? |

Mathematics is therefore a high-observability test bed for search, falsification, repair, and evidence maturation. Generalization beyond it remains a hypothesis requiring domain-specific observational corpora and controlled experiments.

# A Practical Reporting Standard

Future AI-mathematics reports should publish a compact **Research Episode
Dossier** containing:

1. exact source problem, version, and interpretation;
2. prompts and system instructions that can be disclosed;
3. model identifier, settings, tools, and corpus/network policy;
4. full attempt denominator, or an explicit statement that it is absent;
5. branch structure, bridge results, cross-model handoff artifacts,
   model runtime, token/tool budget, and human interventions, with
   active-time or labor-tier evidence kept separate;
6. candidate, repaired, and released artifact hashes;
7. exact formal theorem or checker-to-claim binding;
8. build command, environment lock, placeholder/axiom policy, and
   executed-check manifest;
9. reviewer lineage and review scope;
10. time-stamped prior-art queries and novelty decomposition;
11. corrections, retractions, superseded bridge results,
    simplifications, and strengthening;
12. a human-readable claim card covering all six evidence dimensions;
13. **Trace derivation class**: raw event stream, rewritten log, model reconstruction from private traces, human synthesis, or final-only artifact; state branch coverage and editorial uncertainty.
14. **Release-artifact correlation**: identify shared models, editors, source material, formalizers, and verifiers across process narrative, manuscript, checker, and proof assistant.
15. **Trusted challenge and Comparator boundary**: challenge module/hash, theorem and definition names, permitted axioms, dependency locks, sandbox and kernel assumptions, execution logs, and any additional definition-hole review.
16. **Result-family, dependency, and formal-target hierarchy**: distinguish workflow episode, public result family, shared-method or theorem-dependency edges, claim atom, formal target bundle, manuscript section, source file, and challenge configuration.
17. **Cost and responsibility boundaries**: separate discovery inference, failed attempts, human labor, manuscript preparation, formalization, checking, and independent review; record argument authorship and correctness responsibility by operation.
18. **Benchmark completeness and micro-falsification**: name the strongest relevant optimized baseline, full parameter regime, limit order, and any preregistered small-instance probes that could invalidate the abstraction.

19. **Research-state transitions**: record the key operational, epistemic,
    claim, and artifact deltas without requesting private chain-of-thought.
20. **Transition acceptance basis**: distinguish model proposal, provider
    observation, human decision, exact check, proof-kernel acceptance,
    external review, and public correction.
21. **Continuation contract**: state why the next bounded turn ran, waited,
    redirected, asked for human judgment, or stopped.
22. **Handoff packet**: bind transferred scope, artifacts, established facts,
    failed routes, open obligations, and the next acceptance predicate.
23. **No-change turns and quota**: disclose monitor-only, duplicate, rejected,
    and no-delta turns and whether they were included in reported cost.
24. **Projection provenance**: explain whether a walkthrough, dashboard,
    report, or final paper is a raw event record, derived projection, or
    retrospective reconstruction.
25. **Repository snapshot lineage**: report repository URL, branch or tag,
    resolved commit, observation time, parent count, previous audited commit,
    and any replacement or supersession relation.
26. **Comparator coverage matrix**: map each public headline and manuscript
    claim atom to solution module, `formalization.yaml` main result,
    Comparator configuration, named theorem declarations, and bound
    definitions; uncovered subclaims remain explicit.
27. **Challenge/solution execution status**: distinguish zero `sorry`s in
    solution code from intentional challenge placeholders, configured nanoda
    replay from archived execution, and a declared build command from an
    independently reproduced run.

For systems that use automated pre-search curation, the dossier should
also preserve the perspective sources, question lineage, unresolved-question
register, human steering events, concept-map revisions, outline freeze and
reopen events, and source-coverage or bias audit. These objects are search
provenance, not proof evidence.

This reporting standard does not require private chain-of-thought.
Structured events—candidate, test, defect, repair, replacement,
verification, and release—are sufficient for process analysis.

# Data and Materials Availability

Version 0.14 merges the primary-source C17 branch and the
research-state/continuation-control branch while keeping the corpus at
seventeen episodes. O/E/L coordinates, the nine-component fingerprint counts,
and the four-mechanism matrix are unchanged. The statistical coding remains unchanged, but the companion ledger is
versioned to `evidence_ledger_2026_v0.6.json` so that the C17 resnapshot,
Comparator-coverage hierarchy, and optional research-state profile are
recorded without silently changing population counts.

The ProofFlow Schema Sandbox software release packages:

- the executable event-sourced engine, FastAPI REST service, and CLI (`proofflow` / `schemamath`);
- runtime JSON schemas (`v0.1`–`v0.6`), domain event specifications, and migration engines;
- the standalone dual-canvas workbench and Explorer UI bundles;
- full test and verification suites (`pytest`, `ruff`);
- `operational_evidence_map_v0.14.svg` and `operational_evidence_map_v0.14.png`;
- release manifests, software bill of materials (`THIRD_PARTY_NOTICES.md`, `sbom.cyclonedx.json`), and SHA-256 signatures.

The theoretical qualitative analysis assets—including `evidence_ledger_2026_v0.6.json`, `coding_manual_2026_v0.3.md`, `mechanism_signal_matrix_v0.4.csv`, `descriptive_statistics_v0.5.json`, `C17_Ten_Proofs_Reaudit_v0.2_CN.md`, and `C17_Comparator_Coverage_v0.1.json`—are openly accessible in the companion research dataset repository:
- **Dataset Repository:** [https://github.com/psi-run/From-Prompt-to-Proof-Dataset](https://github.com/psi-run/From-Prompt-to-Proof-Dataset)
- **Persistent Accession & Archive:** [https://psi.run/research/from-prompt-to-proof/v0.14](https://psi.run/research/from-prompt-to-proof/v0.14) (provisional deposit for Zenodo / Open Science Framework DOI).

The uploaded PDFs and public repository were used as primary sources. The JSON
ledger validates against its supplied schema, but the new C17 coverage JSON is
an audit companion rather than a replacement ledger. These remain working
research artifacts under version control until sealed under the final camera-ready DOI deposit.
Mutable URLs or a branch name are not described as archived merely because
they were reachable during the audit.

# Limitations

This release has eight major limitations. First, the corpus is selected
from public successes and unusually transparent authors; its descriptive
frequencies cannot be generalized to unseen attempts. Second, mutable
social-media and shared-chat evidence is sometimes incomplete despite
archival efforts. Third, we did not independently re-prove every result
or rebuild every Lean repository. Fourth, novelty, autonomy, and total
human labor remain difficult to infer from public artifacts; labor tiers
are lower-bound visibility codes only.

Fifth, coding remains single-analyst, meaning that no formal inter-rater reliability has been established. The frozen manual and machine consistency checks improve auditability, but they do not replace the need for blind double-coding.

Sixth, the industrial discussion is speculative because the
corpus contains only mathematical episodes.

Seventh, the corpus rarely exposes the pre-search question agenda. The
STORM/Co-STORM discussion is therefore an adjacent-system hypothesis,
not a coded finding about the seventeen mathematical episodes.

Eighth, C17 was released on the snapshot date. This paper inspected the
official manuscript, walkthrough, repository metadata, trusted challenge
configurations, and checking protocol, but did not independently rebuild the
complete formal repository or observe mature external mathematical review.

Ninth, public cases rarely expose a complete control-plane state. A final
paper may reveal that a route changed without showing who accepted the change,
what alternatives remained open, or why another turn was authorized.
Retrospective timelines are partial-order reconstructions, not causal event
logs.

Tenth, the C17 repository changed between two distinct root snapshots during
the audit window. Version 0.14 records both, but it did not independently
determine why the branch pointer changed, execute every Comparator/nanoda
configuration, or complete a claim-by-claim natural-language/formal coverage
audit.

The next descriptive step is a stratified corpus containing successes,
partial results, retractions, prior-art rediscoveries, failed long runs,
formal-target mismatches, and unverifiable claims, followed by blind
double coding and an adjudication log. The next causal step is an
equal-budget experiment comparing minimal prompting, contract
specification, parallel search, same-model destructive critique,
independent critique, formal feedback, persistent trajectory memory, and perspective-guided question elicitation
on a frozen target set.

# Conclusion

Taken together, the 2026 episodes show a shift from isolated model answers
toward organized research workflows. Those workflows range from single-chat
counterexamples to large formalization projects. Their credibility does not
track complexity in any simple way. The stronger support paths are those in
which the target is pinned, objections are recorded, claims are tied to exact
artifacts, and later review can narrow, repair, or strengthen the result.

The cases also expose a consistent set of hazards. Outcome mandates can
inflate scope; same-model review can manufacture correlated confidence;
formalization can certify the wrong target or silently replace the
argument; an exact checker can skip critical checks; a published success
can hide its denominator; a superseded bridge result can disappear from
the record; prior art can change novelty without changing truth; and a
post-hoc process narrative can launder genuine trial and error into a
smooth heroic arc. The credibility of a result depends on how these failure modes are handled.

Version 0.14 adds two qualifications. Persistent memory is not enough:
durable progress requires a visible basis for accepting state changes and
handing work to the next model, tool, or mathematician. Likewise, a rich
formal release is not one undifferentiated certificate: repository snapshot,
solution build, trusted challenge, named Comparator coverage, second-kernel
configuration, and external review are separate evidence objects.

The central finding is straightforward: **credible AI-assisted discovery depends on the surrounding research system.** In
this selected corpus, the most mature support paths combine goal binding,
falsification, repair lineage, exact artifacts, visible human work, and
external scrutiny. A reliable research machine must preserve goals,
diversify routes, retain negative knowledge and useful bridge artifacts,
reserve capacity for attack and verification, and bind claims to exact
artifacts. Mathematics makes
these requirements unusually visible. Whether the same architecture
improves scientific and industrial discovery remains an empirical
question, but the variables are now explicit enough to test. The
STORM/Co-STORM comparison adds one such variable: whether perspective-
guided, human-steerable question agendas improve route discovery without
increasing source bias, unsupported association, or premature outline
lock-in.

C17 adds a further boundary. A public release can combine a mathematical
manuscript, process reconstruction, formal repository, trusted challenges,
Comparator configurations, and configured second-kernel replay without those
artifacts becoming independent evidence or covering every headline subclaim.
The trusted challenge, configuration coverage, repository snapshot lineage,
inter-result dependencies, full benchmark, and lifecycle cost remain part of
the claim. This does not diminish the release; it specifies what an unusually
mature same-day artifact package can and cannot establish.

> **Box 1. Recommended Guidelines for Future AI4Math Research**

> 1. Define target problems, precise statements, and versions before announcing results.
> 2. Avoid treating the mere existence of a Lean file as proof; build a commit-pinned, dependency-locked kernel verification trail.
> 3. Attribute contributions granularly, distinguishing between autonomous generation, repair, formalization, and human steering.
> 4. Preregister study objectives and report the full denominator of attempts, including abandoned and withdrawn sessions.
> 5. Record reviews, repairs, bridge results, and cross-model handoffs, including what failed and what the next stage reused.
> 6. Design exact checkers to be fail-closed, accompanied by execution manifests and negative tests.
> 7. Disentangle proof validity, mathematical novelty, process independence, and community validation status.
> 8. Store all prompts, repository commits, and build environments in public, immutable archives.

# Appendix A. Artifact-Access Ladder

The six-dimensional evidence card is primary. The following ladder is a
compact description of publicly accessible artifact types.

| Tier | Public evidence object | What it does not establish by itself |
|---|---|---|
| **E0** | Root post or author report | Correctness, complete process, novelty |
| **E1** | Continuation thread or shared conversation | Hidden instructions, omitted attempts, independent review |
| **E2** | Inspectable manuscript, code, or repository | Correct target binding or successful execution |
| **E3** | Kernel-checked proof or hardened exact checker | Natural-language equivalence, novelty, autonomy |
| **E4** | Independent expert review or curator adjudication | Verification of uninspected subclaims or every process step |
| **E5** | Independent re-derivation, mature human proof, or external strengthening | Complete fidelity of the original generation trace |

# Appendix B. Nested Cohort Details: Holter’s Ten Public Pro Sessions

These are ten task-level subepisodes inside C2, not ten independent
campaigns.

| Task label | Public Pro session | Source-binding state and analytical use |
|---|---|---|
| Adenwalla Conjecture 4.12 | <https://chatgpt.com/share/6a628954-3664-83ea-aac7-31286c2f4d68> | Exact source and prior-art state require confirmation; useful for target-binding and rediscovery audit |
| Tang–Zhang Conjecture 3.1 | <https://chatgpt.com/share/6a628b26-5504-83ea-947e-b31aa5d00754> | Matrix-inequality source identifiable; exact session-to-source map pending |
| Aceska–Lort–Ripperger DDMOG conjecture | <https://chatgpt.com/share/6a628b2c-3a48-83ea-b22c-25717a44bc22> | Constructive graph-labeling target; finite-certificate economics |
| Hashemi Conjecture 4.1 | <https://chatgpt.com/share/6a628b33-19d0-83ea-bd81-523d569a787e> | Numerically observed spectrum; numerical-to-symbolic proof boundary |
| Hypercube edge-multiset dimension problem | <https://chatgpt.com/share/6a628b46-cfe4-83ea-81d2-51bdd6e8e2bb> | Exact source and open status pending; finite search/certificate analysis |
| Bubboloni–Fumagalli–Praeger Conjecture/Open Problem 1 | <https://chatgpt.com/share/6a628b4a-f250-83ea-90e2-05b2c857ffe3> | Enhanced-power-graph source identifiable; numbering and scope need round-trip check |
| DeLeo–Henderschedt–Wells Conjecture 1.4 | <https://chatgpt.com/share/6a628b50-3ecc-83ea-a61d-1405a81242f2> | Interval-discrepancy source identifiable; asymptotic constants and proof-repair audit |
| Friedman Conjecture 3.2 | <https://chatgpt.com/share/6a628b64-2e2c-83ea-9103-4ec1fdb34707> | Source author and statement version ambiguous; source-disambiguation stress test |
| Bóna–Maga–Richey Conjecture 3.1 | <https://chatgpt.com/share/6a628b69-4e0c-83ea-9d02-e39baae190a6> | Forbidden-word source identifiable; exact claimed proof pending inspection |
| Suvagiya Conjecture 3 | <https://chatgpt.com/share/6a628b6e-6148-83ea-82b3-30e3b8c862c2> | Very recent source; version freeze and independent review pending |

Before public dataset release, each page should be exported with a
capture time, content hash, visible-turn count, attachment state, and
source-conjecture binding. A valid share URL proves reachability, not
conversation completeness or correctness.

# Appendix C. Compact Evidence Cards

**Table A1a. Evidence state for episodes C1 to C9.**

| Episode | Max visible access tier | Process evidence | Verification/review evidence | Open gaps |
|---|---|---|---|---|
| C1 Wang | E3/E4, uneven | Detailed thread, prompts, repository, run descriptions | Several Lean/CI artifacts and public corrections | Complete denominator, uniform rebuild, final status of all outputs |
| C2 Holter campaign | E2/E3 | Thread plus ten corrected Pro links; aggregate timing | Same-model audits and selected exact checks | Full archival/coding, source binding, independent review, all-attempt denominator |
| C3 #330 | E3/E4 | Process thread and scaffold account | Lean package and community PROVED (LEAN) state | Complete chat, independent rebuild, novelty dossier |
| C4 #635 | E3/E4, partial claim | Initial claim and public correction | Lean artifact and expert/community review of second subproblem | First subproblem remains open |
| C5 #650 | E4 | Collaboration and repair chronology | Lean proof, human paper, solved community state | Independent full-proof review and formalizer-credit conventions |
| C6 #728 | E4 | Process thread and target reconstruction | Lean proof and human writeup | Autonomy granularity, prior-art comparison, source-goal equivalence |
| C7 fixed perimeter | E3 | Public two-pass conversation and artifacts | Large exact finite checks; source-level rerun | Kernel proof, independent review, hardened checker release |
| C8 unit distance | E5 | Prompt/final response and rewritten 125-page trace | External human proof and independent strengthening | Raw complete trace, formal proof assistant, final journal status |
| C9 Rybin | E2/E3, reported | Thread, replies, shared link, prior human context | Concrete counterexample and independent computation reported | Full chat, public exact-checking program, mature paper |

**Table A1b. Evidence state for episodes C10 to C17.**

| Episode | Max visible access tier | Process evidence | Verification/review evidence | Open gaps |
|---|---|---|---|---|
| C10 Chakravarthy | E1/E2, reported | Minimal prompt and announcements | Technical reports reported | Reports, full thread, independent review |
| C11 Devin | E2/E3, reported | Root and video posts; local-only evidence-note SHA-256 `cb7a…752b8` (not reader-verifiable until deposit) | No-placeholder Lean and adversarial checks reported | Stable repository/commit, theorem-to-build map, clean rebuild, independent adjudication |
| C12 #477 | E2 | Repository, commit history, explicit verification notes | Same-family reruns and adversarial passes; Claude primary-source spot checks | Public sessions, full independent proof review, Lean, human number theorist, novelty adjudication |
| C13 #1196 | E5 | Public expert thread, multi-author paper, problem-page chronology | Human proof, public formalization, curator/expert maturation and generalization | Complete original Pro session, exact transformation chronology, independent archive of every linked artifact |
| C14 #870 | E3/E4, reported | Detailed process thread describing scaffold, token scale, and tool failures | Sorry-free/axiom-free 180,000-line Lean project reported | Stable repository/commit, dependency lock, clean rebuild, theorem-to-source binding, community status update |
| C15 OpenAI short proofs | E4 | Public announcement and inspectable six-page paper with explicit AI-role statement | Five-human-author mathematical digestion; partial public GPT-5.4 Pro recreation | Internal model trace, original attempt denominator, independent formalization or external referee status |
| C16 Kemeny three voters | E3, provisional | Detailed arXiv process account, public paper, and two public Lean repositories | Kemeny reduction formalized; broader reduction library states its certificate boundary | Exact commit pair, clean rebuild, complete model sessions, independent review, publication status |
| C17 OpenAI ten advances | E3, unusually strong formal-artifact path | Official announcement, 249-page manuscript, 62-page model-written reconstruction from private trajectories, prior and current zero-parent repository snapshots | Ten top-level solution modules; twelve `main_results`/Comparator bundles; 38 named theorem declarations; four bound definitions; permitted axioms; nanoda configured; metadata says agent-reviewed | Raw trajectories, full attempt denominator, complete lifecycle cost, archived all-bundle Comparator/nanoda execution, headline-to-config coverage, independent clean rebuild, independent expert review, natural/formal binding audit, stable release lineage, community status |


# Appendix D. Proposed Coding Fields for an Expanded Corpus

An expanded 30–50 episode dataset should record: episode identifier;
source problem and age; mathematical field; finite versus asymptotic
target; proof versus counterexample; model and tool stack; prompt class;
problem-selection mechanism; branch count; wall-clock and aggregate
inference; memory mechanism; verification class; source-to-formal binding;
repair count and magnitude; bridge-result relation; cross-model handoff artifact type and receiving impact; perspective origin; question origin and parent lineage; follow-up depth; unresolved-question register; human discourse steering; concept-map revisions; outline freeze/reopen events; source-family diversity and bias audit; unsupported-association status; mechanism-presence and mechanism-outcome codes; result-family and formal-target hierarchy; inter-result dependency edges; trace-derivation class and branch-coverage status; artifact-correlation groups; trusted challenge, theorem names, definition holes, permitted axioms, Comparator/kernels, and natural/formal binding; strongest optimized benchmark and micro-counterexample probes; campaign cost coordinates; responsibility/authorship by operation; release topology, branch/ref, current and prior commit ancestry; operational/epistemic/claim/artifact state visibility; transition trigger, proposal actor, acceptance basis, accepted delta, rejected proposal components, next obligations, continuation decision, concrete gates, todo ownership, lease/revision state, handoff scope and artifact reachability, no-change turns, projection provenance; Comparator configuration count, theorem-name count, definition-name count, headline-to-config coverage and run status; challenge-versus-solution placeholder status; visible human-labor tier, reported active
time, and intervention by stage; coder identity, pre-adjudication label, reviewer lineage; artifact hashes;
prior-art state; correction history; final
six-dimensional evidence vector; and whether every attempted target is
included.

# Appendix E. Machine-Readable Evidence Ledger

The companion JSON package is designed for extension without collapsing
evidence into one score. A minimal episode object has the following
shape:

The v0.6 ledger adds optional `research_state_transition_profile`,
repository-snapshot lineage, and claim-specific Comparator-coverage records.
Version 0.14 does not regenerate the seventeen-case component or mechanism
statistics from these fields because transition acceptance, continuation
evidence, and formal coverage remain incomplete for many episodes. Absence of
public control state or Comparator coverage is recorded as unknown, not as
evidence that no state management or proof exists.

The v0.6 Schema retains the legacy machine field name
`verifier_driven_repair_or_hardening`; prose in this manuscript uses the
more specific terms proof assistant, proof kernel, and exact checker.

```json
{
  "episode_id": "C8",
  "operational_configuration": "O3",
  "artifact_access": {
    "minimum_tier": 5,
    "maximum_tier": 5,
    "display_label": "E5"
  },
  "visible_human_labor": {
    "tier": "L2",
    "lower_bound_only": true
  },
  "workflow_components": {
    "P": "P", "G": "Y", "T": "P", "M": "Y", "F": "Y",
    "V": "P", "R": "Y", "H": "Y", "E": "Y"
  },
  "mechanism_signals": {
    "certificate_asymmetry": "P",
    "destructive_critique": "Y",
    "verifier_driven_repair_or_hardening": "-",
    "compute_plus_persistent_state": "Y",
    "material_defect_or_falsification": "Y"
  },
  "evidence_dimensions": {
    "process_provenance": "partial",
    "artifact_availability": "clear",
    "deterministic_verification": "partial",
    "independent_review": "clear",
    "novelty_and_prior_art": "clear",
    "autonomy_and_attribution": "partial"
  },
  "status_as_of": "2026-07-30",
  "research_state_transition_profile": {
    "operational_state_visibility": "P",
    "epistemic_state_visibility": "Y",
    "claim_state_visibility": "Y",
    "artifact_state_visibility": "Y",
    "key_transitions": [
      {
        "trigger_class": "REPRESENTATION_SHIFT",
        "acceptance_basis": "DERIVED_FROM_PUBLIC_TRACE",
        "status": "PARTIAL"
      }
    ]
  },
  "source_urls": [
    "https://openai.com/index/model-disproves-",
    "  discrete-geometry-conjecture/",
    "https://cdn.openai.com/pdf/1625eff6-5ac1-40d8-",
    "  b1db-5d5cf925de8b/unit-distance-cot.pdf",
    "https://arxiv.org/abs/2605.20695",
    "https://arxiv.org/abs/2605.20579"
  ],
  "snapshot_hashes": [
    {
      "artifact": "unit-distance-cot.pdf",
      "sha256": "d9d78b8b9070ab54eb4a05dca93f8d2a64c74ea7072dacc3e2754374fd19477b",
      "scope": "Locally archived 125-page research trace;\n                reader-verifiable after public deposit"
    }
  ],
  "open_gaps": [
    "Raw complete chronological trace",
    "Proof-assistant formalization of the final theorem",
    "Final journal or community publication state"
  ],
  "bridge_results": [],
  "handoff_artifacts": []
}
```

The full schema constrains identifiers, coding vocabularies, access-tier
ranges, labor-tier uncertainty, component states, source URLs, and
SHA-256 records. Community contributions should preserve the episode/
subepisode distinction, attach an `as_of` date, record bridge results and
handoff artifacts when they affect the support path, and record missing
evidence rather than inferring it.

# Appendix F. Extended Case Notes

These notes preserve the longer reconstructions compressed from the main text. They do not create additional episode counts.

## C1. Contracted parallel search: Shouqiao Wang

Wang’s public campaign used GPT-5.6 Sol and Codex to attack several
Erdős problems over five days (Wang 2026a, 2026b). The important feature
is not a particular prompt phrase but the scaffold: problems were
screened for tractability and prior-art risk; acceptable proof or
disproof conditions were specified; known traps and weak non-solutions
were listed; and up to four incompatible routes were allowed to run for
approximately six to thirty-two hours. This combines two portfolio
problems that should not be conflated: selecting which open questions to
fund, and preserving genuinely different routes within one question.

The outputs had uneven maturity. Selected cases had Lean or CI artifacts;
others remained manuscript-level. Erdős #536 was publicly narrowed after
a scope error, and prior-art questions affected other claims. The case is
therefore strong evidence for structured high-throughput search and
artifact production, not for six equally established solutions or a
reproducible campaign success rate. It also exposes an outcome-coercion
risk: prompts that insist a complete resolution exists can increase
persistence while pressuring a model to package partial evidence as
closure. Search policy and claim policy must be separated.

## C2. High-throughput nested cohort: Adam Holter

Holter disclosed a campaign of ten recent conjecture candidates, each
followed by a dedicated same-model audit (Holter 2026b). The corrected
public Pro links make this one of the few natural within-campaign cohorts:
operator, model family, time window, and audit style are comparatively
stable while target structure varies. The campaign is one episode with
ten nested task-level subepisodes, not ten independent workflow samples.

Two subepisodes illustrate the methodological range. The Aceska–Lort–
Ripperger DDMOG target appears to favor a constructive finite certificate,
where local checking may be comparatively cheap. Hashemi Conjecture 4.1
originates in a numerically observed spectral pattern, where converting
computation into a universal symbolic argument creates a very different
verification burden. The remaining links are listed in Appendix B.

Same-model audits found real defects in the campaign, so self-critique is
not dismissed. It is nevertheless correlated evidence. One session also
revisited a target handled elsewhere before human redirection, showing
that parallel throughput without a global claim registry and prior-
attempt fingerprints can amplify duplication. The author’s “unrefereed”
label is an appropriate evidence boundary, not a reason to erase the
process value.

## C3. End-to-end formalization: David Turturean and Erdős #330

Turturean described a custom scaffold developed over a semester and a
roughly six-hour sequence of fifteen to more than twenty interactions
with ChatGPT-5.5 Pro (Turturean 2026; Erdős Problems community 2026b).
The process produced a manuscript and a substantial Lean package later
integrated into a public repository (Hart and collaborators 2026). At the
snapshot date the community page reported the result as proved in Lean.

The case shows that formalization begins before the first Lean token. The
natural-language problem required semantic choices about positive upper
density and how the source question should be represented. Kernel
acceptance certifies the encoded target; source-to-target equivalence
remains a separate obligation. The repository also demonstrates artifact
role confusion: a benchmark target file may intentionally contain a
placeholder while another directory contains the proof. Repository-wide
`grep` results cannot replace an exact theorem name, commit, build
command, environment, and axiom policy.

Among the corpus, #330 provides one of the strongest visible paths from
scaffolded informal search to a machine-checkable theorem. It still does
not establish full conversation completeness, explanatory quality, or
novelty by kernel acceptance alone.

## C4. Public downgrade as successful governance: Liam Price and Erdős #635

Price initially reported that GPT-5.2 Pro, followed by Aristotle
formalization and human cleanup, resolved a two-part Erdős problem
(Price 2026). Expert review later produced a public correction: the
second subproblem had been answered, while the first remained open
(Erdős Problems community 2026c).

The process is methodologically valuable because the correction preserves
rather than destroys knowledge. A single “solved” flag made the original
overstatement easy. A claim graph with separately decidable subproblems
would have allowed the supported child result to remain while the parent
claim was downgraded. This is a general design principle: corrections
should propagate only through justified dependencies, not erase every
artifact or silently preserve the original headline.

The episode also provides a counterexample to forced-resolution rhetoric.
A useful AI research system must be allowed to end in partial result,
reformulation, or unresolved obligation. Public downgrade is not a
failure of governance; it is evidence that the claim-maturation loop
remained responsive to stronger review.

## C6. Target reconstruction and prior-art reclassification: Erdős #728

The #728 episode combined GPT-5.2 Pro, Aristotle, and substantial human
participation. The source problem was ambiguous, so collaborators first
reconstructed a meaningful nontrivial target. A model proof was refined,
formalized, simplified, and translated into an accessible human writeup
(Barreto and collaborators 2026; Erdős Problems community 2026d;
Sothanaphan 2026).

Human work included semantic reconstruction, high-level redirection,
formalization launch, simplification, exposition, and literature review.
Those interventions do not diminish the result; they make a global
“fully autonomous” label inaccurate. The episode also demonstrates that
validity and novelty can move independently. Related prior work by
Pomerance changed how the contribution should be positioned even if the
new proof remained correct.

The general lesson is that goal reconstruction can be a legitimate
research contribution, but it must be explicit. A system should record
which statement was inherited, which interpretation was selected, what
changed, and whether the formal theorem is equivalent, weaker, stronger,
or simply different.

## C9. Finite counterexample asymmetry: Dmitry Rybin and Dinitz–Garg–Goemans

Rybin reported that GPT-5.6 Pro found a counterexample to the Dinitz–
Garg–Goemans unsplittable-flow conjecture in one shared conversation
(Rybin 2026; OpenAI ChatGPT shared conversation 2026a). The public account
includes a concrete finite graph and a numerical separation between a
fractional optimum and every admissible unsplittable flow under the
stated violation bound. Rybin also disclosed weeks of prior human thought
and unsuccessful brute-force or earlier-model attempts.

This episode illustrates certificate asymmetry. A universal statement
may require many dependent lemmas; one finite graph can refute it and may
be checked with exact optimization or exhaustive enumeration. The
mathematical value can therefore be high even when the prompt is simple
and the explanatory trace is incomplete.

Attribution remains mixed: the human selected the problem, supplied
prior structure, interpreted the output, and arranged public checking.
The full shared-chat body, public exact-checking program, and mature paper were not all
captured in this audit. The case is used as a strong example of favorable
certificate economics, not as evidence that one-shot prompting generally
solves open mathematics.

## C10. Minimal-prompt target discovery: Anirudh Chakravarthy

Chakravarthy reported using a one-sentence instruction asking GPT-5.6
Sol Pro to find an old open conjecture and return a full result. The model
selected two combinatorial targets: McKee’s pentagulation conjecture and
the nonexistence of a $(9,6,1)$ perfect Mendelsohn design
(Chakravarthy 2026). The operator emphasized having no mathematical
background and linked two technical reports.

The process is valuable because it isolates an extreme operational form:
target selection, interpretation, search, and exposition occur inside a
minimal interaction. It does not establish that human mathematical
expertise is generally unnecessary. The likely moderating variable is
certificate structure. A small counterexample or finite nonexistence
certificate can be much cheaper to check than a universal analytic proof.

The linked reports and full continuation thread were not completely
captured in the frozen archive for Version 0.14, so the outcomes remain author-reported in this
analysis. The episode motivates a controlled hypothesis about prompt
complexity and verification cost; it is not used as a mature theorem-
level validation.

## C11. Batch multi-agent research: Jared Zoneraich and Devin

Zoneraich reported a workflow in which Devin was shown Rybin’s post,
asked to find analogous open problems, and used Fable plus GPT-5.6 Sol to
attack Graffiti and regular-supergraph targets (Zoneraich 2026a, 2026b).
The disclosed architecture launched several high-compute agents per
problem, gathered candidate proofs, translated them into Lean without
placeholders, and ran an adversarial stage. A video and public repository
were reported.

This is the clearest episode in the corpus where the relevant unit is a
research-program controller rather than a single solver. The controller
performs problem discovery, branch allocation, proof collection,
formalization routing, and repeated deployment across a portfolio.

The evidence boundary is material. At the snapshot date, the root and
video posts were public, but the frozen archive did not recover a stable
GitHub repository URL, commit hash, or complete target-to-build mapping.
The locally archived C11 metadata snapshot has SHA-256
`cb7a08938982a832371d7934d7c8715abb6358f911313e23d0b1633b650752b8`;
this is a hash of the evidence note, **not** of a full repository, video,
or X thread. We therefore do not invent a repository citation. “No
`sorry`” is useful only after the exact theorem, source binding,
toolchain, dependencies, build command, and successful kernel job are
identified. C11 remains an orchestration exemplar at E2–E3 (reported),
not independent certification of every announced mathematical result.

## C13. Representation escape and expert maturation: Erdős #1196

The public #1196 episode began as a compact GPT-5.4 Pro session prompted by
Liam Price, but its enduring value is visible through Jared Duker Lichtman’s
expert interpretation and the later multi-author paper. Lichtman had spent
years on primitive sets and described the model’s opening as analogous to a
new chess opening: instead of inheriting the field’s standard passage from
analytic identities to probabilistic language, the proof retained von
Mangoldt weights and used the exact identity $\sum_{d\mid n}\Lambda(d)=\log n$
to encode unique factorization. Thomas Bloom similarly emphasized that the
model returned to the beginning and chose a path experts had repeatedly
overlooked (Lichtman 2026; Bloom 2026).

The maturation path is unusually strong. The arXiv paper by Alexeev, Barreto,
Li, Lichtman, Price, Shah, Tang, and Tao attributes the method to GPT-5.4 Pro
and develops it into proofs of #1196 and #1217, a short proof of #164, and a
revised Banks–Martin result. A public formalization was later reported on the
problem page. The episode therefore enters the corpus as O1 at generation but
E5 after expert generalization and formal maturation. It is not evidence that
one-shot prompting alone supplies publication-ready mathematics; it is evidence
that an unconventional representation can become a human research programme.

## C14. Formalization as repository-scale engineering: David Turturean and Erdős #870

Turturean’s third reported Erdős episode is distinct from C3. The mathematical
solution was first elicited with ChatGPT-5.5 Pro, but the public process thread
focuses on the cost of making the result formal. Turturean reports roughly
180,000 lines of Lean, no remaining `sorry` and no added axioms, with the early
portion produced through Codex and the later portion requiring a custom scaffold
in which Claude Opus 4.8 drove compilation and repeatedly requested missing
code from ChatGPT Pro. He estimates approximately $10^8$ generated tokens and
orders of magnitude more aggregate context processed across the project
(Turturean 2026b).

This is valuable even while the evidence is incomplete. Earlier forum history
shows that #870 had unresolved $k=3$ concerns and formalization obstacles; the
later thread reports that those obstacles were eventually overcome. The current
frozen archive has not yet captured a stable repository URL, commit, exact
Lean/Mathlib lock, or clean independent rebuild. C14 is therefore coded as an
O4, E3–E4 reported workflow rather than a settled community-status claim. Its
methodological contribution is the scale transition: when formal developments
reach hundreds of thousands of lines, compiler orchestration, dependency
management, context paging, and human integration become load-bearing.

## C15. Internal model discovery and human digestion: three short Erdős proofs

Alexeev, Putterman, Sawhney, Sellke, and Valiant (2026b) published a six-page paper containing three short proofs for Erdős questions #684, #741, and #997. The paper states that the proofs were due to an internal OpenAI model and that the human authors digested the arguments and revised the exposition for clarity and elegance. This makes the attribution boundary unusually explicit:
core derivation is assigned to the model; publication-quality mathematical
communication and checking remain human work.

The paper also reports a limited public-model recreation exercise. Fewer than
ten identical GPT-5.4 Pro attempts were made on selected targets: the first and
third results each produced another similar solution, while the second was not
reproduced by Pro. This is not a full denominator for the internal campaign, but
it is rare negative evidence about cross-model reproducibility. The episode is
therefore distinct from C8: both involve internal models and human maturation,
but C15 emphasizes short-proof digestion and partial public recreation rather
than a long route trace and independent strengthening.

# Appendix G. Per-Case Mechanism-Signal Matrix

`[Y]` = clearly visible; `[P]` = partial or author-reported; `[-]` = not established. The outcome column is coded independently from mechanism presence.

| Case | Certificate asymmetry | Destructive critique | Proof-assistant or exact-checker feedback | Compute + persistent state | Material defect/falsification |
|---|:---:|:---:|:---:|:---:|:---:|
| C1 | [P] | [P] | [-] | [Y] | [Y] |
| C2 | [Y] | [Y] | [-] | [P] | [Y] |
| C3 | [-] | [P] | [P] | [Y] | [P] |
| C4 | [-] | [P] | [P] | [P] | [Y] |
| C5 | [-] | [P] | [Y] | [P] | [Y] |
| C6 | [-] | [P] | [P] | [P] | [Y] |
| C7 | [Y] | [Y] | [Y] | [P] | [Y] |
| C8 | [P] | [Y] | [-] | [Y] | [Y] |
| C9 | [Y] | [P] | [-] | [-] | [Y] |
| C10 | [P] | [-] | [-] | [-] | [P] |
| C11 | [-] | [P] | [P] | [P] | [P] |
| C12 | [-] | [Y] | [-] | [Y] | [Y] |
| C13 | [-] | [P] | [P] | [P] | [-] |
| C14 | [-] | [Y] | [Y] | [Y] | [Y] |
| C15 | [P] | [P] | [-] | [P] | [-] |
| C16 | [-] | [P] | [P] | [Y] | [P] |
| C17 | [P] | [P] | [P] | [P] | [Y] |


# References

*Mutable web sources were last accessed on 3 August 2026 unless another date is shown; detailed capture metadata is in the companion ledger.*


<div id="refs" class="references csl-bib-body hanging-indent"
entry-spacing="0">

<div id="ref-alexeev2026primitive" class="csl-entry">

Alexeev, Boris, Kevin Barreto, Yanyang Li, Jared Duker Lichtman, Liam
Price, Jibran Iqbal Shah, Quanyu Tang, and Terence Tao. 2026. “Primitive
Sets and von Mangoldt Chains: Erdős Problem #1196 and Beyond.” arXiv:
2605.00301. <https://arxiv.org/abs/2605.00301>.

</div>

<div id="ref-lichtman2026" class="csl-entry">

Lichtman, Jared Duker. 2026. “Process and Expert Interpretation of the
GPT-5.4 Pro Route for Erdős #1196.” X thread, 15 April 2026.
<https://x.com/jdlichtman/status/2044298382852927894>.

</div>

<div id="ref-bloom2026thread1196" class="csl-entry">

Bloom, Thomas. 2026. “How the #1196 Episode Complemented Human Research.”
X thread, 15 April 2026; archived by Thread Reader.
<https://threadreaderapp.com/thread/2044319103310021078.html>.

</div>

<div id="ref-turturean2026_870" class="csl-entry">

Turturean, David. 2026b. “Erdős Problem #870 Solved with ChatGPT-5.5 Pro
and a Large Lean 4 Formalization.” X thread, 26 June 2026.
<https://x.com/DavidTurturean/status/2070531663461756950>.

</div>

<div id="ref-alexeev2026short" class="csl-entry">

Alexeev, Boris, Moe Putterman, Mehtaab Sawhney, Mark Sellke, and Gregory
Valiant. 2026b. “Short Proofs in Combinatorics and Number Theory.”
arXiv:2603.29961. <https://arxiv.org/abs/2603.29961>.

</div>

<div id="ref-sawhney2026thread" class="csl-entry">

Sawhney, Mehtaab. 2026. “Three Further Erdős Problems Solved by an
Internal Model at OpenAI.” X thread, 31 March 2026.
<https://x.com/mehtaab_sawhney/status/2039161544144310453>.

</div>


<div id="ref-white2026erdos477" class="csl-entry">

White, Patrick, and Claude (MathDyad). 2026. “Erdős Problem #477: Every
Integer Power at Least Three Has a Tiling Complement.” GitHub repository,
commit `8440d59`, 23 July 2026.
<https://github.com/pw/erdos477-cubic>.

</div>

<div id="ref-erdos477page" class="csl-entry">

Erdős Problems community. 2026e. “Erdős Problem #477.” Problem page and
discussion thread, accessed 25 July 2026.
<https://www.erdosproblems.com/477>.

</div>

<div id="ref-alon2026remarks" class="csl-entry">

Alon, Noga, Thomas F. Bloom, W. T. Gowers, Daniel Litt, Will Sawin, Arul
Shankar, Jacob Tsimerman, Victor Wang, and Melanie Matchett Wood. 2026.
“Remarks on the Disproof of the Unit Distance Conjecture.” *arXiv
Preprint arXiv:2605.20695*. <https://arxiv.org/abs/2605.20695>.

</div>

<div id="ref-acer2026thread" class="csl-entry">

Barreto, Kevin, and collaborators. 2026. “Process Thread for the
AI-Assisted Resolution of Erdős Problem \#728.” X thread.
<https://x.com/AcerFur/status/2008608669047644398>.

</div>

<div id="ref-chakravarthy2026thread" class="csl-entry">

Chakravarthy, Anirudh. 2026. “Minimal-Prompt AI Attempts on Two Open
Combinatorial Problems.” X thread and linked technical reports.
<https://x.com/anirudhchak/status/2080338128922108085>.

</div>

<div id="ref-erdos650lean" class="csl-entry">

Doorn, Wouter van, and collaborators. 2026. “Lean Formalization of Erdős
Problem \#650.” GitHub source.
<https://github.com/Woett/Lean-files/blob/main/ErdosProblem650.lean>.

</div>

<div id="ref-vandoorn2026erdos650" class="csl-entry">

Doorn, Wouter van, Yanyang Li, and Quanyu Tang. 2026. “Optimal Bounds
for an Erdős Problem on Matching Integers to Distinct Multiples.” *arXiv
Preprint arXiv:2603.28636*. <https://arxiv.org/abs/2603.28636>.

</div>

<div id="ref-erdoswiki2026ai" class="csl-entry">

Erdős Problems community. 2026a. “AI Contributions to Erdős Problems.”
Community-maintained GitHub wiki.
<https://github.com/teorth/erdosproblems/wiki/AI-contributions-to-Erd%C5%91s-problems>.

</div>

<div id="ref-erdos330forum" class="csl-entry">

———. 2026b. “Erdős Problem \#330 Discussion Thread.” Community problem
forum. <https://www.erdosproblems.com/forum/thread/330>.

</div>

<div id="ref-erdos635forum" class="csl-entry">

———. 2026c. “Erdős Problem \#635 Discussion Thread.” Community problem
forum. <https://www.erdosproblems.com/forum/thread/635?order=oldest>.

</div>

<div id="ref-erdos728forum" class="csl-entry">

———. 2026d. “Erdős Problem \#728 Discussion Thread.” Community problem
forum. <https://www.erdosproblems.com/forum/thread/728>.

</div>

<div id="ref-feldman2025godel" class="csl-entry">

Feldman, Moran, and Amin Karbasi. 2025. “Gödel Test: Can Large Language
Models Solve Easy Conjectures?” *arXiv Preprint arXiv:2509.18383*.
<https://arxiv.org/abs/2509.18383>.

</div>

<div id="ref-feng2026gemini" class="csl-entry">

Feng, Tony, Trieu Trinh, Garrett Bingham, Jiwon Kang, Shengtong Zhang,
et al. 2026. “Semi-Autonomous Mathematics Discovery with Gemini: A Case
Study on the Erdős Problems.” *arXiv Preprint arXiv:2601.22401*.
<https://arxiv.org/abs/2601.22401>.

</div>

<div id="ref-firsching2026formal" class="csl-entry">

Firsching, Moritz, Paul Lezeau, Salvatore Mercuri, Miklós Z. Horváth,
Yaël Dillies, et al. 2026. “Formal Conjectures: An Open and Evolving
Benchmark for Verified Discovery in Mathematics.” *arXiv Preprint
arXiv:2605.13171*. <https://arxiv.org/abs/2605.13171>.

</div>

<div id="ref-gray2025perimeter" class="csl-entry">

Gray, Gabriel, Emily Payne, Holly Swisher, and Ren Watson. 2025. “Fixed
Perimeter Analogues of Some Partition Results.” *arXiv Preprint
arXiv:2502.12394*. <https://arxiv.org/abs/2502.12394>.

</div>

<div id="ref-hart2026erdos330" class="csl-entry">

Hart, Allen Graham, and collaborators. 2026. “Formalization of Erdős
Problem \#330.” Lean 4 repository.
<https://github.com/AllenGrahamHart/FormalConjectures-Bench/tree/main/formalizations/erdos330>.

</div>

<div id="ref-holter2026fixed" class="csl-entry">

Holter, Adam. 2026a. “Fixed-Perimeter Conjecture 1.2: Generation,
Kill-Pass, Repair, and Exact Checks.” X thread and shared ChatGPT
conversation. <https://x.com/AdamHoltererer/status/2080264704530764033>.

</div>

<div id="ref-holter2026campaign" class="csl-entry">

———. 2026b. “Ten AI-Generated Conjecture-Resolution Candidates and
Adversarial Audits.” X thread and ten corrected public ChatGPT Pro share
links indexed in the task-level cohort table above.
<https://x.com/AdamHoltererer/status/2080340208990466385>.

</div>

<div id="ref-ju2026automated" class="csl-entry">

Ju, Haocheng, Guoxiong Gao, Jiedong Jiang, Bin Wu, Zeming Sun, et al.
2026. “Automated Conjecture Resolution with Formal Verification.” *arXiv
Preprint arXiv:2604.03789*. <https://arxiv.org/abs/2604.03789>.

</div>

<div id="ref-kung2026leap" class="csl-entry">

Kung, Po-Nien, Linfeng Song, Dawsen Hwang, Jinsung Yoon, Chun-Liang Li,
et al. 2026. “LEAP: Supercharging LLMs for Formal Mathematics with
Agentic Frameworks.” *arXiv Preprint arXiv:2606.03303*.
<https://arxiv.org/abs/2606.03303>.

</div>

<div id="ref-monticone2026thread" class="csl-entry">

Monticone, Pietro. 2026. “Human–GPT-5.4 Pro–Aristotle Collaboration on
Erdős Problem \#650.” X thread.
<https://x.com/PietroMonticone/status/2041344641707004043>.

</div>

<div id="ref-openai2026unitannouncement" class="csl-entry">

OpenAI. 2026a. “An OpenAI Model Has Disproved a Central Conjecture in
Discrete Geometry.” Research announcement, 20 May 2026.
<https://openai.com/index/model-disproves-discrete-geometry-conjecture/>.

</div>

<div id="ref-openai2026unitproof" class="csl-entry">

———. 2026b. “Planar Point Sets with Many Unit Distances.” Public proof
and reproduced original model response.
<https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/unit-distance-proof.pdf>.

</div>

<div id="ref-openai2026unittrace" class="csl-entry">

———. 2026c. “Rewritten Chain of Thought for the Solution to the Unit
Distance Problem.” 125-page rewritten research trace.
<https://cdn.openai.com/pdf/1625eff6-5ac1-40d8-b1db-5d5cf925de8b/unit-distance-cot.pdf>.

</div>

<div id="ref-rybin2026chat" class="csl-entry">

OpenAI ChatGPT shared conversation. 2026a. “Counterexample to Dinitz
Conjecture.” Shared conversation.
<https://chatgpt.com/share/6a60b2eb-0b64-83ee-9c76-7931ca1de063>.

</div>

<div id="ref-holter2026fixedchat" class="csl-entry">

———. 2026b. “Mathematical Conjecture Challenge.” Shared conversation.
<https://chatgpt.com/share/6a61ff8e-ad64-83ea-9c46-9c238d377044>.

</div>

<div id="ref-price2026thread" class="csl-entry">

Price, Liam. 2026. “Erdős Problem \#635: Initial Claim and Public
Correction.” X thread.
<https://x.com/Liam06972452/status/2017287960035516804>.

</div>

<div id="ref-rybin2026thread" class="csl-entry">

Rybin, Dmitry. 2026. “A GPT-5.6 Pro Counterexample to the
Dinitz–Garg–Goemans Conjecture.” X thread.
<https://x.com/DmitryRybin1/status/2079904005652893709>.

</div>

<div id="ref-sawin2026explicit" class="csl-entry">

Sawin, Will. 2026. “An Explicit Lower Bound for the Unit Distance
Problem.” *arXiv Preprint arXiv:2605.20579*.
<https://arxiv.org/abs/2605.20579>.

</div>

<div id="ref-sothanaphan2026erdos728" class="csl-entry">

Sothanaphan, Nat. 2026. “Resolution of Erdős Problem \#728: A Writeup of
Aristotle’s Lean Proof.” *arXiv Preprint arXiv:2601.07421*.
<https://arxiv.org/abs/2601.07421>.

</div>

<div id="ref-tsoukalas2026formalproofsearch" class="csl-entry">

Tsoukalas, George, Anton Kovsharov, Sergey Shirobokov, Anja Surina,
Moritz Firsching, et al. 2026. “Advancing Mathematics Research with
AI-Driven Formal Proof Search.” *arXiv Preprint arXiv:2605.22763*.
<https://arxiv.org/abs/2605.22763>.

</div>

<div id="ref-turturean2026thread" class="csl-entry">

Turturean, David. 2026. “Erdős Problem \#330: An AI-Assisted Discovery
and Formalization Process.” X thread.
<https://x.com/DavidTurturean/status/2053857666691199280>.

</div>

<div id="ref-wang2026repo" class="csl-entry">

Wang, Shouqiao. 2026a. “AI-Assisted Erdős Problem Artifacts.” GitHub
repository. <https://github.com/ShouqiaoW/erdos>.

</div>

<div id="ref-wang2026thread" class="csl-entry">

———. 2026b. “Six Erdős Problems in Five Days: Process Thread.” X thread.
<https://x.com/Qiaoqiao2001/status/2080003441821163958>.

</div>

<div id="ref-zoneraich2026thread" class="csl-entry">

Zoneraich, Jared. 2026a. “Devin Multi-Agent Workflow for Graffiti and
Regular-Supergraph Problems.” X thread.
<https://x.com/imjaredz/status/2080088341262033273>.

</div>

<div id="ref-zoneraich2026video" class="csl-entry">

———. 2026b. “Video Walkthrough of the Devin Mathematical-Discovery
Workflow.” X video thread.
<https://x.com/imjaredz/status/2080378963831005692>.

</div>

<div id="ref-peters2026kemeny" class="csl-entry">

Peters, Dominik. 2026a. “Kemeny Rank Aggregation Is NP-Hard for Three
Voters.” *arXiv Preprint arXiv:2607.25540*.
<https://arxiv.org/abs/2607.25540>.

</div>

<div id="ref-peters2026thread" class="csl-entry">

———. 2026b. “Discovery Process for the Three-Voter Kemeny Hardness
Reduction.” X thread, 30 July 2026.
<https://x.com/DominikPeters/status/2082487442582430013>.

</div>

<div id="ref-peters2026kemenylean" class="csl-entry">

———. 2026c. “KemenyHardnessLean: Formalized Hardness Reduction for
Kemeny Score with Three Voters.” GitHub repository.
<https://github.com/DominikPeters/KemenyHardnessLean>.

</div>

<div id="ref-peters2026hardnesslib" class="csl-entry">

———. 2026d. “HardnessReductionsLean: A Lean 4 Library of NP-Hardness
Reductions.” GitHub repository.
<https://github.com/DominikPeters/HardnessReductionsLean>.

</div>

<div id="ref-shao2024storm" class="csl-entry">

Shao, Yijia, Yucheng Jiang, Theodore Kanell, Peter Xu, Omar Khattab, and
Monica Lam. 2024. “Assisting in Writing Wikipedia-like Articles From
Scratch with Large Language Models.” In *Proceedings of NAACL 2024*,
6252–6278. <https://aclanthology.org/2024.naacl-long.347/>.
DOI: 10.18653/v1/2024.naacl-long.347.

</div>

<div id="ref-jiang2024costorm" class="csl-entry">

Jiang, Yucheng, Yijia Shao, Dekun Ma, Sina Semnani, and Monica Lam. 2024.
“Into the Unknown Unknowns: Engaged Human Learning through Participation
in Language Model Agent Conversations.” In *Proceedings of EMNLP 2024*,
9917–9955. <https://aclanthology.org/2024.emnlp-main.554/>.
DOI: 10.18653/v1/2024.emnlp-main.554.

</div>

<div id="ref-stanfordoval2026storm" class="csl-entry">

Stanford Open Virtual Assistant Lab. 2026. “STORM: Synthesis of Topic
Outlines through Retrieval and Multi-perspective Question Asking.” GitHub
repository, inspected 1 August 2026. `knowledge-storm` v1.1.0; MIT
License. <https://github.com/stanford-oval/storm>.

</div>

<div id="ref-loopx2026" class="csl-entry">

Huang, Ruiteng, and LoopX contributors. 2026. “LoopX: The Local Control
Plane for Long-Running AI Agent Work.” GitHub repository and architecture
documentation, accessed 3 August 2026.
<https://github.com/huangruiteng/loopx>.

</div>

<div id="ref-openai2026tenadvances" class="csl-entry">

OpenAI. 2026d. “Ten Advances in Mathematics and Theoretical Computer
Science.” Publication, 1 August 2026.
<https://openai.com/index/ten-advances-in-mathematics/>.

</div>

<div id="ref-openai2026tenproofspaper" class="csl-entry">

———. 2026e. *Ten Advances in Mathematics and Theoretical Computer
Science*. 249-page public manuscript.
<https://cdn.openai.com/pdf/ten-proofs-oai.pdf>.

</div>

<div id="ref-openai2026walkthroughs" class="csl-entry">

———. 2026f. *How the Ideas Came Together*. 62-page model-written
reconstruction based on original chains of thought and the resulting papers
and writeups.
<https://cdn.openai.com/pdf/reasoning-walkthroughs.pdf>.

</div>

<div id="ref-openai2026tenproofsrepo" class="csl-entry">

———. 2026g. “ten-proofs: Lean Certificates Accompanying Proofs in
Mathematics and Theoretical Computer Science.” GitHub repository. Current
`main` inspected at zero-parent root commit
`94bc0feb6a9ff12c7d31d6de640a725c9d43d2b6`, 3 August 2026; prior audit
snapshot `29362184c2b698c1b279bc85b3957ee813646c63`, 1 August 2026.
Apache-2.0. <https://github.com/openai/ten-proofs>.

</div>

<div id="ref-leanfro2026comparator" class="csl-entry">

Lean FRO. 2026. “Comparator: A Trustworthy Judge for Lean Proofs.” GitHub
repository, inspected 1 August 2026.
<https://github.com/leanprover/comparator>.

</div>

<div id="ref-openai2026formalization" class="csl-entry">

OpenAI. 2026h. “formalization.yaml.” In *ten-proofs*, version `v0.3`,
inspected at the current root commit on 3 August 2026.
<https://github.com/openai/ten-proofs/blob/main/formalization.yaml>.

</div>

<div id="ref-leiden2026" class="csl-entry">

Leiden Declaration on AI and Mathematics. 2026. “Leiden Declaration on AI
and Mathematics.” <https://leidendeclaration.ai/>.

</div>

</div>
