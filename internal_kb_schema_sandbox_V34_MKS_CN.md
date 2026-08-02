# 图式沙箱 V34-KB：面向目标保持型专业 AI 能力机器的模块化知识系统与可信微内核架构

## 策略代数、事件溯源知识状态、Profile 驱动语义、Recipe 交付与签名能力供应链

> [!CAUTION]
> **内部知识库与详细规范（机密——V34-KB）**
>
> 本文档用于 psi.run 内部研究、产品架构、实现与商业化规划，包含专有的控制平面语义、产品包装策略、实现边界与参考规范。本文档不是公开的符合性证明，也不得被表述为：当前实现已经形成安全边界、科学权威、工业认证能力或法律合规结论。

**作者：** Tengjiao Liu  
**组织：** psi.run  
**文档版本：** V34-KB  
**设计快照：** 2026-07-29  
**状态：** 内部规范性架构文档，附说明性实现 Schema  

---

## 0. 文档状态、版本层与规范用语

本文采用 RFC 2119 风格术语：

- **必须（MUST / SHALL / REQUIRED）**：声称具备相应 V34 属性时不可缺少；
- **应该（SHOULD / RECOMMENDED）**：除非存在明确且有证据支持的例外，否则应采用；
- **可以（MAY / OPTIONAL）**：允许变化，但不能突破已声明的保证边界。

V34 严格区分以下版本层：

| 层次 | 标识 | 含义 |
|---|---|---|
| 知识库文档 | `V34-KB` | 本方法与架构规范 |
| 互操作协议 | `SIP v1.2` | 现有 wire/manifest 协议基线，本文件不自动修改它 |
| 模块化扩展 | `MKS Extension v0.1-draft` | 本文提出的模块、Profile、Recipe、Pack 与组合语义 |
| 可信内核实现 | `schemabox-kernel-v0.1.0-alpha` | 参考实现目标，当前不构成安全边界 |
| 符合性套件 | `schemabox-conformance-v0.1-spec` | 组合代数、回放、故障与威胁测试规范 |
| 模块/适配器/包版本 | SemVer | 各独立组件的版本体系 |

V34 **不废除** V33 的 S1–S10 十层参考架构。V34 解决的是：如何把十层方法论实现成可渐进采用、可验证组合、可形成行业 Profile、可产品化交付并可进入可信供应链的模块化知识系统。

---

## 1. 摘要

V33 将图式沙箱定义为一种面向目标保持型专业 AI 能力机器的十层架构，能够把异构模型、工具、记忆、验证器、人类专家与受控行动通道组织为长程研究和工程系统。但它存在现实采用障碍：只需要证据审计输出或研究报告的开发者，不应该被迫一次部署整个架构。最初的“十二块乐高积木”方案解决了渐进采用，却仍过于接近普通中间件：模块顺序可能影响安全结果，规范状态所有权不清，类型层约束容易被误解为运行时保证。

V34 提出 **Schema Sandbox Modular Knowledge System（MKS，图式沙箱模块化知识系统）**。MKS 不是向量数据库、RAG 外壳或插件集合。它是一套受治理的事件溯源系统，其中目标、主张、证据、工件、轨迹、证明/保证义务、审查、配置与发布状态均为可版本化的一等对象。不可绕过的 **K0 可信微内核** 独占外部副作用授权、规范事件提交、工件身份、行动收据、生命周期调度与状态回放；普通模块只能提出约束、变换、证据义务、路线和状态迁移，不能直接提交外部副作用或修改规范状态。

V34 将系统分成五个相互区分的层次：S1–S10 是理论参考模型；Capability Modules 是可部署机制；Domain Profiles 定义领域语义；Recipes 是经过测试的结果型组合；Signed Packs 与 Registry 负责分发、信任和商业交换。模块不再依赖任意 `compose()` 顺序，而是通过显式策略代数组合。有效权限是宿主授权、Recipe 请求与模块限制的交集；风险按 Profile 定义的多维向量 join 合并；证据义务采用规范化并集；主张上限通过 Profile 定义的偏序 lattice meet 合并。任何变换都必须生成新的不可变工件版本和变换收据。任何外部后果都必须经过授权票据、意图记录、执行收据与结果事件。

本文规范了 P0–P10 固定生命周期、多维治理决策、Module/Pack Manifest、事件与工件 Schema、外部效果分类、失败与降级语义、供应链安全、符合性等级、属性测试，以及 SchemaDocs Evidence Room、GEO Audit、Decision Research Dossier 与 AI 数学研究等参考 Recipe。V34 是规范与实现目标；在运行时能力隔离、持久事件日志、不可变工件存储、签名验证、回放、Profile 编译和独立符合性测试完成前，不得宣称已经形成可信微内核、安全边界或专业认证能力。

---

## 2. 执行定义

> **图式沙箱在理论上采用分层参考架构，在实现上采用模块化可信微内核，在领域语义上由 Profile 驱动，在产品交付上以 Recipe 组合，在分发上采用签名 Pack，在信任与交换上由 Registry 治理；模块依靠明确的策略代数组合，而不是依赖任意的中间件执行顺序。**

V34 的整体栈：

```text
S1–S10 参考架构
    完整专业 AI 系统必须治理什么
                         ↓
K0 可信微内核
    身份、授权、生命周期、事件、工件、效果事务、回放
                         ↓
能力模块
    契约、证据、目标、主张、轨迹、保证、编排、容量等
                         ↓
领域 Profile
    GEO、研究、法律、数学、工业、生物证据等领域语义
                         ↓
经过测试的 Recipe
    GEO Audit、Decision Dossier、Evidence Room 等结果型组合
                         ↓
签名 Pack
    模块 + 适配器 + Profile + Recipe + 测试 + 许可 + 签名
                         ↓
SchemaDocs Registry
    发现、版本、哈希、撤回、兼容、授权、交易与工件交换
```

系统的核心商业与技术承诺是：

> **任何模型、工具、模块、人类专家或外部服务进入系统后，其目标、权限、证据、主张、工件、修复与发布都进入同一个可回放的治理框架。**

---

## 3. 为什么称为“模块化知识系统”

### 3.1 不只是知识图谱

知识图谱记录关系；MKS 还要治理：

- 谁或什么有权创建、修改关系；
- 哪些证据支持它；
- 对应哪个配置和工件版本；
- 审查范围是什么；
- 支持何时失效；
- 哪些行动可以由此触发；
- 更正如何传播；
- 失败路线是否仍有复用价值。

### 3.2 不只是 RAG

RAG 检索文本；MKS 必须区分：

```text
检索来源
候选解释
主张
支持集
矛盾证据
验证/审查结果
发布上限
时间状态
下游后果
```

### 3.3 不只是 Agent Runtime

Agent Runtime 可以执行工具和保留状态；MKS 还要回答：

- 当前工作是否仍服务原始目标；
- 结果是候选、已测试、形式检查、独立审查还是可发布；
- 形式化器是转写、修补还是替换了论证；
- 失败路线应归档、复活还是认证关闭；
- 新模块是否静默改变了组合后的保证。

