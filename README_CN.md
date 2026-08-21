# ProofFlow Schema Sandbox

## 图式证明流实验沙箱 `0.1.0-alpha.9`

正式名称是 **ProofFlow Schema Sandbox**，简称 **ProofFlow**。

ProofFlow 是本地优先、人类主导的实验数学研究沙盒。它按照研究真实展开的方式追踪项目——路线、失败、异议与桥接——以追加式、SHA-256 链式事件流记录，可重放、可审计。

ProofFlow 不保证解题，不声称访问模型隐藏思维链，也从不自动把项目标成“已解决”。`UNRESOLVED` 是一等结果；提出异议保持容易，而认证关闭路线仍需要高强度证据和人类确认。

## 为什么是 ProofFlow

- **可观测**：研究以事件流被捕获，可重放、可审计，而不是一个黑箱答案。
- **诚实**：`UNRESOLVED` 是一等结果。异议保持便宜；认证关闭则刻意昂贵，且必须有人类。
- **人类在环**：模型可以提案，但只有人类确认映射与状态转移。

## 适合谁

- 想要 LLM 辅助、又不愿丢失决策痕迹的数学研究者。
- 形式化验证与 Lean 相关的研究者。
- 任何想观察 AI 在难题上的推理如何真实展开的人。

## Alpha.9 内容

- **干净检出可复现**：CI 在测试前构建并装载 Web UI，Alpha.2 导入样例作为正式测试数据纳入版本控制。
- **真实标签门禁**：`v*` 标签会触发严格发布门禁；门禁通过后自动创建对应 GitHub 预发布并上传经校验的资产。
- **合规 SBOM**：CycloneDX 1.5 SBOM 通过官方 JSON Schema 校验，Python 组件来自精确发布锁文件，npm 组件来自锁文件。
- **准确发布溯源**：项目清单和校验和改为分离式构建产物，所记录的提交与标签精确对应构建源。
- **发布元数据一致**：版本、MIT 许可证、仓库地址、OpenAPI、文档、Wheel 与前端元数据统一为 Alpha.9。

## Alpha.6 内容

- **非回环监听安全防护**：当监听 `0.0.0.0` 或外网接口时，未开启认证强制拒绝本地 Python 插件执行，彻底杜绝未授权远程执行风险。
- **磁盘与导入工件全量哈希校验**：`.smath.zip` 导入预检、项目完整性报告及工件读取均强制核对内容寻址路径、SHA-256 哈希与字节大小，杜绝证据篡改。
- **前端生产依赖 0 漏洞**：升级 DOMPurify 与 Mermaid，`npm audit --omit=dev` 保持 0 漏洞。
- **内置插件与容器打包闭环**：Wheel 安装包与 Docker 镜像完整打包 `graphviz.local` 与 `python.local` 插件及许可证。
- **第三方合规清单**：提供完整的 `THIRD_PARTY_NOTICES.md` 许可证与依赖归属。

## Alpha.5 内容

- 事件批次具备 revision、幂等键、批次 ID，并以原子方式写入。
- 四个研究状态平面通过提案、接受/拒绝事件写回；新增类型化延续合同和 V2 交接回执。
- ClaimAtom、六维独立证据卡、审查血缘、执行 manifest、覆盖绑定、仓库快照和修复血缘均可持久化。
- 新增层级节点、尝试结果、CostVector、微型反驳计划、BenchmarkBinding 与 27 项 dossier V2；`/app/` 显示四平面摘要。

## Alpha.4 内容

- 新增 `.smath.zip` 只读导入预检：在复制项目之前报告压缩包路径安全、Schema 兼容性、事件链完整性和缺失工件。
- SQLite 投影采用已登记迁移并公开投影 Schema 版本。
- 规范 JSONL 链被破坏后，系统拒绝继续追加事件并保持可恢复的只读状态。

## Alpha.3 基础能力

- 继续以追加式、SHA-256 链式 JSONL 事件作为规范历史；SQLite 仅是可重建投影。
- 通用项目级插件主机，具有发现、显式安装、健康检查、启用、禁用和卸载生命周期；禁止静默联网安装。
- 保留 `python.local`，新增可选的 `graphviz.local`。成功和失败运行的输入、命令、日志及输出都保存为内容寻址工件。
- 新增 `ModelSession`、`HandoffArtifact` 和只做预览、不自动执行的 `ArenaRecipe`。
- 同一家族模型互审会给出相关性警告，不能当作独立验证。
- 新增类型化 epistemic delta、历史路线检索和近重复路线提示。
- `/app/` 提供 React Flow 与 Excalidraw 双画布。原始草图不可变；机器解释单独保存；只有人类能确认草图到研究图的映射。
- Alpha.2 `.smath.zip` 导入、事件回放和已有能力均有回归测试；不重写历史事件。

