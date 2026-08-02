# ProofFlow Schema Sandbox

## 图式证明流实验沙箱 `0.1.0-alpha.4`

正式名称是 **ProofFlow Schema Sandbox**，简称 **ProofFlow**。

ProofFlow 是本地优先、人类主导的实验数学研究沙箱。它不保证解题，不会声称访问模型隐藏思维链，也不会自动把项目标成“已解决”。`UNRESOLVED`
是一等结果；提出异议保持容易，而认证关闭路线仍需要高强度证据和人类确认。

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

## 本地运行

建议 Python 3.12+ 与 Node.js 20+。

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
npm ci --prefix apps/web
npm run build --prefix apps/web
.\.venv\Scripts\python.exe -m uvicorn schemamath_api.main:app --app-dir apps/api --host 127.0.0.1 --port 8000
```

访问 `http://127.0.0.1:8000/app/`。API 文档位于 `/docs`；Alpha.2
的无依赖原型保留在 `/prototype/`。

优先使用 `PROOFFLOW_WORKSPACE`、`PROOFFLOW_PLUGIN_ROOT` 等
`PROOFFLOW_*` 环境变量。为兼容 Alpha.2，对应的 `SCHEMAMATH_*`
变量仍然有效。

## 验证

```powershell
.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider
.\.venv\Scripts\ruff.exe check apps/api tests scripts
.\.venv\Scripts\python.exe scripts/validate_schemas.py
npm run build --prefix apps/web
npm audit --prefix apps/web --audit-level=high
```

进一步参见 [Alpha.4 发布说明](docs/ALPHA_4_RELEASE_NOTES_CN.md)、
[Alpha.3 到 Alpha.4 迁移说明](docs/MIGRATION_ALPHA3_TO_ALPHA4_CN.md) 和
[验证报告](VALIDATION_REPORT.txt)。

## 安全边界

本地命令与 Python 运行器是进程级隔离，不是操作系统安全沙箱，仍拥有启动
ProofFlow 的本地用户权限。只运行可信代码，并将 API 绑定在 localhost。
OCI 插件要求镜像使用摘要固定，但容器运行时及其安全配置仍由操作者负责。
数学工具按需安装；缺少可选工具时，系统会如实报告不可用。

可选 API 认证：设置 `PROOFFLOW_API_TOKEN`（或 `SCHEMAMATH_API_TOKEN`）后，
所有 `/api/*` 请求必须携带 Bearer 或 `X-API-Key` token。未设置时 API 保持
开放以支持本地优先工作流，因此未配置 token 时请只将服务暴露给 localhost。

Windows 资源限制：Python 运行器仅在 POSIX 上生效 CPU/内存/文件大小限制
（`resource.setrlimit`）。Windows 上只有墙钟超时与输出上限生效，因此在
Windows 主机上绝不要运行不受信的 `python.local` 代码；不受信负载请改用
OCI 运行器。

许可证：Apache-2.0。
