const API = "/api/v1";
const API_KEY_STORAGE_KEY = "proofflow_api_key";
const LANG_STORAGE_KEY = "proofflow_lang";

const LABELS_ZH = {
  SEED: "种子", ACTIVE: "进行中", CHALLENGED: "被挑战", CONDITIONAL: "有条件",
  DORMANT: "休眠", REVIVED: "已复活", BRIDGE_RESULT: "桥接结果", SUPERSEDED: "已被替代",
  COMPLETED: "完成", OPEN: "开放", RESOLVED: "已解决", DISMISSED: "已驳回", IN_PROGRESS: "处理中",
  OBJECTION: "异议", COUNTEREXAMPLE_SEARCH: "反例搜索", SOURCE_CHECK: "来源核查",
  QUANTIFIER_CHECK: "量词检查", FORMALIZATION_TEST: "形式化检验",
  COMPUTATIONAL_TEST: "计算检验", BOUNDARY_CASE: "边界情形", OTHER: "其他",
  GENERAL: "一般", INTUITION: "直觉", DEFINITION: "定义", COUNTEREXAMPLE: "反例",
  ROUTE_PRIORITY: "路线优先级", SIMPLIFICATION_GOAL: "简化目标", REDIRECT: "转向",
  TEXT: "文本", IMAGE: "图像", HAND_DRAWING: "手绘草图", CODE: "代码", GRAPH: "图",
  PROOF_SOURCE: "证明源", MODEL_NOTE: "模型笔记", RESEARCH_CHECKPOINT: "研究检查点",
  CHALLENGE: "挑战", NEW_BRANCH: "新分支", IGNORE: "忽略", OBSERVED: "已观察",
};

const LABELS_EN = {
  SEED: "Seed", ACTIVE: "Active", CHALLENGED: "Challenged", CONDITIONAL: "Conditional",
  DORMANT: "Dormant", REVIVED: "Revived", BRIDGE_RESULT: "Bridge Result", SUPERSEDED: "Superseded",
  COMPLETED: "Completed", OPEN: "Open", RESOLVED: "Resolved", DISMISSED: "Dismissed", IN_PROGRESS: "In Progress",
  OBJECTION: "Objection", COUNTEREXAMPLE_SEARCH: "Counterexample Search", SOURCE_CHECK: "Source Check",
  QUANTIFIER_CHECK: "Quantifier Check", FORMALIZATION_TEST: "Formalization Test",
  COMPUTATIONAL_TEST: "Computational Test", BOUNDARY_CASE: "Boundary Case", OTHER: "Other",
  GENERAL: "General", INTUITION: "Intuition", DEFINITION: "Definition", COUNTEREXAMPLE: "Counterexample",
  ROUTE_PRIORITY: "Route Priority", SIMPLIFICATION_GOAL: "Simplification Goal", REDIRECT: "Redirect",
  TEXT: "Text", IMAGE: "Image", HAND_DRAWING: "Freehand Sketch", CODE: "Code", GRAPH: "Graph",
  PROOF_SOURCE: "Proof Source", MODEL_NOTE: "Model Note", RESEARCH_CHECKPOINT: "Research Checkpoint",
  CHALLENGE: "Challenge", NEW_BRANCH: "New Branch", IGNORE: "Ignore", OBSERVED: "Observed",
};

