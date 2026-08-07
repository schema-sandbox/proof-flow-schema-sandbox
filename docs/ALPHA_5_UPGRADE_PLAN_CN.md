# ProofFlow `0.1.0-alpha.5` 升级计划

- 状态：已在当前仓库完成 Alpha.5 M1–M6 vertical-slice 实施；旧 REST 写入面的 SIP 强制挂载仍明确作为兼容边界，正式发布仍需按验收矩阵执行外部 Lean/依赖审计。
- 输入：[v0.14 理论要求](V0_14_THEORY_REQUIREMENTS_CN.md)与
  [软件审计](V0_14_SOFTWARE_AUDIT_CN.md)。
- 总原则：只做追加式演进，不回退或重写 Alpha.1–Alpha.4 已确认能力。

## 1. 升级目标

Alpha.5 的目标不是提高“自动解出题目”的宣传强度，而是把 Alpha.4 已有的轨迹保留
升级为可验证的研究控制平面：

- M1：继续完整保留观察、失败、工件和研究路线；
- M2：每次规范状态变化都有提案、接受依据、修订和拒绝记录；
- M3：每个有界回合都有延续合同和可恢复的交接包；
- Claim/Artifact/Verification/Repository 证据不混为一个状态或一个总分；
- 任何形式验证结论都能追到实际执行、命名覆盖和负向变异。

## 1.1 当前实现记录

- M1：原子 JSONL 批次、`expected_revision`、幂等键、批次/命令元数据、四平面 transition、SQLite 重放和 command receipt 查询已实现。
- M2：`ContinuationContract`、`HandoffPacketV2`、接受/拒绝回执和人工确认门禁已实现。
- M3：`ClaimAtom`（经 M1 接受写回）、六维独立 EvidenceCard、ReviewLineage、Claim relation 已实现。
- M4：Comparator 无真实内核执行时 fail-closed；执行 manifest、mutation set、coverage binding、RepositorySnapshot、RepairLineage 已实现。
- M5：层级节点、AttemptRecord、CostVector、MicroFalsificationPlan、BenchmarkBinding、QuestionAgenda 和 27 项 Dossier V2 已实现。
- M6：schema `0.6`、Alpha.5 API/OpenAPI/运行时 schema、React 控制面板、CI drift/build/wheel 检查已接入。

兼容边界：Alpha.5 新命令统一使用 revisioned/idempotent event boundary；Alpha.1–Alpha.4
旧 REST 命令继续保持原请求/响应契约，不能把它们 retroactively 描述为已经经过全部
SIP 生命周期钩子。它们仍受事件链、专用状态校验和历史回归保护。

本记录不把 `UNKNOWN`、未执行验证或仅静态检查升级为 `accepted/verified`；外部 Lean、npm audit
和发布提交仍须在具备相应依赖/权限的环境中形成原始证据。

## 2. 非回退约束

所有阶段共同遵守以下约束：

1. 不修改既有 JSONL 事件字节，不“补写”历史接受依据；
2. `SCHEMA_VERSION` 升级时继续支持 `0.1`–`0.5` 读取，旧记录只通过投影解释；
3. 现有 REST 路径和响应字段保持兼容；新增强制字段只用于新版本命令或提供兼容默认值；
4. 不删除 Route/Branch/Challenge 等对象，不把它们强行合并成新对象；
5. 不把旧自由文本自动升级为 accepted/verified；统一标为 legacy、author-reported 或 unknown；
6. `UNRESOLVED`、`NO_CHANGE`、失败、超时、撤回和请求人工仍是成功记录下来的合法结果；
7. 每一阶段先运行现有 398 项回归，再加入新测试；回归失败时不得以删除旧测试解决；
8. 数据迁移先预检、再备份/导出、再追加迁移事件；提供只读诊断和可恢复路径。

## 3. 关键路径

```text
M0 文档与契约
  → M1 规范转移内核与真实原子批次
    → M2 延续合同与交接回执
    → M3 声明原子、六维证据与审查谱系
      → M4 验证清单、Comparator 覆盖、仓库/修复谱系
        → M5 尝试分母、成本向量、微型证伪与 27 项档案
          → M6 API/UI/迁移/发布收口
```

M1 是后续所有阶段的共同依赖。报告、档案和 UI 不得先于规范转移内核成为新的事实来源。

## 4. 分阶段实施

### M0：冻结规范和兼容边界（文档阶段）

范围：PF-014 全部要求的可追踪定义。

