---
version: "0.5"
revision_date: "2026-07-25"
abstract: |
  Public reports of frontier language models resolving or refuting open
  mathematical problems increased sharply in 2026, but the underlying
  evidence is heterogeneous: an X thread, a shared conversation, an
  executable checker, a compiled Lean theorem, an expert review, and a
  later human proof establish different things. We freeze publicly
  visible evidence through 25 July 2026 and audit twelve workflow
  episodes covering more than twenty mathematical targets. The unit of
  analysis is a research episode rather than an announcement object; a
  high-throughput campaign may contain nested task-level subepisodes. Each
  episode is coded along six dimensions: process provenance, artifact
  availability, deterministic verification, independent review, novelty,
  and autonomy or attribution, together with a conservative lower-bound
  tier for publicly visible human labor.

  The corpus does not estimate a population-level success rate and does
  not independently re-prove every mathematical claim. It supports a
  narrower process conclusion: credible AI-assisted discovery is
  increasingly a system property of target selection, goal binding,
  search topology, persistent state, adversarial falsification,
  formalization, repair, human semantic judgment, and post-solution
  maturation. We organize the cases with two orthogonal views: nine
  workflow components and four operational configurations, from
  minimal/direct sessions to orchestrated formal pipelines. Four recurrent
  mechanisms become testable hypotheses—certificate asymmetry,
  destructive critique, verifier-driven repair, and compute headroom
  coupled to persistent state—while eight recurrent failure modes delimit
  the evidence. Mathematics is an unusually observable proving ground;
  transfer to industrial research additionally requires validated
  physical models, manufacturability, qualified test systems,
  configuration control, and field feedback.
author:
- |
  Tengjiao Liu  
  psi.run  
  `psi@psi.run`
bibliography: references.bib
date: "Version 0.6 – Evidence snapshot: 25 July 2026"
title: |
  **From Prompt to Proof: The Anatomy of AI-Assisted Mathematical
  Discovery in 2026**  
  An Evidence-Audited Case Series of Workflows, Failure Modes,
  Formalizer Repair, and Research Engineering
---

> **Draft status:** arXiv-oriented Version 0.6. This revision does not
> overwrite Versions 0.1–0.4. Public evidence is frozen as of 25 July
> 2026; unavailable threads, non-public sessions, and unreviewed claims
> are marked rather than reconstructed.

# Introduction

In 2026, public AI-mathematics reports changed from isolated answers into
visible research processes. The most informative episodes now expose
problem screening, contract-like target specification, parallel or
long-running search, explicit attempts to destroy a proof, compiler- or
checker-driven repair, human reconstruction of ambiguous statements,
and later correction or strengthening. At the same time, the public
record became harder to interpret. A root post, a shared chat, a GitHub
repository, a successful Lean build, and a human-written proof are not
interchangeable forms of evidence.

This paper studies that evidential and engineering gap. It does not ask
only which theorem was announced. It asks how a candidate result was
selected, produced, attacked, repaired, checked, attributed, and matured;
what remained unavailable; and which conclusions are warranted by each
artifact. The corpus consists of twelve public workflow episodes,
including two campaigns with multiple nested targets, four Erdős problem
formalization episodes, a verifier-repair episode, the unit-distance
research trace and its later maturation, two minimal-prompt or finite-
certificate cases, a Devin-orchestrated pipeline, and a newly documented
candidate resolution of Erdős Problem #477.

Four questions organize the study:

1. Which workflow components recur across independently organized
   AI-mathematics episodes?
2. Where do substantive errors enter, and which mechanisms remove or
   merely relocate them?
3. How is labor divided among language models, proof assistants, exact
   programs, human mathematicians, and public reviewers?
4. Which observations plausibly transfer to scientific and industrial
   research, and which depend on mathematics-specific affordances?

Our central claim is deliberately narrower than “AI can solve open
mathematics”:

> **In the most credible public cases, AI-assisted mathematical discovery
> is a property of a research system—not of a base model or prompt in
> isolation.**

The system includes target selection, semantic binding, search budget,
state continuity, adversarial review, deterministic verification, repair
lineage, human intervention, and an external maturation pipeline.

