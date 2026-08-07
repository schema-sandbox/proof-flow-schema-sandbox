# ProofFlow v0.14 理论对齐软件审计

- 审计日期：2026-08-03
- 软件基线：`e77d79d6f5f009b7f5c601a0b37918e4a040c2d3`（`0.1.0-alpha.4`）
- 理论基线：`From_Prompt_to_Proof_v0.14.md`，SHA-256
  `bc82eac917dbebc95075f54da6c6b45616d13727ec82dd9d4d12b06f7d56bfb6`
- 规范基线：[V0_14_THEORY_REQUIREMENTS_CN.md](V0_14_THEORY_REQUIREMENTS_CN.md)

## 1. 审计结论

Alpha.4 是一个可运行、测试基线稳定的本地实验数学研究沙箱，最成熟的能力是
M1（轨迹保留）：追加事件、内容寻址工件、失败路线、研究检查点、模型会话、交接工件、
可重建投影和导入预检均已有产品路径。

它还不能被描述为已经实现论文 v0.14 的 M2（转移接受）和 M3（延续/交接控制）。
按 16 项 PF-014 要求审计，当前为：**完整满足 0 项、部分具备 13 项、尚未具备 3 项**。
这不是对 Alpha.4 的回退，而是新理论基线比 Alpha.4 原始范围更严格。

升级到 Alpha.5 是必要的。发布前有两个必须先关闭的阻断项：

1. `ComparatorProtocol` 在没有执行 Lean 内核时可把无效代码判为 `PASS`；
2. K0 `TransactionExecutor` 的多事件提交并非真正原子，失败后可留下半提交事件。

Alpha.4 可以继续作为明确标注的实验原型使用，但不得把上述接口的结果宣传为内核证书或
原子事务保证。

## 2. 审计范围与方法

本次审计覆盖：

- 论文 v0.14 的四状态平面、M1/M2/M3、六维证据卡、Comparator、仓库快照、
  尝试分母、成本向量和 27 项档案要求；
- 根目录文档、Pydantic/JSON Schema/OpenAPI、FastAPI 服务、JSONL 事件存储、SQLite 投影、
  K0/SIP、验证器、独立审计模块、React/Vite 界面和发布脚本；
- 正向测试、静态检查、构建检查，以及针对原子提交和 Comparator 的两项临时负向复现。

不在本次范围内：数学命题本身的正确性证明、未提供的外部仓库快照、需要向外部注册表
发送依赖元数据的在线漏洞查询、真实 nanoda 第二内核复现。

## 3. 当前基线验证

| 检查 | 本次结果 | 说明 |
|---|---|---|
| `pytest -q -p no:cacheprovider` | PASS | 398 个测试；仅有 Starlette/httpx2 迁移警告 |
| `ruff check .` | PASS | 0 个错误 |
| `scripts/validate_schemas.py` | PASS | 30 个 JSON Schema 文档通过元验证 |
| `npm run build --prefix apps/web` | PASS | 2,375 个模块；Vite 报告大 chunk 警告 |
| 离线 wheel 构建 | PASS | 131 个条目；源码未放置可选 `_ui` 资源，wheel 只具备纯文本 fallback |
| `pip check` | PASS | 未发现损坏的 Python 依赖关系 |
| `npm audit --audit-level=high` | NOT RUN | 会向外部注册表发送依赖元数据，本次没有该外发授权；历史结果不作为本次结论 |

测试通过说明已有回归基线稳定，不等于 PF-014 新要求已经实现。

## 4. 发布阻断和主要发现

严重度定义：P0 为可能产生错误证书或破坏规范事件一致性的发布阻断；P1 为 Alpha.5
核心语义缺口；P2 为报告、自动化或文档完整性缺口。

### A-01（P0）：Comparator 可在未执行内核时产生假阳性 `PASS`