## 论文 v0.14 与 Alpha.5 边界

`From_Prompt_to_Proof_v0.14.md` 提出四个彼此独立的研究状态平面、状态转移接受、
类型化延续决定、证据化交接、声明到正式证书的覆盖矩阵和仓库快照谱系。
这些要求已在 Alpha.5 控制面实现；Alpha.4 事件仍保持只读兼容，不重写历史。

规范见 [v0.14 理论对齐升级要求](docs/V0_14_THEORY_REQUIREMENTS_CN.md) 和
[目标架构](docs/ARCHITECTURE.md)。Alpha.4 仍以轨迹保留为强项；Alpha.5 已补齐
转移接受、延续控制、向量化声明证据和正式发布覆盖控制面。真实 Lean、依赖审计和
干净发布证据仍是独立发布门禁，不能由本地静态检查推断。

本次逐项结果见 [v0.14 软件审计](docs/V0_14_SOFTWARE_AUDIT_CN.md)，实施顺序见
[Alpha.5 升级计划](docs/ALPHA_5_UPGRADE_PLAN_CN.md)，发布门禁见
[Alpha.5 验收矩阵](docs/ALPHA_5_ACCEPTANCE_MATRIX_CN.md)。这些文件保留审计依据和验收门禁；
新写入使用 Schema `0.6`。
另见 [Alpha.5 实施报告](docs/ALPHA_5_IMPLEMENTATION_REPORT_CN.md)，其中记录本地验证和外部证据边界。

## 本地运行

建议 Python 3.12+ 与 Node.js 22+。

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
npm ci --prefix apps/web
npm run build --prefix apps/web
.\.venv\Scripts\python.exe -m uvicorn schemamath_api.main:app --app-dir apps/api --host 127.0.0.1 --port 8000
```

访问 `http://127.0.0.1:8000/app/`。API 文档位于 `/docs`；Alpha.2
的无依赖原型保留在 `/prototype/`。

生产容器配置需要显式认证。请将 `.env.production.example` 复制为受保护的
`.env.production`，替换两个占位符后运行：

```powershell
docker compose --env-file .env.production -f docker-compose.prod.yml up --build
```

生产配置将数据持久化到 `/data`、端口绑定到回环地址，并默认禁用本地进程插件；`/app/`
在收到 401 后会提示输入 API key，密钥只保存在当前浏览器会话中。

优先使用 `PROOFFLOW_ENV`、`PROOFFLOW_WORKSPACE`、`PROOFFLOW_PLUGIN_ROOT` 等
`PROOFFLOW_*` 环境变量，`PROOFFLOW_ENV=production` 切换到 fail-closed 行为。
为兼容 Alpha.2，对应的 `SCHEMAMATH_*` 变量仍然有效。

## 验证

```powershell
.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider
.\.venv\Scripts\ruff.exe check apps/api tests scripts
.\.venv\Scripts\python.exe scripts/validate_schemas.py
.\.venv\Scripts\python.exe scripts/export_runtime_schemas.py
.\.venv\Scripts\python.exe scripts/export_k0_schemas.py
.\.venv\Scripts\python.exe scripts/export_openapi.py
npm run build --prefix apps/web
npm audit --prefix apps/web --audit-level=high
python scripts/stage_wheel_ui.py
python -m pip wheel . --no-deps --no-build-isolation -w /tmp/proofflow-wheel
```

进一步参见 [Alpha.4 发布说明](docs/ALPHA_4_RELEASE_NOTES_CN.md)、
[Alpha.3 到 Alpha.4 迁移说明](docs/MIGRATION_ALPHA3_TO_ALPHA4_CN.md) 和
[验证报告](VALIDATION_REPORT.txt)。Alpha.5 要求以
[v0.14 理论对齐升级要求](docs/V0_14_THEORY_REQUIREMENTS_CN.md) 为准。

## 安全边界

本地命令与 Python 运行器是进程级隔离，不是操作系统安全沙箱，仍拥有启动
ProofFlow 的本地用户权限。只运行可信代码，并将 API 绑定在 localhost。生产模式在缺少
`PROOFFLOW_SECRET_KEY` 或 `PROOFFLOW_API_KEYS` 时会拒绝启动，并默认禁用本地进程插件。
OCI 插件要求镜像使用摘要固定，但容器运行时及其安全配置仍由操作者负责。
数学工具按需安装；缺少可选工具时，系统会如实报告不可用。

许可证：MIT。
