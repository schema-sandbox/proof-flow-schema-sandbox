import {
  lazy,
  Suspense,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from "react";
import {
  Background,
  Controls,
  MiniMap,
  ReactFlow,
  type Edge,
  type Node,
  type ReactFlowInstance,
} from "@xyflow/react";
import {
  api,
  setApiKey,
  isAuthError,
  type BranchRecord,
  type BridgeResultRecord,
  type ChallengeRecord,
  type EpistemicDelta,
  type EventRecord,
  type HistoricalSearchHit,
  type ProjectManifest,
  type ProjectSummary,
  type ClaimAtomRecord,
  type EvidenceCardRecord,
  type ResearchStateSnapshot,
  type TransitionProposalRecord,
  type RouteRecord,
} from "./api";
import { AuthGate } from "./components/AuthGate";
import { Sidebar } from "./components/Sidebar";
import { ControlPlane } from "./components/ControlPlane";
import {
  labelChallengeType,
  labelEnum,
  labelKind,
} from "./labels";
import {
  getInitialLanguage,
  saveLanguage,
  translations,
  type SupportedLanguage,
} from "./i18n";

const Excalidraw = lazy(async () => {
  const module = await import("@excalidraw/excalidraw");
  return { default: module.Excalidraw };
});

type SceneDraft = {
  elements: readonly unknown[];
  appState: Record<string, unknown>;
  files: Record<string, unknown>;
};

type GraphData = {
  label: ReactNode;
  detail: string;
  kind: "route" | "branch" | "challenge" | "bridge";
  state: string;
};

function buildGraph(
  routes: RouteRecord[],
  branches: BranchRecord[],
  challenges: ChallengeRecord[],
  bridges: BridgeResultRecord[],
  lang: SupportedLanguage,
): { nodes: Node<GraphData>[]; edges: Edge[] } {
  const nodes: Node<GraphData>[] = [];
  const edges: Edge[] = [];

  routes.forEach((route, index) => {
    nodes.push({
      id: route.route_id,
      position: { x: (index % 3) * 330, y: Math.floor(index / 3) * 260 },
      data: {
        label: route.title,
        detail: route.description,
        kind: "route",
        state: route.state,
      },
      className: `research-node route-node state-${route.state.toLowerCase()}`,
    });
    if (route.parent_route_id) {
      edges.push({
        id: `route-${route.parent_route_id}-${route.route_id}`,
        source: route.parent_route_id,
        target: route.route_id,
        type: "smoothstep",
      });
    }
  });

  branches.forEach((branch, index) => {
    const routeIndex = Math.max(
      0,
      routes.findIndex((route) => route.route_id === branch.route_id),
    );
    nodes.push({
      id: branch.branch_id,
      position: {
        x: (routeIndex % 3) * 330 + 38,
        y: Math.floor(routeIndex / 3) * 260 + 130 + (index % 2) * 82,
      },
      data: {
        label: branch.title,
        detail: branch.description,
        kind: "branch",
        state: branch.state,
      },
      className: "research-node branch-node",
    });
    edges.push({
      id: `branch-${branch.route_id}-${branch.branch_id}`,
      source: branch.parent_branch_id ?? branch.route_id,
      target: branch.branch_id,
      type: "smoothstep",
    });
  });

  challenges.forEach((challenge, index) => {
    const target = challenge.branch_id ?? challenge.route_id;
    if (!target) return;
    nodes.push({
      id: challenge.challenge_id,
      position: { x: 1020 + (index % 2) * 245, y: index * 105 },
      data: {
        label: labelChallengeType(challenge.challenge_type, lang),
        detail: challenge.statement,
        kind: "challenge",
        state: challenge.status,
      },
      className: "research-node challenge-node",
    });
    edges.push({
      id: `challenge-${target}-${challenge.challenge_id}`,
      source: target,
      target: challenge.challenge_id,
      type: "smoothstep",
      style: { strokeDasharray: "5 4" },
    });
  });

  bridges.forEach((bridge, index) => {
    nodes.push({
      id: bridge.bridge_result_id,
      position: { x: 640 + (index % 2) * 280, y: 620 + index * 110 },
      data: {
        label: bridge.title,
        detail: bridge.summary,
        kind: "bridge",
        state: bridge.status,
      },
      className: "research-node bridge-node",
    });
    edges.push({
      id: `bridge-${bridge.route_id}-${bridge.bridge_result_id}`,
      source: bridge.route_id,
      target: bridge.bridge_result_id,
      animated: true,
      type: "smoothstep",
    });
  });

  return { nodes, edges };
}

function nodeLabel({ data, lang }: { data: GraphData; lang: SupportedLanguage }) {
  return (
    <div className="node-copy">
      <span className="node-kind">{labelKind(data.kind, lang)}</span>
      <strong>{data.label}</strong>
      <small title={data.state}>{labelEnum(data.state, lang)}</small>
    </div>
  );
}

function formatTime(value: string, lang: SupportedLanguage) {
  return new Intl.DateTimeFormat(lang === "en" ? "en-US" : "zh-CN", {
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(value));
}

export function App() {
  const [lang, setLang] = useState<SupportedLanguage>(getInitialLanguage);
  const [projects, setProjects] = useState<ProjectSummary[]>([]);
  const [project, setProject] = useState<ProjectManifest | null>(null);
  const [routes, setRoutes] = useState<RouteRecord[]>([]);
  const [branches, setBranches] = useState<BranchRecord[]>([]);
  const [challenges, setChallenges] = useState<ChallengeRecord[]>([]);
  const [bridges, setBridges] = useState<BridgeResultRecord[]>([]);
  const [events, setEvents] = useState<EventRecord[]>([]);
  const [deltas, setDeltas] = useState<EpistemicDelta[]>([]);
  const [researchState, setResearchState] = useState<ResearchStateSnapshot | null>(null);
  const [transitionProposals, setTransitionProposals] = useState<TransitionProposalRecord[]>([]);
  const [claimAtoms, setClaimAtoms] = useState<ClaimAtomRecord[]>([]);
  const [evidenceCards, setEvidenceCards] = useState<EvidenceCardRecord[]>([]);
  const [canvasScene, setCanvasScene] = useState<Record<string, unknown> | null>(null);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [selectedNode, setSelectedNode] = useState<GraphData | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchHits, setSearchHits] = useState<HistoricalSearchHit[]>([]);
  const [searchOpen, setSearchOpen] = useState(false);
  const [timelineExpanded, setTimelineExpanded] = useState(false);
  const [deltasExpanded, setDeltasExpanded] = useState(false);
  const searchWrapRef = useRef<HTMLDivElement | null>(null);
  const [canvasNote, setCanvasNote] = useState("");
  const [selectedCount, setSelectedCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [apiKeyDraft, setApiKeyDraft] = useState("");
  const [authRequired, setAuthRequired] = useState(false);
  const [version, setVersion] = useState("");
  const [integrityResult, setIntegrityResult] = useState<{
    valid: boolean;
    text: string;
  } | null>(null);
  const [systemDark, setSystemDark] = useState(
    () => window.matchMedia("(prefers-color-scheme: dark)").matches,
  );
  const sceneDraft = useRef<SceneDraft | null>(null);
  const selectedElementIds = useRef<string[]>([]);
  const flowInstance = useRef<ReactFlowInstance<Node<GraphData>, Edge> | null>(null);

  const t = translations[lang];

  function handleLanguageChange(nextLang: SupportedLanguage) {
    setLang(nextLang);
    saveLanguage(nextLang);
  }

  useEffect(() => {
    const onLangChange = (e: Event) => {
      const customEvent = e as CustomEvent<SupportedLanguage>;
      if (customEvent.detail && (customEvent.detail === "en" || customEvent.detail === "zh")) {
        setLang(customEvent.detail);
      }
    };
    const onStorage = (e: StorageEvent) => {
      if (e.key === "proofflow_lang" && (e.newValue === "en" || e.newValue === "zh")) {
        setLang(e.newValue);
      }
    };
    window.addEventListener("proofflow-lang-change", onLangChange);
    window.addEventListener("storage", onStorage);
    return () => {
      window.removeEventListener("proofflow-lang-change", onLangChange);
      window.removeEventListener("storage", onStorage);
    };
  }, []);

  const graph = useMemo(
    () => buildGraph(routes, branches, challenges, bridges, lang),
    [routes, branches, challenges, bridges, lang],
  );

  const renderedNodes = useMemo<Node<GraphData>[]>(
    () =>
      graph.nodes.map((node): Node<GraphData> => ({
        ...node,
        selected: node.id === selectedNodeId,
        data: { ...node.data, label: nodeLabel({ data: node.data, lang }) },
      })),
    [graph.nodes, selectedNodeId, lang],
  );

  const openChallenges = challenges.filter((item) => item.status !== "RESOLVED").length;

  useEffect(() => {
    const media = window.matchMedia("(prefers-color-scheme: dark)");
    const onChange = (event: MediaQueryListEvent) => setSystemDark(event.matches);
    media.addEventListener("change", onChange);
    return () => media.removeEventListener("change", onChange);
  }, []);

  useEffect(() => {
    if (!searchOpen) return;
    const onMouseDown = (event: MouseEvent) => {
      if (
        searchWrapRef.current &&
        !searchWrapRef.current.contains(event.target as Element)
      ) {
        setSearchOpen(false);
      }
    };
    document.addEventListener("mousedown", onMouseDown);
    return () => document.removeEventListener("mousedown", onMouseDown);
  }, [searchOpen]);

  useEffect(() => {
    void startup();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function startup() {
    setLoading(true);
    setAuthRequired(false);
    setError("");
    try {
      const health = await fetch("/health").then((response) =>
        response.json().catch(() => ({})),
      );
      if (health.version) setVersion(String(health.version));
    } catch {
      // Health endpoint is optional; the project list is authoritative.
    }
    try {
      const items = await api.projects();
      setProjects(items);
      if (items[0]) return openProject(items[0].project_id);
      return undefined;
    } catch (reason) {
      if (isAuthError(reason)) setAuthRequired(true);
      setError(reason instanceof Error ? reason.message : t.notices.projectListLoadFailed);
      return undefined;
    } finally {
      setLoading(false);
    }
  }

  function connectWithApiKey() {
    setApiKey(apiKeyDraft);
    setApiKeyDraft("");
    void startup();
  }

  async function createProject(title: string, problem: string, notes: string) {
    try {
      const created = await api.createProject(title, problem, notes);
      setProjects((items) => [created, ...items]);
      await openProject(created.project_id);
      setNotice(t.notices.projectCreated);
      return true;
    } catch (reason) {
      if (isAuthError(reason)) setAuthRequired(true);
      setError(reason instanceof Error ? reason.message : t.notices.projectCreateFailed);
      return false;
    }
  }

  async function openProject(id: string) {
    setLoading(true);
    setError("");
    try {
      const [
        p,
        r,
        b,
        c,
        bridgeItems,
        eventItems,
        deltaItems,
        latestCanvas,
        stateSnapshot,
        proposalItems,
        claimItems,
        evidenceItems,
      ] =
        await Promise.all([
          api.project(id),
          api.routes(id),
          api.branches(id),
          api.challenges(id),
          api.bridges(id),
          api.events(id),
          api.deltas(id),
          api.latestCanvas(id),
          api.researchState(id),
          api.transitionProposals(id),
          api.claimAtoms(id),
          api.evidenceCards(id),
        ]);
      setProject(p);
      setRoutes(r);
      setBranches(b);
      setChallenges(c);
      setBridges(bridgeItems);
      setEvents(eventItems);
      setDeltas(deltaItems);
      setResearchState(stateSnapshot);
      setTransitionProposals(proposalItems);
      setClaimAtoms(claimItems);
      setEvidenceCards(evidenceItems);
      const scene = latestCanvas?.scene ?? {
        type: "excalidraw",
        version: 2,
        source: "ProofFlow",
        elements: [],
        appState: {},
        files: {},
      };
      setCanvasScene(scene);
      sceneDraft.current = {
        elements: (scene.elements as readonly unknown[]) ?? [],
        appState: (scene.appState as Record<string, unknown>) ?? {},
        files: (scene.files as Record<string, unknown>) ?? {},
      };
      setSelectedNodeId(null);
      setSelectedNode(null);
      setSelectedCount(0);
      setIntegrityResult(null);
      setNotice("");
    } catch (reason) {
      if (isAuthError(reason)) setAuthRequired(true);
      setError(reason instanceof Error ? reason.message : t.notices.projectLoadFailed);
    } finally {
      setLoading(false);
    }
  }

  function focusGraphNode(id: string | null) {
    if (!id) return;
    const node = graph.nodes.find((item) => item.id === id);
    if (!node) return;
    setSelectedNodeId(id);
    setSelectedNode(node.data);
    flowInstance.current?.fitView({
      nodes: [{ id }],
      duration: 240,
      padding: 1.1,
      maxZoom: 1.4,
    });
  }

  async function runSearch() {
    if (!project || !searchQuery.trim()) {
      setSearchHits([]);
      setSearchOpen(false);
      return;
    }
    setError("");
    try {
      setSearchHits(await api.search(project.project_id, searchQuery.trim()));
      setSearchOpen(true);
    } catch (reason) {
      if (isAuthError(reason)) setAuthRequired(true);
      setError(reason instanceof Error ? reason.message : t.notices.searchFailed);
    }
  }

  useEffect(() => {
    if (!project || !searchQuery.trim()) return;
    const timer = setTimeout(() => void runSearch(), 300);
    return () => clearTimeout(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchQuery, project?.project_id]);

  async function runIntegrity() {
    if (!project) return;
    setError("");
    setIntegrityResult(null);
    try {
      const report = await api.integrity(project.project_id);
      setIntegrityResult({
        valid: report.valid,
        text: report.valid
          ? t.notices.integrityValid(report.event_count)
          : report.error ?? t.notices.integrityCorrupted(report.first_invalid_index ?? 0),
      });
    } catch (reason) {
      if (isAuthError(reason)) setAuthRequired(true);
      setError(reason instanceof Error ? reason.message : t.notices.integrityFailed);
    }
  }

  async function runExport() {
    if (!project) return;
    setError("");
    setNotice("");
    try {
      await api.downloadExport(project.project_id, `${project.title || "project"}.smath.zip`);
      setNotice(t.notices.exportStarted);
    } catch (reason) {
      if (isAuthError(reason)) setAuthRequired(true);
      setError(reason instanceof Error ? reason.message : t.notices.exportFailed);
    }
  }

  function currentScene() {
    const draft = sceneDraft.current;
    if (!draft) return canvasScene ?? {};
    return {
      type: "excalidraw",
      version: 2,
      source: "ProofFlow",
      elements: draft.elements,
      appState: draft.appState,
      files: draft.files,
    };
  }

  async function saveCanvas(mappingStatus = "UNMAPPED", targetNodeId?: string) {
    if (!project) return null;
    setSaving(true);
    setError("");
    try {
      const links = Object.fromEntries(
        selectedElementIds.current.map((elementId) => [
          elementId,
          targetNodeId ?? selectedNodeId
            ? `research:${targetNodeId ?? selectedNodeId}`
            : "research:unlinked",
        ]),
      );
      const saved = await api.saveCanvas(project.project_id, {
        scene: currentScene(),
        author_description: canvasNote,
        machine_interpretation: "",
        mapping_status: mappingStatus,
        element_links: links,
        actor: { type: "human", id: "local-researcher" },
      });
      setNotice(t.notices.canvasSaved(saved.original_artifact_ref.slice(0, 8)));
      setCanvasNote("");
      const [eventItems, deltaItems] = await Promise.all([
        api.events(project.project_id),
        api.deltas(project.project_id),
      ]);
      setEvents(eventItems);
      setDeltas(deltaItems);
      return saved;
    } catch (reason) {
      if (isAuthError(reason)) setAuthRequired(true);
      setError(reason instanceof Error ? reason.message : t.notices.canvasSaveFailed);
      return null;
    } finally {
      setSaving(false);
    }
  }

  async function deriveRouteFromSelection() {
    if (!project || selectedElementIds.current.length === 0) {
      setError(t.notices.deriveRouteSelectElement);
      return;
    }
    const title = canvasNote.trim();
    if (!title) {
      setError(t.notices.deriveRouteProvideTitle);
      return;
    }
    setSaving(true);
    try {
      const route = await api.createRoute(
        project.project_id,
        title,
        t.notices.derivedRouteDesc,
      );
      setSelectedNodeId(route.route_id);
      await saveCanvas("CONFIRMED", route.route_id);
      setRoutes(await api.routes(project.project_id));
      setNotice(t.notices.deriveRouteSuccess);
    } catch (reason) {
      if (isAuthError(reason)) setAuthRequired(true);
      setError(reason instanceof Error ? reason.message : t.notices.deriveRouteFailed);
    } finally {
      setSaving(false);
    }
  }

  return (
    <main className="app-shell">
      <Sidebar
        projects={projects}
        activeProjectId={project?.project_id}
        version={version || undefined}
        busy={loading}
        lang={lang}
        onLanguageChange={handleLanguageChange}
        t={t.sidebar}
        onOpen={(id) => void openProject(id)}
        onCreate={createProject}
      />

      <section className="research-space">
        {authRequired && (
          <div className="auth-banner" role="region" aria-label={t.authGate.title}>
            <AuthGate
              apiKeyDraft={apiKeyDraft}
              setApiKeyDraft={setApiKeyDraft}
              onConnect={connectWithApiKey}
              message={t.authGate.bannerMessage}
              t={t.authGate}
            />
          </div>
        )}
        {loading && (
          <div className="loading-layout" aria-label={t.explorer.loadingAria}>
            <span />
            <span />
            <span />
          </div>
        )}
        {!loading && !project && (
          <div className="welcome">
            {error && !authRequired && (
              <div className="message error-message" role="alert">{error}</div>
            )}
            <h2>{t.explorer.welcomeTitle}</h2>
            <p>{t.explorer.welcomeDesc}</p>
            <ul className="capability-list">
              <li>
                <strong>{t.explorer.capabilityList[0].bold}</strong>：{t.explorer.capabilityList[0].text}
              </li>
              <li>
                <strong>{t.explorer.capabilityList[1].bold}</strong>
                （
                <a href="/prototype/">{t.explorer.capabilityList[1].linkText}</a>
                ）：{t.explorer.capabilityList[1].text}
              </li>
            </ul>
            <p className="welcome-hint">{t.explorer.welcomeHint}</p>
          </div>
        )}
        {!loading && project && (
          <>
            <header className="project-header">
              <div>
                <div className="status-line">
                  {project.project_status.map((status) => (
                    <span key={status} title={status}>
                      {labelEnum(status, lang)}
                    </span>
                  ))}
                </div>
                <h2>{project.title}</h2>
                <p>{project.original_problem.source_text}</p>
              </div>
              <dl className="project-facts">
                <div><dt>{t.explorer.routesStat}</dt><dd>{routes.length}</dd></div>
                <div><dt>{t.explorer.openChallengesStat}</dt><dd>{openChallenges}</dd></div>
                <div><dt>{t.explorer.bridgesStat}</dt><dd>{bridges.length}</dd></div>
                <div><dt>{t.explorer.eventsStat}</dt><dd>{events.length}</dd></div>
              </dl>
              <div className="project-tools">
                <button type="button" onClick={() => void runExport()}>
                  {t.explorer.exportButton}
                </button>
                <button type="button" onClick={() => void runIntegrity()}>
                  {t.explorer.integrityButton}
                </button>
                <a
                  className="workbench-link-inline"
                  href={`/prototype/?project=${project.project_id}`}
                  title={t.explorer.openWorkbenchTitle}
                >
                  {t.explorer.openWorkbench}
                </a>
              </div>
              {integrityResult && (
                <div
                  className={`message ${integrityResult.valid ? "notice-message" : "error-message"}`}
                  role={integrityResult.valid ? "status" : "alert"}
                >
                  {integrityResult.text}
                </div>
              )}
            </header>

            <ControlPlane
              researchState={researchState}
              transitionProposals={transitionProposals}
              claimAtoms={claimAtoms}
              evidenceCards={evidenceCards}
              lang={lang}
              t={t.controlPlane}
            />

            {error && <div className="message error-message" role="alert">{error}</div>}
            {notice && <div className="message notice-message" role="status">{notice}</div>}

            <div className="search-strip" ref={searchWrapRef}>
              <label htmlFor="history-search">{t.explorer.searchLabel}</label>
              <div>
                <input
                  id="history-search"
                  value={searchQuery}
                  onChange={(event) => {
                    setSearchQuery(event.target.value);
                    setSearchHits([]);
                    setSearchOpen(false);
                  }}
                  onKeyDown={(event) => {
                    if (event.key === "Enter") void runSearch();
                    if (event.key === "Escape") setSearchOpen(false);
                  }}
                  placeholder={t.explorer.searchPlaceholder}
                />
                <button onClick={() => void runSearch()}>{t.explorer.searchButton}</button>
              </div>
              {searchOpen && (
                <div className="search-results">
                  {searchHits.length > 0 ? (
                    searchHits.map((hit) => (
                      <button
                        key={`${hit.kind}-${hit.object_id}`}
                        onClick={() => {
                          focusGraphNode(hit.route_id ?? hit.object_id);
                          setSearchOpen(false);
                        }}
                      >
                        <span title={hit.kind}>{labelEnum(hit.kind, lang)}</span>
                        <strong>{hit.title}</strong>
                        <small>{hit.excerpt}</small>
                      </button>
                    ))
                  ) : (
                    <div className="search-empty">
                      {t.explorer.searchEmpty}
                    </div>
                  )}
                </div>
              )}
            </div>

            <div className="dual-canvas">
              <section className="canvas-panel route-panel" aria-label={t.explorer.routePanelTitle}>
                <div className="panel-heading">
                  <div>
                    <h3>{t.explorer.routePanelTitle}</h3>
                    <p>{t.explorer.routePanelDesc}</p>
                  </div>
                  {selectedNode && (
                    <div className="selected-summary">
                      <span>{labelKind(selectedNode.kind, lang)}</span>
                      <strong>{selectedNode.label}</strong>
                    </div>
                  )}
                </div>
                <div className="node-detail">
                  {selectedNode ? (
                    <>
                      <span title={selectedNode.state}>
                        {labelKind(selectedNode.kind, lang)} · {labelEnum(selectedNode.state, lang)}
                      </span>
                      <p>{selectedNode.detail || t.explorer.nodeDetailNone}</p>
                    </>
                  ) : (
                    <p className="node-detail-hint">{t.explorer.nodeDetailEmpty}</p>
                  )}
                </div>
                <div className="flow-stage">
                  <ReactFlow
                    nodes={renderedNodes}
                    edges={graph.edges}
                    onInit={(instance) => {
                      flowInstance.current = instance;
                    }}
                    onNodeClick={(_, node) => {
                      focusGraphNode(node.id);
                    }}
                    fitView
                    minZoom={0.15}
                    maxZoom={2}
                  >
                    <Background gap={28} size={1} />
                    <MiniMap pannable zoomable />
                    <Controls showInteractive={false} />
                  </ReactFlow>
                </div>
              </section>

              <section className="canvas-panel sketch-panel" aria-label={t.explorer.sketchPanelTitle}>
                <div className="panel-heading">
                  <div>
                    <h3>{t.explorer.sketchPanelTitle}</h3>
                    <p>{t.explorer.sketchPanelDesc}</p>
                  </div>
                  <button disabled={saving} onClick={() => void saveCanvas()}>
                    {saving ? t.explorer.savingSnapshot : t.explorer.saveSnapshot}
                  </button>
                </div>
                <div className="sketch-stage">
                  {canvasScene && (
                    <Suspense
                      fallback={<div className="canvas-loading">{t.explorer.sketchLoading}</div>}
                    >
                      <Excalidraw
                        key={project.project_id}
                        theme={systemDark ? "dark" : "light"}
                        initialData={canvasScene as never}
                        onChange={(elements, appState, files) => {
                          sceneDraft.current = {
                            elements,
                            appState: JSON.parse(JSON.stringify(appState)) as Record<
                              string,
                              unknown
                            >,
                            files: JSON.parse(JSON.stringify(files)) as Record<
                              string,
                              unknown
                            >,
                          };
                          selectedElementIds.current = Object.keys(
                            appState.selectedElementIds,
                          );
                          setSelectedCount(selectedElementIds.current.length);
                        }}
                        UIOptions={{
                          canvasActions: { saveAsImage: true, export: false },
                        }}
                      />
                    </Suspense>
                  )}
                </div>
                <div className="canvas-actions">
                  <label htmlFor="canvas-note">{t.explorer.authorNoteLabel}</label>
                  <textarea
                    id="canvas-note"
                    value={canvasNote}
                    onChange={(event) => setCanvasNote(event.target.value)}
                    placeholder={t.explorer.authorNotePlaceholder}
                  />
                  <p className="canvas-note-hint">
                    {t.explorer.canvasNoteHint}
                  </p>
                  <button
                    className="secondary-action"
                    disabled={saving || selectedCount === 0 || !canvasNote.trim()}
                    title={
                      selectedCount === 0
                        ? t.explorer.deriveRouteTooltipNoSelection
                        : !canvasNote.trim()
                          ? t.explorer.deriveRouteTooltipNoNote
                          : t.explorer.deriveRouteTooltipReady
                    }
                    onClick={() => void deriveRouteFromSelection()}
                  >
                    {t.explorer.deriveRouteButton}
                  </button>
                </div>
              </section>
            </div>

            <div className="lower-deck">
              <section className="timeline-panel">
                <div className="section-heading">
                  <div>
                    <h3>{t.explorer.timelineTitle}</h3>
                    <span>{t.explorer.timelineSubtitle}</span>
                  </div>
                  {events.length > 30 && (
                    <button
                      className="expand-toggle"
                      onClick={() => setTimelineExpanded((value) => !value)}
                    >
                      {timelineExpanded ? t.explorer.timelineCollapse : t.explorer.timelineShowAll(events.length)}
                    </button>
                  )}
                </div>
                <div className="timeline-list">
                  {(timelineExpanded ? events : events.slice(-30))
                    .reverse()
                    .map((event) => (
                      <button
                        key={event.event_id}
                        onClick={() => focusGraphNode(event.branch_id ?? event.route_id)}
                      >
                        <time>{formatTime(event.timestamp, lang)}</time>
                        <strong title={event.event_type}>{labelEnum(event.event_type, lang)}</strong>
                        <span>{event.epistemic_delta ?? t.explorer.timelineNoDelta}</span>
                      </button>
                    ))}
                </div>
              </section>
              <section className="delta-panel">
                <div className="section-heading">
                  <div>
                    <h3>{t.explorer.deltaTitle}</h3>
                    <span>{t.explorer.deltaSubtitle}</span>
                  </div>
                  {deltas.length > 12 && (
                    <button
                      className="expand-toggle"
                      onClick={() => setDeltasExpanded((value) => !value)}
                    >
                      {deltasExpanded ? t.explorer.deltaCollapse : t.explorer.deltaShowAll(deltas.length)}
                    </button>
                  )}
                </div>
                <div className="delta-list">
                  {(deltasExpanded ? deltas : deltas.slice(-12))
                    .reverse()
                    .map((delta) => (
                      <button
                        key={delta.event_id}
                        onClick={() => focusGraphNode(delta.branch_id ?? delta.route_id)}
                      >
                        <strong title={delta.delta_type}>{labelEnum(delta.delta_type, lang)}</strong>
                        <span>{delta.description}</span>
                      </button>
                    ))}
                  {deltas.length === 0 && (
                    <div className="empty-copy">{t.explorer.deltaEmpty}</div>
                  )}
                </div>
              </section>
            </div>
          </>
        )}
      </section>
    </main>
  );
}