Figure 1 in the cross-case synthesis maps the operational
configuration of each episode against the strongest visible public
evidence tier. The axes are deliberately orthogonal: a compact finite
counterexample from an O1 session may be more auditable than an O4
pipeline whose repository, formal target, or build cannot be pinned.
Conversely, an elaborate workflow may be methodologically informative
while remaining evidentially immature.

## Contributions

This paper makes five contributions.

1. It reconstructs twelve public workflow episodes covering more than
   twenty mathematical targets using a six-dimensional evidence card.
2. It introduces two orthogonal descriptive views: nine workflow
   components and a map from four operational configurations to the
   strongest visible public evidence tier.
3. It adds conservative lower-bound coding of visible human labor, making
   hidden curation and maturation work harder to erase behind a global
   “fully autonomous” label.
4. It identifies four mechanisms that can be tested in controlled,
   equal-budget studies and eight recurrent failure modes with concrete
   controls, and instantiates a machine-readable JSON evidence ledger.
5. It separates mathematics-specific verification advantages from
   domain-general research-engineering principles and states the
   additional conditions required for industrial transfer.

## Claim boundaries and threats to validity

The paper does **not** claim a success rate for frontier models, a causal
advantage for long inference or any prompt class, independent validation
of every theorem, novelty of every reported result, or full autonomy of
any episode. The sample is selected for public process visibility and is
therefore affected by survivor and disclosure bias. Several X threads,
shared conversations, reports, and videos were only partially
recoverable. Coding in Version 0.6 is by one analyst. Public links are
mutable. Human-labor tiers are lower bounds on visible effort rather than
estimates of total labor, and they exclude model wall-clock time. These
limitations are part of the method, not footnotes to be ignored.

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

Those projects are controlled benchmarks, system evaluations, or formal
proof-search studies. The present work is a **wild observational case
series**: independently organized episodes whose evidence is distributed
across social-media reply chains, shared conversations, manuscripts,
repositories, corrections, community problem pages, and later human
papers. Its contribution is process forensics and comparative workflow
analysis, not a leaderboard.

# Method

## Corpus and case selection

Episodes were included when at least two of the following were visible:
a continuation thread, a public conversation or prompt, a manuscript or
technical report, code or a proof-assistant artifact, an explicit repair
or correction, an external review, or an unusually detailed route
history. Table 1 summarizes the twelve episode-level units. “Reported”
means that the process fact is author-reported but the full underlying
artifact was not independently captured.

**Visible human-labor tiers.** `L0` denotes minimal visible
intervention (typically no more than a short prompt/start-and-release
sequence); `L1` denotes bounded curation, cleanup, checking, or
single-researcher coordination; `L2` denotes sustained multi-day or team
work involving reconstruction, formalization, or maturation; `L?` means
that public evidence is insufficient. These are conservative lower
bounds on *visible* human effort, not total labor estimates, and they
exclude model runtime.

**Table 1. Core workflow episodes, visible human labor, and strongest
public evidence.**