### 3.4 不只是治理文档

V34 要求可执行 Schema、确定性组合规则、可回放事件、工件哈希、行动收据、符合性夹具与威胁测试。只有政策文本而没有强制与证据，不能声称符合 MKS。

---

## 4. 与 V33 和 SIP 的关系

### 4.1 V33 保留为理论参考模型

S1–S10 回答：

> 完整专业 AI 能力机器必须治理哪些维度？

V34 回答：

> 如何把这些维度拆成可采用模块，又不在重新组合时丢失目标、证据、权限和主张语义？

```text
参考架构 ≠ 包目录
```

一个模块可以覆盖多个 S 层，一个 S 层也可以由多个模块、内核服务和 Profile 共同实现。

### 4.2 SIP 继续是互操作协议

SIP 负责发现、manifest 交换、挂载、调用、完整性与跨运行时互操作。V34 定义模块化实现架构，并提出 `MKS Extension v0.1-draft`：

- `ModuleManifest`；
- `ProfileManifest`；
- `RecipeManifest`；
- `PackManifest`；
- `CompositionAssuranceManifest`；
- 能力接口依赖；
- 生命周期订阅；
- 失败语义；
- 符合性证据。

在 SIP 正式修订前，不得把这些对象说成已纳入 SIP v1.2 的标准 wire contract。

### 4.3 协议名与实现名必须分开

建议：

```text
SIP                     开放互操作规范
@schemabox/kernel       psi.run 参考实现
@schemabox/evidence     psi.run 模块实现
SchemaDocs              Registry、Artifact Exchange、信任与发布层
```

如果 SIP 要成为开放标准，不应长期用 `@sip/*` 命名 psi.run 私有实现。

---

## 5. V34 十二条架构不变量

### 不变量 1：十层是理论参考，模块是部署机制

S1–S10 必须保留为参考模型，不得冻结成 npm 包目录。

### 不变量 2：模块数量不是协议常数

“十二块积木”可以保留为产品表面，但模块可以按状态所有权、失败语义、测试边界和采用价值拆分或合并。

### 不变量 3：K0 独占外部副作用提交权

模块可以提出动作；只有 K0 可以准备、授权、执行并记录外部后果。

### 不变量 4：模块没有环境型隐式权限

模块不能因为被加载就自动获得文件、网络、环境变量、子进程、数据库、发布或设备权限；访问必须通过 K0 的能力句柄或受控适配器。

### 不变量 5：增加未授权模块不能扩大后果边界

没有新的签名授权时，增加模块不得：

- 扩大文件、网络、数据库、工具或设备范围；
- 提高主张发布上限；
- 删除证据义务；
- 降低任何风险坐标。

### 不变量 6：治理决策是向量，不是一个布尔值

权限、证据、目标、容量、发布、风险和主张上限必须保持正交。

### 不变量 7：规范状态只有一个来源

规范状态必须能从持久、追加式事件日志中重建；模块仪表盘、图、缓存和索引只是投影。

### 不变量 8：变换生成不可变新工件

不得覆盖旧版本。任何实质变换必须生成新内容哈希与 `TransformationReceipt`。

### 不变量 9：失败行为必须预先声明

超时、不可用、无效状态和依赖失败时的行为必须在执行前确定，不能临时为了“继续运行”而放松硬边界。

### 不变量 10：领域语义属于 Profile

“什么算验证、合格、安全、相关、新颖、可发布”必须由领域 Profile 定义，通用模块只提供状态机、证据、权限和组合机制。

### 不变量 11：产品以经过测试的 Recipe 交付

Recipe 必须说明 Profile、能力需求、模块版本、适配器、测试夹具、威胁测试、性能范围、保证与非保证。

### 不变量 12：轨迹是组织资产

失败路线、修复、表示变化、测试异常、配置变化与复活条件必须能够作为结构化资产保存和复用，而不要求公开私有思维链。

---

## 6. 形式化组合模型

V34 组合记为：

\[
\mathcal{C}=\langle K_0, H, R, P, M, A, E \rangle
\]

其中：

- \(K_0\)：可信微内核；
- \(H\)：宿主授权；
- \(R\)：Recipe；
- \(P\)：领域 Profile；
- \(M\)：解析后的模块集合；
- \(A\)：适配器集合；
- \(E\)：执行环境与信任库。

### 6.1 有效能力范围

\[
C_{effective}
=
C_{host-authorized}
\cap C_{recipe-requested}
\cap \bigcap_{m \in M} C_{module-restricted}(m)
\]

权限交集必须基于规范化语义，而不是字符串：真实路径、符号链接、域名、端口、重定向、工具别名、数据库操作、设备动作等都必须先规范化。

### 6.2 多维治理决策

模块返回部分决策向量：

\[
D=\langle A_u,E_v,G_t,C_p,R_l,\rho,\kappa\rangle
\]

分别表示：权限、证据、目标、容量、发布、风险向量和主张上限。

内核逐坐标合并。容量不足不能被改写成权限拒绝，证据不足不能自动等同人工审批，允许执行也不能自动允许发布。

### 6.3 风险向量

默认风险维度：

```yaml
RiskVector:
  confidentiality: LOW | MEDIUM | HIGH | CRITICAL
  integrity: LOW | MEDIUM | HIGH | CRITICAL
  irreversibility: LOW | MEDIUM | HIGH | CRITICAL
  financial: LOW | MEDIUM | HIGH | CRITICAL
  physicalSafety: LOW | MEDIUM | HIGH | CRITICAL
  claimCriticality: LOW | MEDIUM | HIGH | CRITICAL
  regulatory: LOW | MEDIUM | HIGH | CRITICAL
```

Profile 可以增加维度。风险采用逐维 join；除非 Profile 明确定义全序，否则不能用一个标量 `maxRisk()` 代替。

### 6.4 主张 lattice

主张成熟度和发布上限由 Profile 定义偏序与 `meet`：

```typescript
interface AssertionLattice<T> {
  meet(a: T, b: T): T;
  join(a: T, b: T): T;
  isAtLeast(a: T, b: T): boolean;
  validate(value: T): void;
}
```

通用内核不得假设形式证明、专家审查、产品资格鉴定、监管批准处于同一条线性阶梯。

### 6.5 证据义务

证据义务按规范化集合并集。只有当主张范围、工件身份、验证类别、独立性组、时间有效性和环境要求等价时，两个义务才可去重。

### 6.6 单调后果安全性质

若满足：模块无 ambient authority、所有效果经过 K0、宿主授权固定、权限规范化正确、Profile 的 meet/join 单调，则增加未授权模块后应满足：

\[
C_{effective}(\mathcal{C}\oplus m) \subseteq C_{effective}(\mathcal{C})
\]

\[
\kappa(\mathcal{C}\oplus m) \preceq \kappa(\mathcal{C})
\]

\[
Req_E(\mathcal{C}\oplus m) \supseteq Req_E(\mathcal{C})
\]

