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

const API_KEY_STORAGE_KEY = "proofflow_api_key";

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
    throw new Error(body.detail ?? response.statusText);
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
};
