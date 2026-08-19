export type ProjectSummary = {
  project_id: string;
  title: string;
  description: string;
  updated_at: string;
  project_status: string[];
};

export type ProjectManifest = ProjectSummary & {
  original_problem: { source_text: string; author_notes: string };
};

export type RouteRecord = {
  route_id: string;
  parent_route_id: string | null;
  title: string;
  description: string;
  state: string;
  revival_conditions: string[];
};

export type BranchRecord = {
  branch_id: string;
  route_id: string;
  parent_branch_id: string | null;
  title: string;
  description: string;
  state: string;
};

export type ChallengeRecord = {
  challenge_id: string;
  route_id: string | null;
  branch_id: string | null;
  challenge_type: string;
  status: string;
  statement: string;
};

export type BridgeResultRecord = {
  bridge_result_id: string;
  route_id: string;
  branch_id: string | null;
  title: string;
  summary: string;
  status: string;
};

export type EventRecord = {
  event_id: string;
  event_type: string;
  timestamp: string;
  route_id: string | null;
  branch_id: string | null;
  epistemic_delta: string | null;
  epistemic_delta_type: string | null;
  revision?: number | null;
  idempotency_key?: string | null;
};

export type ResearchStateSnapshot = {
  project_id: string;
  revision: number;
  operational: Record<string, unknown>;
  epistemic: Record<string, unknown>;
  claim: Record<string, unknown>;
  artifact: Record<string, unknown>;
  as_of: string;
};

export type TransitionProposalRecord = {
  proposal_id: string;
  status: string;
  trigger_class: string;
  accepted_delta: Record<string, Record<string, unknown>>;
  next_obligation_refs: string[];
  handoff_refs: string[];
  created_at: string;
};

export type ClaimAtomRecord = {
  claim_id: string;
  statement: string;
  state: string;
  source_class: string;
  open_obligation_refs: string[];
};

export type EvidenceCardRecord = {
  card_id: string;
  claim_id: string;
  dimensions: Record<string, { status: string; evidence_refs: string[] }>;
};

export type EpistemicDelta = {
  event_id: string;
  event_type: string;
  delta_type: string;
  description: string;
  timestamp: string;
  route_id: string | null;
  branch_id: string | null;
};

export type HistoricalSearchHit = {
  kind: string;
  object_id: string;
  title: string;
  excerpt: string;
  route_id: string | null;
  branch_id: string | null;
  created_at: string;
  score: number;
  reopen_conditions: string[];
};

export type CanvasSnapshot = {
  visual_id: string;
  original_artifact_ref: string;
  author_description: string;
  machine_interpretation: string;
  mapping_status: string;
  element_links: Record<string, string>;
  created_at: string;
  confirmed_by: string | null;
};

export type CanvasSnapshotResponse = {
  visual_artifact: CanvasSnapshot;
  scene: Record<string, unknown>;
};

export type IntegrityReport = {
  project_id: string;
  event_count: number;
  valid: boolean;
  projection_schema_version?: number;
  first_invalid_index: number | null;
  error: string | null;
};

const API_KEY_STORAGE_KEY = "proofflow_api_key";

export class ApiError extends Error {
  status: number;
  detail: unknown;
  constructor(status: number, message: string, detail?: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }
}

export function isAuthError(reason: unknown): boolean {
  return reason instanceof ApiError && (reason.status === 401 || reason.status === 403);
}

function storedApiKey(): string {
  try {
    return window.sessionStorage.getItem(API_KEY_STORAGE_KEY) ?? "";
  } catch {
    return "";
  }
}

export function setApiKey(apiKey: string): void {
  try {
    if (apiKey.trim()) window.sessionStorage.setItem(API_KEY_STORAGE_KEY, apiKey.trim());
    else window.sessionStorage.removeItem(API_KEY_STORAGE_KEY);
  } catch {
    // Private browsing policies may disable sessionStorage; local mode remains usable.
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const headers = new Headers(init?.headers);
  if (init?.body) headers.set("Content-Type", "application/json");
  const apiKey = storedApiKey();
  if (apiKey) headers.set("X-API-Key", apiKey);
  const response = await fetch(path, {
    ...init,
    headers,
  });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    const message = (
      typeof body.detail === "string" ? body.detail : response.statusText
    ) || response.statusText;
    throw new ApiError(response.status, message, body.detail);
  }
  return response.json() as Promise<T>;
}