这是一项设计不变量，不是已经机器证明的定理；符合性套件必须验证其运行后果。

---

## 7. 四平面架构

### 7.1 K0 可信内核平面

```text
模块与 Pack 身份
发布者信任与撤回
能力授权
固定生命周期调度
策略代数
规范事件日志
工件注册表
外部效果事务执行
状态投影与回放
Schema 迁移与回滚
```

K0 不是普通业务模块，而是 V34 声称的最小可信计算基。

### 7.2 知识与治理平面

```text
Contract
Evidence
Artifact
Telos
Assertion
Trajectory
Assurance
```

回答：目标是什么、主张是什么、凭什么相信、涉及哪个工件版本、哪里失败或被替换、最强可发布状态是什么。

### 7.3 编排与资源平面

```text
Workspace
Federation
Capacity
Portfolio
Accommodation
```

回答：在哪里运行、谁来做、用多少资源、哪些路线保持活跃、何时允许挑战现有框架。

### 7.4 领域与产品平面

```text
Profiles
Adapters
Recipes
Signed Packs
Registry
```

把通用治理解释为具体行业结果。

---

## 8. K0 可信微内核

### 8.1 最小职责

K0 必须保持足够小，便于审计。其职责包括：

1. 身份与信任；
2. 能力授权；
3. 生命周期调度；
4. 决策合并；
5. 规范事件提交；
6. 工件注册；
7. 行动准备与执行；
8. 收据与幂等；
9. 状态投影与回放；
10. 迁移、恢复与回滚。

K0 不应包含 GEO 规则、行业 Prompt、法律推理、数学策略或评分权重。

### 8.2 模块身份与证明

加载模块前，K0 必须检查：

- 内容摘要；
- 发布者身份；
- 签名；
- 撤回状态；
- 内核兼容范围；
- SBOM；
- 请求权限；
- 生命周期订阅；
- 状态 Schema 与迁移；
- 测试/威胁测试摘要；
- 许可证与分发权。

### 8.3 能力授权

K0 拥有最终 Grant。模块可以缩小、拒绝、请求审批或提出新的授权提案，但不能给自己或其他模块新增权限。

### 8.4 运行时隔离

TypeScript 类型不是安全边界。安全符合性实现必须阻止模块直接调用 ambient `fetch`、文件系统、环境变量、子进程、数据库或设备接口。

建议执行类别：

| 类别 | 执行方式 | 适合模块 | 保证边界 |
|---|---|---|---|
| `M0-PURE` | 进程内纯函数 | 代数、Schema 校验 | 无外部权限 |
| `M1-WORKER` | Worker/线程消息接口 | Observer、Transformer | 语言/进程隔离有限 |
| `M2-WASI` | WASI/Wasmtime 显式能力 | 第三方模块 | 能力型运行时约束 |
| `M3-REMOTE` | K0 代理的签名远程服务 | 企业策略、重验证器 | 依赖网络与服务信任 |
| `K0-NATIVE` | 审计过的内核代码 | 权限、日志提交、执行器 | 最高信任，代码最小化 |

### 8.5 不可变上下文

```typescript
interface ModuleContext {
  readonly runId: string;
  readonly phase: LifecyclePhase;
  readonly stateSnapshotHash: string;
  readonly artifactSnapshotHash: string;
  readonly policySnapshotHash: string;
  readonly state: Readonly<StateView>;
  readonly artifacts: ReadonlyArtifactView;
  readonly emitProposal: (proposal: ModuleProposal) => void;
}
```

Handler 不能修改规范状态，只能返回决策、拟议事件和拟议工件，由 K0 裁决提交。

---

## 9. 固定 P0–P10 生命周期

```text
P0  MODULE_LOAD_AND_ATTEST
P1  INPUT_NORMALIZATION
P2  GOAL_PROFILE_CONTEXT_BINDING
P3  PLAN_AND_ROUTE_PROPOSAL
P4  ACTION_GOVERNANCE
P5  ACTION_PREPARE_AND_INTENT_COMMIT
P6  KERNEL_ACTION_EXECUTION
P7  RESULT_ARTIFACT_EVIDENCE_REGISTRATION
P8  ASSERTION_AND_SUPPORT_EVALUATION
P9  RELEASE_GOVERNANCE_AND_STATE_COMMIT
P10 MERGE_COMPACT_STAGNATION_TEARDOWN
```

### 9.1 阶段权属

| 阶段 | 模块参与 | K0 权力 |
|---|---|---|
| P0 | Manifest | 校验、解析、拒绝、加载 |
| P1 | Contract Transformer/Gate | 冻结规范输入 |
| P2 | Telos、Profile、Contract | 封存目标与语义 |
| P3 | Portfolio、Federation、Telos | 冻结计划快照 |
| P4 | Gate、Assurance、Capacity | 合并决策向量 |
| P5 | 普通模块不得执行 | 记录意图、幂等键、授权票据 |
| P6 | 普通模块无 Handler | 通过受控适配器执行 |
| P7 | Evidence、Artifact、Assurance | 注册收据、工件与证据 |
| P8 | Assertion、Trajectory、Assurance、Telos | 评估支持集和上限 |
| P9 | 发布 Gate | 以受治理外部效果执行发布并原子提交 |
| P10 | 合并、压缩、停滞、销毁 | 持久化、重建、撤销临时 Grant |

### 9.2 确定性

Gate 的最终结果必须与完成顺序无关。相同快照、模块版本、Profile 与配置应产生相同合并结果，除非明确声明非确定性观察并记录原始证据。

### 9.3 超时语义

| 关键性 | 默认超时行为 |
|---|---|
| `SECURITY_CRITICAL` | 拒绝或 fail-closed |
| `CLAIM_CRITICAL` | 阻止发布并保留候选 |
| `OPERATION_CRITICAL` | defer 或 require human |
| `ADVISORY` | 降级并记录缺失信号，Profile 允许时继续 |

### 9.4 发布也是外部动作

持久化或公开发布主张必须使用与其他外部动作相同的授权票据和行动收据。

---

## 10. 多维策略代数

### 10.1 权限坐标

```typescript
type AuthorizationDecision =
  | { status: 'ALLOW' }
  | { status: 'DENY'; reasons: Reason[] }
  | { status: 'REQUIRE_HUMAN'; approvalClass: string; reasons: Reason[] };
```

### 10.2 证据坐标

```typescript
type EvidenceDecision =
  | { status: 'SUFFICIENT' }
  | { status: 'REQUIRE_EVIDENCE'; requirements: EvidenceRequirement[] };
```

### 10.3 目标坐标

```typescript
type GoalDecision =
  | { status: 'CONTINUE' }
  | { status: 'EXPLORE'; ticketClass: string }
  | { status: 'VERIFY' }
  | { status: 'REFRAME'; proposalRef: string }
  | { status: 'STOP'; outcomeClass: string }
  | { status: 'ASK'; questionRef: string };
```

### 10.4 容量坐标