| ID | Episode and target | Model or system | Human labor | Material human role | Strongest visible verification or review | Status at snapshot |
|---|---|---|:---:|---|---|---|
| **C1** | Shouqiao Wang, six Erdős targets | GPT-5.6 Sol, Codex, selected Lean | **L2** | Problem filtering, contract design, publication and correction | Several manuscripts and Lean/CI artifacts | Uneven; one scope downgrade; no campaign success-rate claim |
| **C2** | Adam Holter, ten-candidate campaign | GPT-5.6 Pro, same-model audits | **L?** | Campaign selection, redirection, release labeling | Ten public Pro share links; selected exact checks | Unrefereed nested cohort; correlated audit |
| **C3** | David Turturean et al., Erdős #330 | ChatGPT-5.5 Pro, scaffold, Lean | **L1** | Semantic choices, scaffold, formalization and exposition | Public Lean package and community PROVED (LEAN) state | Strong formal path; full chat unavailable |
| **C4** | Liam Price et al., Erdős #635 | GPT-5.2 Pro, Aristotle | **L1** | Cleanup, expert review, public correction | Lean artifact for one subproblem; public downgrade | Partial result; first subproblem open |
| **C5** | Pietro Monticone et al., Erdős #650 | GPT-5.4 Pro, Aristotle, Lean | **L2** | Problem framing, formal-proof interpretation, human paper | Lean proof and human-written arXiv paper | Solved support path; original prose step replaced |
| **C6** | Acer et al., Erdős #728 | GPT-5.2 Pro, Aristotle | **L2** | Target reconstruction, steering, prior-art review, humanization | Lean proof, human writeup, community discussion | Valid target required reconstruction; novelty nuanced |
| **C7** | Adam Holter, fixed-perimeter Conjecture 1.2 | GPT-5.6 Pro, exact Python checker | **L1** | Prompting, artifact release, checker inspection, external challenge | Kill-pass, repaired proof, millions of finite checks | Candidate; no kernel proof; checker required hardening |
| **C8** | OpenAI unit-distance disproof | Internal model, AI grading, human editors | **L2** | Internal review, external digestion, strengthening | Public proof, rewritten trace, nine-author human proof, explicit strengthening | Strong theorem-level evidence; trace not raw-complete |
| **C9** | Dmitry Rybin, Dinitz–Garg–Goemans counterexample | GPT-5.6 Pro | **L2** | Weeks of prior thought, problem choice, interpretation and release | Concrete finite graph and independent checking reported | Strong certificate form; full chat/verifier incompletely captured |
| **C10** | Anirudh Chakravarthy, two minimal-prompt targets | GPT-5.6 Sol Pro | **L0** | Minimal prompt and publication | Technical reports reported | Process-rich hypothesis, limited captured verification |
| **C11** | Jared Zoneraich/Devin, Graffiti and regular-supergraph targets | Devin, Fable, GPT-5.6 Sol, Lean | **L?** | Workflow initiation and public demonstration | Repository/video and no-`sorry` Lean builds reported | Target-to-build mapping not fully reconstructed |
| **C12** | Patrick White/MathDyad, Erdős #477 | GPT-5.6 Sol construction and attacks; Claude source checks | **L1** | Prompt orchestration, source pinning, repository curation and triage | Same-family reruns, adversarial passes, cross-model source spot checks | Candidate proof only; no human number theorist or Lean proof |

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
path.

Features are coded as clearly observed, partially visible or
author-reported, or not established. Absence of public evidence is not
coded as evidence of absence.

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

## Source collection, archival, and missing evidence

Each social-media thread was treated as an event stream: root post,
author replies, linked conversations, attachments, repositories,
corrections, and current problem-page status. The evidence snapshot is
25 July 2026. Source URLs and captured artifacts are stored in a
content-addressed local case library with per-file SHA-256 manifests.
Mutable pages are tagged as full capture, partial capture, or URL-only.
A public immutable deposit is required before arXiv v1; until then the
manuscript does not claim that inaccessible sessions have been fully
archived.

The newly added Erdős #477 repository is pinned to commit `8440d59`
(23 July 2026). Its public record is unusually explicit about what was
and was not checked, but the complete model sessions are not public and
the repository itself states that no working number theorist or Lean
proof has yet reviewed the claim (White and Claude 2026).

## No success-rate claim

Public campaigns are selected after the fact. Problem age, ambiguity,
certificate cost, and publication incentives alter which episodes are
visible. We therefore report no population-level success percentage. A
future benchmark should disclose a preregistered target set and compute

