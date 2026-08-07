# ProofFlow Alpha.5 v0.14 对齐验收矩阵

- 状态：Alpha.5 实施验收矩阵；本地代码/Schema/API/投影门禁已覆盖，外部 Lean/npm audit 仍需在授权环境复核。
- 当前基线：Alpha.5 工作树（由 Alpha.4 `e77d79d6f5f009b7f5c601a0b37918e4a040c2d3` 追加演进）。
- 状态含义：`部分`＝存在可复用基础但未形成产品闭环；`缺失`＝没有规范对象或强制路径；
  `通过`＝实现、负向测试、API/Schema/投影和发布证据全部满足。

| ID | Alpha.4 | Alpha.5 必须交付 | 最小验收证据 | 阶段 |
|---|---|---|---|---|
| PF-014-01 | 部分 | 四个独立状态平面及逐平面 delta | 改 Artifact plane 不改变 Claim plane；重放后四平面一致 | M1 |
| PF-014-02 | 部分 | 提案、接受/拒绝、修订、幂等、接受依据 | 无依据/陈旧/重复/引用缺失均零写入；拒绝可审计 | M1 |
| PF-014-03 | 缺失 | 六类 `ContinuationContract` | 每回合恰有一个 typed receipt；计时器/自述不能授权 `RUN_NEXT` | M2 |
| PF-014-04 | 部分 | `HandoffPacketV2` 与接收回执 | 哈希、范围、义务、谓词、双修订齐全；陈旧接收失败 | M2 |
| PF-014-05 | 部分 | 持久 `ClaimAtom` 与六维 `EvidenceCard` | 无全局总分；来源/范围/关系/unknown 可查询；无隐式升级 | M3 |
| PF-014-06 | 部分 | `ReviewLineage` 和相关性图 | 同家族/同组织不会计为独立审查；范围和未检查项可见 | M3 |
| PF-014-07 | 部分 | `VerificationExecutionManifest` 与真实负向变异 | 命令/环境/锁/退出/检查 ID 完整；每个 mutation 必须按预期失败 | M4 |
| PF-014-08 | 缺失 | 正式 Comparator 覆盖矩阵 | 无效 Lean 永不 PASS；每个 headline 可追到定理/定义；缺口开放 | M4 |
| PF-014-09 | 缺失 | `RepositorySnapshot` 谱系 | ref 解析到 commit；父提交/前快照/关系/观察时间齐全 | M4 |
| PF-014-10 | 部分 | 类型化 `RepairLineage` | 输入输出哈希、关系、受影响 Claim、失效证据和重开义务齐全 | M4 |
| PF-014-11 | 部分 | 结果层级和依赖图 | Episode/Family/Claim/Target/File/Config 不混计；依赖可遍历 | M5 |
| PF-014-12 | 部分 | `AttemptRecord` 与 `CostVector` | 分母含失败/超时/重复/撤回/无效/无变化；成本各维可追溯 | M5 |
| PF-014-13 | 部分 | 微型证伪与最强基准门禁 | 扩大搜索前有小实例探针和优化基准；较弱基准不冒充 SOTA | M5 |
| PF-014-14 | 部分 | 27 项 Dossier V2 | 27 项逐字段 source class/ref；缺失写 unknown；投影漂移可检测 | M5 |
| PF-014-15 | 部分 | 问题议程谱系和非证据标签 | 来源/父子/引导/重开/偏差可审计；不改变 Claim maturity | M5 |
| PF-014-16 | 部分 | 原子批次、修订、幂等、租约、职责分离 | 半提交=0；并发陈旧写=0；投影绑定规范修订；越权门禁失败 | M1/M6 |

## 全局非回退门禁

以下项目任一失败，Alpha.5 都不得发布：

- 现有 398 项测试有回归；
- Alpha.1–Alpha.4 `.smath` 样本不可读取或事件被重写；
- 任何 unavailable/unknown 被转成 verified/accepted；
- `UNRESOLVED`、失败、超时、撤回或 `NO_CHANGE` 不再是合法记录；
- Route/Branch/Challenge/BridgeResult/DeadEndConstraint/ResearchCheckpoint/ModelSession/
  HandoffArtifact/CanvasSnapshot 的既有 REST 契约被无迁移删除；
- 原始工件内容或 SHA-256 地址发生变化；
- SQLite 投影无法从规范事件完全重建；
- 前端 `/app/`、兼容 `/prototype/`、导入预检或导出往返失效；
- Comparator 在未执行真实内核时产生 `PASS`；
- 批次失败后留下无 receipt 的规范事件。

## 发布证据清单

最终验收包至少包含：

1. 干净 commit、版本号、Schema 版本和迁移说明；
2. pytest/Ruff/Schema/OpenAPI/TypeScript/Vite/wheel/导入导出结果；
3. 并发与故障注入原始日志；
4. Lean/Comparator 执行 Manifest、负向变异和覆盖矩阵；
5. 仓库快照和修复谱系样本；
6. 一个包含成功、失败、`NO_CHANGE`、交接和请求人工的完整 episode；
7. 该 episode 的 27 项 Dossier 与其字段来源映射；
8. 未覆盖声明、未知值、相关审查、未执行验证和外部审计状态清单；
9. Alpha.1–Alpha.4 兼容回归报告；
10. 发布文件清单、SHA-256、ZIP 自检和 wheel 内置 UI 烟测。