```typescript
type CapacityDecision =
  | { status: 'ADMIT' }
  | { status: 'HOLD' }
  | { status: 'SCALE_UP'; leaseRequestRef: string }
  | { status: 'SCALE_DOWN'; targetRef: string }
  | { status: 'OVERFLOW'; routeId: string }
  | { status: 'REQUEST_BUDGET'; requestRef: string };
```

### 10.5 发布坐标

```typescript
type ReleaseDecision =
  | { status: 'ALLOW_RELEASE'; scopeRef: string }
  | { status: 'BLOCK_RELEASE'; reasons: Reason[] }
  | { status: 'RELEASE_PARTIAL'; claimAtomRefs: string[]; exclusions: string[] };
```

### 10.6 总决策

```typescript
interface GovernanceDecision<TAssertion> {
  authorization: AuthorizationDecision;
  evidence: EvidenceDecision;
  goal: GoalDecision;
  capacity: CapacityDecision;
  release: ReleaseDecision;
  risk: RiskVector;
  assertionCeiling: TAssertion;
  proposedEvents: ProposedEvent[];
  proposedArtifacts: ProposedArtifact[];
}
```

### 10.7 必须测试的代数性质

Profile 定义的合并操作应测试：交换律、结合律、幂等律、单调性、确定性序列化与稳定规范化。

---

## 11. 规范事件日志与状态投影

### 11.1 日志要求

规范日志必须提供：

- append-only API；
- 单调 sequence；
- previous-event hash；
- event hash；
- Schema version；
- actor/module identity；
- 持久提交确认；
- 幂等键；
- 事务边界；
- 损坏检测；
- 快照与回放；
- 迁移历史。

```typescript
interface KernelEvent<T = unknown> {
  eventId: string;
  sequence: string;
  eventType: string;
  schemaVersion: string;
  payload: T;
  runId: string;
  actorRef: string;
  moduleRef?: string;
  previousEventHash: string;
  eventHash: string;
  timestamp: string;
  idempotencyKey?: string;
}
```

### 11.2 两类证据，一个提交边界

- **操作证据**：动作、参数、收据、资源、权限；
- **认识证据**：目标、主张、缺陷、修复、审查、成熟度迁移。

可为扩展性分开存储，但后果性迁移必须通过同一事务 envelope 互相引用。

### 11.3 可重建投影

包括：目标状态、主张图、替代支持集、路线图、保证义务、审查覆盖矩阵、工件谱系、容量与验证债务、公开主张卡、工业配置基线。

### 11.4 回放确定性

相同事件序列和投影版本必须产生相同投影哈希。迁移必须形成新投影版本并保留旧版本可重现性。

---

## 12. 工件注册与变换收据

### 12.1 工件身份

```typescript
interface ArtifactRecord {
  artifactId: string;
  versionId: string;
  artifactType:
    | 'DOCUMENT' | 'DATASET' | 'CODE' | 'MODEL' | 'PROOF'
    | 'CHECKER' | 'REPORT' | 'CONFIG' | 'TEST_RESULT'
    | 'SIMULATION' | 'CAD' | 'MEDIA' | 'OTHER';
  contentHash: string;
  mediaType: string;
  producerRef: string;
  createdAt: string;
  sourceRefs: string[];
  derivedFrom: string[];
  supersedes: string[];
  contradictedBy: string[];
  transformationReceiptRef?: string;
  accessPolicyRef: string;
  retentionPolicyRef: string;
  integrityStatus: 'UNVERIFIED' | 'HASHED' | 'SIGNED' | 'REVOKED';
}
```

### 12.2 变换收据

```typescript
interface TransformationReceipt {
  transformationId: string;
  moduleId: string;
  moduleVersion: string;
  inputArtifactVersions: string[];
  outputArtifactVersions: string[];
  configurationHash: string;
  evidenceRefs: string[];
  deterministic: boolean;
  executedAt: string;
}
```

### 12.3 禁止原地覆盖

Registry 必须拒绝修改既有 `versionId` 对应字节。逻辑工件可以产生新版本，但历史必须可寻址。

### 12.4 变换冲突

两个 Transformer 对同一逻辑工件产生不兼容继任者且无合并规则时，必须生成 `TRANSFORMATION_CONFLICT`，不得由加载顺序决定胜者。

### 12.5 SchemaDocs 的角色

SchemaDocs 适合作为以下对象的公共/企业实现：工件身份与护照、内容寻址版本、发布者身份、主张—来源绑定、Recipe/Pack 页面、信任与撤回、API/MCP 访问、授权和交换。

---

## 13. 行动事务与效果分类

### 13.1 效果类别

```typescript
type EffectClass =
  | 'PURE'
  | 'LOCAL_REVERSIBLE'
  | 'EXTERNALLY_IDEMPOTENT'
  | 'EXTERNAL_COMPENSATABLE'
  | 'IRREVERSIBLE';
```

| 类别 | 示例 | 关键控制 |
|---|---|---|
| `PURE` | 纯计算 | 主张关键时保存确定性证据 |
| `LOCAL_REVERSIBLE` | 私有 worktree 写入 | 快照与回滚 |
| `EXTERNALLY_IDEMPOTENT` | 带幂等键 API | 去重与收据 |
| `EXTERNAL_COMPENSATABLE` | 创建云资源 | 补偿动作计划 |
| `IRREVERSIBLE` | 公开发布、支付、物理动作 | 明确审批与预提交证据 |

### 13.2 事务序列

```text
ActionProposal
    → 合并 GovernanceDecision
    → AuthorizationTicket
    → 提交 Intent Event
    → K0 经适配器执行
    → 捕获 ActionReceipt
    → 注册工件/证据
    → 提交 Outcome Event
    → 可补偿时执行补偿
```

### 13.3 行动收据

```typescript
interface ActionReceipt {
  actionId: string;
  idempotencyKey: string;
  effectClass: EffectClass;
  requestHash: string;
  responseHash?: string;
  externalReceiptRef?: string;
  status: 'PREPARED' | 'COMMITTED' | 'FAILED' | 'COMPENSATED';
  preparedAt: string;
  completedAt?: string;
}
```

V34 不承诺不可逆外部效果的普遍回滚。

---

## 14. 模块模型

### 14.1 模块类别

```text
OBSERVER
GATE
STATE_MACHINE
TRANSFORMER
ASSURANCE_PROVIDER
ROUTER
SCHEDULER
ADAPTER
META_CONTROLLER
```

`EXECUTOR` 仅保留给 K0，不对普通模块开放。

### 14.2 模块契约

```typescript
interface SchemaBoxModule {
  readonly manifest: ModuleManifest;
  readonly handlers?: Partial<Record<LifecyclePhase, ModuleHandler>>;
}
```

### 14.3 依赖能力接口，不依赖包名

```yaml
requires:
  - capability: kernel.event_journal
    version: ^1.0
  - capability: artifact.identity
    version: ^1.0
optional:
  - capability: evidence.epistemic
    version: ^1.0
provides:
  - capability: telos.routing
    version: 1.0.0
```

### 14.4 失败语义

