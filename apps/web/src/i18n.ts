export type SupportedLanguage = "en" | "zh";

const STORAGE_KEY = "proofflow_lang";

export function getInitialLanguage(): SupportedLanguage {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved === "en" || saved === "zh") return saved;
    const browserLang = navigator.language?.toLowerCase() ?? "";
    if (browserLang.startsWith("zh")) return "zh";
  } catch {
    // fallback if localStorage not accessible
  }
  return "en";
}

export function saveLanguage(lang: SupportedLanguage): void {
  try {
    localStorage.setItem(STORAGE_KEY, lang);
    window.dispatchEvent(new CustomEvent("proofflow-lang-change", { detail: lang }));
  } catch {
    // ignore
  }
}

export interface SidebarTranslations {
  ariaLabel: string;
  brandSubtitle: string;
  constitution: string;
  researchProjects: string;
  emptyCopy: string;
  newProject: string;
  projectTitleAria: string;
  projectTitlePlaceholder: string;
  originalProblemAria: string;
  originalProblemPlaceholder: string;
  notesAria: string;
  notesPlaceholder: string;
  createButton: string;
  creatingButton: string;
  sidebarRule: string;
  workbenchLink: string;
  langSwitcher: string;
}

export interface PlaneCardTranslation {
  name: string;
  desc: string;
}

export interface ControlPlaneTranslations {
  ariaLabel: string;
  heading: string;
  meta: (rev: string | number, proposals: number, claims: number, evidence: number) => string;
  statusNote: string;
  planeCards: {
    operational: PlaneCardTranslation;
    epistemic: PlaneCardTranslation;
    claim: PlaneCardTranslation;
    artifact: PlaneCardTranslation;
  };
  viewProposalDetails: string;
  proposalSummary: (id: string, status: string) => string;
  proposalMeta: (trigger: string, created: string, obligations: number, handoffs: number) => string;
  claimEvidenceSummary: (claims: number, evidence: number) => string;
  openObligations: (count: number) => string;
}

export interface AuthGateTranslations {
  title: string;
  defaultDesc: string;
  placeholder: string;
  connectButton: string;
  bannerMessage: string;
}

export interface CapabilityItem {
  bold: string;
  linkText?: string;
  text: string;
}

export interface ExplorerTranslations {
  loadingAria: string;
  welcomeTitle: string;
  welcomeDesc: string;
  capabilityList: CapabilityItem[];
  welcomeHint: string;
  exportButton: string;
  integrityButton: string;
  openWorkbench: string;
  openWorkbenchTitle: string;
  searchLabel: string;
  searchPlaceholder: string;
  searchButton: string;
  searchEmpty: string;
  routesStat: string;
  openChallengesStat: string;
  bridgesStat: string;
  eventsStat: string;
  routePanelTitle: string;
  routePanelDesc: string;
  nodeDetailEmpty: string;
  nodeDetailNone: string;
  sketchPanelTitle: string;
  sketchPanelDesc: string;
  saveSnapshot: string;
  savingSnapshot: string;
  sketchLoading: string;
  authorNoteLabel: string;
  authorNotePlaceholder: string;
  canvasNoteHint: string;
  deriveRouteButton: string;
  deriveRouteTooltipNoSelection: string;
  deriveRouteTooltipNoNote: string;
  deriveRouteTooltipReady: string;
  timelineTitle: string;
  timelineSubtitle: string;
  timelineShowAll: (count: number) => string;
  timelineCollapse: string;
  timelineNoDelta: string;
  deltaTitle: string;
  deltaSubtitle: string;
  deltaShowAll: (count: number) => string;
  deltaCollapse: string;
  deltaEmpty: string;
}

export interface NoticesTranslations {
  projectCreated: string;
  projectCreateFailed: string;
  projectLoadFailed: string;
  projectListLoadFailed: string;
  searchFailed: string;
  integrityFailed: string;
  integrityValid: (count: number) => string;
  integrityCorrupted: (index: number) => string;
  exportStarted: string;
  exportFailed: string;
  canvasSaved: (ref: string) => string;
  canvasSaveFailed: string;
  deriveRouteSelectElement: string;
  deriveRouteProvideTitle: string;
  deriveRouteSuccess: string;
  deriveRouteFailed: string;
  derivedRouteDesc: string;
}

export interface AppTranslations {
  sidebar: SidebarTranslations;
  controlPlane: ControlPlaneTranslations;
  authGate: AuthGateTranslations;
  explorer: ExplorerTranslations;
  notices: NoticesTranslations;
}