const UI_TEXT = {
  en: {
    topbarTitle: "ProofFlow Workbench",
    topbarSubtitle: "Main Workbench · Branches, challenges, bridge results, chat imports, and on-demand Python experiments.",
    explorerLink: "Explorer (Demo) →",
    apiKeySummary: "API Key",
    apiKeyLabel: "Session API Key (shared with Explorer)",
    apiKeyPlaceholder: "Required in production to authorize requests",
    save: "Save",
    clear: "Clear",
    cancel: "Cancel",
    confirm: "Confirm",
    apiKeyNote: "Keys are saved only in this browser session. Without key in production fail-closed mode, writes are rejected.",
    healthConnecting: "Connecting…",
    healthUnavailable: "Local service unavailable",
    healthOk: (ver) => `Local service ${ver}`,
    projectsHeading: "Projects",
    refresh: "Refresh",
    noProjects: "No projects yet. Create one above.",
    newProjectSummary: "New Experiment Project",
    labelProjectTitle: "Title",
    placeholderTitle: "e.g. A combinatorial structure conjecture",
    labelOriginalProblem: "Original Problem",
    placeholderProblem: "Preserves the original problem; will not be overridden by sub-goals",
    labelResearcherNotes: "Researcher Notes",
    placeholderNotes: "Known background, intuition, boundaries",
    createProjectBtn: "Create Project",
    constitutionTitle: "Experimental Constitution",
    constitutionItems: [
      "No guaranteed solution",
      "Objections are easy; closures are hard",
      "Failures and bridge results are reusable",
      "Imported content requires human confirmation",
      "Tools enabled on-demand",
    ],
    emptyHeading: "Select or Create a Project",
    emptyDesc: "Unify visible model dialogues, research branches, challenges, and tool experiments into a single event trajectory.",
    integrityBtn: "Verify Event Chain",
    exportBtn: "Export .smath.zip",
    researchPacketBtn: "Generate Research Packet",
    routeGraphHeading: "Route & Branch Graph",
    newRouteBtn: "New Route",
    newBranchBtn: "New Branch",
    splitRouteBtn: "Split Selected Route",
    mergeRoutesBtn: "Merge Routes",
    routeDetailsDefault: "Click a route or branch to view details and status.",
    routeBranchOverflow: (n) => `Showing up to 3 branches per route in graph; ${n} other branch(es) hidden.`,
    noRoutesSvg: "No routes yet. Create distinct thinking paths first.",
    sketchHeading: "Freehand Sketch",
    clearSketch: "Clear",
    saveSketch: "Save as Artifact",
    sketchNote: "Original sketches are permanently retained. Structured interpretations from LLMs or tools are derived objects.",
    challengeSectionHeading: "Challenges: Easy to Raise, Don't Auto-Kill Routes",
    labelChallengeRoute: "Route",
    labelChallengeBranch: "Branch (Optional)",
    labelChallengeType: "Type",
    labelChallengeStatement: "Objection or Question",
    labelChallengeTestPlan: "Proposed Test Plan",
    openChallengeBtn: "Open Challenge",
    noChallenges: "No challenges yet.",
    bridgeSectionHeading: "Bridge Results & Known Dead Ends",
    labelBridgeRoute: "Route",
    labelBridgeBranch: "Branch (Optional)",
    labelBridgeTitle: "Title",
    labelBridgeSummary: "Summary",
    labelBridgeRetainedValue: "Retained Value (one per line)",
    saveBridgeBtn: "Save Bridge Result",
    deadEndSummary: "Record Known Dead End",
    labelDeadEndRoute: "Route",
    labelDeadEndTitle: "Title",
    labelDeadEndDesc: "Obstacle Description",
    labelDeadEndReopen: "Reopening Conditions (one per line)",
    saveDeadEndBtn: "Save Dead End Constraint",
    bridgesHeading: "Bridge Results",
    deadEndsHeading: "Known Dead Ends",
    noBridges: "No bridge results yet.",
    noDeadEnds: "No explicit dead-end constraints yet.",
    checkpointSectionHeading: "Research Checkpoint",
    labelCheckpointTarget: "Current Target",
    labelCheckpointRoute: "Route",
    labelCheckpointBranch: "Branch (Optional)",
    labelCheckpointIntended: "Intended Move",
    labelCheckpointObserved: "Observed Failure or Gain",
    labelCheckpointObligations: "Unresolved Obligations (one per line)",
    saveCheckpointBtn: "Save Checkpoint",
    noCheckpoints: "No structured checkpoints yet.",
    chatImportHeading: "ChatGPT Companion Import",
    chatImportPill: "Human Confirmation Required",
    chatImportDesc: "Supports Markdown, HTML, JSON, and plain text. Imports generate previews and are not auto-promoted to conclusions.",
    labelChatImportFile: "Dialogue File",
    parseChatBtn: "Parse Dialogue",
    noChatImports: "No dialogues imported yet.",
    pythonPluginHeading: "On-Demand Python Experiment Plugin",
    pythonPluginWarning: "This environment provides process-level isolation, not an OS sandbox. Run only trusted code.",
    enablePythonBtn: "Enable Plugin",
    pythonEnabled: "Python Enabled",
    labelPythonRoute: "Linked Route",
    labelPythonBranch: "Linked Branch",
    labelPythonCode: "Python Code",
    labelPythonTimeout: "Timeout (seconds)",
    runExperimentBtn: "Run Experiment",
    noPluginRuns: "No tool runs yet.",
    humanNoteHeading: "Human Hot-Insertion",
    labelNoteRoute: "Linked Route",
    labelNoteBranch: "Linked Branch",
    labelNoteType: "Type",
    labelNoteContent: "Content",
    addNoteBtn: "Add to Trajectory",
    uploadArtifactHeading: "Upload Artifact",
    labelArtifactFile: "File",
    labelArtifactType: "Artifact Type",
    saveArtifactBtn: "Save Original Artifact",
    noArtifacts: "No artifacts yet.",
    timelineHeading: "Observable Research Trajectory",
    noEvents: "No events recorded yet.",
    // Dialogs
    dialogNewRouteTitle: "New Route",
    dialogRouteTitleLabel: "Title",
    dialogRouteDescLabel: "Description",
    dialogRouteStateLabel: "Initial State",
    dialogNewBranchTitle: "New Branch",
    dialogBranchRouteLabel: "Parent Route",
    dialogBranchTitleLabel: "Title",
    dialogBranchDescLabel: "Description",
    dialogBranchStateLabel: "Initial State",
    stateDialogTitle: "Change State",
    stateReasonLabel: "Reason (must describe this state transition)",
    stateReasonPlaceholder: "Why transition to this state? What evidence and obligations are involved?",
    dialogStateConfirm: "Confirm Change",
    dialogSplitTitle: "Split Selected Route",
    dialogSplitChildrenLabel: "Sub-route titles (one per line, at least two)",
    dialogSplitReasonLabel: "Reason for split",
    dialogSplitExecute: "Execute Split",
    dialogMergeTitle: "Merge Routes",
    dialogMergeSelectLabel: "Select routes to merge (at least two)",
    dialogMergeTitleLabel: "New Unified Route Title",
    dialogMergeReasonLabel: "Basis for Merge",
    dialogMergeCreate: "Create Unified Route",
    dialogPacketHeading: "Research Packet",
    copyPacket: "Copy to Clipboard",
    dialogChatImportHeading: "Candidate Nodes from Dialogue",
    dialogChatImportHint: "Each candidate defaults to a Model Note. You may change to Challenge, Bridge Result, New Branch, Checkpoint, or Ignore.",
    confirmChatImport: "Confirm Selected Nodes",
    // Options
    projectLevel: "Project-level",
    routeLevel: "Route-level",
    selectRoutePrompt: "Please select a route",
    noBranch: "No branch",
    noneOrRouteLevel: "None / Route-level",
    // Notifications
    projectCreated: "Project created",
    routeCreated: "Route created",
    branchCreated: "Branch created",
    stateUpdated: "State updated",
    routeSplit: "Route split; source route preserved",
    routesMerged: "Unified route created; source routes marked as SUPERSEDED with history preserved",
    challengeOpened: "Challenge opened; route preserved",
    bridgeSaved: "Bridge result saved",
    deadEndSaved: "Dead end & reopening conditions saved",
    checkpointSaved: "Research Checkpoint saved",
    noteSaved: "Researcher note added to trajectory",
    artifactSaved: "Artifact saved by content hash",
    sketchSaved: "Sketch saved as original artifact",
    chatImportConfirmed: "Dialogue nodes entered trajectory per human selection",
    pythonPluginEnabled: "Python plugin enabled for current project",
    pythonRunFinished: (status) => `Python experiment finished: ${status}`,
    packetCopied: "Research Packet copied to clipboard",
    exportStarted: "Export download started",
    apiKeySaved: "Session API Key saved",
    apiKeyCleared: "Session API Key cleared",
    needApiKeyAuth: (status, detail) => `Authentication rejected (${status}): Please configure API Key in topbar first. ${detail}`,
    authWriteSessionError: "Cannot write to session storage; this mode may still require an API key.",
    moreHidden: (n) => `${n} more not shown.`,
    showAll: "Show all",
    collapse: "Collapse",
  },
  zh: {
    topbarTitle: "ProofFlow 工作台",
    topbarSubtitle: "主工作台 · 分支、挑战、桥接结果、会话导入与按需 Python 实验。",
    explorerLink: "探索台 (案例演示) →",
    apiKeySummary: "API Key",
    apiKeyLabel: "会话内 API Key（与探索台共享）",
    apiKeyPlaceholder: "生产模式需要并用于授权请求",
    save: "保存",
    clear: "清除",
    cancel: "取消",
    confirm: "确认",
    apiKeyNote: "密钥仅保存在本次浏览器会话中。生产 fail-closed 下无 Key 时写入会被拒绝。",
    healthConnecting: "连接中…",
    healthUnavailable: "本地服务不可用",
    healthOk: (ver) => `本地服务 ${ver}`,
    projectsHeading: "项目",
    refresh: "刷新",
    noProjects: "还没有项目。先在上方创建。",
    newProjectSummary: "新建实验项目",
    labelProjectTitle: "标题",
    placeholderTitle: "例如：某个组合结构猜想",
    labelOriginalProblem: "原始问题",
    placeholderProblem: "保存原始问题，不会被工作目标覆盖",
    labelResearcherNotes: "研究者备注",
    placeholderNotes: "已知背景、直觉、边界",
    createProjectBtn: "创建项目",
    constitutionTitle: "实验宪法",
    constitutionItems: [
      "不保证解答",
      "异议容易，关闭困难",
      "失败与桥接结果都可复用",
      "导入内容必须由人类确认",
      "工具按需启用",
    ],
    emptyHeading: "选择或创建一个项目",
    emptyDesc: "将可见模型会话、研究分支、挑战和工具实验纳入同一条事件轨迹。",
    integrityBtn: "检查事件链",
    exportBtn: "导出 .smath.zip",
    researchPacketBtn: "生成 Research Packet",
    routeGraphHeading: "路线与分支图",
    newRouteBtn: "新建路线",
    newBranchBtn: "新建分支",
    splitRouteBtn: "拆分选中路线",
    mergeRoutesBtn: "合并路线",
    routeDetailsDefault: "点击路线或分支查看状态。",
    routeBranchOverflow: (n) => `图内每个路线只展示最近 3 条分支，另有 ${n} 条分支未在图内显示。`,
    noRoutesSvg: "尚无路线。先建立几条不同的思考路径。",
    sketchHeading: "自由草图",
    clearSketch: "清空",
    saveSketch: "保存为工件",
    sketchNote: "原始草图永久保留；LLM 或专业工具的结构化解释只是派生对象。",
    challengeSectionHeading: "挑战：易提出，不自动杀路线",
    labelChallengeRoute: "路线",
    labelChallengeBranch: "分支（可选）",
    labelChallengeType: "类型",
    labelChallengeStatement: "异议或问题",
    labelChallengeTestPlan: "建议检验",
    openChallengeBtn: "打开挑战",
    noChallenges: "暂无挑战。",
    bridgeSectionHeading: "桥接结果与已知死路",
    labelBridgeRoute: "路线",
    labelBridgeBranch: "分支（可选）",
    labelBridgeTitle: "标题",
    labelBridgeSummary: "摘要",
    labelBridgeRetainedValue: "保留价值（每行一项）",
    saveBridgeBtn: "保存桥接结果",
    deadEndSummary: "记录已知死路",
    labelDeadEndRoute: "路线",
    labelDeadEndTitle: "标题",
    labelDeadEndDesc: "障碍描述",
    labelDeadEndReopen: "重新开放条件（每行一项）",
    saveDeadEndBtn: "保存死路约束",
    bridgesHeading: "桥接结果",
    deadEndsHeading: "已知死路",
    noBridges: "暂无桥接结果。",
    noDeadEnds: "暂无明确死路约束。",
    checkpointSectionHeading: "Research Checkpoint",
    labelCheckpointTarget: "当前目标",
    labelCheckpointRoute: "路线",
    labelCheckpointBranch: "分支（可选）",
    labelCheckpointIntended: "准备做什么",
    labelCheckpointObserved: "本轮失败或收获",
    labelCheckpointObligations: "未完成义务（每行一项）",
    saveCheckpointBtn: "保存检查点",
    noCheckpoints: "暂无结构化检查点。",
    chatImportHeading: "ChatGPT Companion Import",
    chatImportPill: "人工确认后入图",
    chatImportDesc: "支持 Markdown、HTML、JSON 和纯文本。导入只生成预览，不会自动提升为研究结论。",
    labelChatImportFile: "会话文件",
    parseChatBtn: "解析会话",
    noChatImports: "尚未导入会话。",
    pythonPluginHeading: "按需 Python 实验插件",
    pythonPluginWarning: "本环境仅提供进程级隔离，不是 OS 安全沙箱。只运行你信任的代码。",
    enablePythonBtn: "启用 Python 插件",
    pythonEnabled: "Python 已启用",
    labelPythonRoute: "关联路线",
    labelPythonBranch: "关联分支",
    labelPythonCode: "Python 代码",
    labelPythonTimeout: "时限（秒）",
    runExperimentBtn: "运行实验",
    noPluginRuns: "暂无工具运行。",
    humanNoteHeading: "人类热插入",
    labelNoteRoute: "关联路线",
    labelNoteBranch: "关联分支",
    labelNoteType: "类型",
    labelNoteContent: "内容",
    addNoteBtn: "加入研究轨迹",
    uploadArtifactHeading: "上传工件",
    labelArtifactFile: "文件",
    labelArtifactType: "工件类型",
    saveArtifactBtn: "保存原始工件",
    noArtifacts: "暂无工件。",
    timelineHeading: "可观察研究轨迹",
    noEvents: "暂无事件记录。",
    // Dialogs
    dialogNewRouteTitle: "新建路线",
    dialogRouteTitleLabel: "标题",
    dialogRouteDescLabel: "说明",
    dialogRouteStateLabel: "初始状态",
    dialogNewBranchTitle: "新建分支",
    dialogBranchRouteLabel: "所属路线",
    dialogBranchTitleLabel: "标题",
    dialogBranchDescLabel: "说明",
    dialogBranchStateLabel: "初始状态",
    stateDialogTitle: "更改状态",
    stateReasonLabel: "原因（必须说明本次状态变化）",
    stateReasonPlaceholder: "为什么进入该状态？含哪些证据与义务？",
    dialogStateConfirm: "确认更改",
    dialogSplitTitle: "拆分选中路线",
    dialogSplitChildrenLabel: "子路线标题（每行一条，至少两条）",
    dialogSplitReasonLabel: "为什么需要拆分",
    dialogSplitExecute: "执行拆分",
    dialogMergeTitle: "合并路线",
    dialogMergeSelectLabel: "选择要合并的路线（至少两条）",
    dialogMergeTitleLabel: "新的综合路线标题",
    dialogMergeReasonLabel: "合并依据",
    dialogMergeCreate: "创建综合路线",
    dialogPacketHeading: "Research Packet",
    copyPacket: "复制到剪贴板",
    dialogChatImportHeading: "会话候选节点",
    dialogChatImportHint: "每条候选默认只是模型笔记。你可以改成挑战、桥接结果、新分支或检查点，也可以忽略。",
    confirmChatImport: "确认所选节点",
    // Options
    projectLevel: "项目级",
    routeLevel: "路线级",
    selectRoutePrompt: "请选择路线",
    noBranch: "无分支",
    noneOrRouteLevel: "无 / 路线级",
    // Notifications
    projectCreated: "项目已创建",
    routeCreated: "路线已创建",
    branchCreated: "分支已创建",
    stateUpdated: "状态已更新",
    routeSplit: "路线已拆分，源路线仍被保留",
    routesMerged: "综合路线已创建；原路线被标记为 SUPERSEDED，但历史仍保留",
    challengeOpened: "挑战已打开；路线仍然保留",
    bridgeSaved: "桥接结果已保存",
    deadEndSaved: "已保存死路与重新开放条件",
    checkpointSaved: "Research Checkpoint 已保存",
    noteSaved: "研究者输入已加入轨迹",
    artifactSaved: "工件已按内容哈希保存",
    sketchSaved: "草图已保存为原始工件",
    chatImportConfirmed: "会话节点已按人工选择进入研究轨迹",
    pythonPluginEnabled: "Python 插件已为当前项目启用",
    pythonRunFinished: (status) => `Python 实验结束：${status}`,
    packetCopied: "已复制 Research Packet",
    exportStarted: "导出已开始下载",
    apiKeySaved: "已保存会话内 API Key",
    apiKeyCleared: "已清除会话内 API Key",
    needApiKeyAuth: (status, detail) => `认证被拒绝（${status}）：请先在顶栏「API Key」中配置密钥。${detail}`,
    authWriteSessionError: "无法写入会话存储；本模式可能仍需密钥",
    moreHidden: (n) => `还有 ${n} 条未显示。`,
    showAll: "显示全部",
    collapse: "收起",
  },
};

