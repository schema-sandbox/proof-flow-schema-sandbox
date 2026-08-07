# ProofFlow Alpha.5 实施与审计报告

## 结论

Alpha.5 的代码升级已在本目录完成。Alpha.4 的 JSONL、REST 对象、导入/导出和旧版测试保持兼容；新写入使用 Schema `0.6`，历史事件只通过兼容模型和可重建投影解释，不回写旧字节。

## 已完成的控制面

| 批次 | 结果 |
|---|---|
| M1 | 原子批次、SHA-256 链、revision、幂等、四平面 transition、CommandReceipt 查询、SQLite 重放 |
| M2 | ContinuationContract、RUN_NEXT 人工确认、HandoffPacketV2、接受/拒绝回执 |
| M3 | ClaimAtom 提案—接受写回、六维 EvidenceCard、ReviewLineage、Claim relation |
| M4 | Comparator fail-closed、VerificationExecutionManifest、MutationSet、FormalCoverageBinding、RepositorySnapshot、RepairLineage |
| M5 | 研究层级图、AttemptRecord、CostVector、MicroFalsificationPlan、BenchmarkBinding、QuestionAgenda、27 项 Dossier V2 |
| M6 | 72 个 JSON Schema 文档、72 条 OpenAPI 路径、React 四平面摘要、Schema 0.6 迁移、CI 漂移/前端/wheel 门禁 |

## 本地验证

- `pytest -q -p no:cacheprovider`：全量通过（包含 Alpha.4 回归与 Alpha.5 负向/端到端样例）。
- `ruff check .`：通过。
- `scripts/validate_schemas.py`：72 个 schema 通过。
- `npm run build --prefix apps/web`：TypeScript/Vite 构建通过。
- Python wheel：系统 Python 离线构建通过；执行 `scripts/stage_wheel_ui.py` 后内置 prototype/Vite UI 烟测通过。`.venv` 因缺少 `setuptools.build_meta` 不能构建，CI 使用标准构建环境复核。

## 仍需外部授权的证据

真实 Lean 内核、第二内核独立复现、npm audit 和发布 ZIP 的干净提交/哈希清单不能在无网络或无工具链环境中伪造。系统会保留 `UNAVAILABLE`/`UNKNOWN`/未执行状态，不能把它们升级为 verified；这些原始证据应在授权 CI 中补齐后再打正式候选包。

兼容边界说明：Alpha.5 新增的控制面命令都经过 revisioned/idempotent event boundary；旧版 REST
命令继续保留原契约并使用同一条规范事件链，但不宣称已经强制挂载全部 SIP 生命周期钩子。
当前工作树还保留用户提供的未跟踪论文/证据文件，因此没有在脏树上刷新
`package_manifest.json` 与 `SHA256SUMS.txt`；完成干净提交后应运行 `scripts/build_release.py`
重新绑定文件清单、提交和哈希。