```yaml
failureSemantics:
  onUnavailable: REQUIRE_HUMAN
  onTimeout: DEFER
  onInvalidState: FAIL_CLOSED
  onDependencyFailure: DEGRADE
```

允许值：`FAIL_CLOSED`、`DEFER`、`DEGRADE`、`REQUIRE_HUMAN`、`FALLBACK_TO_SIGNED_ROUTE`。

### 14.5 保证必须绑定前提与证据

```yaml
guarantees:
  - guaranteeId: goal.lineage_preserved
    onlyIf:
      - kernel.event_journal.available
      - goal.anchor.sealed
    evidenceRefs:
      - fixture:goal-lineage-v1
nonGuarantees:
  - mathematical_correctness
  - scientific_novelty
```

Manifest 字段是声明，不是保证已经成立的证据。

---

## 15. 标准能力表面

以下十二个名称是推荐的开发者入口，不是永久协议公理。

### 15.1 Foundation

#### 1. Contract

输入/输出 Schema、语义字段约束、目标/需求规范化、来源—目标绑定。

#### 2. Evidence

操作与认识证据、来源快照、审计等级、OpenTelemetry 与证据账本导出。

#### 3. Artifact

工件身份、不可变版本、谱系、变换收据、访问与保留策略。

#### 4. Workspace

Context/worktree/WASI/container/remote 隔离、快照、读写边界、销毁证据。

### 15.2 Governance

#### 5. Telos

封存目标、GoalDelta、进展与停滞、结果中立处置、重构提案。

#### 6. Assertion

主张注册、claim atoms、替代支持集、Profile 定义成熟度与发布上限、降级与撤回传播。

#### 7. Trajectory

路线/分支生命周期、生产性否决、义务重开、修复/替换谱系、负面知识与表示变化资产。

#### 8. Assurance

Proof kernel、exact checker、测试、仿真、审查适配；目标绑定；验证器加固；审查者资格、独立性、覆盖与暴露；证据上限。

### 15.3 Orchestration

#### 9. Federation

模型/工具/专家角色路由、类型化交接、数据政策、相关性审查、签名回退路径。

#### 10. Capacity

容量 Envelope/Lease、验证储备、认识背压、验证债务、溢出与预算请求。容量不能改变权限边界和发布标准。

#### 11. Portfolio

项目/目标组合、全局目标去重、路线多样性签名、凭证经济学、campaign/subepisode 核算、少数路线保留。

#### 12. Accommodation

竞争性框架提案、等预算 tournament、迁移/回滚、兼容与重新验证。只能提案，不能自行改变权限、保密、审计或主张上限。

---

## 16. ModuleManifest 规范形态

```yaml
ModuleManifest:
  moduleId: psi.schemabox.telos
  version: 1.0.0
  implementationRef: "@schemabox/telos"
  kernelCompatibility: ">=0.1.0 <0.2.0"
  moduleKinds: [STATE_MACHINE, ROUTER]
  provides:
    - capability: goal.state
      version: 1.0.0
    - capability: telos.routing
      version: 1.0.0
  requires:
    - capability: kernel.event_journal
      version: ^1.0
    - capability: artifact.identity
      version: ^1.0
  optional:
    - capability: evidence.epistemic
      version: ^1.0
  conflicts: []
  lifecyclePhases:
    - P2_GOAL_PROFILE_CONTEXT_BINDING
    - P3_PLAN_AND_ROUTE_PROPOSAL
    - P8_ASSERTION_AND_SUPPORT_EVALUATION
    - P10_MERGE_COMPACT_STAGNATION_TEARDOWN
  privileges:
    fsRead: []
    fsWrite: []
    network: []
    tools: []
    environment: []
  criticality: CLAIM_CRITICAL
  failureSemantics:
    onUnavailable: REQUIRE_HUMAN
    onTimeout: DEFER
    onInvalidState: FAIL_CLOSED
    onDependencyFailure: DEGRADE
  state:
    schemaRef: schemas/telos_state_v1.json
    migrationRefs: []
    rebuildableFromJournal: true
  events:
    consumes: [plan.proposed, assertion.proposed, progress.window.closed]
    emits: [telos.signal, goal.delta.proposed]
  integrity:
    packageDigest: sha256:...
    signatureRef: sigstore:...
    sbomRef: spdx:...
    publisherRef: did:psi:...
    revocationRef: https://registry.example/revocations/...
  guarantees:
    - guaranteeId: goal.lineage_preserved
      onlyIf: [kernel.event_journal.available, goal.anchor.sealed]
      evidenceRefs: [fixture:goal-lineage-v1]
  nonGuarantees: [mathematical_correctness, scientific_novelty]
  conformance:
    fixtureRefs: []
    threatTestRefs: []
    independentAuditRefs: []
```

配套 JSON Schema 已包含在 V34 软件包中。

---

## 17. Transformer DAG

```typescript
interface TransformerSpec {
  moduleId: string;
  consumes: string[];
  produces: string[];
  after: string[];
  before: string[];
  readStatePaths: string[];
  deterministic: boolean;
  idempotent: boolean;
  cacheKeyFields: string[];
  mergeStrategy?: string;
}
```

编译器必须拒绝：循环依赖、未解析输入类型、未声明写入、无合并策略的冲突继任、请求 P6 执行权、对规范快照的可变访问。

用户声明顺序决定变换顺序属于不符合 V34 的行为。

---

## 18. Profile

Profile 定义领域语义，不定义通用运行机制。

### 18.1 必备字段

```yaml
ProfileManifest:
  profileId: psi.profile.geo-audit
  version: 1.0.0
  domain: GEO
  goalTypes: [...]
  assertionTypes: [...]
  evidenceClasses: [...]
  riskDimensions: [...]
  assertionLatticeRef: ...
  supportSetPolicies: ...
  approvalPoints: [...]
  releaseForms: [...]
  temporalValidityRules: ...
  reviewerQualificationRules: ...
  requiredFixtures: [...]
  nonGuarantees: [...]
```

### 18.2 Research Profile

定义 hypothesis/candidate/tested/corroborated/formally checked/independently reviewed/published/corrected/retracted；claim atoms；支持集；prior art；研究档案；生产性否决；formalizer/checker delta。

### 18.3 GEO Profile

定义监测问题、平台与地区、品牌/产品主张、引用与检索状态、观察与因果边界、错误修正、前后窗口、发布者权威，以及不保证排名/推荐。

### 18.4 Decision Research Profile

定义决策问题、非目标、来源层级、时间截止、主张—证据矩阵、反方证据、不确定性、情景假设、人类审查点、更新/撤回与行动边界。

### 18.5 SchemaDocs Evidence Profile

定义文档护照、发布者、来源/许可、主张、版本、替代/矛盾/撤回、机器访问策略、签名和归档状态。

### 18.6 Industrial Realization Profile

定义需求、运行包线、架构与接口预算、模型可信度、试验系统资格、配置基线、制造与供应、危险/可靠性、现场反馈。不得从数学或软件符合性推导工业认证。

---

## 19. Adapter、Recipe、Pack 与 Registry