function getInitialLanguage() {
  try {
    const saved = localStorage.getItem(LANG_STORAGE_KEY);
    if (saved === "en" || saved === "zh") return saved;
    const browser = navigator.language?.toLowerCase() ?? "";
    if (browser.startsWith("zh")) return "zh";
  } catch {}
  return "en";
}

function saveLanguage(lang) {
  try {
    localStorage.setItem(LANG_STORAGE_KEY, lang);
    window.dispatchEvent(new CustomEvent("proofflow-lang-change", { detail: lang }));
  } catch {}
}

const state = {
  lang: getInitialLanguage(),
  projects: [], currentProject: null, routes: [], branches: [], challenges: [],
  bridges: [], deadEnds: [], checkpoints: [], events: [], artifacts: [],
  chatImports: [], plugins: [], projectPlugins: [], pluginRuns: [],
  selectedNode: null, currentChatPreview: null, pendingState: null, busy: false,
  expand: { challenges: false, bridges: false, deadEnds: false, checkpoints: false,
    chatImports: false, pluginRuns: false, artifacts: false, events: false },
};

function t() {
  return UI_TEXT[state.lang] || UI_TEXT.zh;
}

function labelOf(value) {
  if (!value) return "";
  const table = state.lang === "en" ? LABELS_EN : LABELS_ZH;
  return table[value] || String(value).replaceAll("_", " ");
}

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];
const projectList = $("#projectList");
const workspace = $("#projectWorkspace");
const emptyState = $("#emptyState");
const toast = $("#toast");
const busyLabel = $("#projectBusy");

function storedApiKey() {
  try { return window.sessionStorage.getItem(API_KEY_STORAGE_KEY) ?? ""; } catch { return ""; }
}

function notify(message, error = false) {
  toast.textContent = message;
  toast.style.background = error ? "#8e2732" : "#1d2433";
  toast.setAttribute("role", error ? "alert" : "status");
  toast.classList.remove("hidden");
  clearTimeout(notify._timer);
  notify._timer = setTimeout(() => toast.classList.add("hidden"), 3600);
}

async function api(path, options = {}) {
  const headers = new Headers(options.headers || {});
  const apiKey = storedApiKey();
  if (apiKey) headers.set("X-API-Key", apiKey);
  const response = await fetch(`${API}${path}`, { ...options, headers });
  if (!response.ok) {
    let detail = `${response.status} ${response.statusText}`;
    try { detail = (await response.json()).detail ?? detail; } catch {}
    if (response.status === 401 || response.status === 403) {
      throw new Error(t().needApiKeyAuth(response.status, detail));
    }
    throw new Error(detail);
  }
  const type = response.headers.get("content-type") || "";
  return type.includes("application/json") ? response.json() : response;
}

async function checkHealth() {
  try {
    const response = await fetch("/health");
    const data = await response.json();
    $("#healthStatus").textContent = t().healthOk(data.version);
  } catch {
    $("#healthStatus").textContent = t().healthUnavailable;
  }
}

function setProjectBusy(value) {
  state.busy = value;
  busyLabel.classList.toggle("hidden", !value);
  renderProjects();
}

async function loadProjects() {
  state.projects = await api("/projects");
  renderProjects();
}

function renderProjects() {
  projectList.innerHTML = "";
  if (!state.projects.length) {
    projectList.innerHTML = `<p class="muted">${t().noProjects}</p>`;
    return;
  }
  for (const project of state.projects) {
    const card = document.createElement("button");
    card.type = "button";
    card.className = `project-card ${state.currentProject?.project_id === project.project_id ? "active" : ""}`;
    card.disabled = state.busy;
    const dateStr = new Date(project.updated_at).toLocaleString(state.lang === "en" ? "en-US" : "zh-CN");
    card.innerHTML = `<strong>${escapeHtml(project.title)}</strong><small>${dateStr}</small>`;
    card.addEventListener("click", () => selectProject(project.project_id));
    projectList.appendChild(card);
  }
}

async function selectProject(projectId) {
  if (state.busy) return;
  setProjectBusy(true);
  try {
    state.currentProject = await api(`/projects/${projectId}`);
    const results = await Promise.all([
      api(`/projects/${projectId}/routes`),
      api(`/projects/${projectId}/branches`),
      api(`/projects/${projectId}/challenges`),
      api(`/projects/${projectId}/bridge-results`),
      api(`/projects/${projectId}/dead-ends`),
      api(`/projects/${projectId}/checkpoints?limit=20`),
      api(`/projects/${projectId}/events`),
      api(`/projects/${projectId}/artifacts`),
      api(`/projects/${projectId}/chat-imports`),
      api(`/plugins`),
      api(`/projects/${projectId}/plugins`),
      api(`/projects/${projectId}/plugin-runs`),
    ]);
    [state.routes, state.branches, state.challenges, state.bridges, state.deadEnds,
      state.checkpoints, state.events, state.artifacts, state.chatImports,
      state.plugins, state.projectPlugins, state.pluginRuns] = results;
    state.selectedNode = null;
    renderProjects();
    renderWorkspace();
    history.replaceState(null, "", `${location.pathname}?project=${projectId}`);
  } catch (error) {
    notify(error.message, true);
  } finally {
    setProjectBusy(false);
  }
}

async function refreshCurrent() {
  if (!state.currentProject) return;
  await selectProject(state.currentProject.project_id);
}

function renderWorkspace() {
  if (!state.currentProject) return;
  emptyState.classList.add("hidden");
  workspace.classList.remove("hidden");
  $("#projectTitle").textContent = state.currentProject.title;
  $("#projectDescription").textContent = state.currentProject.description || "";
  $("#problemText").textContent = state.currentProject.original_problem.source_text;
  $("#problemNotes").textContent = state.currentProject.original_problem.author_notes || "";
  renderRoutes();
  renderChallenges();
  renderBridgesAndDeadEnds();
  renderCheckpoints();
  renderChatImports();
  renderPluginState();
  renderTimeline();
  renderArtifacts();
  fillAllRouteSelects();
}

function routeOptions(includeEmpty = false) {
  const prefix = includeEmpty ? `<option value="">${t().projectLevel}</option>` : `<option value="">${t().selectRoutePrompt}</option>`;
  return prefix + state.routes.map(route => `<option value="${route.route_id}">${escapeHtml(route.title)} [${labelOf(route.state)}]</option>`).join("");
}

function branchOptions(routeId, includeEmpty = true) {
  const prefix = includeEmpty ? `<option value="">${t().noneOrRouteLevel}</option>` : "";
  return prefix + state.branches.filter(branch => !routeId || branch.route_id === routeId)
    .map(branch => `<option value="${branch.branch_id}">${escapeHtml(branch.title)} [${labelOf(branch.state)}]</option>`).join("");
}

function fillAllRouteSelects() {
  const requiredRouteIds = ["branchRouteSelect", "challengeRouteSelect", "bridgeRouteSelect"];
  const optionalRouteIds = ["deadEndRouteSelect", "checkpointRouteSelect", "noteRouteSelect", "pythonRouteSelect"];
  for (const id of requiredRouteIds) {
    const element = $(`#${id}`); if (element) element.innerHTML = routeOptions(false);
  }
  for (const id of optionalRouteIds) {
    const element = $(`#${id}`); if (element) element.innerHTML = routeOptions(true);
  }
  syncDependentBranchSelect("challengeRouteSelect", "challengeBranchSelect");
  syncDependentBranchSelect("bridgeRouteSelect", "bridgeBranchSelect");
  syncDependentBranchSelect("checkpointRouteSelect", "checkpointBranchSelect");
  syncDependentBranchSelect("noteRouteSelect", "noteBranchSelect");
  syncDependentBranchSelect("pythonRouteSelect", "pythonBranchSelect");
}

