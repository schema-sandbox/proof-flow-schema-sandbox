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
  type BranchRecord,
  type BridgeResultRecord,
  type ChallengeRecord,
  type EpistemicDelta,
  type EventRecord,
  type HistoricalSearchHit,
  type ProjectManifest,
  type ProjectSummary,
  type RouteRecord,
} from "./api";

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
        label: challenge.challenge_type.replaceAll("_", " "),
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

function nodeLabel({ data }: { data: GraphData }) {
  return (
    <div className="node-copy">
      <span className="node-kind">{data.kind}</span>
      <strong>{data.label}</strong>
      <small>{data.state}</small>
    </div>
  );
}

function formatTime(value: string) {
  return new Intl.DateTimeFormat("zh-CN", {
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(value));
}

export function App() {
  const [projects, setProjects] = useState<ProjectSummary[]>([]);
  const [project, setProject] = useState<ProjectManifest | null>(null);
  const [routes, setRoutes] = useState<RouteRecord[]>([]);
  const [branches, setBranches] = useState<BranchRecord[]>([]);
  const [challenges, setChallenges] = useState<ChallengeRecord[]>([]);
  const [bridges, setBridges] = useState<BridgeResultRecord[]>([]);
  const [events, setEvents] = useState<EventRecord[]>([]);
  const [deltas, setDeltas] = useState<EpistemicDelta[]>([]);
  const [canvasScene, setCanvasScene] = useState<Record<string, unknown> | null>(null);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [selectedNode, setSelectedNode] = useState<GraphData | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchHits, setSearchHits] = useState<HistoricalSearchHit[]>([]);
  const [canvasNote, setCanvasNote] = useState("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [apiKeyDraft, setApiKeyDraft] = useState("");
  const sceneDraft = useRef<SceneDraft | null>(null);
  const selectedElementIds = useRef<string[]>([]);
  const flowInstance = useRef<ReactFlowInstance<Node<GraphData>, Edge> | null>(null);

  const graph = useMemo(
    () => buildGraph(routes, branches, challenges, bridges),
    [routes, branches, challenges, bridges],
  );
  const renderedNodes = useMemo<Node<GraphData>[]>(
    () =>
      graph.nodes.map((node): Node<GraphData> => ({
        ...node,
        selected: node.id === selectedNodeId,
        data: { ...node.data, label: nodeLabel({ data: node.data }) },
      })),
    [graph.nodes, selectedNodeId],
  );
  const openChallenges = challenges.filter((item) => item.status !== "RESOLVED").length;

  useEffect(() => {
    api
      .projects()
      .then((items) => {
        setProjects(items);
        if (items[0]) return openProject(items[0].project_id);
        return undefined;
      })
      .catch((reason: Error) => setError(reason.message))
      .finally(() => setLoading(false));
  }, []);

  async function openProject(id: string) {
    setLoading(true);
    setError("");
    try {
      const [p, r, b, c, bridgeItems, eventItems, deltaItems, latestCanvas] =
        await Promise.all([
          api.project(id),
          api.routes(id),
          api.branches(id),
          api.challenges(id),
          api.bridges(id),
          api.events(id),
          api.deltas(id),
          api.latestCanvas(id),
        ]);
      setProject(p);
      setRoutes(r);
      setBranches(b);
      setChallenges(c);
      setBridges(bridgeItems);
      setEvents(eventItems);
      setDeltas(deltaItems);
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
      setNotice("");
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "项目加载失败");
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
      return;
    }
    setError("");
    try {
      setSearchHits(await api.search(project.project_id, searchQuery.trim()));
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "历史检索失败");
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
      setNotice(`画布快照已保存，工件 ${saved.original_artifact_ref.slice(0, 8)}`);
      setCanvasNote("");
      const [eventItems, deltaItems] = await Promise.all([
        api.events(project.project_id),
        api.deltas(project.project_id),
      ]);
      setEvents(eventItems);
      setDeltas(deltaItems);
      return saved;
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "画布保存失败");
      return null;
    } finally {
      setSaving(false);
    }
  }

  async function deriveRouteFromSelection() {
    if (!project || selectedElementIds.current.length === 0) {
      setError("请先在自由草图中选择至少一个元素。");
      return;
    }
    const title = canvasNote.trim();
    if (!title) {
      setError("请先填写作者说明，作为派生路线标题。");
      return;
    }
    setSaving(true);
    try {
      const route = await api.createRoute(
        project.project_id,
        title,
        `由自由草图元素派生。原始草图保持为不可变内容寻址工件。`,
      );
      setSelectedNodeId(route.route_id);
      await saveCanvas("CONFIRMED", route.route_id);
      setRoutes(await api.routes(project.project_id));
      setNotice("派生路线已建立，草图原件未被覆盖。");
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "派生路线创建失败");
    } finally {
      setSaving(false);
    }
  }

  return (
    <main className="app-shell">
      <aside className="project-sidebar" aria-label="项目列表">
        <div className="brand-block">
          <span className="brand-mark" aria-hidden="true">PF</span>
          <div>
            <h1>ProofFlow</h1>
            <p>Schema Sandbox</p>
          </div>
        </div>
        <p className="constitution">
          实验数学沙盒。UNRESOLVED 是有效结果，不自动宣称问题已解决。
        </p>
        <nav className="project-list" aria-label="研究项目">
          {projects.map((item) => (
            <button
              className={project?.project_id === item.project_id ? "active" : ""}
              key={item.project_id}
              onClick={() => openProject(item.project_id)}
            >
              <strong>{item.title}</strong>
              <span>{item.project_status.join(" / ")}</span>
            </button>
          ))}
          {!loading && projects.length === 0 && (
            <div className="empty-copy">
              尚无项目。先通过本地 API 或原型界面创建研究空间。
            </div>
          )}
        </nav>
        <div className="sidebar-rule">
          事件流为规范记录。SQLite、路线图和时间线均可重建。
        </div>
      </aside>

      <section className="research-space">
        {loading && (
          <div className="loading-layout" aria-label="正在加载">
            <span />
            <span />
            <span />
          </div>
        )}
        {!loading && !project && (
          <div className="welcome">
            {error.toLowerCase().includes("authentication required") && (
              <div className="auth-box">
                <h3>API 认证</h3>
                <p>生产模式需要 API key；密钥只保存在本次浏览器会话中。</p>
                <input
                  aria-label="API key"
                  type="password"
                  value={apiKeyDraft}
                  onChange={(event) => setApiKeyDraft(event.target.value)}
                  placeholder="输入 PROOFFLOW_API_KEYS 中的一个 key"
                />
                <button
                  disabled={!apiKeyDraft.trim()}
                  onClick={() => {
                    setApiKey(apiKeyDraft);
                    window.location.reload();
                  }}
                >
                  连接 API
                </button>
              </div>
            )}
            <h2>选择研究项目</h2>
            <p>双画布会保留路线、失败、异议、桥接结果和人工介入。</p>
          </div>
        )}
        {!loading && project && (
          <>
            <header className="project-header">
              <div>
                <div className="status-line">
                  {project.project_status.map((status) => (
                    <span key={status}>{status}</span>
                  ))}
                </div>
                <h2>{project.title}</h2>
                <p>{project.original_problem.source_text}</p>
              </div>
              <dl className="project-facts">
                <div><dt>路线</dt><dd>{routes.length}</dd></div>
                <div><dt>开放挑战</dt><dd>{openChallenges}</dd></div>
                <div><dt>桥接结果</dt><dd>{bridges.length}</dd></div>
                <div><dt>事件</dt><dd>{events.length}</dd></div>
              </dl>
            </header>

            {error && <div className="message error-message" role="alert">{error}</div>}
            {notice && <div className="message notice-message" role="status">{notice}</div>}

            <div className="search-strip">
              <label htmlFor="history-search">历史路线与失败资产</label>
              <div>
                <input
                  id="history-search"
                  value={searchQuery}
                  onChange={(event) => setSearchQuery(event.target.value)}
                  onKeyDown={(event) => {
                    if (event.key === "Enter") void runSearch();
                  }}
                  placeholder="检索死路、桥接结果、挑战或复活条件"
                />
                <button onClick={() => void runSearch()}>检索</button>
              </div>
              {searchHits.length > 0 && (
                <div className="search-results">
                  {searchHits.map((hit) => (
                    <button
                      key={`${hit.kind}-${hit.object_id}`}
                      onClick={() => focusGraphNode(hit.route_id ?? hit.object_id)}
                    >
                      <span>{hit.kind}</span>
                      <strong>{hit.title}</strong>
                      <small>{hit.excerpt}</small>
                    </button>
                  ))}
                </div>
              )}
            </div>

            <div className="dual-canvas">
              <section className="canvas-panel route-panel" aria-label="结构化路线图">
                <div className="panel-heading">
                  <div>
                    <h3>研究路线图</h3>
                    <p>路线、分支、挑战和桥接工件</p>
                  </div>
                  {selectedNode && (
                    <div className="selected-summary">
                      <span>{selectedNode.kind}</span>
                      <strong>{selectedNode.label}</strong>
                    </div>
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

              <section className="canvas-panel sketch-panel" aria-label="自由草图">
                <div className="panel-heading">
                  <div>
                    <h3>自由草图</h3>
                    <p>每次保存都创建不可变快照</p>
                  </div>
                  <button disabled={saving} onClick={() => void saveCanvas()}>
                    {saving ? "保存中" : "保存快照"}
                  </button>
                </div>
                <div className="sketch-stage">
                  {canvasScene && (
                    <Suspense
                      fallback={<div className="canvas-loading">正在加载自由草图</div>}
                    >
                      <Excalidraw
                        key={project.project_id}
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
                        }}
                        UIOptions={{
                          canvasActions: { saveAsImage: true, export: false },
                        }}
                      />
                    </Suspense>
                  )}
                </div>
                <div className="canvas-actions">
                  <label htmlFor="canvas-note">作者说明</label>
                  <textarea
                    id="canvas-note"
                    value={canvasNote}
                    onChange={(event) => setCanvasNote(event.target.value)}
                    placeholder="说明所选草图元素的研究含义"
                  />
                  <button
                    className="secondary-action"
                    disabled={saving}
                    onClick={() => void deriveRouteFromSelection()}
                  >
                    从所选元素建立派生路线
                  </button>
                </div>
              </section>
            </div>

            <div className="lower-deck">
              <section className="timeline-panel">
                <div className="section-heading">
                  <h3>可观察时间线</h3>
                  <span>点击定位到路线节点</span>
                </div>
                <div className="timeline-list">
                  {events.slice(-30).reverse().map((event) => (
                    <button
                      key={event.event_id}
                      onClick={() => focusGraphNode(event.branch_id ?? event.route_id)}
                    >
                      <time>{formatTime(event.timestamp)}</time>
                      <strong>{event.event_type.replaceAll("_", " ")}</strong>
                      <span>{event.epistemic_delta ?? "事件已记录，无状态增量说明"}</span>
                    </button>
                  ))}
                </div>
              </section>
              <section className="delta-panel">
                <div className="section-heading">
                  <h3>本轮改变了什么</h3>
                  <span>NO_STATE_CHANGE 默认折叠</span>
                </div>
                <div className="delta-list">
                  {deltas.slice(-12).reverse().map((delta) => (
                    <button
                      key={delta.event_id}
                      onClick={() => focusGraphNode(delta.branch_id ?? delta.route_id)}
                    >
                      <strong>{delta.delta_type.replaceAll("_", " ")}</strong>
                      <span>{delta.description}</span>
                    </button>
                  ))}
                  {deltas.length === 0 && (
                    <div className="empty-copy">尚无可展开的认识增量。</div>
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