### 19.1 Adapter

连接模型/API、浏览器、MCP、数据库、DMS、Lean、exact checker、仿真器、容器/WASI 和人类审查队列。Adapter 必须声明数据外传、凭据、效果类别、重试/幂等与收据。

### 19.2 Recipe

经过测试的结果型组合，必须包含 Profile、能力需求、模块/适配器、配置、夹具、威胁测试、性能范围、降级、保证/非保证、升级/回滚。

### 19.3 Pack

```text
Modules
+ Adapters
+ Profile
+ Recipes
+ Schemas
+ Fixtures
+ Documentation
+ SBOM
+ Signature
+ License
+ Revocation metadata
```

### 19.4 Registry

提供发现、发布者身份、版本、兼容、签名、撤回、漏洞、许可、授权、符合性报告、计费和交易。SchemaDocs 是 psi.run 推荐的 Registry 与 Artifact Exchange 实现。

---

## 20. 组合编译器

### 20.1 输入

```typescript
const compilation = await compileComposition({
  recipe,
  profile,
  modules,
  adapters,
  hostAuthority,
  environment,
  trustStore,
});
```

### 20.2 编译步骤

1. 规范化 Manifest；
2. 验证签名与撤回；
3. 解析能力依赖/版本；
4. 冲突检查；
5. Profile 要求校验；
6. 计算有效权限；
7. 计算风险向量；
8. 合并证据义务；
9. meet 主张上限；
10. 编译生命周期订阅；
11. 编译 Transformer DAG；
12. 校验事件 Schema 与迁移；
13. 生成降级计划；
14. 绑定夹具与威胁测试；
15. 输出解析组合与保证清单。

### 20.3 ResolvedComposition

```typescript
interface ResolvedComposition<TAssertion> {
  modules: ResolvedModule[];
  adapters: ResolvedAdapter[];
  phaseGraph: PhaseGraph;
  capabilityScope: CapabilityGrant;
  risk: RiskVector;
  requiredEvidence: EvidenceRequirement[];
  assertionCeiling: TAssertion;
  degradationPlan: DegradationPlan;
  configurationHash: string;
}
```

### 20.4 CompositionAssuranceManifest

```typescript
interface CompositionAssuranceManifest {
  recipeId: string;
  profileId: string;
  resolvedModules: string[];
  resolvedAdapters: string[];
  dependencyGraphHash: string;
  lifecyclePlanHash: string;
  configurationHash: string;
  effectiveCapabilityScope: CapabilityGrant;
  finalRisk: RiskVector;
  assertionCeiling: unknown;
  requiredEvidence: EvidenceRequirement[];
  declaredGuarantees: GuaranteeClaim[];
  verifiedGuarantees: VerifiedGuarantee[];
  unverifiedGuarantees: GuaranteeClaim[];
  nonGuarantees: string[];
  fixtureResults: TestResult[];
  threatTestResults: TestResult[];
  degradedModes: DegradedMode[];
  unresolvedConflicts: Conflict[];
  conformanceLevel:
    | 'UNVALIDATED'
    | 'TYPE_CHECKED'
    | 'FIXTURE_TESTED'
    | 'THREAT_TESTED'
    | 'INDEPENDENTLY_REPRODUCED'
    | 'EXTERNALLY_AUDITED';
}
```

必须区分声明保证、已验证保证和未验证保证。

---

## 21. Standalone、Degraded 与 Profile-Conformant

| 缺失能力 | 仍可做 | 不得声称 |
|---|---|---|
| Evidence | 临时内部处理 | 可审计、可回放 |
| K0 权限 | R0 纯推理 | 受保护外部动作 |
| Telos | 有界事务 | 长程目标保持 |
| Assertion | 生成文本 | 证据分层主张治理 |
| Assurance | 候选输出 | 已验证结果 |
| Trajectory | 当前尝试 | 路线替换/失败资产化 |
| Artifact Registry | 临时字节 | 版本化谱系工件 |
| Durable Journal | 本地原型 | 规范回放与崩溃恢复 |

---

## 22. 失败与降级语义

| 能力 | 默认失败行为 |
|---|---|
| Contract | 阻止外部输出；保留内部候选和违规记录 |
| Evidence | 阻止 A2/A3；Profile 允许时仅 A0 可降级 |
| Artifact | 身份/哈希不明时阻止发布和替换 |
| Workspace | 阻止高风险执行 |
| Telos | 长程任务暂停或询问人工；有界事务可继续 |
| Assertion | 阻止主张升级与发布 |
| Trajectory | 阻止无谱系路线替换/成熟化声明 |
| Assurance | 保持候选，不能提高上限 |
| Federation | 使用签名回退或停止 |
| Capacity | 仅保持/缩减，不扩大授权 |
| Portfolio | 停止新开目标，保留已验证工作 |
| Accommodation | 保持现有框架，不自行替换 |

失败必须产生类型化事件，并说明 unavailable/degraded/deferred/denied。

---

## 23. 供应链与 Registry 安全

每个第三方模块/Pack 必须提供：发布者身份、签名、摘要、SBOM、权限、网络/数据外传、生命周期阶段、状态路径/迁移、兼容内核、测试、许可、漏洞/撤回、回滚版本。

| 威胁 | 控制 |
|---|---|
| 加载时副作用 | 受限加载器，无 ambient authority |
| Manifest 欺骗 | 规范化与签名验证 |
| 权限扩大 | 三重交集与宿主批准 |
| Hook 顺序捕获 | 固定生命周期与 DAG |
| 事件篡改 | 哈希链持久日志 |
| 工件覆盖 | 不可变内容寻址版本 |
| 保证洗白 | 证据绑定保证成熟度 |
| Profile 混淆 | 签名 Profile 身份与兼容检查 |
| Recipe 降级隐藏 | 显式降级清单与发布上限 |
| Adapter 外泄 | egress policy、DLP、收据、最小化 |
| 回放分歧 | 投影哈希与迁移测试 |
| 外部动作重复 | 幂等键与 ActionReceipt |
| 模块 DoS | 超时、配额、关键性失败语义 |
| 相关性审查 | 审查者/模型独立性图 |

---

## 24. 可观测性与 OpenTelemetry

```text
OpenTelemetry
    记录运行、延迟、错误、资源

Schema Sandbox Evidence
    记录目标、主张、证据、工件、修复、审查、发布含义
```

建议属性：

```text
sip.goal.id
sip.formulation.id
sip.route.id
sip.branch.id
sip.assertion.id
sip.support_set.id
sip.artifact.version_id
sip.evidence.class
sip.assertion.ceiling
sip.actor.class
sip.model.run_id
sip.human.intervention
sip.assurance.class
sip.repair.relation
sip.capacity.lease_id
sip.action.effect_class
sip.action.receipt_id
sip.recipe.id
sip.profile.id
```

Telemetry 不得成为规范认识状态。

---

## 25. 符合性与成熟度

### 25.1 实现成熟度