function syncDependentBranchSelect(routeSelectId, branchSelectId) {
  const route = $(`#${routeSelectId}`);
  const branch = $(`#${branchSelectId}`);
  if (!route || !branch) return;
  const current = branch.value;
  branch.innerHTML = branchOptions(route.value, true);
  if ([...branch.options].some(option => option.value === current)) branch.value = current;
}

for (const [routeId, branchId] of [
  ["challengeRouteSelect", "challengeBranchSelect"], ["bridgeRouteSelect", "bridgeBranchSelect"],
  ["checkpointRouteSelect", "checkpointBranchSelect"], ["noteRouteSelect", "noteBranchSelect"],
  ["pythonRouteSelect", "pythonBranchSelect"],
]) {
  $(`#${routeId}`).addEventListener("change", () => syncDependentBranchSelect(routeId, branchId));
}

function moreNote(key, total, limit) {
  const hidden = total - limit;
  if (hidden <= 0) return "";
  if (state.expand[key]) {
    return `<button type="button" class="ghost tiny expand-toggle" data-expand="${key}" data-open="0">${t().collapse}</button>`;
  }
  return `<p class="minor expand-row">${t().moreHidden(hidden)}
    <button type="button" class="ghost tiny expand-toggle" data-expand="${key}" data-open="1">${t().showAll}</button></p>`;
}

function bindExpandToggles(root) {
  root.querySelectorAll(".expand-toggle").forEach((button) => {
    button.addEventListener("click", () => {
      const key = button.dataset.expand;
      state.expand[key] = button.dataset.open === "1";
      renderWorkspace();
    });
  });
}

function take(key, items, limit) {
  return state.expand[key] ? items : items.slice(0, limit);
}

function renderRoutes() {
  const svg = $("#routeGraph");
  svg.innerHTML = "";
  if (!state.routes.length) {
    svg.innerHTML = `<text x="40" y="60" class="empty-svg">${t().noRoutesSvg}</text>`;
    return;
  }
  const positions = new Map();
  const branchPositions = new Map();
  const routeW = 250, routeH = 70, branchW = 190, branchH = 50;
  let hiddenBranches = 0;
  state.routes.forEach((route, index) => {
    const col = index % 3, row = Math.floor(index / 3);
    const x = 42 + col * 315, y = 34 + row * 185;
    positions.set(route.route_id, {x, y});
    const routeBranches = state.branches.filter(branch => branch.route_id === route.route_id);
    if (routeBranches.length > 3) hiddenBranches += routeBranches.length - 3;
    routeBranches.slice(0, 3).forEach((branch, bIndex) => {
      branchPositions.set(branch.branch_id, {x: x + 28, y: y + 88 + bIndex * 60});
    });
  });

  for (const route of state.routes) {
    if (route.parent_route_id && positions.has(route.parent_route_id)) {
      drawLine(svg, positions.get(route.parent_route_id), positions.get(route.route_id), routeW, routeH, "route-edge");
    }
  }
  for (const branch of state.branches) {
    const parent = branch.parent_branch_id ? branchPositions.get(branch.parent_branch_id) : positions.get(branch.route_id);
    const child = branchPositions.get(branch.branch_id);
    if (!parent || !child) continue;
    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", parent.x + (branch.parent_branch_id ? branchW/2 : routeW/2));
    line.setAttribute("y1", parent.y + (branch.parent_branch_id ? branchH : routeH));
    line.setAttribute("x2", child.x + branchW/2);
    line.setAttribute("y2", child.y);
    line.setAttribute("class", "branch-edge");
    svg.appendChild(line);
  }
  for (const route of state.routes) drawRouteNode(svg, route, positions.get(route.route_id), routeW, routeH);
  for (const branch of state.branches) {
    const pos = branchPositions.get(branch.branch_id);
    if (pos) drawBranchNode(svg, branch, pos, branchW, branchH);
  }
  const overflow = $("#routeBranchOverflow");
  if (hiddenBranches > 0) {
    overflow.textContent = t().routeBranchOverflow(hiddenBranches);
    overflow.classList.remove("hidden");
  } else {
    overflow.classList.add("hidden");
  }
}

function drawLine(svg, a, b, width, height, className) {
  const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
  line.setAttribute("x1", a.x + width / 2); line.setAttribute("y1", a.y + height);
  line.setAttribute("x2", b.x + width / 2); line.setAttribute("y2", b.y);
  line.setAttribute("class", className); svg.appendChild(line);
}

function drawRouteNode(svg, route, pos, width, height) {
  const group = document.createElementNS("http://www.w3.org/2000/svg", "g");
  group.setAttribute("class", `route-node ${state.selectedNode?.id === route.route_id ? "active" : ""}`);
  group.innerHTML = `<rect x="${pos.x}" y="${pos.y}" width="${width}" height="${height}"></rect>
    <text x="${pos.x+14}" y="${pos.y+27}">${escapeHtml(trim(route.title, 30))}</text>
    <text class="route-state" x="${pos.x+14}" y="${pos.y+51}">${escapeHtml(labelOf(route.state))}</text>`;
  group.addEventListener("click", () => selectNode("route", route));
  svg.appendChild(group);
}

function drawBranchNode(svg, branch, pos, width, height) {
  const group = document.createElementNS("http://www.w3.org/2000/svg", "g");
  group.setAttribute("class", `branch-node ${state.selectedNode?.id === branch.branch_id ? "active" : ""}`);
  group.innerHTML = `<rect x="${pos.x}" y="${pos.y}" width="${width}" height="${height}"></rect>
    <text x="${pos.x+10}" y="${pos.y+21}">${escapeHtml(trim(branch.title, 25))}</text>
    <text class="route-state" x="${pos.x+10}" y="${pos.y+39}">${escapeHtml(labelOf(branch.state))}</text>`;
  group.addEventListener("click", () => selectNode("branch", branch));
  svg.appendChild(group);
}

function selectNode(kind, record) {
  state.selectedNode = {kind, id: kind === "route" ? record.route_id : record.branch_id, record};
  renderRoutes();
  const details = $("#routeDetails");
  const description = record.description || (state.lang === "en" ? "No description" : "无说明");
  const allowed = kind === "route"
    ? ["ACTIVE", "CHALLENGED", "CONDITIONAL", "DORMANT", "REVIVED", "BRIDGE_RESULT", "SUPERSEDED"]
    : ["ACTIVE", "CHALLENGED", "DORMANT", "REVIVED", "BRIDGE_RESULT", "SUPERSEDED", "COMPLETED"];
  const typeLabel = kind === "route" ? (state.lang === "en" ? "Route" : "路线") : (state.lang === "en" ? "Branch" : "分支");
  const curStateLabel = state.lang === "en" ? "Current State:" : "当前状态：";
  const colon = state.lang === "en" ? ": " : "：";
  details.innerHTML = `<strong>${typeLabel}${colon}${escapeHtml(record.title)}</strong>
    <p>${escapeHtml(description)}</p>
    <p class="minor">${curStateLabel} ${escapeHtml(labelOf(record.state))} <code>${escapeHtml(record.state)}</code></p>
    <div class="actions">${allowed.map(value => `<button class="tiny ghost node-state" data-state="${value}" title="${value}">${labelOf(value)}</button>`).join("")}</div>`;
  $$(".node-state").forEach(button => button.addEventListener("click", () => changeSelectedState(button.dataset.state)));
}

function changeSelectedState(newState) {
  if (!state.selectedNode || !state.currentProject) return;
  state.pendingState = newState;
  const targetLabel = state.lang === "en"
    ? `Target: "${state.selectedNode.record.title}" → ${labelOf(newState)} (${newState})`
    : `目标：「${state.selectedNode.record.title}」 → ${labelOf(newState)} (${newState})`;
  $("#stateDialogTarget").textContent = targetLabel;
  $("#stateReason").value = "";
  $("#stateDialog").showModal();
}

$("#stateForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const newState = state.pendingState;
  if (!newState || !state.selectedNode || !state.currentProject) return;
  const reason = $("#stateReason").value.trim();
  if (!reason) { notify(state.lang === "en" ? "Please enter a reason for the state change" : "请填写状态变化的原因", true); return; }
  try {
    const endpoint = state.selectedNode.kind === "route"
      ? `/projects/${state.currentProject.project_id}/routes/${state.selectedNode.id}/state`
      : `/projects/${state.currentProject.project_id}/branches/${state.selectedNode.id}/state`;
    const body = state.selectedNode.kind === "route"
      ? {new_state:newState, reason, evidence_refs:[], human_confirmed:false, actor:{type:"human", id:"local-researcher"}}
      : {new_state:newState, reason, evidence_refs:[], actor:{type:"human", id:"local-researcher"}};
    await api(endpoint, {method:"PATCH", headers:{"Content-Type":"application/json"}, body:JSON.stringify(body)});
    $("#stateDialog").close(); state.pendingState = null;
    await refreshCurrent(); notify(t().stateUpdated);
  } catch (error) { notify(error.message, true); }
});