const jsonPost = <T>(path: string, body: unknown) =>
  request<T>(path, { method: "POST", body: JSON.stringify(body) });

export const api = {
  projects: () => request<ProjectSummary[]>("/api/v1/projects"),
  project: (id: string) => request<ProjectManifest>(`/api/v1/projects/${id}`),
  routes: (id: string) => request<RouteRecord[]>(`/api/v1/projects/${id}/routes`),
  branches: (id: string) => request<BranchRecord[]>(`/api/v1/projects/${id}/branches`),
  challenges: (id: string) =>
    request<ChallengeRecord[]>(`/api/v1/projects/${id}/challenges`),
  bridges: (id: string) =>
    request<BridgeResultRecord[]>(`/api/v1/projects/${id}/bridge-results`),
  events: (id: string) => request<EventRecord[]>(`/api/v1/projects/${id}/events`),
  researchState: (id: string) =>
    request<ResearchStateSnapshot>(`/api/v1/projects/${id}/research-state`),
  transitionProposals: (id: string) =>
    request<TransitionProposalRecord[]>(`/api/v1/projects/${id}/transition-proposals`),
  claimAtoms: (id: string) =>
    request<ClaimAtomRecord[]>(`/api/v1/projects/${id}/claim-atoms`),
  evidenceCards: (id: string) =>
    request<EvidenceCardRecord[]>(`/api/v1/projects/${id}/evidence-cards`),
  deltas: (id: string) =>
    request<EpistemicDelta[]>(`/api/v1/projects/${id}/epistemic-deltas?limit=80`),
  search: (id: string, query: string) =>
    request<HistoricalSearchHit[]>(
      `/api/v1/projects/${id}/search?q=${encodeURIComponent(query)}&limit=30`,
    ),
  latestCanvas: (id: string) =>
    request<CanvasSnapshotResponse | null>(`/api/v1/projects/${id}/canvas/latest`),
  saveCanvas: (id: string, body: unknown) =>
    jsonPost<CanvasSnapshot>(`/api/v1/projects/${id}/canvas/snapshots`, body),
  createRoute: (id: string, title: string, description: string) =>
    jsonPost<RouteRecord>(`/api/v1/projects/${id}/routes`, {
      title,
      description,
      initial_state: "SEED",
      revival_conditions: [],
      actor: { type: "human", id: "local-researcher" },
    }),
  createProject: (title: string, problem: string, notes: string) =>
    jsonPost<ProjectManifest>("/api/v1/projects", {
      title,
      description: "",
      problem: {
        source_text: problem,
        author_notes: notes,
        definitions: [],
        assumptions: [],
      },
      actor: { type: "human", id: "local-researcher" },
    }),
  integrity: (id: string) =>
    request<IntegrityReport>(`/api/v1/projects/${id}/integrity`),
  exportUrl: (id: string) => `/api/v1/projects/${id}/export`,
  /** Authenticated download: anchor navigation cannot send X-API-Key. */
  downloadExport: async (id: string, filename?: string) => {
    const headers = new Headers();
    const apiKey = storedApiKey();
    if (apiKey) headers.set("X-API-Key", apiKey);
    const response = await fetch(`/api/v1/projects/${id}/export`, { headers });
    if (!response.ok) {
      const body = await response.json().catch(() => ({}));
      const message =
        (typeof body.detail === "string" ? body.detail : response.statusText) ||
        response.statusText;
      throw new ApiError(response.status, message, body.detail);
    }
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = filename ?? `project-${id.slice(0, 8)}.smath.zip`;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    URL.revokeObjectURL(url);
  },
};