$$
\mathrm{SR}(\tau)=
\frac{\#\{\text{all preregistered episodes satisfying evidence threshold }\tau\}}
{\#\{\text{all preregistered attempted episodes}\}},
$$

with the threshold, duplicate policy, withdrawals, and failed attempts
specified before evaluation.

# Case Reconstructions

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

## C5. The formalizer as co-author: when Aristotle rewrites the proof

The Erdős #650 collaboration combined human mathematicians, GPT-5.4 Pro,
and Aristotle. The final exact result was published in a human-written
arXiv paper with Lean source (Monticone 2026; Doorn, Li, and Tang 2026;
Doorn and collaborators 2026).

The decisive process fact is that the informal proof contained a
structural gap. Aristotle did not merely translate it into Lean. The
formalizer found a different injection that repaired or replaced the
invalid step, and the human collaborators recovered that new argument
from the formal artifact. Two propositions must therefore remain
separate: the exact formal theorem was accepted in the declared Lean
environment; the original prose proof was verified unchanged. The
visible evidence supports the first and rejects the second.

This is the corpus’s clearest challenge to the “proof assistant as final
checker” metaphor. When a formalizer changes the support path, it becomes
a research contributor and should receive granular credit. The same
pattern can recur outside mathematics whenever a compiler, synthesizer,
optimizer, or simulator changes a design rather than merely validating
one.

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

## C7. Adversarial self-repair and checker hardening: fixed-perimeter Conjecture 1.2

Holter’s first prompt asked GPT-5.6 Pro to choose and finish a real open
conjecture. A second instruction asked it to “kill” the proof and, if it
survived, make it airtight (Holter 2026a; OpenAI ChatGPT shared
conversation 2026b). The model found a genuine asymptotic defect,
replaced the affected step, and produced an exact-checking bundle over
millions of finite instances. The target came from fixed-perimeter
partition identities (Gray et al. 2025).

The audit changed the support path. The repaired candidate may gain
evidence; the original “complete proof” cannot inherit that status. A
reproducible record should therefore store the defect, affected claims,
pre- and post-repair artifacts, replacement argument, and rerun evidence.

The checker itself also required audit. During source review, optimized
Python execution could remove proof-critical `assert` statements while
allowing a success message to print. The episode thus links mathematical
repair to verifier engineering: exact arithmetic and 7.3 million checks
are meaningful only if failure is fail-closed, executed checks are
manifested, negative mutations fail as expected, and the checker’s finite
scope is not inflated into an unbounded theorem.

## C8. Route replacement, not local patch: the unit-distance episode

OpenAI’s unit-distance episode has the richest public maturation chain in
the corpus. An internal general-purpose model produced a disproof of the
$n^{1+o(1)}$ conjectural scale; OpenAI released the proof and a 125-page
document explicitly labeled a rewritten research trace (OpenAI 2026a,
2026b, 2026c). Nine mathematicians later published a shorter human-
digested proof, and Sawin obtained an explicit exponent exceeding 1.014
(Alon et al. 2026; Sawin 2026).

The theorem-level evidence is strong. The trace has a different status:
it is detailed but not established as a raw, complete chronological log.
Its value is process visibility. It records quantifier calibration,
repeated negative tests, preserved cost constraints, and a decisive
upstream replacement.

**Reconstructed route timeline:**

```text
incidence / Fourier / additive-combinatorial routes
    → number-field and relative-unit constructions
    → almost-totally-real route rejected (height and lattice-shape costs)
    → CM sign-ideal and cut-and-project kernel retained
    → cyclic-cubic pro-3 tower replaces the upstream existence mechanism
    → human re-derivation, compression, and explicit strengthening
```

The key methodological event was **route replacement rather than local
patch**. The arithmetic engine changed, while a downstream geometric and
Minkowski-window kernel was retained and revalidated. Failed routes also
left reusable constraints instead of disappearing. The episode therefore
shows why negative knowledge, support-path lineage, and post-solution
maturation are first-class research artifacts.

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
The full shared-chat body, public verifier, and mature paper were not all
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
captured for Version 0.4, so the outcomes remain author-reported in this
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

## C12. Transparent candidate proof with bounded review: Patrick White, GPT-5.6 Sol, and Claude on Erdős #477

The `pw/erdos477-cubic` repository claims that every integer power
$K\ge 3$ has a tiling complement, which would answer Erdős Problem #477
affirmatively (White and Claude 2026). The construction is attributed to
GPT-5.6 Sol. Two same-family runs produced cubic proofs with different
case splits; fresh GPT-5.6 sessions were then instructed to refute the
argument. Claude’s role was narrower but valuable: checking primary
source statements, re-deriving selected elementary steps, recomputing
exponents, and helping document corrections.

The repository records real defect discovery. One citation/indexing
detail was corrected, and a second adversarial round found an incorrect
even-$K$ genus-drop formula. The authors triaged the latter as
non-load-bearing because the main theorem used absolute irreducibility,
not the erroneous genus calculation. This is unusually good process
provenance for an unreviewed candidate.

The evidence ceiling is equally explicit. The full model sessions are
not public; construction and adversarial attack share the same model
family; Claude did not conduct a complete independent proof review; no
Lean proof or working number theorist has validated the claim; and the
Erdős problem page remained OPEN at the snapshot date (Erdős Problems
community 2026e). The repository also identifies a source-binding hazard:
the natural-language problem ranges over $k\in\mathbb Z$, while one
Formal Conjectures encoding uses only positive inputs. This episode is
valuable precisely as an evidence-rich **candidate-proof and audit
trail**, not as a settled “Claude solution.”

# Cross-Case Synthesis

## Nine workflow components

The cases are better described by component vectors than by mutually
exclusive paradigms.

| Code | Component | Operational question |
|---|---|---|
| **P** | Problem portfolio management | How are targets screened for importance, tractability, ambiguity, prior art, and certificate cost? |
| **G** | Goal binding and specification | Are definitions, quantifiers, claim atoms, and forbidden shortcuts explicit? |
| **T** | Search topology | Is search sequential, parallel, batch, or controller-mediated? |
| **M** | State and trajectory management | Are failed routes, obligations, prior attempts, and negative knowledge preserved? |
| **F** | Falsification topology | Who or what tries to refute the candidate, and how independent is that path? |
| **V** | Formal or executable verification | What exact theorem or finite domain is checked, in which environment? |
| **R** | Repair semantics | Was the proof transcribed, completed, locally repaired, replaced, or retargeted? |
| **H** | Human semantic and domain intervention | Where did humans select, steer, bind, interpret, or approve? |
| **E** | External maturation | Was there prior-art adjudication, independent re-derivation, correction, simplification, or strengthening? |

## Four operational configurations

Operational scale is orthogonal to evidence maturity.

| Level | Configuration | Distinguishing feature | Illustrative cases |
|---|---|---|---|
| **O1 — Minimal/direct** | One prompt or one visible session | Target discovery or finite certificate inside one interaction | C9, C10 |
| **O2 — Self-adversarial** | Generate, then explicitly attack the candidate | Local objective switches from completion to defect discovery | C2, C7, C12 |
| **O3 — Scaffolded extended** | Contracted target, persistent state, multiple routes or long run | Search management and route memory become explicit | C1, C4, C6, C8 |
| **O4 — Orchestrated formal** | Controller or specialist pipeline with formalization/checking | Artifacts move through generation, critique, formalization, and release stages | C3, C5, C11 |

## Two-axis map: operational complexity versus public evidence

![Figure 1. Operational configuration (O1–O4) versus strongest visible public evidence tier (E0–E5).](operational_evidence_map_v0.5.png)

**Figure 1. Operational configuration versus strongest visible public
evidence tier.** Vertical bars show cases whose accessible support paths
span a tier range or are uneven across nested claims. Small horizontal
offsets are only for label readability. The y-axis uses the artifact-
access ladder in Appendix A; it is not a scalar truth score. The map
makes the central non-implication visible: organizational complexity
does not guarantee evidential maturity. C8 reaches E5 at O3, whereas the
reported O4 Devin pipeline remains E2–E3 until a repository, exact formal
targets, and clean builds are pinned. Conversely, C9 illustrates how a
compact finite certificate can approach E3 within an O1 workflow.


## Workflow fingerprints

**Table 2. Visible workflow components.** `[Y]` = clearly present in
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

## Common lifecycle

```text
Select and screen target
    → Bind source, definitions, quantifiers, and claim atoms
    → Generate non-equivalent routes
    → Preserve state, obligations, failures, and duplicate fingerprints
    → Falsify with counterexamples, destructive critique, or exact tests
    → Repair locally or replace an upstream route
    → Formalize or check the exact claimed domain
    → Seek independent review and prior-art adjudication
    → Publish, correct, simplify, strengthen, or reopen
```

The loop is more informative than “prompt → answer.” Formalization,
source checking, or expert review may reopen goal binding and proof
search instead of merely approving the current artifact.

# Four Testable Mechanisms

The corpus is observational. The following mechanisms are therefore
stated as hypotheses with concrete experimental designs rather than as
causal conclusions.

| Mechanism | Observed signal | Equal-budget controlled test | Primary outcomes |
|---|---|---|---|
| **Certificate asymmetry** | Finite graph/certificate cases are often cheaper to audit than universal proofs | Hold model and budget fixed; randomize whether the workflow estimates verification cost before target selection | Independently checkable-result rate, human review time, false-complete rate, certificate size |
| **Destructive critique** | “Kill the proof” prompts find real defects in C2, C7, and C12 | Compare generic polish, same-model destructive critique, and different-lineage critique on the same candidate proofs | Fatal-gap recall, valid-repair rate, residual false-complete rate, correlation-adjusted review value |
| **Verifier-driven repair** | Lean, Aristotle, or exact checkers expose gaps and can change the accepted argument | Compare prose-only review, exact checker feedback, and formalizer feedback with frozen source targets | Gap detection, repair success, target fidelity, proportion of repaired versus replaced arguments |
| **Compute headroom plus persistent state** | Long/parallel search is useful when failed routes and obligations survive | Equalize total tokens/tool time; compare stateless retries with structured trajectory memory and reserved verification capacity | Verified yield, duplicate-route rate, reopened obligations, verification debt, useful negative knowledge |

The first mechanism is a property of the task and evidence structure, not
an unsupported theory of language-model internals. The second separates
cheap internal filtering from independent review. The third requires a
formalizer delta when the proof changes. The fourth predicts that elapsed
time alone is insufficient: additional generation without memory and
verification can increase backlog rather than knowledge.

# Failure Modes and Controls

**Table 3. Recurrent failure modes, observations, and controls.**

| Failure mode | Observed manifestation | Control | Where visible |
|---|---|---|---|
| **Forced resolution** | “Full solution only” wording pressures partial evidence toward closure | Separate aggressive search persistence from outcome-neutral claim disposition | C1, C4, C7, C10 |
| **Target or scope drift** | One subproblem, variant, or positive-only formalization is mistaken for the source claim | Independent source reconstruction; claim atoms; formal-to-natural round trip | C3, C4, C6, C12 |
| **Correlated self-audit** | Same model family generates and attacks a proof, sharing the same citations and blind spots | Different-lineage critic, deterministic evidence, blinded expert review | C2, C7, C12 |
| **Formalization laundering** | Kernel acceptance is described as verification of the original prose or source problem | Exact theorem binding, axiom audit, formalizer delta, granular attribution | C3, C5, C6, C11 |
| **Verifier execution gap** | Assertions, timeouts, dead branches, or unconditional success messages prevent critical checks from running | Fail-closed logic, executed-check manifest, negative mutations, environment capture | C7 |
| **Missing attempt denominator** | Public successes omit abandoned, duplicated, or unpublished attempts | Preregistered target set, all-attempt ledger, fixed evidence threshold | C1, C2, C10, C11 |
| **Prior-art drift or rediscovery** | A valid argument is later found to be known, related, or differently scoped | Time-stamped search dossier; separate theorem, proof, method, and operational novelty | C1, C2, C6, large Erdős scans |
| **Route and narrative amnesia** | Failed routes repeat; repaired or replaced proofs are retold as smooth unchanged derivations | Global claim registry, obligation reopening, repair lineage, narrative-compression audit | C2, C5, C8, C12 |

The fixed-perimeter case yields a concrete verifier lesson:

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

# Cross-Case Findings

## Credibility accumulates through pipelines, not prompts

Minimal prompting can produce valuable finite certificates, but the
strongest public evidence states involve additional machinery: semantic
binding, exact verification, correction, human re-derivation, or external
strengthening. Prompt simplicity and research-system simplicity are not
the same.

## Human labor is redistributed, not removed

The lower-bound coding in Table 1 assigns one episode to `L0`, four to
`L1`, five to `L2`, and leaves two as `L?`. These counts are not estimates
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

## Verification economics shapes apparent capability

Models may appear unusually strong on targets with compact falsifying
certificates. Comparative studies should stratify by certificate cost,
not only by field, age, or perceived difficulty.

## Formalization is a discovery operator

C5 is the clearest case, but the pattern is broader: compiler feedback
can force definitions, locate unsupported assumptions, and synthesize a
replacement argument. The accepted proof and the original prose may be
different support paths.

## Negative knowledge is reusable capital

C8 shows that a rejected route can reveal the exact denominator,
embedding, or uniformity cost that a successor must pay. C12 records a
non-load-bearing bug rather than hiding it. Bare rejection destroys this
capital; productive veto preserves failure witness, scope, salvageable
kernel, and reactivation conditions.

## Claim status is temporal and vector-valued

A result can be correct but not novel; formally checked but poorly bound;
autonomous at generation but dependent on human target choice; or
publicly discussed while still awaiting expert review. “Solved” is a
presentation shorthand, not an adequate stored state.

# What Transfers Beyond Mathematics?

## Likely domain-general invariants

Several mechanisms do not depend on theorem proving:

- preserve the original objective while allowing explicit reformulation;
- maintain non-equivalent architecture or hypothesis routes;
- separate proposer, adversary, verifier, and release authority;
- preserve negative knowledge and reopen invalidated obligations;
- record when a tool repairs or replaces a human/model proposal;
- version every claim, artifact, review, and configuration;
- distinguish internal exploration from externally consequential release.

These principles plausibly apply to chip design, aerospace, chemistry,
software engineering, and other long-horizon technical work.

## Mathematics-specific affordances

Mathematics supplies two unusually strong advantages. First, one finite
counterexample can decisively refute a universal statement. Second, a
small trusted proof kernel can validate an exact formal theorem. Neither
advantage automatically exists in engineering, where models are
approximate, measurements are uncertain, and field behavior may differ
from simulation.

## Additional requirements for industrial research systems

| Requirement beyond mathematical proof | Engineering question |
|---|---|
| **Model credibility** | Which physical regimes, simplifications, calibrations, and uncertainty bounds justify a simulation or surrogate? |
| **Manufacturability and supply** | Can the design be fabricated, inspected, sourced, assembled, repaired, and produced at acceptable yield? |
| **Qualified test systems** | Can the rig, sensor, benchmark, compiler, or metrology chain reliably make a bad design fail? |
| **Configuration control** | Which requirement, CAD, material, software, process, and test versions support the released claim? |
| **Field feedback** | Do telemetry, degradation, maintenance, incidents, and operator observations update the model and next design generation? |

Mathematics is therefore a high-observability test bed for search,
falsification, repair, and evidence maturation—not a complete validation
of an autonomous industrial “super-machine.”

# A Practical Reporting Standard

Future AI-mathematics reports should publish a compact **Research Episode
Dossier** containing:

1. exact source problem, version, and interpretation;
2. prompts and system instructions that can be disclosed;
3. model identifier, settings, tools, and corpus/network policy;
4. full attempt denominator, or an explicit statement that it is absent;
5. branch structure, model runtime, token/tool budget, and human
   interventions with active-time or labor-tier evidence kept separate;
6. candidate, repaired, and released artifact hashes;
7. exact formal theorem or checker-to-claim binding;
8. build command, environment lock, placeholder/axiom policy, and
   executed-check manifest;
9. reviewer lineage and review scope;
10. time-stamped prior-art queries and novelty decomposition;
11. corrections, retractions, simplifications, and strengthening;
12. a human-readable claim card covering all six evidence dimensions.

This reporting standard does not require private chain-of-thought.
Structured events—candidate, test, defect, repair, replacement,
verification, and release—are sufficient for process analysis.

# Data and Materials Availability

Version 0.6 is accompanied by a machine-readable companion package:

- `evidence_ledger_2026_v0.1.json`, containing the twelve episode records,
  O1–O4 configuration, E0–E5 access range, visible human-labor tier,
  workflow-component fingerprint, six evidence dimensions, source URLs,
  snapshot hashes, current status, and open gaps;
- `evidence_ledger_2026_schema_v0.1.json`, a JSON Schema 2020-12 contract
  for community extensions and validation;
- `operational_evidence_map_v0.5.svg` and `.png`, the source figure used
  in Figure 1; and
- the versioned local evidence library containing source registries,
  capture states, content hashes, episode cards, the Holter nested cohort,
  and immutable manuscript versions.

The JSON ledger validates against the supplied schema. It is a living
observational ledger, not a benchmark leaderboard: corrections append or
revise time-stamped records rather than silently overwriting history. A
public Zenodo and GitHub deposit with a persistent DOI, release tag, and
SHA-256 manifest is planned before arXiv v1. This draft deliberately does
not invent a repository URL or DOI before that deposit exists. Until the
deposit is complete, mutable X and ChatGPT links are not represented as
durably archived.

# Limitations

This version has six major limitations. First, the corpus is selected
from public successes and unusually transparent authors. Second, social-
media and shared-chat evidence is mutable and sometimes inaccessible.
Third, we did not independently re-prove every result or rebuild every
Lean repository. Fourth, novelty, autonomy, and total human labor remain difficult to
infer from public artifacts; the labor tiers are lower-bound visibility
codes only. Fifth, coding is currently single-analyst; a publishable
empirical dataset should use a preregistered manual and at least two
independent coders. Sixth, the industrial implications are structural
hypotheses, not validated transfers.

The next empirical step is not merely more success stories. It is a
stratified corpus containing successes, partial results, retractions,
prior-art rediscoveries, failed long runs, formal-target mismatches, and
unverifiable claims. The next causal step is an equal-budget experiment
comparing minimal prompting, contract specification, parallel search,
same-model destructive critique, independent critique, formal feedback,
and persistent trajectory memory on a frozen target set.

# Conclusion

The 2026 case series marks a transition from isolated model answers to
engineered research workflows. Operational complexity ranges from one-
chat counterexamples to orchestrated formal pipelines, but complexity
alone does not determine credibility. The most defensible episodes
combine target binding, search management, falsification, exact checking
or formalization, repair, human semantic judgment, and external
maturation.

The cases also expose a consistent set of hazards. Outcome mandates can
inflate scope; same-model review can manufacture correlated confidence;
formalization can certify the wrong target or silently replace the
argument; an exact checker can skip critical checks; a published success
can hide its denominator; and prior art can change novelty without
changing truth. These are not reasons to dismiss AI-assisted discovery.
They are the engineering requirements of making it trustworthy.

The strongest conclusion is therefore neither celebratory nor
dismissive: **credible AI-assisted discovery is a system property.** A
reliable research machine must preserve goals, diversify routes, retain
negative knowledge, reserve capacity for attack and verification, bind
claims to exact artifacts, record material repairs, and mature outputs
through independent scrutiny. Mathematics makes these requirements
unusually visible. Whether they can support reliable scientific and
industrial discovery remains an empirical question, but it is now a
question that can be measured.

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

**Table 4. Evidence state as of 25 July 2026.**

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
| C9 Rybin | E2/E3, reported | Thread, replies, shared link, prior human context | Concrete counterexample and independent computation reported | Full chat, public verifier, mature paper |
| C10 Chakravarthy | E1/E2, reported | Minimal prompt and announcements | Technical reports reported | Reports, full thread, independent review |
| C11 Devin | E2/E3, reported | Root and video posts; local metadata snapshot SHA-256 `cb7a…752b8` | No-placeholder Lean and adversarial checks reported | Stable repository/commit, theorem-to-build map, clean rebuild, independent adjudication |
| C12 #477 | E2 | Repository, commit history, explicit verification notes | Same-family reruns and adversarial passes; Claude primary-source spot checks | Public sessions, full independent proof review, Lean, human number theorist, novelty adjudication |

# Appendix D. Proposed Coding Fields for an Expanded Corpus

An expanded 30–50 episode dataset should record: episode identifier;
source problem and age; mathematical field; finite versus asymptotic
target; proof versus counterexample; model and tool stack; prompt class;
problem-selection mechanism; branch count; wall-clock and aggregate
inference; memory mechanism; verifier class; source-to-formal binding;
repair count and magnitude; visible human-labor tier, reported active
time, and intervention by stage; reviewer lineage; artifact hashes;
prior-art state; correction history; final
six-dimensional evidence vector; and whether every attempted target is
included.

# Appendix E. Machine-Readable Evidence Ledger

The companion JSON package is designed for extension without collapsing
evidence into one score. A minimal episode object has the following
shape:

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
  "evidence_dimensions": {
    "process_provenance": "partial",
    "artifact_availability": "clear",
    "deterministic_verification": "partial",
    "independent_review": "clear",
    "novelty_and_prior_art": "clear",
    "autonomy_and_attribution": "partial"
  },
  "status_as_of": "2026-07-25",
  "source_urls": [],
  "snapshot_hashes": [],
  "open_gaps": []
}
```

The full schema constrains identifiers, coding vocabularies, access-tier
ranges, labor-tier uncertainty, component states, source URLs, and
SHA-256 records. Community contributions should preserve the episode/
subepisode distinction, attach an `as_of` date, and record missing
evidence rather than inferring it.

# References


<div id="refs" class="references csl-bib-body hanging-indent"
entry-spacing="0">


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

</div>