function renderChallenges() {
  const container = $("#challengeList"); container.innerHTML = "";
  for (const item of take("challenges", state.challenges, 12)) {
    const div = document.createElement("div"); div.className = "object-card";
    const testPrefix = state.lang === "en" ? "Test Plan: " : "检验：";
    div.innerHTML = `<div><strong title="${escapeHtml(item.challenge_type)}">${escapeHtml(labelOf(item.challenge_type))}</strong> <span class="pill" title="${escapeHtml(item.status)}">${escapeHtml(labelOf(item.status))}</span></div>
      <p>${escapeHtml(trim(item.statement, 240))}</p>${item.test_plan ? `<small>${testPrefix}${escapeHtml(trim(item.test_plan, 180))}</small>` : ""}`;
    container.appendChild(div);
  }
  if (!state.challenges.length) container.innerHTML = `<p class="muted">${t().noChallenges}</p>`;
  else container.insertAdjacentHTML("beforeend", moreNote("challenges", state.challenges.length, 12));
  bindExpandToggles(container);
}

function renderBridgesAndDeadEnds() {
  const bridges = $("#bridgeList"); bridges.innerHTML = `<h3>${t().bridgesHeading}</h3>`;
  for (const item of take("bridges", state.bridges, 8)) {
    bridges.innerHTML += `<div class="object-card"><strong>${escapeHtml(item.title)}</strong><p>${escapeHtml(trim(item.summary, 240))}</p></div>`;
  }
  if (!state.bridges.length) bridges.innerHTML += `<p class="muted">${t().noBridges}</p>`;
  else bridges.insertAdjacentHTML("beforeend", moreNote("bridges", state.bridges.length, 8));
  bindExpandToggles(bridges);

  const dead = $("#deadEndList"); dead.innerHTML = `<h3>${t().deadEndsHeading}</h3>`;
  for (const item of take("deadEnds", state.deadEnds, 8)) {
    dead.innerHTML += `<div class="object-card"><strong>${escapeHtml(item.title)}</strong> <span class="pill" title="${escapeHtml(item.strength)}">${escapeHtml(labelOf(item.strength))}</span><p>${escapeHtml(trim(item.description, 220))}</p></div>`;
  }
  if (!state.deadEnds.length) dead.innerHTML += `<p class="muted">${t().noDeadEnds}</p>`;
  else dead.insertAdjacentHTML("beforeend", moreNote("deadEnds", state.deadEnds.length, 8));
  bindExpandToggles(dead);
}

function renderCheckpoints() {
  const container = $("#checkpointList"); container.innerHTML = "";
  const dateLocale = state.lang === "en" ? "en-US" : "zh-CN";
  const noGainText = state.lang === "en" ? "No round delta recorded" : "未记录本轮增量";
  for (const item of take("checkpoints", state.checkpoints, 8)) {
    container.innerHTML += `<div class="object-card"><strong>${new Date(item.created_at).toLocaleString(dateLocale)}</strong>
      <p>${escapeHtml(trim(item.current_target, 180))}</p><small>${escapeHtml(trim(item.observed_failure_or_gain || noGainText, 180))}</small></div>`;
  }
  if (!state.checkpoints.length) container.innerHTML = `<p class="muted">${t().noCheckpoints}</p>`;
  else container.insertAdjacentHTML("beforeend", moreNote("checkpoints", state.checkpoints.length, 8));
  bindExpandToggles(container);
}

function renderChatImports() {
  const container = $("#chatImportList"); container.innerHTML = "";
  for (const item of take("chatImports", state.chatImports, 8)) {
    const status = item.confirmed_at ? (state.lang === "en" ? "Confirmed" : "已确认") : (state.lang === "en" ? "Pending" : "待确认");
    const candSuffix = state.lang === "en" ? `candidates · ${item.parser_name}` : `条候选 · ${item.parser_name}`;
    container.innerHTML += `<div class="object-card"><strong>${escapeHtml(item.source_filename)}</strong> <span class="pill">${status}</span>
      <p>${item.candidates.length} ${candSuffix}</p></div>`;
  }
  if (!state.chatImports.length) container.innerHTML = `<p class="muted">${t().noChatImports}</p>`;
  else container.insertAdjacentHTML("beforeend", moreNote("chatImports", state.chatImports.length, 8));
  bindExpandToggles(container);
}

function renderPluginState() {
  const enabled = state.projectPlugins.some(item => item.plugin_id === "python.local" && item.enabled);
  $("#enablePythonButton").textContent = enabled ? t().pythonEnabled : t().enablePythonBtn;
  $("#enablePythonButton").disabled = enabled;
  const container = $("#pluginRunList"); container.innerHTML = "";
  const dateLocale = state.lang === "en" ? "en-US" : "zh-CN";
  for (const run of take("pluginRuns", state.pluginRuns, 8)) {
    const artifactCount = state.lang === "en" ? `${run.produced_artifact_refs.length} output artifact(s)` : `${run.produced_artifact_refs.length} 个输出工件`;
    container.innerHTML += `<div class="object-card"><strong title="${escapeHtml(run.status)}">${escapeHtml(labelOf(run.status))}</strong> <span class="pill">exit=${run.exit_code ?? "—"}</span>
      <p>${new Date(run.started_at).toLocaleString(dateLocale)} · ${artifactCount}</p>${run.error ? `<small>${escapeHtml(run.error)}</small>` : ""}</div>`;
  }
  if (!state.pluginRuns.length) container.innerHTML = `<p class="muted">${t().noPluginRuns}</p>`;
  else container.insertAdjacentHTML("beforeend", moreNote("pluginRuns", state.pluginRuns.length, 8));
  bindExpandToggles(container);
}

function renderTimeline() {
  const container = $("#timeline"); container.innerHTML = "";
  const ordered = [...state.events].reverse();
  const dateLocale = state.lang === "en" ? "en-US" : "zh-CN";
  for (const event of take("events", ordered, 160)) {
    const item = document.createElement("div"); item.className = "timeline-item";
    item.innerHTML = `<strong title="${escapeHtml(event.event_type)}">${new Date(event.timestamp).toLocaleString(dateLocale)} · ${escapeHtml(labelOf(event.event_type))}</strong>
      <p>${escapeHtml(event.epistemic_delta || summarizePayload(event.payload))}</p>`;
    container.appendChild(item);
  }
  if (!state.events.length) container.innerHTML = `<p class="muted">${t().noEvents}</p>`;
  else container.insertAdjacentHTML("beforeend", moreNote("events", state.events.length, 160));
  bindExpandToggles(container);
}

function renderArtifacts() {
  const container = $("#artifactList"); container.innerHTML = "";
  for (const artifact of take("artifacts", state.artifacts, 30)) {
    const link = `${API}/projects/${state.currentProject.project_id}/artifacts/${artifact.artifact_id}/content`;
    container.innerHTML += `<div class="artifact-item"><a href="${link}" target="_blank" rel="noopener">${escapeHtml(artifact.original_filename)}</a>
      <small title="${escapeHtml(artifact.artifact_type)}">${escapeHtml(labelOf(artifact.artifact_type))} · ${formatBytes(artifact.size_bytes)} · ${artifact.sha256.slice(0,12)}…</small></div>`;
  }
  if (!state.artifacts.length) container.innerHTML = `<p class="muted">${t().noArtifacts}</p>`;
  else container.insertAdjacentHTML("beforeend", moreNote("artifacts", state.artifacts.length, 30));
  bindExpandToggles(container);
}

function summarizePayload(payload) {
  if (!payload) return "";
  if (payload.content) return String(payload.content);
  if (payload.reason) return String(payload.reason);
  if (payload.note_type) return String(payload.note_type);
  return JSON.stringify(payload).slice(0, 240);
}

$("#createProjectForm").addEventListener("submit", async (event) => {
  event.preventDefault(); const data = new FormData(event.target);
  try {
    const project = await api("/projects", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({
      title:data.get("title"), description:"", problem:{source_text:data.get("problem"), author_notes:data.get("notes"), definitions:[], assumptions:[]}, actor:{type:"human", id:"local-researcher"}
    })});
    event.target.reset(); await loadProjects(); await selectProject(project.project_id); notify(t().projectCreated);
  } catch (error) { notify(error.message, true); }
});

$("#refreshProjects").addEventListener("click", loadProjects);
$("#refreshCurrent").addEventListener("click", refreshCurrent);
$("#newRouteButton").addEventListener("click", () => $("#routeDialog").showModal());
$("#newBranchButton").addEventListener("click", () => {
  if (!state.routes.length) return notify(state.lang === "en" ? "Please create a route first" : "请先创建路线", true);
  fillAllRouteSelects(); $("#branchDialog").showModal();
});

$("#routeForm").addEventListener("submit", async (event) => {
  event.preventDefault(); if (!state.currentProject) return; const data = new FormData(event.target);
  try {
    await api(`/projects/${state.currentProject.project_id}/routes`, {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({
      title:data.get("title"), description:data.get("description"), initial_state:data.get("initial_state"), revival_conditions:[], actor:{type:"human", id:"local-researcher"}
    })});
    $("#routeDialog").close(); event.target.reset(); await refreshCurrent(); notify(t().routeCreated);
  } catch (error) { notify(error.message, true); }
});

$("#branchForm").addEventListener("submit", async (event) => {
  event.preventDefault(); const data = new FormData(event.target);
  try {
    await api(`/projects/${state.currentProject.project_id}/branches`, {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({
      route_id:data.get("route_id"), title:data.get("title"), description:data.get("description"), assumptions:[], parameters:{}, initial_state:data.get("initial_state"), actor:{type:"human", id:"local-researcher"}
    })});
    $("#branchDialog").close(); event.target.reset(); await refreshCurrent(); notify(t().branchCreated);
  } catch (error) { notify(error.message, true); }
});