交付物：

- v0.14 理论要求、目标架构、软件审计、升级计划和验收矩阵；
- 论文文件 SHA-256、软件基线 commit、当前测试和未执行检查的明确记录；
- Alpha.4 历史发布说明保持原样，README 明确 current/target 边界。

退出门禁：文档链接有效；PF-014-01–16 均有实现阶段和验收条件；没有把目标能力写成
Alpha.4 现状。

### M1：规范转移内核与真实原子批次

范围：PF-014-01、02、16；关闭审计 A-02、A-03、A-04。

建议新增模型：

- `ResearchStateSnapshot`：operational/epistemic/claim/artifact 四平面摘要；
- `TransitionProposal`：触发证据、提案者、候选 delta、幂等键和预期修订；
- `TransitionDecision`：接受者/机制、接受与拒绝部分、理由和新义务；
- `ResearchStateTransition`：被接受 delta、前后修订、来源和可见性；
- `CommandReceipt`：命令 ID、幂等结果、事件批次和投影修订。

实现要求：

1. 以事件序号加尾哈希或等价单调值定义规范修订；
2. 所有会改变规范状态的 FastAPI/Service 命令经过统一命令总线和 K0 门禁；
3. 预检全部事件和工件后，以单一可恢复批次写入；禁止逐事件“先写一半”；
4. 写入时检查 `expected_revision`，陈旧请求返回冲突且零写入；
5. 幂等键重复提交返回同一 receipt，不复制事件；
6. 拒绝提案可追加审计事件，但不得改变四平面状态；
7. SQLite 投影只消费已提交批次，并保存其规范修订和漂移状态。

强制负向测试：第二事件无效、磁盘写中断、投影更新失败、重复请求、陈旧修订、两个进程
竞争同一修订、拒绝提案夹带 Artifact/Claim delta。任何情形都不得出现无 receipt 的半提交。

### M2：延续合同与证据化交接

范围：PF-014-03、04。

交付物：

- `ContinuationContract`：`RUN_NEXT`、`WAIT`、`REDIRECT`、`ASK_HUMAN`、`STOP`、
  `NO_CHANGE`；
- `HandoffPacketV2`：声明范围、工件哈希、事实证据、失败见证、复活条件、义务/所有者、
  下一接受谓词、发送/接收修订；
- `HANDOFF_ACCEPTED` / `HANDOFF_REJECTED` 回执及原因；
- 每次自动/人工研究回合结束时的 typed continuation receipt。

门禁：定时器、模型自述、生成新文件或消耗更多 token 不能单独授权 `RUN_NEXT`；接收者在
旧修订上确认交接必须失败；`NO_CHANGE` 仍计入尝试分母和成本。

兼容策略：现有 `HandoffArtifactRecord` 保持可读，通过可选关联 ID 指向 V2 packet；历史记录
不得伪造接收回执。

### M3：声明原子、六维证据和审查谱系

范围：PF-014-05、06；关闭审计 A-05。

交付物：

- 持久化 `ClaimAtom`：来源/版本/解释/定义/量词/范围、关系、`as_of` 和开放义务；
- `EvidenceCard` 六个独立维度，每一维绑定证据引用、状态和评估者；
- `ReviewLineage`：模型家族、组织、编辑者、来源材料、形式化器、检查器、范围和未检查项；
- claim-to-artifact/verifier 绑定和 supersede/refute/support 关系；
- 新 REST API、运行时 Schema、OpenAPI 和 SQLite 投影。

门禁：删除或弃用 `EvidenceCardScores.total` 的规范输出；任何维度未知时保留 unknown；
同模型/同组织材料不得按数量增加 independent-review 维度；Claim 状态只能通过 M1 接受事件
改变。

### M4：形式验证、覆盖矩阵和谱系

范围：PF-014-07、08、09、10；关闭审计 A-01、A-07。

第一项安全修复：在真实 Lean 进程成功、执行记录持久化和策略检查全部完成前，
`ComparatorProtocol` 一律不得产生 `PASS/is_verified/primary_kernel_accepts=True`。

交付物：

- `VerificationExecutionManifest`：命令、工作目录、环境指纹、依赖锁、退出状态、stdout/stderr
  工件、实际检查 ID、公理/占位符策略、适用域和超时；