[comparator_protocol.py](../apps/api/schemamath_api/comparator_protocol.py#L109) 明确把内核接受
实现为 mock：只要文本声明相同、没有字符串 `sorry` 且扫描到的公理未超限，就设置
`primary_kernel_accepts=True` 并返回 `PASS`。本次用明显不存在的 Lean tactic
`definitely_not_a_lean_tactic` 复现，结果仍为：

```text
verdict=PASS, is_verified=True, primary_kernel_accepts=True,
secondary_kernel_accepts=None
```

这违反 PF-014-07/08 的失败关闭，以及“configured / executed / independently reproduced”分离。
在真实内核执行清单完成前，该接口只能返回 `UNAVAILABLE` 或静态预检结果，不能返回
`PASS`、`is_verified=True` 或 `primary_kernel_accepts=True`。

### A-02（P0）：K0 多事件事务可留下半提交规范事件

[transaction.py](../apps/api/schemamath_api/k0/transaction.py#L156) 逐个追加事件；异常处理只删除
本次新写入的 blob，无法撤销已经追加的 JSONL 事件。临时负向复现中，第一个事件合法、
第二个事件的 actor 非法，返回值为失败且 `rolled_back=True`，但事件日志仍保留第一个事件：

```text
success=False, rolled_back=True, events_remaining=1, event_types=[FIRST]
```

失败结果还没有返回这个已提交事件的 ID。因而当前实现不满足其文档所写的“要么全部提交、
要么全部不提交”，也不满足 PF-014-02/16。生产接入 K0 前必须引入可恢复批次协议或单一
原子写入边界，并增加中途失败、进程崩溃和投影失败的负向测试。

### A-03（P1）：K0/SIP 不是生产 FastAPI 的强制执行路径

主服务在 [service.py](../apps/api/schemamath_api/service.py#L777) 等位置直接调用
`EventStore.append()`，然后更新 SQLite 投影。K0/SIP 组合主要被 SDK、CLI 和测试使用；
API 服务没有通过统一的 P0–P10 提案、授权、接受和提交路径。因此“模块存在”和“生产操作
受模块门禁约束”是两件事。

Alpha.5 应先让所有改变规范状态的 API 命令经过同一命令总线；否则 Claim、Verifier、
Capacity、Federation 等模块无法成为强制不变量。

### A-04（P1）：缺少通用的观察—提案—接受—写回分离

当前 [EventRecord](../apps/api/schemamath_api/domain.py#L649) 没有规范修订号、提案者、
接受者/接受机制、四平面 delta、拒绝部分、幂等键或预期修订号。
[EventStore.append](../apps/api/schemamath_api/event_store.py#L96) 有进程/线程锁和完整链校验，
但没有乐观并发检查或重复命令抑制。专用路由状态接口有局部规则，却没有通用的
`ResearchStateTransition`。

此外，[ClaimModule](../apps/api/schemamath_api/sip/claim.py#L147) 在 P7 评估钩子内直接修改
内存 claim，早于 P9，和“模块只提案、K0 才执行副作用”的架构约束冲突。

### A-05（P1）：四平面和声明原子仍是混合/内存模型

[ProjectManifest](../apps/api/schemamath_api/domain.py#L312) 使用一个全局 `project_status` 列表；
Route/Branch/Challenge/Artifact 各自有局部状态，但没有四个独立状态平面。
`ClaimEnvelope` 仅在内存中保存自由文本声明、标量 maturity 和证据引用，没有精确来源、
定义/量词/范围、反驳关系、`as_of` 或六维状态。

[dossier_generator.py](../apps/api/schemamath_api/dossier_generator.py#L30) 还把六个证据维度求和为
`total` 并导出，与 v0.14“不得折叠为总分”冲突。Alpha.5 必须删除该总分的规范含义，
仅保留六维向量和各维证据来源。

### A-06（P1）：交接已有产品基础，但不是可接受的延续合同

持久化 `HandoffArtifact` 已包含生产/接收会话、已建立事实、拒绝方向、未决项和工件引用，
是现有实现中最接近 v0.14 的部分。但 [HandoffArtifactRecord](../apps/api/schemamath_api/domain.py#L966)
缺少声明原子范围、工件哈希快照、义务所有者/门禁、下一接受谓词、发送/接收修订号和
接收确认。系统也没有 `RUN_NEXT / WAIT / REDIRECT / ASK_HUMAN / STOP / NO_CHANGE`
延续合同；K0 的 `ALLOW/DENY` 是授权决定，不能替代延续决定。

### A-07（P1）：验证执行证据和覆盖矩阵未闭环

Lean/Z3 适配器已改为外部工具缺失时失败关闭，这是 Alpha.4 的实质改进。然而：

- 没有持久化 `VerificationExecutionManifest`；
- 未保存精确命令、依赖锁、环境、实际检查 ID 和适用域；
- [lean4.py](../apps/api/schemamath_api/verifiers/lean4.py#L104) 把一次普通执行标为
  `mutation_tested=True`，但没有实际生成和执行必须失败的负向变异；
- 没有 headline → claim atom → module → main result → Comparator config → theorem/definition
  的覆盖矩阵；
- 没有仓库快照谱系或第二内核执行凭证。

### A-08（P2）：v0.13 独立模块尚未成为规范投影

Campaign Auditor、Cost Tracker、Question Agenda、Evidence Ledger 和 Dossier Generator 都有
单元测试，但只被测试直接导入，没有 FastAPI 路由、规范事件或 SQLite 投影接入。
它们依赖调用方传入自由数据，无法证明报告来自当前规范状态。

其中 [evidence_ledger.py](../apps/api/schemamath_api/evidence_ledger.py#L146) 的函数名为
`validate_against_schema`，实际只做少量手写结构检查，并没有加载 JSON Schema；
`six_dim_card` 也没有维度、范围或来源校验。18 项 Dossier 与 v0.14 的 27 项标准之间仍有
9 项控制平面字段差距。

### A-09（P2）：CI 和仓库说明没有覆盖完整发布门禁

CI 当前运行 Python lint、pytest 和 Schema 导出/校验，但没有：

- 在导出 Schema 后以 `git diff --exit-code` 检测漂移；
- 导出并检查 OpenAPI 漂移；
- 安装 Node、执行 TypeScript/Vite 构建；
- 构建并安装 wheel 后验证内置 UI；
- 运行发布包清单/哈希/ZIP 自检；
- 运行 Comparator 假阳性、事务半提交等发布阻断负向测试。

原 `REPOSITORY_MAP.md` 仍写“28 个测试、24+4 个 Schema”，已与当前 398 个测试和 30 个
Schema 文件不符，本次文档修订会同步纠正。

本次 wheel 可以构建，但 `apps/api/schemamath_api/_ui` 不存在，因此不能把可选 package-data
配置当成“完整 React UI 已内置 wheel”的证据；该项仍应由 M6 的 wheel 安装烟测闭环。

## 5. PF-014 逐项符合度

| ID | 当前状态 | 已有基础 | 仍需完成 |
|---|---|---|---|
| PF-014-01 四平面 | 部分 | Project/Route/Branch/Challenge/Artifact 局部状态 | 四个独立平面及显式 delta |
| PF-014-02 接受转移 | 部分 | 追加事件、局部转移规则、K0 提案容器 | 通用提案/接受记录、修订、幂等、拒绝审计、原子写回 |
| PF-014-03 延续合同 | 缺失 | K0 授权决定、检查点建议 | 六类延续决定、预算/门禁/下一谓词 |
| PF-014-04 交接包 | 部分 | 持久化 HandoffArtifact 与 API | 范围、哈希、所有权、修订、接收回执、下一谓词 |
| PF-014-05 声明/证据向量 | 部分 | 内存 ClaimEnvelope、六维卡 | 持久 ClaimAtom、来源/范围/关系、去除总分 |
| PF-014-06 审查谱系 | 部分 | model family、相关审查警告、correlation 文本 | 组织/编辑/来源/检查器/范围的规范谱系 |
| PF-014-07 执行清单 | 部分 | Lean/Z3 失败关闭、事件/工件哈希 | 执行 Manifest、真实负向变异、三态执行/复现 |
| PF-014-08 覆盖矩阵 | 缺失 | Comparator 静态原型 | 禁止 mock PASS、正式覆盖图、挑战/解答边界 |
| PF-014-09 仓库快照 | 缺失 | 发布包有 git 跟踪文件清单 | RepositorySnapshot、父提交/前快照/替代关系 |
| PF-014-10 修复谱系 | 部分 | Dossier 中的自由文本列表 | 类型化关系、输入/输出哈希、下游失效传播 |
| PF-014-11 结果层级 | 部分 | Route/Branch、campaign family/dependency 参数 | Episode/Family/Claim/Target/File/Config 规范图 |
| PF-014-12 分母/成本 | 部分 | `NO_STATE_CHANGE` 事件、超时/撤回状态、两类成本 | AttemptRecord、完整分母、重复/无效尝试、成本向量 |
| PF-014-13 微型证伪 | 部分 | Challenge、falsification 文本、benchmark 原型 | 扩大搜索前强制门禁、最强优化基准绑定 |
| PF-014-14 27 项档案 | 部分 | 独立 18 项生成器 | 27 项、逐字段来源、从规范事件生成、漂移检测 |
| PF-014-15 问题议程 | 部分 | Question Agenda 独立生成器 | 事件/API/谱系、偏差审计、明确非证据标签 |
| PF-014-16 并发/权限 | 部分 | 进程/线程锁、认证、局部人工门禁 | 原子批次、预期修订、幂等、租约、职责分离、投影修订 |

## 6. 必须保护的 Alpha.4 资产

升级不得破坏以下已确认能力：

1. Alpha.1–Alpha.4 事件和 `.smath.zip` 继续可读，历史事件不重写；
2. JSONL 仍为规范轨迹，SQLite 仍可从事件重建；
3. 工件仍使用 SHA-256 内容寻址，原始工件不可变；
4. Route、Branch、Challenge、BridgeResult、DeadEndConstraint、ResearchCheckpoint、
   ModelSession、HandoffArtifact 和 CanvasSnapshot 的现有 API 保持兼容；
5. 高门槛闭合继续要求人工及证据，`UNRESOLVED`、失败和无变化继续是合法结果；
6. 外部验证器不可用时继续返回 unavailable/unverified，不生成替代成功；
7. React Flow、Excalidraw、原型 UI、插件安全边界和导入预检保留回归测试。

## 7. 审计处置

- 文档层面：需要升级，已建立 v0.14 规范、目标架构、审计、计划和验收矩阵；
- 软件层面：Alpha.4 保持当前功能，不在本次文档审计中直接改动；
- 发布层面：建议以 `0.1.0-alpha.5` 承载新 Schema 和控制平面；
- 首要顺序：先关闭 A-01/A-02，再接入统一转移内核，之后才扩展档案和 UI；
- 外部依赖漏洞查询必须在获得明确外发授权后重新运行并归档原始结果。

## 8. Alpha.5 执行后复核（2026-08-03）

本节是对上述 Alpha.4 基线发现的执行结果追加，不改写原始审计事实：

- A-01 已关闭：Comparator 在没有真实内核执行清单时返回 `UNAVAILABLE`，执行异常失败关闭，不能由静态文本产生 `PASS`。
- A-02 已关闭：K0 事件批次统一走 `EventStore.append_batch`，全批次预检、单次可恢复替换、陈旧 revision 和幂等重试均有负向回归；历史 JSONL 字节不被重写。
- A-03 收敛为兼容边界：Alpha.5 新增控制面命令走 revisioned event boundary；Alpha.1–Alpha.4 旧 REST 命令保留原契约，仍是兼容写入面，不能宣称已经强制挂载全部 SIP 生命周期钩子。
- A-04–A-08 已形成规范模型、投影、API、Schema 和负向测试：四平面转移、延续/交接、ClaimAtom、六维 EvidenceCard、ReviewLineage、执行清单、覆盖/仓库/修复谱系、Attempt/Cost/Dossier V2 均可追溯。
- A-09 的本地门禁已接入 Schema/OpenAPI 漂移、前端构建和 wheel UI 烟测；真实 Lean、第二内核、npm audit、干净提交发布清单仍须在授权环境取得原始证据。

因此，Alpha.5 代码垂直切片已完成；“正式候选版发布”仍以外部证据和干净提交打包为独立门禁，不能用本地静态检查替代。