$("#splitRouteButton").addEventListener("click", async () => {
  if (!state.currentProject) return;
  if (!state.selectedNode || state.selectedNode.kind !== "route") {
    notify(state.lang === "en" ? "Please select a route to split on the route map first" : "请先在路线图中选择一条要拆分的路线", true); return;
  }
  const splitPrompt = state.lang === "en"
    ? `Source route: "${state.selectedNode.record.title}". The source route will be preserved, and child routes will evolve independently.`
    : `源路线：「${state.selectedNode.record.title}」拆分后将保留，子路线独立演进。`;
  $("#splitTarget").textContent = splitPrompt;
  $("#splitChildren").value = "";
  $("#splitReason").value = "";
  $("#splitDialog").showModal();
});

$("#splitForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!state.currentProject || !state.selectedNode || state.selectedNode.kind !== "route") return;
  const titles = lines($("#splitChildren").value);
  const children = titles.map((title, index) => ({
    title,
    description: state.lang === "en"
      ? `Child route #${index + 1} split from route "${state.selectedNode.record.title}".`
      : `由路线“${state.selectedNode.record.title}”拆分出的第 ${index + 1} 条子路线。`,
    initial_state: index === 0 ? "ACTIVE" : "SEED",
    revival_conditions: [],
  }));
  if (children.length < 2) { notify(state.lang === "en" ? "Route split requires at least two sub-routes" : "路线拆分至少需要两条子路线", true); return; }
  const reason = $("#splitReason").value.trim();
  if (!reason) { notify(state.lang === "en" ? "Please explain why this route needs to be split" : "请说明为什么需要拆分这条路线", true); return; }
  try {
    await api(`/projects/${state.currentProject.project_id}/routes/${state.selectedNode.id}/split`, {
      method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({
        children, reason, actor:{type:"human", id:"local-researcher"}
      })
    });
    $("#splitDialog").close();
    await refreshCurrent(); notify(t().routeSplit);
  } catch (error) { notify(error.message, true); }
});

$("#mergeRoutesButton").addEventListener("click", async () => {
  if (!state.currentProject || state.routes.length < 2) { notify(state.lang === "en" ? "At least two routes are required for merging" : "至少需要两条路线才能合并", true); return; }
  const select = $("#mergeSources");
  select.innerHTML = "";
  for (const route of state.routes) {
    const option = document.createElement("option");
    option.value = route.route_id;
    option.textContent = `${route.title} [${labelOf(route.state)}]`;
    select.appendChild(option);
  }
  $("#mergeTitle").value = "";
  $("#mergeReason").value = "";
  $("#mergeDialog").showModal();
});

$("#mergeForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!state.currentProject) return;
  const source_route_ids = [...$("#mergeSources").selectedOptions].map(option => option.value);
  if (source_route_ids.length < 2) { notify(state.lang === "en" ? "Please select at least two valid routes" : "请至少选择两条有效路线", true); return; }
  const title = $("#mergeTitle").value.trim();
  const reason = $("#mergeReason").value.trim();
  if (!title) { notify(state.lang === "en" ? "Please enter a title for the unified route" : "请填写新的综合路线标题", true); return; }
  if (!reason) { notify(state.lang === "en" ? "Please provide a basis for the merge" : "请说明合并依据", true); return; }
  try {
    await api(`/projects/${state.currentProject.project_id}/routes/merge`, {
      method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({
        source_route_ids, title, description: state.lang === "en" ? "Synthesized from multiple research routes." : "由多条研究路线综合形成。", reason,
        supersede_sources:true, actor:{type:"human", id:"local-researcher"}
      })
    });
    $("#mergeDialog").close();
    await refreshCurrent(); notify(t().routesMerged);
  } catch (error) { notify(error.message, true); }
});

$("#challengeForm").addEventListener("submit", async (event) => {
  event.preventDefault(); const data = new FormData(event.target);
  try {
    await api(`/projects/${state.currentProject.project_id}/challenges`, {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({
      route_id:data.get("route_id"), branch_id:data.get("branch_id") || null, challenge_type:data.get("challenge_type"), statement:data.get("statement"), test_plan:data.get("test_plan"), actor:{type:"human", id:"local-researcher"}
    })});
    event.target.reset(); await refreshCurrent(); notify(t().challengeOpened);
  } catch (error) { notify(error.message, true); }
});

$("#bridgeForm").addEventListener("submit", async (event) => {
  event.preventDefault(); const data = new FormData(event.target);
  try {
    await api(`/projects/${state.currentProject.project_id}/bridge-results`, {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({
      route_id:data.get("route_id"), branch_id:data.get("branch_id") || null, title:data.get("title"), summary:data.get("summary"), retained_value:lines(data.get("retained_value")), actor:{type:"human", id:"local-researcher"}
    })});
    event.target.reset(); await refreshCurrent(); notify(t().bridgeSaved);
  } catch (error) { notify(error.message, true); }
});

$("#deadEndForm").addEventListener("submit", async (event) => {
  event.preventDefault(); const data = new FormData(event.target);
  try {
    await api(`/projects/${state.currentProject.project_id}/dead-ends`, {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({
      route_id:data.get("route_id") || null, title:data.get("title"), description:data.get("description"), strength:"OBSERVED", reopen_conditions:lines(data.get("reopen_conditions")), actor:{type:"human", id:"local-researcher"}
    })});
    event.target.reset(); await refreshCurrent(); notify(t().deadEndSaved);
  } catch (error) { notify(error.message, true); }
});

$("#checkpointForm").addEventListener("submit", async (event) => {
  event.preventDefault(); const data = new FormData(event.target);
  try {
    await api(`/projects/${state.currentProject.project_id}/checkpoints`, {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({
      current_target:data.get("current_target"), route_id:data.get("route_id") || null, branch_id:data.get("branch_id") || null, intended_move:data.get("intended_move"), observed_failure_or_gain:data.get("observed_failure_or_gain"), unresolved_obligations:lines(data.get("unresolved_obligations")), confidence:"UNSPECIFIED", actor:{type:"human", id:"local-researcher"}
    })});
    event.target.reset(); await refreshCurrent(); notify(t().checkpointSaved);
  } catch (error) { notify(error.message, true); }
});

$("#noteForm").addEventListener("submit", async (event) => {
  event.preventDefault(); const data = new FormData(event.target);
  try {
    await api(`/projects/${state.currentProject.project_id}/notes`, {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({
      content:data.get("content"), route_id:data.get("route_id") || null, branch_id:data.get("branch_id") || null, note_type:data.get("note_type"), actor:{type:"human", id:"local-researcher"}
    })});
    event.target.reset(); await refreshCurrent(); notify(t().noteSaved);
  } catch (error) { notify(error.message, true); }
});

$("#artifactForm").addEventListener("submit", async (event) => {
  event.preventDefault(); const data = new FormData(event.target);
  try {
    await api(`/projects/${state.currentProject.project_id}/artifacts`, {method:"POST", body:data});
    event.target.reset(); await refreshCurrent(); notify(t().artifactSaved);
  } catch (error) { notify(error.message, true); }
});

$("#chatImportForm").addEventListener("submit", async (event) => {
  event.preventDefault(); const data = new FormData(event.target);
  try {
    const preview = await api(`/projects/${state.currentProject.project_id}/chat-imports/preview`, {method:"POST", body:data});
    state.currentChatPreview = preview; renderChatCandidateDialog(preview); $("#chatImportDialog").showModal();
  } catch (error) { notify(error.message, true); }
});

function renderChatCandidateDialog(preview) {
  const container = $("#chatCandidateList"); container.innerHTML = "";
  const includeLabel = state.lang === "en" ? "Include" : "纳入";
  const titlePlaceholder = state.lang === "en" ? "Optional title" : "可选标题";
  const noBranchText = state.lang === "en" ? "No branch" : "无分支";
  for (const candidate of preview.candidates) {
    const row = document.createElement("div"); row.className = "chat-candidate"; row.dataset.candidateId = candidate.candidate_id;
    row.innerHTML = `<div class="candidate-head"><label class="inline"><input class="candidate-include" type="checkbox" ${candidate.role === "assistant" ? "checked" : ""}/>${includeLabel}</label>
      <span class="pill">${candidate.role}</span><select class="candidate-disposition">
        ${["MODEL_NOTE","RESEARCH_CHECKPOINT","CHALLENGE","BRIDGE_RESULT","NEW_BRANCH","IGNORE"].map(value => `<option value="${value}" ${value===candidate.suggested_disposition ? "selected" : ""}>${labelOf(value)}</option>`).join("")}
      </select></div>
      <pre>${escapeHtml(trim(candidate.content, 1200))}</pre>
      <div class="candidate-targets"><select class="candidate-route">${routeOptions(true)}</select><select class="candidate-branch"><option value="">${noBranchText}</option></select><input class="candidate-title" placeholder="${titlePlaceholder}" /></div>`;
    const routeSelect = row.querySelector(".candidate-route"); const branchSelect = row.querySelector(".candidate-branch");
    const sync = () => branchSelect.innerHTML = branchOptions(routeSelect.value, true);
    routeSelect.addEventListener("change", sync); sync(); container.appendChild(row);
  }
}

