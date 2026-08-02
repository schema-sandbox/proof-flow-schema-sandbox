# SchemaMath Research Packet: Demo: unresolved combinatorial exploration

Generated: 2026-07-30T08:18:37.582257+00:00

## Purpose
Generate non-equivalent next moves without forcing a solution.

## Original Problem (immutable source record)
Given a finite family of subsets with a specified intersection pattern, determine whether a stronger extremal bound should hold.

### Researcher Notes
Synthetic prompt. The goal is to test the research sandbox, not to claim a theorem.

### Definitions
- A route is a mechanism-level line of attack.

### Assumptions
- No completeness claim is required.

## Open Challenges
- [OPEN] route=c70795b6-1e94-4eb9-b736-4ce9da3a2501 branch=48d85869-b0f8-4c5d-9ad3-3bdba7e2db40 The candidate inequality may fail for the empty family. Test: Include empty and singleton families in the exact enumeration.
- [OPEN] route=76800db7-7e56-4dc4-9ee6-006aa40c80c6 Objection: the empty family makes the normalization undefined; test the boundary separately. Test: Check empty and singleton families.

## Research Routes

### Small-case counterexample search [ACTIVE]
Enumerate small structures and look for a minimal obstruction.

Branches:
- Enumerate n <= 10 [ACTIVE]: A bounded branch used to expose parity and boundary effects.

Challenges:
- [OPEN] The candidate inequality may fail for the empty family. Test: Include empty and singleton families in the exact enumeration.

### Compression / entropy route [DORMANT]
Try to encode the family and derive an information inequality.

Branches:
- Signed incidence vector [SEED]: Alternative approach: define a signed incidence vector and compare its squared norm.

Challenges:
- [OPEN] Objection: the empty family makes the normalization undefined; test the boundary separately. Test: Check empty and singleton families.

Known dead ends (deprioritization, not automatic deletion):
- [OBSERVED] Naive averaging loses the intersection constraint: Previous attempts average over sets before preserving the local intersection pattern. Deprioritize this exact reduction.; reopen on A weighted average preserves the local constraint.

### Signed parity synthesis [ACTIVE]
A synthesis route connecting the even-parity obstruction to a weighted incidence encoding.

## Bridge Results
- Parity classification for the smallest cases: The enumeration does not settle the conjecture, but it separates two parity classes that can guide a later invariant.

## Structured Research Checkpoints

### 2026-07-30T08:18:37.459200+00:00
Target: Find an invariant consistent with the small parity split.
Intended move: Export the parity classes to the compression route.
Expected result: (not stated)
Observed failure/gain: No theorem yet; a reusable classification emerged.
Confidence: UNSPECIFIED
Unresolved obligations:
- prove the classification beyond n=10

