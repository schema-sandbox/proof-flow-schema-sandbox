const API = "/api/v1";
const state = {
  projects: [], currentProject: null, routes: [], branches: [], challenges: [],
  bridges: [], deadEnds: [], checkpoints: [], events: [], artifacts: [],
  chatImports: [], plugins: [], projectPlugins: [], pluginRuns: [],
  selectedNode: null, currentChatPreview: null,
};

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];
const projectList = $("#projectList");
const workspace = $("#projectWorkspace");
const emptyState = $("#emptyState");
const toast = $("#toast");

function notify(message, error = false) {
  toast.textContent = message;
  toast.style.background = error ? "#8e2732" : "#1d2433";
  toast.classList.remove("hidden");
  setTimeout(() => toast.classList.add("hidden"), 3600);
}

async function api(path, options = {}) {
  const response = await fetch(`${API}${path}`, options);
  if (!response.ok) {
    let detail = `${response.status} ${response.statusText}`;
    try { detail = (await response.json()).detail || detail; } catch {}
    throw new Error(detail);
  }
  const type = response.headers.get("content-type") || "";
  return type.includes("application/json") ? response.json() : response;
}

async function checkHealth() {
  try {
    const response = await fetch("/health");
    const data = await response.json();
    $("#healthStatus").textContent = `本地服务 ${data.version}`;
  } catch {
    $("#healthStatus").textContent = "本地服务不可用";
  }
}

async function loadProjects() {
  state.projects = await api("/projects");
  renderProjects();
}

function renderProjects() {
  projectList.innerHTML = "";
  if (!state.projects.length) {
    projectList.innerHTML = '<p class="muted">还没有项目。</p>';
    return;
  }
  for (const project of state.projects) {
    const card = document.createElement("div");
    card.className = `project-card ${state.currentProject?.project_id === project.project_id ? "active" : ""}`;
    card.innerHTML = `<strong>${escapeHtml(project.title)}</strong><small>${new Date(project.updated_at).toLocaleString()}</small>`;
    card.addEventListener("click", () => selectProject(project.project_id));
    projectList.appendChild(card);
  }
}

async function selectProject(projectId) {
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
  const prefix = includeEmpty ? '<option value="">项目级</option>' : '<option value="">请选择路线</option>';
  return prefix + state.routes.map(route => `<option value="${route.route_id}">${escapeHtml(route.title)} [${route.state}]</option>`).join("");
}