$("#confirmChatImport").addEventListener("click", async () => {
  if (!state.currentChatPreview) return;
  const selections = $$(".chat-candidate").map(row => {
    const include = row.querySelector(".candidate-include").checked;
    const disposition = include ? row.querySelector(".candidate-disposition").value : "IGNORE";
    return {
      candidate_id: row.dataset.candidateId,
      disposition,
      route_id: row.querySelector(".candidate-route").value || null,
      branch_id: row.querySelector(".candidate-branch").value || null,
      title: row.querySelector(".candidate-title").value || null,
      structured_payload: {},
    };
  });
  try {
    await api(`/projects/${state.currentProject.project_id}/chat-imports/${state.currentChatPreview.import_id}/confirm`, {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({selections, actor:{type:"human", id:"local-researcher"}})});
    $("#chatImportDialog").close(); state.currentChatPreview = null; await refreshCurrent(); notify(t().chatImportConfirmed);
  } catch (error) { notify(error.message, true); }
});
$("#closeChatImport").addEventListener("click", () => $("#chatImportDialog").close());

$("#enablePythonButton").addEventListener("click", async () => {
  try {
    await api(`/projects/${state.currentProject.project_id}/plugins/python.local/enable`, {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({type:"human", id:"local-researcher"})});
    await refreshCurrent(); notify(t().pythonPluginEnabled);
  } catch (error) { notify(error.message, true); }
});

$("#pythonRunForm").addEventListener("submit", async (event) => {
  event.preventDefault(); const data = new FormData(event.target);
  try {
    const run = await api(`/projects/${state.currentProject.project_id}/plugin-runs/python`, {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({
      source_code:data.get("source_code"), timeout_seconds:Number(data.get("timeout_seconds")), route_id:data.get("route_id") || null, branch_id:data.get("branch_id") || null, input_artifact_ids:[], actor:{type:"human", id:"local-researcher"}
    })});
    await refreshCurrent(); notify(t().pythonRunFinished(run.status), run.status !== "SUCCEEDED");
  } catch (error) { notify(error.message, true); }
});

$("#integrityButton").addEventListener("click", async () => {
  try {
    const report = await api(`/projects/${state.currentProject.project_id}/integrity`);
    const validMsg = state.lang === "en" ? `Event chain intact: ${report.event_count} events` : `事件链完整：${report.event_count} 条事件`;
    notify(report.valid ? validMsg : report.error, !report.valid);
  }
  catch (error) { notify(error.message, true); }
});

$("#exportProjectButton").addEventListener("click", async () => {
  if (!state.currentProject) return;
  try {
    const headers = new Headers();
    const key = storedApiKey();
    if (key) headers.set("X-API-Key", key);
    const response = await fetch(`${API}/projects/${state.currentProject.project_id}/export`, { headers });
    if (!response.ok) {
      let detail = `${response.status} ${response.statusText}`;
      try { detail = (await response.json()).detail ?? detail; } catch {}
      if (response.status === 401 || response.status === 403) {
        throw new Error(t().needApiKeyAuth(response.status, detail));
      }
      throw new Error(detail);
    }
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = `${state.currentProject.title || "project"}.smath.zip`;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    URL.revokeObjectURL(url);
    notify(t().exportStarted);
  } catch (error) { notify(error.message, true); }
});

$("#researchPacketButton").addEventListener("click", async () => {
  try {
    const result = await api(`/projects/${state.currentProject.project_id}/research-packets`, {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({route_ids:[], include_recent_events:60, include_checkpoints:10, purpose:"Continue open mathematical exploration without forcing closure."})});
    $("#packetOutput").value = result.markdown; $("#packetDialog").showModal();
  } catch (error) { notify(error.message, true); }
});
$("#closePacket").addEventListener("click", () => $("#packetDialog").close());
$("#copyPacket").addEventListener("click", async () => { await navigator.clipboard.writeText($("#packetOutput").value); notify(t().packetCopied); });

const canvas = $("#sketchCanvas"), ctx = canvas.getContext("2d"); let drawing = false;
function point(event) { const rect = canvas.getBoundingClientRect(); return {x:(event.clientX-rect.left)*canvas.width/rect.width, y:(event.clientY-rect.top)*canvas.height/rect.height}; }
canvas.addEventListener("pointerdown", event => { drawing = true; const p=point(event); ctx.beginPath(); ctx.moveTo(p.x,p.y); });
canvas.addEventListener("pointermove", event => { if(!drawing) return; const p=point(event); ctx.lineWidth=3; ctx.lineCap="round"; ctx.strokeStyle="#20293b"; ctx.lineTo(p.x,p.y); ctx.stroke(); });
window.addEventListener("pointerup", () => drawing=false);
$("#clearSketch").addEventListener("click", () => ctx.clearRect(0,0,canvas.width,canvas.height));
$("#saveSketch").addEventListener("click", () => {
  if (!state.currentProject) return;
  canvas.toBlob(async blob => {
    const data = new FormData(); data.append("file", blob, `sketch-${Date.now()}.png`); data.append("artifact_type","HAND_DRAWING"); data.append("origin","HUMAN"); data.append("interpretation_status","RAW");
    try { await api(`/projects/${state.currentProject.project_id}/artifacts`, {method:"POST", body:data}); await refreshCurrent(); notify(t().sketchSaved); }
    catch (error) { notify(error.message,true); }
  }, "image/png");
});