## Recent Observable Research Events
- 2026-07-30T08:18:37.364539+00:00 | human:demo-researcher | PROJECT_CREATED | A new unresolved research space was created.
- 2026-07-30T08:18:37.388868+00:00 | human:demo-researcher | ROUTE_CREATED route=c70795b6-1e94-4eb9-b736-4ce9da3a2501 | A new route 'Small-case counterexample search' entered the research space.
- 2026-07-30T08:18:37.393037+00:00 | human:demo-researcher | ROUTE_CREATED route=76800db7-7e56-4dc4-9ee6-006aa40c80c6 | A new route 'Compression / entropy route' entered the research space.
- 2026-07-30T08:18:37.397468+00:00 | human:demo-researcher | BRANCH_CREATED route=c70795b6-1e94-4eb9-b736-4ce9da3a2501 branch=48d85869-b0f8-4c5d-9ad3-3bdba7e2db40 | A concrete branch 'Enumerate n <= 10' was created.
- 2026-07-30T08:18:37.402562+00:00 | human:demo-researcher | CHALLENGE_CREATED route=c70795b6-1e94-4eb9-b736-4ce9da3a2501 branch=48d85869-b0f8-4c5d-9ad3-3bdba7e2db40 | A challenge was raised: The candidate inequality may fail for the empty family.
- 2026-07-30T08:18:37.412687+00:00 | human:demo-researcher | HUMAN_INTERVENTION_ADDED route=c70795b6-1e94-4eb9-b736-4ce9da3a2501 branch=48d85869-b0f8-4c5d-9ad3-3bdba7e2db40 | Human intuition note added.
- 2026-07-30T08:18:37.420687+00:00 | human:demo-researcher | DEAD_END_CONSTRAINT_CREATED route=76800db7-7e56-4dc4-9ee6-006aa40c80c6 | A known dead-end constraint was recorded without deleting the route: Naive averaging loses the intersection constraint
- 2026-07-30T08:18:37.427891+00:00 | human:demo-researcher | BRIDGE_RESULT_CREATED route=c70795b6-1e94-4eb9-b736-4ce9da3a2501 branch=48d85869-b0f8-4c5d-9ad3-3bdba7e2db40 | Bridge result preserved: Parity classification for the smallest cases
- 2026-07-30T08:18:37.433428+00:00 | human:demo-researcher | ROUTE_CREATED route=712b5152-1303-4aa6-a135-1e484b0cf39c | A new route 'Even-parity obstruction route' entered the research space.
- 2026-07-30T08:18:37.438517+00:00 | human:demo-researcher | ROUTE_CREATED route=4dfa4012-5783-4bc2-9c72-30c0a9839a1f | A new route 'Odd-parity construction route' entered the research space.
- 2026-07-30T08:18:37.443079+00:00 | human:demo-researcher | ROUTE_SPLIT route=c70795b6-1e94-4eb9-b736-4ce9da3a2501 | Route 'Small-case counterexample search' was split into 2 explicit child routes without closing the source route.
- 2026-07-30T08:18:37.449154+00:00 | human:demo-researcher | ROUTE_CREATED route=e671bc6c-3378-4fee-b832-c2733d578119 | A new route 'Signed parity synthesis' entered the research space.
- 2026-07-30T08:18:37.454181+00:00 | human:demo-researcher | ROUTES_MERGED route=e671bc6c-3378-4fee-b832-c2733d578119 | 2 routes were synthesized into 'Signed parity synthesis'. The source routes remain in the event history.
- 2026-07-30T08:18:37.459412+00:00 | human:demo-researcher | RESEARCH_CHECKPOINT_CREATED route=c70795b6-1e94-4eb9-b736-4ce9da3a2501 branch=48d85869-b0f8-4c5d-9ad3-3bdba7e2db40 | No theorem yet; a reusable classification emerged.
- 2026-07-30T08:18:37.471871+00:00 | human:demo-researcher | ROUTE_STATE_CHANGED route=76800db7-7e56-4dc4-9ee6-006aa40c80c6 | Route state changed from SEED to DORMANT: No useful encoding yet; preserve the route for later revival.
- 2026-07-30T08:18:37.476591+00:00 | human:demo-researcher | ARTIFACT_ADDED | Artifact 'demo-chat.md' was preserved.
- 2026-07-30T08:18:37.482013+00:00 | human:demo-researcher | CHAT_IMPORT_PREVIEW_CREATED | A model conversation was preserved and parsed into candidates. No candidate entered the research graph without human confirmation.
- 2026-07-30T08:18:37.487748+00:00 | human:demo-researcher | BRANCH_CREATED route=76800db7-7e56-4dc4-9ee6-006aa40c80c6 branch=fb35fc1f-8cc7-4d43-96d1-82faef715b61 | A concrete branch 'Signed incidence vector' was created.
- 2026-07-30T08:18:37.492542+00:00 | human:demo-researcher | CHALLENGE_CREATED route=76800db7-7e56-4dc4-9ee6-006aa40c80c6 | A challenge was raised: Objection: the empty family makes the normalization undefined; test the boundary separately.
- 2026-07-30T08:18:37.496805+00:00 | human:demo-researcher | CHAT_IMPORT_CONFIRMED | A human confirmed selected imported conversation fragments. Unselected text remains preserved only in the raw transcript artifact.
- 2026-07-30T08:18:37.501764+00:00 | human:demo-researcher | PLUGIN_ENABLED | Optional plugin python.local was enabled for this project.
- 2026-07-30T08:18:37.508340+00:00 | human:demo-researcher | ARTIFACT_ADDED | Artifact 'python-run-2f7e3132-2b8e-4bf4-901e-1164f929caf6.py' was preserved.
- 2026-07-30T08:18:37.513041+00:00 | human:demo-researcher | PLUGIN_RUN_STARTED route=c70795b6-1e94-4eb9-b736-4ce9da3a2501 branch=48d85869-b0f8-4c5d-9ad3-3bdba7e2db40 | A local Python experiment started. This event records intent and inputs even if the host process ends before a completion event.
- 2026-07-30T08:18:37.554134+00:00 | tool:python.local | ARTIFACT_ADDED | Artifact 'python-run-2f7e3132-2b8e-4bf4-901e-1164f929caf6.stdout.log' was preserved.
- 2026-07-30T08:18:37.559956+00:00 | tool:python.local | ARTIFACT_ADDED | Artifact 'python-run-2f7e3132-2b8e-4bf4-901e-1164f929caf6.stderr.log' was preserved.
- 2026-07-30T08:18:37.566382+00:00 | tool:python.local | ARTIFACT_ADDED | Artifact 'parity.json' was preserved.
- 2026-07-30T08:18:37.571910+00:00 | tool:python.local | PLUGIN_RUN_COMPLETED route=c70795b6-1e94-4eb9-b736-4ce9da3a2501 branch=48d85869-b0f8-4c5d-9ad3-3bdba7e2db40 | python.local run ended as SUCCEEDED. Successful and failed runs are both retained as experiment evidence.

## Working Constitution
- Do not force a complete solution.
- Raise objections freely, but do not close a route without strong evidence.
- Distinguish a conjecture, candidate argument, finite test, formal target, and reviewed result.
- Preserve failed routes, bridge results, and open obligations.
- State what changed in the research state, not merely what was written.

## Requested Output Format
Return a visible research checkpoint with:
1. current target and route;
2. assumptions used;
3. proposed move;
4. produced artifact or obstruction;
5. unresolved obligations;
6. next non-equivalent routes.