function branchOptions(routeId, includeEmpty = true) {
  const prefix = includeEmpty ? '<option value="">无 / 路线级</option>' : "";
  return prefix + state.branches.filter(branch => !routeId || branch.route_id === routeId)
    .map(branch => `<option value="${branch.branch_id}">${escapeHtml(branch.title)} [${branch.state}]</option>`).join("");
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

function renderRoutes() {
  const svg = $("#routeGraph");
  svg.innerHTML = "";
  if (!state.routes.length) {
    svg.innerHTML = '<text x="40" y="60" class="empty-svg">尚无路线。先建立几条不同的思考路径。</text>';
    return;
  }
  const positions = new Map();
  const branchPositions = new Map();
  const routeW = 250, routeH = 70, branchW = 190, branchH = 50;
  state.routes.forEach((route, index) => {
    const col = index % 3, row = Math.floor(index / 3);
    const x = 42 + col * 315, y = 34 + row * 185;
    positions.set(route.route_id, {x, y});
    const routeBranches = state.branches.filter(branch => branch.route_id === route.route_id);
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
    <text class="route-state" x="${pos.x+14}" y="${pos.y+51}">${route.state}</text>`;
  group.addEventListener("click", () => selectNode("route", route));
  svg.appendChild(group);
}

function drawBranchNode(svg, branch, pos, width, height) {
  const group = document.createElementNS("http://www.w3.org/2000/svg", "g");
  group.setAttribute("class", `branch-node ${state.selectedNode?.id === branch.branch_id ? "active" : ""}`);
  group.innerHTML = `<rect x="${pos.x}" y="${pos.y}" width="${width}" height="${height}"></rect>
    <text x="${pos.x+10}" y="${pos.y+21}">${escapeHtml(trim(branch.title, 25))}</text>
    <text class="route-state" x="${pos.x+10}" y="${pos.y+39}">${branch.state}</text>`;
  group.addEventListener("click", () => selectNode("branch", branch));
  svg.appendChild(group);
}

function selectNode(kind, record) {
  state.selectedNode = {kind, id: kind === "route" ? record.route_id : record.branch_id, record};
  renderRoutes();
  const details = $("#routeDetails");
  const description = record.description || "无说明";
  const allowed = kind === "route"
    ? ["ACTIVE", "CHALLENGED", "CONDITIONAL", "DORMANT", "REVIVED", "BRIDGE_RESULT", "SUPERSEDED"]
    : ["ACTIVE", "CHALLENGED", "DORMANT", "REVIVED", "BRIDGE_RESULT", "SUPERSEDED", "COMPLETED"];
  details.innerHTML = `<strong>${kind === "route" ? "路线" : "分支"}：${escapeHtml(record.title)}</strong>
    <p>${escapeHtml(description)}</p><div class="actions">${allowed.map(value => `<button class="tiny ghost node-state" data-state="${value}">${value}</button>`).join("")}</div>`;
  $$(".node-state").forEach(button => button.addEventListener("click", () => changeSelectedState(button.dataset.state)));
}

async function changeSelectedState(newState) {
  if (!state.selectedNode || !state.currentProject) return;
  const reason = prompt("说明本次状态变化的原因：");
  if (!reason) return;
  try {
    const endpoint = state.selectedNode.kind === "route"
      ? `/projects/${state.currentProject.project_id}/routes/${state.selectedNode.id}/state`
      : `/projects/${state.currentProject.project_id}/branches/${state.selectedNode.id}/state`;
    const body = state.selectedNode.kind === "route"
      ? {new_state:newState, reason, evidence_refs:[], human_confirmed:false, actor:{type:"human", id:"local-researcher"}}
      : {new_state:newState, reason, evidence_refs:[], actor:{type:"human", id:"local-researcher"}};
    await api(endpoint, {method:"PATCH", headers:{"Content-Type":"application/json"}, body:JSON.stringify(body)});
    await refreshCurrent(); notify("状态已更新");
  } catch (error) { notify(error.message, true); }
}

function renderChallenges() {
  const container = $("#challengeList"); container.innerHTML = "";
  for (const item of state.challenges.slice(0, 12)) {
    const div = document.createElement("div"); div.className = "object-card";
    div.innerHTML = `<div><strong>${item.challenge_type}</strong> <span class="pill">${item.status}</span></div>
      <p>${escapeHtml(trim(item.statement, 240))}</p>${item.test_plan ? `<small>检验：${escapeHtml(trim(item.test_plan, 180))}</small>` : ""}`;
    container.appendChild(div);
  }
  if (!state.challenges.length) container.innerHTML = '<p class="muted">暂无挑战。</p>';
}

function renderBridgesAndDeadEnds() {
  const bridges = $("#bridgeList"); bridges.innerHTML = '<h3>桥接结果</h3>';
  for (const item of state.bridges.slice(0, 8)) {
    bridges.innerHTML += `<div class="object-card"><strong>${escapeHtml(item.title)}</strong><p>${escapeHtml(trim(item.summary, 240))}</p></div>`;
  }
  if (!state.bridges.length) bridges.innerHTML += '<p class="muted">暂无桥接结果。</p>';
  const dead = $("#deadEndList"); dead.innerHTML = '<h3>已知死路</h3>';
  for (const item of state.deadEnds.slice(0, 8)) {
    dead.innerHTML += `<div class="object-card"><strong>${escapeHtml(item.title)}</strong> <span class="pill">${item.strength}</span><p>${escapeHtml(trim(item.description, 220))}</p></div>`;
  }
  if (!state.deadEnds.length) dead.innerHTML += '<p class="muted">暂无明确死路约束。</p>';
}

function renderCheckpoints() {
  const container = $("#checkpointList"); container.innerHTML = "";
  for (const item of state.checkpoints.slice(0, 8)) {
    container.innerHTML += `<div class="object-card"><strong>${new Date(item.created_at).toLocaleString()}</strong>
      <p>${escapeHtml(trim(item.current_target, 180))}</p><small>${escapeHtml(trim(item.observed_failure_or_gain || "未记录本轮增量", 180))}</small></div>`;
  }
  if (!state.checkpoints.length) container.innerHTML = '<p class="muted">暂无结构化检查点。</p>';
}

function renderChatImports() {
  const container = $("#chatImportList"); container.innerHTML = "";
  for (const item of state.chatImports.slice(0, 8)) {
    const status = item.confirmed_at ? "已确认" : "待确认";
    container.innerHTML += `<div class="object-card"><strong>${escapeHtml(item.source_filename)}</strong> <span class="pill">${status}</span>
      <p>${item.candidates.length} 条候选 · ${item.parser_name}</p></div>`;
  }
  if (!state.chatImports.length) container.innerHTML = '<p class="muted">尚未导入会话。</p>';
}

function renderPluginState() {
  const enabled = state.projectPlugins.some(item => item.plugin_id === "python.local" && item.enabled);
  $("#enablePythonButton").textContent = enabled ? "Python 已启用" : "启用 Python 插件";
  $("#enablePythonButton").disabled = enabled;
  const container = $("#pluginRunList"); container.innerHTML = "";
  for (const run of state.pluginRuns.slice(0, 8)) {
    container.innerHTML += `<div class="object-card"><strong>${run.status}</strong> <span class="pill">exit=${run.exit_code ?? "—"}</span>
      <p>${new Date(run.started_at).toLocaleString()} · ${run.produced_artifact_refs.length} 个输出工件</p>${run.error ? `<small>${escapeHtml(run.error)}</small>` : ""}</div>`;
  }
  if (!state.pluginRuns.length) container.innerHTML = '<p class="muted">暂无工具运行。</p>';
}

function renderTimeline() {
  const container = $("#timeline"); container.innerHTML = "";
  for (const event of [...state.events].reverse().slice(0, 160)) {
    const item = document.createElement("div"); item.className = "timeline-item";
    item.innerHTML = `<strong>${new Date(event.timestamp).toLocaleString()} · ${escapeHtml(event.event_type)}</strong>
      <p>${escapeHtml(event.epistemic_delta || summarizePayload(event.payload))}</p>`;
    container.appendChild(item);
  }
}

function renderArtifacts() {
  const container = $("#artifactList"); container.innerHTML = "";
  for (const artifact of state.artifacts.slice(0, 30)) {
    const link = `${API}/projects/${state.currentProject.project_id}/artifacts/${artifact.artifact_id}/content`;
    container.innerHTML += `<div class="artifact-item"><a href="${link}" target="_blank">${escapeHtml(artifact.original_filename)}</a>
      <small>${artifact.artifact_type} · ${formatBytes(artifact.size_bytes)} · ${artifact.sha256.slice(0,12)}…</small></div>`;
  }
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
    event.target.reset(); await loadProjects(); await selectProject(project.project_id); notify("项目已创建");
  } catch (error) { notify(error.message, true); }
});

$("#refreshProjects").addEventListener("click", loadProjects);
$("#refreshCurrent").addEventListener("click", refreshCurrent);
$("#newRouteButton").addEventListener("click", () => $("#routeDialog").showModal());
$("#newBranchButton").addEventListener("click", () => {
  if (!state.routes.length) return notify("请先创建路线", true);
  fillAllRouteSelects(); $("#branchDialog").showModal();
});

$("#routeForm").addEventListener("submit", async (event) => {
  event.preventDefault(); if (!state.currentProject) return; const data = new FormData(event.target);
  try {
    await api(`/projects/${state.currentProject.project_id}/routes`, {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({
      title:data.get("title"), description:data.get("description"), initial_state:data.get("initial_state"), revival_conditions:[], actor:{type:"human", id:"local-researcher"}
    })});
    $("#routeDialog").close(); event.target.reset(); await refreshCurrent(); notify("路线已创建");
  } catch (error) { notify(error.message, true); }
});

$("#branchForm").addEventListener("submit", async (event) => {
  event.preventDefault(); const data = new FormData(event.target);
  try {
    await api(`/projects/${state.currentProject.project_id}/branches`, {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({
      route_id:data.get("route_id"), title:data.get("title"), description:data.get("description"), assumptions:[], parameters:{}, initial_state:data.get("initial_state"), actor:{type:"human", id:"local-researcher"}
    })});
    $("#branchDialog").close(); event.target.reset(); await refreshCurrent(); notify("分支已创建");
  } catch (error) { notify(error.message, true); }
});

$("#splitRouteButton").addEventListener("click", async () => {
  if (!state.currentProject) return;
  if (!state.selectedNode || state.selectedNode.kind !== "route") {
    notify("请先在路线图中选择一条要拆分的路线", true); return;
  }
  const titles = prompt("每行输入一个子路线标题（至少两条）：", "代数路线\n组合路线");
  if (!titles) return;
  const children = lines(titles).map((title, index) => ({
    title,
    description: `由路线“${state.selectedNode.record.title}”拆分出的第 ${index + 1} 条子路线。`,
    initial_state: index === 0 ? "ACTIVE" : "SEED",
    revival_conditions: [],
  }));
  if (children.length < 2) { notify("路线拆分至少需要两条子路线", true); return; }
  const reason = prompt("说明为什么需要拆分这条路线：", "存在两个不同的数学机制，需要独立发展。");
  if (!reason) return;
  try {
    await api(`/projects/${state.currentProject.project_id}/routes/${state.selectedNode.id}/split`, {
      method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({
        children, reason, actor:{type:"human", id:"local-researcher"}
      })
    });
    await refreshCurrent(); notify("路线已拆分，源路线仍被保留");
  } catch (error) { notify(error.message, true); }
});

$("#mergeRoutesButton").addEventListener("click", async () => {
  if (!state.currentProject || state.routes.length < 2) { notify("至少需要两条路线才能合并", true); return; }
  const menu = state.routes.map((route, index) => `${index + 1}. ${route.title} [${route.state}]`).join("\n");
  const raw = prompt(`输入要合并的路线序号，用逗号分隔：\n${menu}`, "1,2");
  if (!raw) return;
  const indices = [...new Set(raw.split(/[,，\s]+/).map(value => Number(value) - 1).filter(value => Number.isInteger(value) && value >= 0 && value < state.routes.length))];
  if (indices.length < 2) { notify("请至少选择两条有效路线", true); return; }
  const source_route_ids = indices.map(index => state.routes[index].route_id);
  const title = prompt("新的综合路线标题：", "综合路线");
  if (!title) return;
  const reason = prompt("说明合并依据：", "各路线提供互补结构，需要形成一条综合路线。");
  if (!reason) return;
  try {
    await api(`/projects/${state.currentProject.project_id}/routes/merge`, {
      method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({
        source_route_ids, title, description:"由多条研究路线综合形成。", reason,
        supersede_sources:true, actor:{type:"human", id:"local-researcher"}
      })
    });
    await refreshCurrent(); notify("综合路线已创建；原路线被标记为 SUPERSEDED，但历史仍保留");
  } catch (error) { notify(error.message, true); }
});

$("#challengeForm").addEventListener("submit", async (event) => {
  event.preventDefault(); const data = new FormData(event.target);
  try {
    await api(`/projects/${state.currentProject.project_id}/challenges`, {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({
      route_id:data.get("route_id"), branch_id:data.get("branch_id") || null, challenge_type:data.get("challenge_type"), statement:data.get("statement"), test_plan:data.get("test_plan"), actor:{type:"human", id:"local-researcher"}
    })});
    event.target.reset(); await refreshCurrent(); notify("挑战已打开；路线仍然保留");
  } catch (error) { notify(error.message, true); }
});

$("#bridgeForm").addEventListener("submit", async (event) => {
  event.preventDefault(); const data = new FormData(event.target);
  try {
    await api(`/projects/${state.currentProject.project_id}/bridge-results`, {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({
      route_id:data.get("route_id"), branch_id:data.get("branch_id") || null, title:data.get("title"), summary:data.get("summary"), retained_value:lines(data.get("retained_value")), actor:{type:"human", id:"local-researcher"}
    })});
    event.target.reset(); await refreshCurrent(); notify("桥接结果已保存");
  } catch (error) { notify(error.message, true); }
});

$("#deadEndForm").addEventListener("submit", async (event) => {
  event.preventDefault(); const data = new FormData(event.target);
  try {
    await api(`/projects/${state.currentProject.project_id}/dead-ends`, {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({
      route_id:data.get("route_id") || null, title:data.get("title"), description:data.get("description"), strength:"OBSERVED", reopen_conditions:lines(data.get("reopen_conditions")), actor:{type:"human", id:"local-researcher"}
    })});
    event.target.reset(); await refreshCurrent(); notify("已保存死路与重新开放条件");
  } catch (error) { notify(error.message, true); }
});

$("#checkpointForm").addEventListener("submit", async (event) => {
  event.preventDefault(); const data = new FormData(event.target);
  try {
    await api(`/projects/${state.currentProject.project_id}/checkpoints`, {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({
      current_target:data.get("current_target"), route_id:data.get("route_id") || null, branch_id:data.get("branch_id") || null, intended_move:data.get("intended_move"), observed_failure_or_gain:data.get("observed_failure_or_gain"), unresolved_obligations:lines(data.get("unresolved_obligations")), confidence:"UNSPECIFIED", actor:{type:"human", id:"local-researcher"}
    })});
    event.target.reset(); await refreshCurrent(); notify("Research Checkpoint 已保存");
  } catch (error) { notify(error.message, true); }
});

$("#noteForm").addEventListener("submit", async (event) => {
  event.preventDefault(); const data = new FormData(event.target);
  try {
    await api(`/projects/${state.currentProject.project_id}/notes`, {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({
      content:data.get("content"), route_id:data.get("route_id") || null, branch_id:data.get("branch_id") || null, note_type:data.get("note_type"), actor:{type:"human", id:"local-researcher"}
    })});
    event.target.reset(); await refreshCurrent(); notify("研究者输入已加入轨迹");
  } catch (error) { notify(error.message, true); }
});

$("#artifactForm").addEventListener("submit", async (event) => {
  event.preventDefault(); const data = new FormData(event.target);
  try {
    await api(`/projects/${state.currentProject.project_id}/artifacts`, {method:"POST", body:data});
    event.target.reset(); await refreshCurrent(); notify("工件已按内容哈希保存");
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
  for (const candidate of preview.candidates) {
    const row = document.createElement("div"); row.className = "chat-candidate"; row.dataset.candidateId = candidate.candidate_id;
    row.innerHTML = `<div class="candidate-head"><label class="inline"><input class="candidate-include" type="checkbox" ${candidate.role === "assistant" ? "checked" : ""}/>纳入</label>
      <span class="pill">${candidate.role}</span><select class="candidate-disposition">
        ${["MODEL_NOTE","RESEARCH_CHECKPOINT","CHALLENGE","BRIDGE_RESULT","NEW_BRANCH","IGNORE"].map(value => `<option ${value===candidate.suggested_disposition ? "selected" : ""}>${value}</option>`).join("")}
      </select></div>
      <pre>${escapeHtml(trim(candidate.content, 1200))}</pre>
      <div class="candidate-targets"><select class="candidate-route">${routeOptions(true)}</select><select class="candidate-branch"><option value="">无分支</option></select><input class="candidate-title" placeholder="可选标题" /></div>`;
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
    $("#chatImportDialog").close(); state.currentChatPreview = null; await refreshCurrent(); notify("会话节点已按人工选择进入研究轨迹");
  } catch (error) { notify(error.message, true); }
});
$("#closeChatImport").addEventListener("click", () => $("#chatImportDialog").close());

$("#enablePythonButton").addEventListener("click", async () => {
  try {
    await api(`/projects/${state.currentProject.project_id}/plugins/python.local/enable`, {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({type:"human", id:"local-researcher"})});
    await refreshCurrent(); notify("Python 插件已为当前项目启用");
  } catch (error) { notify(error.message, true); }
});

$("#pythonRunForm").addEventListener("submit", async (event) => {
  event.preventDefault(); const data = new FormData(event.target);
  try {
    const run = await api(`/projects/${state.currentProject.project_id}/plugin-runs/python`, {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({
      source_code:data.get("source_code"), timeout_seconds:Number(data.get("timeout_seconds")), route_id:data.get("route_id") || null, branch_id:data.get("branch_id") || null, input_artifact_ids:[], actor:{type:"human", id:"local-researcher"}
    })});
    await refreshCurrent(); notify(`Python 实验结束：${run.status}`, run.status !== "SUCCEEDED");
  } catch (error) { notify(error.message, true); }
});

$("#integrityButton").addEventListener("click", async () => {
  try { const report = await api(`/projects/${state.currentProject.project_id}/integrity`); notify(report.valid ? `事件链完整：${report.event_count} 条事件` : report.error, !report.valid); }
  catch (error) { notify(error.message, true); }
});
$("#exportProjectButton").addEventListener("click", () => { if (state.currentProject) window.location.href = `${API}/projects/${state.currentProject.project_id}/export`; });
$("#researchPacketButton").addEventListener("click", async () => {
  try {
    const result = await api(`/projects/${state.currentProject.project_id}/research-packets`, {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({route_ids:[], include_recent_events:60, include_checkpoints:10, purpose:"Continue open mathematical exploration without forcing closure."})});
    $("#packetOutput").value = result.markdown; $("#packetDialog").showModal();
  } catch (error) { notify(error.message, true); }
});
$("#closePacket").addEventListener("click", () => $("#packetDialog").close());
$("#copyPacket").addEventListener("click", async () => { await navigator.clipboard.writeText($("#packetOutput").value); notify("已复制 Research Packet"); });

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
    try { await api(`/projects/${state.currentProject.project_id}/artifacts`, {method:"POST", body:data}); await refreshCurrent(); notify("草图已保存为原始工件"); }
    catch (error) { notify(error.message,true); }
  }, "image/png");
});

function lines(value) { return String(value || "").split(/\r?\n/).map(x => x.trim()).filter(Boolean); }
function trim(value, length) { const text=String(value || ""); return text.length > length ? `${text.slice(0,length)}…` : text; }
function formatBytes(bytes) { if (bytes < 1024) return `${bytes} B`; if (bytes < 1024*1024) return `${(bytes/1024).toFixed(1)} KB`; return `${(bytes/1024/1024).toFixed(1)} MB`; }
function escapeHtml(value) { return String(value).replace(/[&<>'"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;",'"':"&quot;"}[c])); }

checkHealth(); loadProjects().catch(error => notify(error.message, true));