function lines(value) { return String(value || "").split(/\r?\n/).map(x => x.trim()).filter(Boolean); }
function trim(value, length) { const text=String(value || ""); return text.length > length ? `${text.slice(0,length)}…` : text; }
function formatBytes(bytes) { if (bytes < 1024) return `${bytes} B`; if (bytes < 1024*1024) return `${(bytes/1024).toFixed(1)} KB`; return `${(bytes/1024/1024).toFixed(1)} MB`; }
function escapeHtml(value) { return String(value).replace(/[&<>'"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;",'"':"&quot;"}[c])); }

$("#saveApiKey").addEventListener("click", () => {
  const key = $("#apiKeyInput").value.trim();
  try {
    if (key) window.sessionStorage.setItem(API_KEY_STORAGE_KEY, key);
    else window.sessionStorage.removeItem(API_KEY_STORAGE_KEY);
    notify(key ? t().apiKeySaved : t().apiKeyCleared);
  } catch {
    notify(t().authWriteSessionError, true);
  }
  $$("details.key-control").forEach(detail => { detail.open = false; });
});

$("#clearApiKey").addEventListener("click", () => {
  try { window.sessionStorage.removeItem(API_KEY_STORAGE_KEY); } catch {}
  $("#apiKeyInput").value = "";
  notify(t().apiKeyCleared);
});

$("#apiKeyInput").addEventListener("keydown", (event) => {
  if (event.key === "Enter") $("#saveApiKey").click();
});

$("#apiKeyInput").value = storedApiKey();

function updateStaticUI() {
  const cur = t();
  const isEn = state.lang === "en";
  document.documentElement.lang = isEn ? "en" : "zh-CN";
  document.title = isEn ? "ProofFlow Workbench" : "ProofFlow 实验数学工作台";
  const btnEn = $("#langBtnEn");
  const btnZh = $("#langBtnZh");
  if (btnEn && btnZh) {
    btnEn.classList.toggle("active", isEn);
    btnEn.setAttribute("aria-pressed", isEn ? "true" : "false");
    btnZh.classList.toggle("active", !isEn);
    btnZh.setAttribute("aria-pressed", !isEn ? "true" : "false");
  }
  $("#topbarTitle").textContent = cur.topbarTitle || "ProofFlow Workbench";
  $("#topbarSubtitle").textContent = cur.topbarSubtitle;
  $("#explorerLink").textContent = cur.explorerLink;
  $("#apiKeySummary").textContent = cur.apiKeySummary;
  $("#apiKeyLabel").textContent = cur.apiKeyLabel;
  $("#apiKeyInput").placeholder = cur.apiKeyPlaceholder;
  $("#saveApiKey").textContent = cur.save;
  $("#clearApiKey").textContent = cur.clear;
  $("#apiKeyNote").textContent = cur.apiKeyNote;

  $("#projectsHeading").textContent = cur.projectsHeading;
  $("#refreshProjects").textContent = cur.refresh;
  $("#newProjectSummary").textContent = cur.newProjectSummary;
  $("#labelProjectTitle").textContent = cur.labelProjectTitle;
  $("input[name='title']").placeholder = cur.placeholderTitle;
  $("#labelOriginalProblem").textContent = cur.labelOriginalProblem;
  $("textarea[name='problem']").placeholder = cur.placeholderProblem;
  $("#labelResearcherNotes").textContent = cur.labelResearcherNotes;
  $("textarea[name='notes']").placeholder = cur.placeholderNotes;
  $("#createProjectBtn").textContent = cur.createProjectBtn;
  $("#constitutionTitle").textContent = cur.constitutionTitle;
  $("#constitutionList").innerHTML = cur.constitutionItems.map(item => `<li>${escapeHtml(item)}</li>`).join("");

  $("#emptyHeading").textContent = cur.emptyHeading;
  $("#emptyDesc").textContent = cur.emptyDesc;

  $("#integrityButton").textContent = cur.integrityBtn;
  $("#exportProjectButton").textContent = cur.exportBtn;
  $("#researchPacketButton").textContent = cur.researchPacketBtn;

  $("#routeGraphHeading").textContent = cur.routeGraphHeading;
  $("#newRouteButton").textContent = cur.newRouteBtn;
  $("#newBranchButton").textContent = cur.newBranchBtn;
  $("#splitRouteButton").textContent = cur.splitRouteBtn;
  $("#mergeRoutesButton").textContent = cur.mergeRoutesBtn;
  if (!state.selectedNode) {
    $("#routeDetails").textContent = cur.routeDetailsDefault;
  }

  $("#sketchHeading").textContent = cur.sketchHeading;
  $("#clearSketch").textContent = cur.clearSketch;
  $("#saveSketch").textContent = cur.saveSketch;
  $("#sketchNote").textContent = cur.sketchNote;

  $("#challengeSectionHeading").textContent = cur.challengeSectionHeading;
  $("#labelChallengeRoute").textContent = cur.labelChallengeRoute;
  $("#labelChallengeBranch").textContent = cur.labelChallengeBranch;
  $("#labelChallengeType").textContent = cur.labelChallengeType;
  $("#labelChallengeStatement").textContent = cur.labelChallengeStatement;
  $("#labelChallengeTestPlan").textContent = cur.labelChallengeTestPlan;
  $("#openChallengeBtn").textContent = cur.openChallengeBtn;

  $("#bridgeSectionHeading").textContent = cur.bridgeSectionHeading;
  $("#labelBridgeRoute").textContent = cur.labelBridgeRoute;
  $("#labelBridgeBranch").textContent = cur.labelBridgeBranch;
  $("#labelBridgeTitle").textContent = cur.labelBridgeTitle;
  $("#labelBridgeSummary").textContent = cur.labelBridgeSummary;
  $("#labelBridgeRetainedValue").textContent = cur.labelBridgeRetainedValue;
  $("#saveBridgeBtn").textContent = cur.saveBridgeBtn;

  $("#deadEndSummary").textContent = cur.deadEndSummary;
  $("#labelDeadEndRoute").textContent = cur.labelDeadEndRoute;
  $("#labelDeadEndTitle").textContent = cur.labelDeadEndTitle;
  $("#labelDeadEndDesc").textContent = cur.labelDeadEndDesc;
  $("#labelDeadEndReopen").textContent = cur.labelDeadEndReopen;
  $("#saveDeadEndBtn").textContent = cur.saveDeadEndBtn;

  $("#checkpointSectionHeading").textContent = cur.checkpointSectionHeading;
  $("#labelCheckpointTarget").textContent = cur.labelCheckpointTarget;
  $("#labelCheckpointRoute").textContent = cur.labelCheckpointRoute;
  $("#labelCheckpointBranch").textContent = cur.labelCheckpointBranch;
  $("#labelCheckpointIntended").textContent = cur.labelCheckpointIntended;
  $("#labelCheckpointObserved").textContent = cur.labelCheckpointObserved;
  $("#labelCheckpointObligations").textContent = cur.labelCheckpointObligations;
  $("#saveCheckpointBtn").textContent = cur.saveCheckpointBtn;

  $("#chatImportHeading").textContent = cur.chatImportHeading;
  $("#chatImportPill").textContent = cur.chatImportPill;
  $("#chatImportDesc").textContent = cur.chatImportDesc;
  $("#labelChatImportFile").textContent = cur.labelChatImportFile;
  $("#parseChatBtn").textContent = cur.parseChatBtn;

  $("#pythonPluginHeading").textContent = cur.pythonPluginHeading;
  $("#pythonPluginWarning").textContent = cur.pythonPluginWarning;
  $("#labelPythonRoute").textContent = cur.labelPythonRoute;
  $("#labelPythonBranch").textContent = cur.labelPythonBranch;
  $("#labelPythonCode").textContent = cur.labelPythonCode;
  $("#labelPythonTimeout").textContent = cur.labelPythonTimeout;
  $("#runExperimentBtn").textContent = cur.runExperimentBtn;

  $("#humanNoteHeading").textContent = cur.humanNoteHeading;
  $("#labelNoteRoute").textContent = cur.labelNoteRoute;
  $("#labelNoteBranch").textContent = cur.labelNoteBranch;
  $("#labelNoteType").textContent = cur.labelNoteType;
  $("#labelNoteContent").textContent = cur.labelNoteContent;
  $("#addNoteBtn").textContent = cur.addNoteBtn;

  $("#uploadArtifactHeading").textContent = cur.uploadArtifactHeading;
  $("#labelArtifactFile").textContent = cur.labelArtifactFile;
  $("#labelArtifactType").textContent = cur.labelArtifactType;
  $("#saveArtifactBtn").textContent = cur.saveArtifactBtn;

  $("#timelineHeading").textContent = cur.timelineHeading;
  $("#refreshCurrent").textContent = cur.refresh;

  // Dialogs
  $("#dialogNewRouteTitle").textContent = cur.dialogNewRouteTitle;
  $("#dialogRouteTitleLabel").textContent = cur.dialogRouteTitleLabel;
  $("#dialogRouteDescLabel").textContent = cur.dialogRouteDescLabel;
  $("#dialogRouteStateLabel").textContent = cur.dialogRouteStateLabel;
  $("#dialogRouteCancel").textContent = cur.cancel;
  $("#dialogRouteSave").textContent = cur.save;

  $("#dialogNewBranchTitle").textContent = cur.dialogNewBranchTitle;
  $("#dialogBranchRouteLabel").textContent = cur.dialogBranchRouteLabel;
  $("#dialogBranchTitleLabel").textContent = cur.dialogBranchTitleLabel;
  $("#dialogBranchDescLabel").textContent = cur.dialogBranchDescLabel;
  $("#dialogBranchStateLabel").textContent = cur.dialogBranchStateLabel;
  $("#dialogBranchCancel").textContent = cur.cancel;
  $("#dialogBranchSave").textContent = cur.save;

  $("#stateDialogTitle").textContent = cur.stateDialogTitle;
  $("#stateReasonLabel").textContent = cur.stateReasonLabel;
  $("#stateReason").placeholder = cur.stateReasonPlaceholder;
  $("#dialogStateCancel").textContent = cur.cancel;
  $("#dialogStateConfirm").textContent = cur.dialogStateConfirm;

  $("#dialogSplitTitle").textContent = cur.dialogSplitTitle;
  $("#dialogSplitChildrenLabel").textContent = cur.dialogSplitChildrenLabel;
  $("#dialogSplitReasonLabel").textContent = cur.dialogSplitReasonLabel;
  $("#dialogSplitCancel").textContent = cur.cancel;
  $("#dialogSplitExecute").textContent = cur.dialogSplitExecute;

  $("#dialogMergeTitle").textContent = cur.dialogMergeTitle;
  $("#dialogMergeSelectLabel").textContent = cur.dialogMergeSelectLabel;
  $("#dialogMergeTitleLabel").textContent = cur.dialogMergeTitleLabel;
  $("#dialogMergeReasonLabel").textContent = cur.dialogMergeReasonLabel;
  $("#dialogMergeCancel").textContent = cur.cancel;
  $("#dialogMergeCreate").textContent = cur.dialogMergeCreate;

  $("#dialogPacketHeading").textContent = cur.dialogPacketHeading;
  $("#closePacket").textContent = cur.clear;
  $("#copyPacket").textContent = cur.copyPacket;

  $("#dialogChatImportHeading").textContent = cur.dialogChatImportHeading;
  $("#dialogChatImportHint").textContent = cur.dialogChatImportHint;
  $("#closeChatImport").textContent = cur.clear;
  $("#confirmChatImport").textContent = cur.confirmChatImport;

  // Re-translate dropdown options
  $("#challengeTypeSelect").innerHTML = [
    "OBJECTION", "COUNTEREXAMPLE_SEARCH", "SOURCE_CHECK", "QUANTIFIER_CHECK",
    "FORMALIZATION_TEST", "COMPUTATIONAL_TEST", "BOUNDARY_CASE", "OTHER"
  ].map(key => `<option value="${key}">${escapeHtml(labelOf(key))}</option>`).join("");

  $("#noteTypeSelect").innerHTML = [
    "GENERAL", "INTUITION", "DEFINITION", "COUNTEREXAMPLE",
    "ROUTE_PRIORITY", "SIMPLIFICATION_GOAL", "REDIRECT"
  ].map(key => `<option value="${key}">${escapeHtml(labelOf(key))}</option>`).join("");

  $("#artifactTypeSelect").innerHTML = [
    "OTHER", "TEXT", "IMAGE", "HAND_DRAWING", "CODE", "GRAPH", "COUNTEREXAMPLE", "PROOF_SOURCE"
  ].map(key => `<option value="${key}">${escapeHtml(labelOf(key))}</option>`).join("");

  $("#dialogRouteStateSelect").innerHTML = ["SEED", "ACTIVE"].map(key => `<option value="${key}">${escapeHtml(labelOf(key))}</option>`).join("");
  $("#dialogBranchStateSelect").innerHTML = ["SEED", "ACTIVE"].map(key => `<option value="${key}">${escapeHtml(labelOf(key))}</option>`).join("");

  checkHealth();
}

function switchLanguage(nextLang) {
  state.lang = nextLang;
  saveLanguage(nextLang);
  updateStaticUI();
  renderProjects();
  if (state.currentProject) {
    renderWorkspace();
  }
}

$("#langBtnEn")?.addEventListener("click", () => switchLanguage("en"));
$("#langBtnZh")?.addEventListener("click", () => switchLanguage("zh"));

window.addEventListener("proofflow-lang-change", (e) => {
  if (e.detail && (e.detail === "en" || e.detail === "zh") && e.detail !== state.lang) {
    state.lang = e.detail;
    updateStaticUI();
    renderProjects();
    if (state.currentProject) renderWorkspace();
  }
});

window.addEventListener("storage", (e) => {
  if (e.key === LANG_STORAGE_KEY && (e.newValue === "en" || e.newValue === "zh") && e.newValue !== state.lang) {
    state.lang = e.newValue;
    updateStaticUI();
    renderProjects();
    if (state.currentProject) renderWorkspace();
  }
});

updateStaticUI();

const bootProjectId = new URLSearchParams(location.search).get("project");
loadProjects().then(() => {
  if (bootProjectId && state.projects.some(project => project.project_id === bootProjectId)) {
    selectProject(bootProjectId);
  }
}).catch(error => notify(error.message, true));