- 真实负向变异集合及每个 mutation 的 expected/observed 结果；
- `FormalCoverageBinding` 与覆盖矩阵；
- 挑战占位符和解答未完成证明的不同策略；
- `RepositorySnapshot`：URL/ref/commit/观察时间/父提交/前快照/关系；
- `RepairLineage`：类型化关系、输入输出哈希、受影响声明和下游重开义务；
- configured、executed、kernel-accepted、independently-reproduced 分离状态。

强制负向测试：不存在 tactic、伪造 stdout、非零退出但含成功词、超时、空输出、`sorry`/
`admit`、挑战/解答占位符混淆、未覆盖 headline、陈旧仓库 ref、未执行第二内核。所有未知
和未执行状态必须失败关闭。

### M5：结果层级、尝试分母、成本和档案

范围：PF-014-11–15；关闭审计 A-08。

交付物：

- Episode → ResultFamily → dependency/method → ClaimAtom → FormalTargetBundle →
  ManuscriptSection → SourceFile → ChallengeConfig 的类型化图；
- `AttemptRecord`：预注册目标、成功、失败、超时、重复、撤回、作用域无效、拒绝和无变化；
- `CostVector`：发现、失败尝试、人工选择/绑定/审查、稿件、形式化/检查、独立复现、基础设施；
- `MicroFalsificationPlan` 和 `BenchmarkBinding`；
- 从规范事件/工件生成的 27 项 `ResearchEpisodeDossierV2`；
- 问题议程谱系与明确的 `SEARCH_PROVENANCE_ONLY` 标签。

门禁：档案每个字段都带 source class 和 source refs；缺失值写 unknown/absent；总数不能把
层级节点相加；任何问题数量、人格数量或概念图密度不得升级 Claim State。

### M6：API、UI、迁移和发布收口

范围：全部 PF-014 的用户路径和发布证据；关闭审计 A-09。

交付物：

- UI 中分开展示四平面、提案/接受、延续、交接、Claim、覆盖和未决义务；
- 旧项目只读预检、Schema `0.6`（建议值）迁移投影和导出/再导入测试；
- OpenAPI/Schema 生成漂移门禁；
- CI 增加 Node 构建、wheel 安装烟测、内置 UI、发布 ZIP/清单/哈希检查；
- 干净 commit 上生成的发布清单，绑定 git commit 和执行证据；
- 27 项档案、未覆盖声明和未执行验证的发布摘要。

退出门禁：验收矩阵全部达到目标；外部依赖审计在明确授权的联网环境执行并归档；发布包
从干净工作树生成；旧样本包和当前项目往返后规范事件哈希不变。

## 5. 测试策略

测试分为五层，不能只增加 happy-path 单元测试：

| 层 | 目标 | 最小门禁 |
|---|---|---|
| 模型/Schema | 新记录的结构和不变量 | Pydantic + JSON Schema 正负样本 |
| 状态机 | 提案、接受、拒绝、延续 | 属性测试/状态迁移表，无非法跨平面升级 |
| 并发/故障注入 | 原子性、幂等、陈旧状态 | 多进程竞争、写中断、重试、投影失败 |
| 端到端 | API → 事件 → 投影 → 导出/档案 | 完整 receipt、修订一致、可重建 |
| 发布/形式验证 | 不产生假证书 | 无效 Lean、占位符、负向变异、覆盖缺口必须失败 |

现有 398 项测试是每个里程碑的前置门禁，不是最终验收总数目标。

## 6. 发布门禁

Alpha.5 候选版必须同时满足：

1. A-01/A-02 两个 P0 已关闭并有负向回归；
2. 生产写操作全部经过统一转移内核；
3. 验收矩阵 PF-014-01–16 无“缺失”，关键项无“仅原型”；
4. Python、Schema、OpenAPI、前端、wheel、导入/导出和发布包检查全部通过；
5. Comparator 不会在未执行真实内核时返回 PASS；
6. 事件批次中途失败不会留下半提交，重复/陈旧命令不会改变状态；
7. 发布档案披露 unknown、未覆盖声明、相关审查和未执行配置；
8. Alpha.1–Alpha.4 兼容样本和现有 UI/API 回归全部通过；
9. 发布说明明确实验边界，不承诺数学正确性、完整性、新颖性或必然解题。

## 7. 建议实施顺序

先实施 M1 的最小垂直切片：一个现有 Route 状态变更通过提案、接受、原子事件批次、
投影和 receipt 完整往返。该切片通过故障注入后，再把其余写接口逐个迁移。不要先重做
整个 UI，也不要先扩展 Dossier 字段；否则新报告会继续建立在不可验证的状态写回之上。