export const translations: Record<SupportedLanguage, AppTranslations> = {
  en: {
    sidebar: {
      ariaLabel: "Project list",
      brandSubtitle: "Schema Sandbox",
      constitution:
        "Experimental mathematics sandbox. UNRESOLVED is a valid outcome; does not automatically declare problems solved.",
      researchProjects: "Research Projects",
      emptyCopy: "No projects yet. Create a research workspace or import from the workbench.",
      newProject: "New Project",
      projectTitleAria: "Project title",
      projectTitlePlaceholder: "Title",
      originalProblemAria: "Original problem statement",
      originalProblemPlaceholder: "Original problem (will not be overridden by sub-goals)",
      notesAria: "Researcher notes",
      notesPlaceholder: "Notes (optional)",
      createButton: "Create Project",
      creatingButton: "Creating…",
      sidebarRule:
        "Event streams are canonical. SQLite, route maps, and timelines are fully reconstructible.",
      workbenchLink: "Main Workbench → /prototype/",
      langSwitcher: "Language",
    },
    controlPlane: {
      ariaLabel: "Alpha 5 Research Control Plane",
      heading: "Canonical Research State",
      meta: (rev: string | number, proposals: number, claims: number, evidence: number) =>
        `Revision ${rev} · Proposals ${proposals} · Claims ${claims} · Evidence ${evidence}`,
      statusNote: "State can only be written back by accepted transitions",
      planeCards: {
        operational: { name: "operational", desc: "Reconstructible plane summary" },
        epistemic: { name: "epistemic", desc: "Reconstructible plane summary" },
        claim: { name: "claim", desc: "Claims keep unresolved/candidate separation" },
        artifact: { name: "artifact", desc: "Reconstructible plane summary" },
      },
      viewProposalDetails: "View proposal details",
      proposalSummary: (id: string, status: string) => `Proposal ${id} · ${status}`,
      proposalMeta: (trigger: string, created: string, obligations: number, handoffs: number) =>
        `Trigger ${trigger} · Created ${created} · Next obligations ${obligations} · Handoffs ${handoffs}`,
      claimEvidenceSummary: (claims: number, evidence: number) =>
        `Claims & Evidence (${claims} / ${evidence})`,
      openObligations: (count: number) => `Open obligations: ${count}`,
    },
    authGate: {
      title: "API Authentication",
      defaultDesc: "Production mode requires an API key. Keys are saved only in this browser session.",
      placeholder: "Enter one key from PROOFFLOW_API_KEYS",
      connectButton: "Connect API",
      bannerMessage:
        "API Key required (401/403). Keys are saved only in this browser session and shared with the workbench.",
    },
    explorer: {
      loadingAria: "Loading",
      welcomeTitle: "Explorer Studio (Case Demo)",
      welcomeDesc:
        "Dual-canvas for exploring route maps, freehand sketches, historical search, and epistemic deltas. To use the full system and experiment controls, use the Main Workbench.",
      capabilityList: [
        {
          bold: "This Page (Explorer Demo)",
          text: "Graph reading, sketch snapshots, search, Claim/Evidence summary, project creation, export.",
        },
        {
          bold: "Main Workbench",
          linkText: "/prototype/",
          text: "Primary workspace: change route states, challenges, bridge results, dead ends, checkpoints, Python plugins, and session imports.",
        },
      ],
      welcomeHint:
        "You can switch back to the Main Workbench at any time using the link in the sidebar. If auth is enabled in production, configure API Key first.",
      exportButton: "Export .smath.zip",
      integrityButton: "Verify Event Chain",
      openWorkbench: "Open Main Workbench →",
      openWorkbenchTitle: "Edit routes, challenges, and checkpoints in Main Workbench",
      searchLabel: "Historical Routes & Dead-End Assets",
      searchPlaceholder: "Search dead ends, bridge results, challenges, or revival conditions",
      searchButton: "Search",
      searchEmpty: "No matching historical routes, challenges, or bridge results found.",
      routesStat: "Routes",
      openChallengesStat: "Open Challenges",
      bridgesStat: "Bridge Results",
      eventsStat: "Events",
      routePanelTitle: "Research Route Map",
      routePanelDesc: "Routes, branches, challenges, and bridge artifacts",
      nodeDetailEmpty: "Click a node on the route map to view full description, challenges, or bridge summaries",
      nodeDetailNone: "No detail description available for this node.",
      sketchPanelTitle: "Freehand Sketch",
      sketchPanelDesc: "Immutable snapshot created on every save",
      saveSnapshot: "Save Snapshot",
      savingSnapshot: "Saving…",
      sketchLoading: "Loading freehand sketch…",
      authorNoteLabel: "Author Notes",
      authorNotePlaceholder: "Describe the research intent of selected sketch elements",
      canvasNoteHint:
        "Derived routes will use the author notes as the new route title. Original sketch remains an immutable artifact.",
      deriveRouteButton: "Derive Route from Selection",
      deriveRouteTooltipNoSelection: "Please select at least one element on the sketch canvas first",
      deriveRouteTooltipNoNote: "Please provide author notes as the derived route title first",
      deriveRouteTooltipReady: "Create a derived route from selected elements",
      timelineTitle: "Observable Timeline",
      timelineSubtitle: "Click to locate route node",
      timelineShowAll: (count: number) => `View all ${count} events`,
      timelineCollapse: "Collapse",
      timelineNoDelta: "Event recorded, no state delta note",
      deltaTitle: "What Changed This Round",
      deltaSubtitle: "Excluded events without state changes",
      deltaShowAll: (count: number) => `View all ${count} items`,
      deltaCollapse: "Collapse",
      deltaEmpty: "No epistemic deltas to display yet.",
    },
    notices: {
      projectCreated: "Project created successfully",
      projectCreateFailed: "Failed to create project",
      projectLoadFailed: "Failed to load project",
      projectListLoadFailed: "Failed to load project list",
      searchFailed: "Historical search failed",
      integrityFailed: "Integrity check failed",
      integrityValid: (count: number) => `Event chain intact: ${count} events`,
      integrityCorrupted: (index: number) =>
        `Event chain corrupted at index ${index}. Project is in read-only recovery mode.`,
      exportStarted: "Export download started",
      exportFailed: "Export failed",
      canvasSaved: (ref: string) => `Canvas snapshot saved, artifact ${ref}`,
      canvasSaveFailed: "Failed to save canvas snapshot",
      deriveRouteSelectElement: "Please select at least one element in the freehand sketch first.",
      deriveRouteProvideTitle: "Please enter author notes to serve as the derived route title.",
      deriveRouteSuccess: "Derived route created. Original sketch remains intact as an immutable artifact.",
      deriveRouteFailed: "Failed to create derived route",
      derivedRouteDesc: "Derived from freehand sketch elements. Original sketch preserved as immutable content-addressed artifact.",
    },
  },
  zh: {
    sidebar: {
      ariaLabel: "项目列表",
      brandSubtitle: "Schema Sandbox",
      constitution:
        "实验数学沙盒。UNRESOLVED 是有效结果，不自动宣称问题已解决。",
      researchProjects: "研究项目",
      emptyCopy: "尚无项目。先创建研究空间，或到工作台导入。",
      newProject: "新建项目",
      projectTitleAria: "项目标题",
      projectTitlePlaceholder: "标题",
      originalProblemAria: "原始问题",
      originalProblemPlaceholder: "原始问题（不会被工作目标覆盖）",
      notesAria: "研究者备注",
      notesPlaceholder: "备注（可选）",
      createButton: "创建项目",
      creatingButton: "创建中…",
      sidebarRule:
        "事件流为规范记录。SQLite、路线图和时间线均可重建。",
      workbenchLink: "主工作台 → /prototype/",
      langSwitcher: "语言",
    },
    controlPlane: {
      ariaLabel: "Alpha 5 研究控制面板",
      heading: "规范研究状态",
      meta: (rev: string | number, proposals: number, claims: number, evidence: number) =>
        `修订 ${rev} · 提案 ${proposals} · Claim ${claims} · Evidence ${evidence}`,
      statusNote: "状态只能由已接受 transition 写回",
      planeCards: {
        operational: { name: "operational", desc: "可重建平面摘要" },
        epistemic: { name: "epistemic", desc: "可重建平面摘要" },
        claim: { name: "claim", desc: "Claim 保持未决/候选分离" },
        artifact: { name: "artifact", desc: "可重建平面摘要" },
      },
      viewProposalDetails: "查看提案详情",
      proposalSummary: (id: string, status: string) => `提案 ${id} · ${status}`,
      proposalMeta: (trigger: string, created: string, obligations: number, handoffs: number) =>
        `触发 ${trigger} · 创建于 ${created} · 下步义务 ${obligations} · 交接 ${handoffs}`,
      claimEvidenceSummary: (claims: number, evidence: number) =>
        `Claim 与 Evidence（${claims} / ${evidence}）`,
      openObligations: (count: number) => `开放义务 ${count} 条`,
    },
    authGate: {
      title: "API 认证",
      defaultDesc: "生产模式需要 API key；密钥只保存在本次浏览器会话中。",
      placeholder: "输入 PROOFFLOW_API_KEYS 中的一个 key",
      connectButton: "连接 API",
      bannerMessage:
        "请求需要 API Key（401/403）。密钥只保存在本次浏览器会话，与工作台共享。",
    },
    explorer: {
      loadingAria: "正在加载",
      welcomeTitle: "探索台（案例演示）",
      welcomeDesc:
        "双画布用于浏览路线图、自由草图、历史检索与认知增量演示。若需使用完整核心研究功能与工具，请进入主工作台。",
      capabilityList: [
        {
          bold: "本页（探索台演示）",
          text: "读图、草图快照、搜索、Claim/Evidence 摘要、建项目、导出。",
        },
        {
          bold: "主工作台（完整模型）",
          linkText: "/prototype/",
          text: "核心工作区：改路线状态、挑战、桥接、死胡同、检查点、Python 插件与会话导入。",
        },
      ],
      welcomeHint:
        "随时可通过左下角或顶部的「主工作台」返回核心工作区。生产环境若启用鉴权，请先配置 API Key。",
      exportButton: "导出 .smath.zip",
      integrityButton: "检查事件链",
      openWorkbench: "打开主工作台 →",
      openWorkbenchTitle: "在主工作台中编辑路线、挑战与检查点",
      searchLabel: "历史路线与失败资产",
      searchPlaceholder: "检索死路、桥接结果、挑战或复活条件",
      searchButton: "检索",
      searchEmpty: "未找到匹配的历史路线、挑战或桥接结果。",
      routesStat: "路线",
      openChallengesStat: "开放挑战",
      bridgesStat: "桥接结果",
      eventsStat: "事件",
      routePanelTitle: "研究路线图",
      routePanelDesc: "路线、分支、挑战和桥接工件",
      nodeDetailEmpty: "点击路线图节点查看完整描述、质疑或桥接摘要",
      nodeDetailNone: "该节点暂无详情说明。",
      sketchPanelTitle: "自由草图",
      sketchPanelDesc: "每次保存都创建不可变快照",
      saveSnapshot: "保存快照",
      savingSnapshot: "保存中",
      sketchLoading: "正在加载自由草图",
      authorNoteLabel: "作者说明",
      authorNotePlaceholder: "说明所选草图元素的研究含义",
      canvasNoteHint:
        "派生路线会使用作者说明作为新路线标题；保存快照后原草图保持为不可变工件。",
      deriveRouteButton: "从所选元素建立派生路线",
      deriveRouteTooltipNoSelection: "请先在自由草图中框选至少一个元素",
      deriveRouteTooltipNoNote: "请先填写作者说明作为派生路线标题",
      deriveRouteTooltipReady: "从所选元素建立派生路线",
      timelineTitle: "可观察时间线",
      timelineSubtitle: "点击定位到路线节点",
      timelineShowAll: (count: number) => `查看全部 ${count} 条`,
      timelineCollapse: "收起",
      timelineNoDelta: "事件已记录，无状态增量说明",
      deltaTitle: "本轮改变了什么",
      deltaSubtitle: "已排除无状态变化事件",
      deltaShowAll: (count: number) => `查看全部 ${count} 条`,
      deltaCollapse: "收起",
      deltaEmpty: "尚无可展开的认识增量。",
    },
    notices: {
      projectCreated: "项目已创建",
      projectCreateFailed: "项目创建失败",
      projectLoadFailed: "项目加载失败",
      projectListLoadFailed: "项目列表加载失败",
      searchFailed: "历史检索失败",
      integrityFailed: "完整性检查失败",
      integrityValid: (count: number) => `事件链完整：${count} 条事件`,
      integrityCorrupted: (index: number) =>
        `事件链在 ${index} 处损坏，项目进入只读恢复`,
      exportStarted: "导出已开始下载",
      exportFailed: "导出失败",
      canvasSaved: (ref: string) => `画布快照已保存，工件 ${ref}`,
      canvasSaveFailed: "画布保存失败",
      deriveRouteSelectElement: "请先在自由草图中选择至少一个元素。",
      deriveRouteProvideTitle: "请先填写作者说明，作为派生路线标题。",
      deriveRouteSuccess: "派生路线已建立，草图原件未被覆盖。",
      deriveRouteFailed: "派生路线创建失败",
      derivedRouteDesc: "由自由草图元素派生。原始草图保持为不可变内容寻址工件。",
    },
  },
};