| 等级 | 含义 |
|---|---|
| `M0 EXPERIMENTAL` | 原型，接口可能变化，无保证 |
| `M1 PACKAGED` | 有 Manifest、版本、Schema、基本测试 |
| `M2 COMPOSITION_TESTED` | 生命周期、代数、回放、故障夹具通过 |
| `M3 SIGNED_PROFILE_CONFORMANT` | 签名、SBOM、Profile 要求、持久回放 |
| `M4 INDEPENDENTLY_AUDITED` | 独立威胁审查与复现 |

### 25.2 V34 发布时参考实现状态

| 区域 | 状态 | 可以声称 |
|---|---|---|
| Core 类型 | `PROTOTYPED` | 架构对齐类型表面 |
| 固定生命周期骨架 | `PROTOTYPED` | 本地原型阶段顺序 |
| 标量代数函数 | `PROTOTYPED` | 不足以支撑领域保证 |
| 多维决策代数 | `SPECIFIED` | 暂无运行时保证 |
| 运行时能力隔离 | `SPECIFIED` | 不能声称安全边界 |
| 持久事件日志 | `SPECIFIED` | 不能声称回放/恢复 |
| 不可变工件注册 | `SPECIFIED` | 不能声称谱系保证 |
| 模块签名/撤回 | `SPECIFIED` | 不能声称供应链信任 |
| Profile/Recipe 编译 | `SPECIFIED` | 不能声称 Profile 符合 |
| 独立测试 | `PLANNED` | 不能声称独立保证 |

P0 完成前，正确名称是：**架构对齐的模块化知识系统骨架原型**。

---

## 26. 符合性测试套件

### 26.1 组合代数

必须测试：权限交集/风险 join/证据并集/主张 meet 的交换律、结合律、幂等律；增加未授权模块不扩大权限；增加模块不抬高主张上限；移除证据不能提高成熟度；Gate 完成顺序不影响结果。

### 26.2 日志与工件

必须测试：相同日志回放同一投影哈希；previous-event hash 损坏被检测；重复幂等键不重复执行；工件版本不可覆盖；每次变换有收据；发布主张绑定精确版本；迁移保留旧状态可重现。

### 26.3 失败语义

必须测试：安全关键超时 fail-closed；主张关键超时阻止发布；缺少 Evidence 阻止 A2/A3；缺少 Assurance 不得标记 verified；Accommodation 不可用不改变框架；Capacity 失败不能扩大范围；Profile 不匹配阻止编译。

### 26.4 恶意模块

测试：直接 fetch、越权写、修改 context、伪造 sequence/moduleId、重复提交、无限阻塞、超大 payload、加载时副作用、未声明权限、无证据保证、撤回模块挂载、未声明工件继任。

---

## 27. 参考 Recipe

### 27.1 SchemaDocs Evidence Room

```text
Contract + Evidence + Artifact + Assertion + Trajectory + Trust/Signing Adapter
```

结果：文档护照、发布者身份、主张—来源绑定、不可变版本、替代/矛盾/撤回、API/MCP、授权与交换。

不保证：签名发布者的主张必然真实、全球新颖、监管批准。

### 27.2 GEO Audit

```text
Contract + Evidence + Artifact + Telos + Assertion + Trajectory
+ Assurance + Portfolio + Search/Browser Adapters
```

结果：问题组合、平台/地区快照、品牌/产品主张、引用图、错误/遗漏、修复建议、前后证据比较、Evidence Pack。

不保证：排名、推荐、单一页面变化的因果、模型更新后永久有效。

### 27.3 Decision Research Dossier

```text
Contract + Evidence + Artifact + Telos + Assertion + Trajectory
+ Assurance + Federation + Capacity + Portfolio
```

结果：封存决策问题、多路线研究、主张—证据矩阵、反方证据、不确定性、专家介入、决策报告、更新/降级/撤回。

### 27.4 AI 数学研究

```text
Contract + Evidence + Artifact + Telos + Assertion + Trajectory
+ Assurance + Portfolio + Workspace
+ 可选 Federation/Capacity
```

Profile 控制：来源/量词绑定、证明/反例证书类型、formalizer delta、exact checker 加固、审查独立性/覆盖、prior art、campaign/subepisode、结果成熟化。

数学案例推动这些控制，但不验证 V34 整体有效性。

---

## 28. 从数学案例吸收的设计要求

| 观察 | V34 机制 |
|---|---|
| 一个 campaign 十道题可能被重复计数 | Portfolio 与全局目标注册 |
| 小反例比一般证明更易审计 | 凭证经济学 |
| 同模型批判能发现错误但高度相关 | Federation 独立性与 Assurance 覆盖 |
| 形式化器可能替换证明步骤 | 工件谱系、TransformationReceipt、Assurance delta |
| checker 在 `assert` 被关闭时仍“成功” | exact-checker 加固与环境捕获 |
| 上游路线失败、下游内核保留 | Trajectory Asset 与 Accommodation 迁移 |
| 后来人类证明不追认所有早期步骤 | 替代支持集与结果成熟图 |
| 超大形式化成为仓库工程 | Workspace、Capacity、Artifact、工作量证据 |
| 新表示法可能突破惯例盲区 | Representation-shift 轨迹资产 |
| 过程透明不等于数学已验证 | 过程证据与主张上限正交 |

---

## 29. 实施路线

### P0：先让“可信”成立

1. 多维决策代数；
2. K0 唯一副作用路径；
3. 运行时移除 ambient authority；
4. 持久哈希链追加日志；
5. 不可变工件与变换收据；
6. host × Recipe × module 权限交集；
7. 模块签名、摘要、权限与撤回；
8. 组合代数与单调后果安全属性测试。

### P1：可回放、可解释

状态投影/回放、Transformer DAG、失败语义、证据化保证清单、Profile/Recipe 编译、迁移/回滚、崩溃恢复、幂等/收据。

### P2：连接真实产品

文件/对象存储、HTTP/API、数据库、OpenAI/MCP/LangGraph、OpenTelemetry、SchemaDocs、GEO Audit、Decision Research。

### P3：规模化

Federation、Capacity、多租户、企业策略、私有 Registry 与 Pack 分发。

### P4：高风险元控制

Accommodation、等预算 tournament、迁移/重新验证、独立红队与工业试点。

---

## 30. V33 与最初模块化构想的迁移

| 旧对象 | V34 处理 |
|---|---|
| S1–S10 | 保留为理论参考 |
| 任意 `compose()` 顺序 | 编译为 P0–P10 生命周期 |
| `@sip/permission` | 策略可模块化，强制移入 K0 |
| `@sip/partition` | Workspace + Runtime Adapter |
| `claim` | 规范名 Assertion |
| `verifier` | 规范名 Assurance |
| `campaign` | 规范名 Portfolio |
| `schema-tournament` | Accommodation，仅提案 |
| 包名依赖 | 能力接口依赖 |
| “模块独立” | Standalone/Degraded/Profile-Conformant |
| 自我声明保证 | declared/verified/unverified 分离 |
| 内存日志 | 仅原型，不符合规范 |
| 只有 `supersedes` 字段 | 不可变工件 + 变换收据 |
| 标量风险/主张上限 | Profile 向量 join / lattice meet |
| 单一决策枚举 | 多维治理决策 |
| 普通文档站 | SchemaDocs Artifact/Pack/Trust Registry |

---

## 31. 商业与开放策略

### 31.1 应开放

SIP 核心与模块扩展 Schema、生命周期、能力接口词汇、策略代数接口、Module/Profile/Recipe/Pack Schema、基础 SDK、符合性夹具、示例 Profile/Recipe、签名验证逻辑。

### 31.2 应保留商业 IP

托管 K0 控制平面、企业证据/工件存储、私有行业 Profile、高价值 Recipe/Pack、GEO 诊断、研究质量策略、方法/失败模式库、领域本体、客户适配器、私有部署/审计/支持、市场信任服务。

### 31.3 产品阶梯

```text
开源：Schema、SDK、本地原型、示例 Recipe
专业版：托管 Evidence / Artifact / Assertion / Telos
企业版：私有 K0、SSO、策略、审计、数据连接
行业版：GEO、研究、法律、工业、生物证据 Pack
生态版：SchemaDocs Registry、发布者信任、授权与市场
```

### 31.4 近期优先级

优先服务已有产品：SchemaDocs Evidence Room、GEO Audit、Decision Research Dossier。它们能在通用平台之前产生真实客户、工件、失败数据与回归夹具。

---

## 32. 非目标与限制

V34 不声称：当前已有完整安全内核；模块在无隔离情况下不能逃逸；策略代数已形式证明；提升科学发现能力；具备工业认证；外部效果普遍可回滚；自动判断新颖性；多模型调用自动独立；签名 Pack 自动安全；Profile 可超范围使用；模块越多系统越强。

V34 暂缓：自授权 Schema 演化、广泛工业自治、在没有可信供给前建设开放市场、用一个分数统一有效性/安全/新颖/商业价值。

---

## 33. 可以称为“可信微内核”的发布条件

必须证明：

1. 普通模块无法绕过 K0 产生外部效果；
2. 权限范围在运行时规范化并强制；
3. 后果动作有授权票据和收据；
4. 日志持久、追加、哈希链、可回放；
5. 工件不可变且变换有收据；
6. 代数属性测试通过；
7. 崩溃恢复和重复动作防护演示；
8. 签名、撤回和权限声明被强制；
9. 至少一个 Profile/Recipe 通过夹具与威胁测试；
10. 独立审查者复现声明保证。

此前正确称谓是：

> **V34 架构对齐的模块化知识系统骨架原型。**

---

## 34. 结论

V33 建立了图式沙箱方法论的广度；最初模块化方案解决了采用问题；V34 要解决的是模块化之后还能否保持可信。

关键变化不是包数量，而是：

```text
小型可信内核
+ 固定生命周期
+ 多维策略代数
+ 事件溯源规范知识状态
+ 不可变工件谱系
+ 受治理的外部效果事务
+ Profile 定义领域语义
+ Recipe 交付结果
+ 签名 Pack 供应链
+ Registry 信任与交换
```

它同时是：

1. **方法学**：保持目标、区分候选与发布、保留负面知识、跟踪证据成熟；
2. **架构**：阻止模块绕过授权、覆盖历史或利用顺序制造保证；
3. **商业系统**：把专业能力变成可测试 Recipe、可分发 Pack 和 SchemaDocs 中可交换的可信工件。

其长期类别不是普通 Agent 框架，而是：

> **一种模块化知识系统与专业 AI 能力操作层，使目标、主张、证据、工件、修复、审查和后果能够跨异构模型与工具持续受治理。**

---

# 附录 A：参考 TypeScript 接口

```typescript
export type LifecyclePhase =
  | 'P0_MODULE_LOAD_AND_ATTEST'
  | 'P1_INPUT_NORMALIZATION'
  | 'P2_GOAL_PROFILE_CONTEXT_BINDING'
  | 'P3_PLAN_AND_ROUTE_PROPOSAL'
  | 'P4_ACTION_GOVERNANCE'
  | 'P5_ACTION_PREPARE_AND_INTENT_COMMIT'
  | 'P6_KERNEL_ACTION_EXECUTION'
  | 'P7_RESULT_ARTIFACT_EVIDENCE_REGISTRATION'
  | 'P8_ASSERTION_AND_SUPPORT_EVALUATION'
  | 'P9_RELEASE_GOVERNANCE_AND_STATE_COMMIT'
  | 'P10_MERGE_COMPACT_STAGNATION_TEARDOWN';

export type ModuleKind =
  | 'OBSERVER'
  | 'GATE'
  | 'STATE_MACHINE'
  | 'TRANSFORMER'
  | 'ASSURANCE_PROVIDER'
  | 'ROUTER'
  | 'SCHEDULER'
  | 'ADAPTER'
  | 'META_CONTROLLER';

export type FailureAction =
  | 'FAIL_CLOSED'
  | 'DEFER'
  | 'DEGRADE'
  | 'REQUIRE_HUMAN'
  | 'FALLBACK_TO_SIGNED_ROUTE';

export type Criticality =
  | 'ADVISORY'
  | 'OPERATION_CRITICAL'
  | 'CLAIM_CRITICAL'
  | 'SECURITY_CRITICAL';
```

# 附录 B：组合保证清单示例

```yaml
recipeId: psi.recipe.geo-audit
profileId: psi.profile.geo-audit
resolvedModules:
  - psi.schemabox.contract@1.0.0
  - psi.schemabox.evidence@1.0.0
  - psi.schemabox.artifact@1.0.0
  - psi.schemabox.telos@1.0.0
  - psi.schemabox.assertion@1.0.0
  - psi.schemabox.trajectory@1.0.0
  - psi.schemabox.assurance@1.0.0
  - psi.schemabox.portfolio@1.0.0
resolvedAdapters:
  - psi.adapter.browser@0.2.0
  - psi.adapter.search@0.2.0
conformanceLevel: TYPE_CHECKED
nonGuarantees:
  - ranking_improvement
  - causal_attribution
  - permanent_model_behavior
```

# 附录 C：V34 软件包结构

```text
docs/
  internal_kb_schema_sandbox_V34_MKS_EN.md
  internal_kb_schema_sandbox_V34_MKS_CN.md
  V34_RELEASE_NOTES_CN.md
  V33_TO_V34_MIGRATION_CN.md
schemas/
  module_manifest.schema.json
  profile_manifest.schema.json
  recipe_manifest.schema.json
  pack_manifest.schema.json
  kernel_event.schema.json
  artifact_record.schema.json
  action_receipt.schema.json
  composition_assurance_manifest.schema.json
examples/
  evidence_module_manifest.json
  geo_profile.json
  geo_audit_recipe.json
  geo_composition_assurance.json
  kernel_event.json
  artifact_record.json
  action_receipt.json
  geo_pack_manifest.json
tests/
  VALIDATION_REPORT.txt
  SHA256SUMS.txt
```
