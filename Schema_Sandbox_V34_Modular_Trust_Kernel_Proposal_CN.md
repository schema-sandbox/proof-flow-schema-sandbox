# 图式沙箱 V34：模块化可信微内核与专业能力组合架构

## 从“12 块乐高积木”走向可验证组合、领域 Profile、结果 Recipe 与能力市场

**文档性质**：V34 架构提案 / 内部方法学与产品化方案  
**基线**：`internal_kb_schema_sandbox_paper_V33_EN.md` 与《Schema Sandbox：乐高式模块化架构》  
**目标**：在不破坏 V33 十层方法论完整性的前提下，把 Schema Sandbox 改造成可渐进采用、可验证组合、可形成生态和商业产品的模块化系统。

---

## 0. 执行结论

“12 块乐高积木”的产品直觉是正确的，但 **12 这个数字、npm 包边界和任意 `compose()` 顺序都不应成为规范本身**。更稳健的 V34 应采用以下结构：

```text
S1–S10                  理论参考模型：完整专业 AI 系统应考虑什么
        ↓
K0 Trust Kernel         不可绕过的可信微内核：身份、权限、事件、工件、事务、生命周期
        ↓
Capability Modules      可插拔能力模块：目标、主张、轨迹、验证、编排、容量等
        ↓
Domain Profiles         领域语义：GEO、研究、法律、工业工程、医药等
        ↓
Tested Recipes          结果型组合：GEO Audit、Decision Dossier、Evidence Room
        ↓
Signed Packs            可分发商业包：模块 + 适配器 + Profile + Recipe + 测试
        ↓
SchemaDocs Registry     发布、签名、版本、撤回、兼容、授权、交易与证据交换
```

V34 的核心不是“更多插件”，而是五项基础能力：

1. **不可绕过的微内核**；
2. **固定生命周期与组合代数**；
3. **事件溯源和一等工件注册**；
4. **Profile 驱动的领域语义与 Recipe 驱动的产品交付**；
5. **带保证边界、测试、签名和撤回机制的模块供应链**。

一句话定义：

> **图式沙箱在理论上采用分层参考架构，在实现上采用模块化可信微内核，在领域语义上由 Profile 驱动，在产品交付上以 Recipe 组合；模块依靠明确的策略代数组合，而不是依赖任意的中间件执行顺序。**

---

# 1. 当前模块化构想为什么是对的

V33 的主要问题不是缺少能力，而是采用成本过高。开发者通常不会先理解目标保存、主张成熟度、证明义务、容量弹性、联邦编排和工业数字线程，再决定是否使用一个输出约束器。

“乐高式模块化”正确解决了三个问题：

- **渐进采用**：用户从一个局部结果进入，而非一次接受完整理论；
- **商业分层**：免费基础模块、付费治理模块、企业编排和行业 Pack 可以形成不同价格层；
- **生态扩展**：第三方能够实现兼容模块、适配器和行业 Profile。

但当前构想仍然主要是一张产品包拆分图，而不是完整的运行规范。其关键缺口是：

- 模块按声明顺序串联，安全结果可能依赖加载顺序；
- 权限、工作区、主张、证据和状态的最终所有权不清；
- 模块能否直接执行副作用没有统一约束；
- 缺少模块冲突、失败和降级语义；
- 缺少统一工件身份、事件提交和重放机制；
- “可以独立安装”容易被误读为“可以独立提供完整保证”；
- SIP 开放协议与 psi.run 的具体 npm 实现名称混在一起；
- Profile、Recipe、Pack、Adapter 和 Registry 尚未严格区分。

因此，V34 不应推翻模块化，而应为模块增加“底板、凸点、受力规则和质量认证”。

---

# 2. V34 的十条架构公理

## 公理 1：十层是参考模型，不是十二个包的目录

S1–S10 回答“一个完整专业 AI 系统必须治理哪些问题”；模块回答“这些能力如何被部署和复用”。二者不是一对一关系。

```text
Reference Architecture ≠ Package Layout
```

一个模块可以覆盖多个层，一个层也可以由多个模块共同实现。

## 公理 2：模块数量不是设计不变量

“12 块积木”适合营销和初始产品设计，但不应写入协议的永久语义。模块可以根据独立状态、失败语义、采用价值和测试边界合并或拆分。

## 公理 3：所有外部副作用只由内核提交

模块只能提出：

- 决策建议；
- 约束；
- 变换提案；
- 证据义务；
- 需要执行的动作。

模块不得绕过内核直接写文件、调用网络、发布主张或修改规范状态。

## 公理 4：增加模块不能隐式扩大权限或主张上限

除非存在新的、经过签名和授权的能力授予，否则组合新模块后：

```text
外部能力范围只能不变或缩小
主张发布上限只能不变或降低
必要证据集合只能不变或增加
风险等级只能不变或提高
```

## 公理 5：所有变换生成新工件，不原地覆盖

任何模块修改目标、证明、代码、报告、查询、配置或结论时，必须形成：

```text
旧工件哈希 → 变换事件 → 新工件哈希
```

## 公理 6：规范状态来源唯一，视图可以很多

规范状态来自内核控制的不可变事件日志；各模块维护的索引、图和仪表盘只是可重建投影，不能成为第二权威来源。

## 公理 7：每个模块必须声明失败语义

模块失败时只能执行预先声明的行为：

```text
FAIL_CLOSED
DEFER
DEGRADE
REQUIRE_HUMAN
FALLBACK_TO_SIGNED_ROUTE
```

不得临时自行决定“为了继续运行而绕过”。

## 公理 8：领域语义属于 Profile，不属于通用模块

“什么算证明、审查、合格测试、制造可行或 GEO 证据”由领域 Profile 定义。通用模块只提供状态机、证据、权限和组合机制。

## 公理 9：产品按结果交付，不按模块编号销售

用户从“我要完成什么”进入：

- GEO 审计；
- 决策研究；
- 企业 Evidence Room；
- AI 数学研究；
- 合同审查；
- 工业设计资格鉴定。

模块是实现细节，Recipe 才是主要产品入口。

## 公理 10：任何保证都必须声明前提和非保证

模块、Recipe 和 Pack 都必须给出：

- 能保证什么；
- 依赖哪些模块、配置和证据；
- 在什么范围内有效；
- 明确不能保证什么。

---

# 3. 四平面总体架构

V34 建议把系统划分为四个正交平面。

## 3.1 可信内核平面 K0

负责不可绕过的系统宪法：

```text
Module Identity & Signature
Capability Authority
Lifecycle Scheduler
Decision Algebra
Canonical Event Journal
Artifact Identity & Lineage
Transactional Side-Effect Commit
State Projection & Replay
Version Migration & Rollback
```

K0 不作为普通业务模块出售，也不允许 Agent 动态替换。

## 3.2 认识与治理平面

负责“系统知道什么、为什么相信、哪些路线仍然有效”：

```text
Contract
Evidence
Telos
Assertion
Trajectory
Assurance
```

## 3.3 编排与资源平面

负责“谁做、以什么顺序、用多少资源、何时改框架”：

```text
Federation
Capacity
Portfolio
Accommodation
```

## 3.4 领域与产品平面

负责把通用能力解释成实际行业结果：

```text
Domain Profiles
Adapters
Recipes
Signed Packs
Registry
```

---

# 4. K0 可信微内核

## 4.1 内核的最小职责

### A. 身份服务

为以下对象分配稳定、内容可寻址的身份：

- 模块；
- Recipe；
- Profile；
- 工件；
- 事件；
- 目标；
- 主张；
- 支持集；
- 路线；
- 模型运行；
- 人类审批；
- 配置基线。

### B. 能力授权服务

内核拥有最终的 `CapabilityGrant`。模块可以提出缩小权限、要求审批或拒绝动作，但不能自行扩大权限。

### C. 生命周期调度器

内核按照固定阶段执行模块，而不是按照用户写入 `compose()` 的顺序执行。

### D. 决策合并器

把多个模块的权限、风险、证据、主张和路线决策按照固定代数合并。

### E. 规范事件日志

所有改变目标、主张、证据、配置或外部世界的动作先生成事件，再原子提交。

### F. 工件注册表

存储工件哈希、媒体类型、来源、版本、生成者、权限、替换关系和保留策略。

### G. 事务执行器

只有事务执行器可以真正：

- 写文件；
- 调用 API；
- 执行代码；
- 发布内容；
- 发送消息；
- 变更数据库；
- 升级知识状态。

### H. 重放、恢复和迁移

系统必须能从事件日志重建：

- 目标状态；
- 主张状态；
- 路线状态；
- 证据图；
- 模块投影；
- 审计报告。

---

# 5. 固定生命周期，而不是任意中间件顺序

建议采用如下规范生命周期：

```text
P0  MODULE_LOAD_AND_ATTEST
P1  INPUT_NORMALIZATION
P2  GOAL_AND_CONTEXT_BINDING
P3  PLAN_PROPOSAL
P4  ACTION_AUTHORIZATION
P5  ACTION_EXECUTION
P6  RESULT_AND_ARTIFACT_RECORDING
P7  ASSERTION_EVALUATION
P8  RELEASE_AUTHORIZATION
P9  ATOMIC_STATE_COMMIT
P10 MERGE / COMPACT / STAGNATION / TEARDOWN
```

每个模块声明订阅阶段：

```typescript
interface SchemaBoxModule {
  manifest: ModuleManifest;
  handlers?: {
    onInputNormalized?: Handler<InputEnvelope>;
    onGoalBound?: Handler<GoalEnvelope>;
    onPlanProposed?: Handler<PlanProposal>;
    onActionProposed?: Handler<ActionProposal>;
    onActionCompleted?: Handler<ActionResult>;
    onAssertionProposed?: Handler<AssertionProposal>;
    onReleaseProposed?: Handler<ReleaseProposal>;
    onStateMerge?: Handler<StateMergeProposal>;
    onCompaction?: Handler<CompactionProposal>;
    onStagnation?: Handler<StagnationSignal>;
  };
}
```

同一阶段内：

- `Observer` 可以并行；
- `Gate` 必须全部完成；
- `Transformer` 必须声明依赖 DAG；
- `Executor` 只有内核；
- `Verifier` 只产生证据与证据上限，不直接发布主张；
- `Scheduler` 只能在已授权能力范围内路由。

---

# 6. 模块组合代数

## 6.1 能力范围采用交集

```text
FinalCapability = Cap₁ ∩ Cap₂ ∩ ... ∩ Capₙ
```

## 6.2 风险等级采用最大值

```text
FinalRisk = max(Risk₁, Risk₂, ..., Riskₙ)
```

## 6.3 必要证据采用并集

```text
RequiredEvidence = Req₁ ∪ Req₂ ∪ ... ∪ Reqₙ
```

## 6.4 主张发布上限采用最保守值

```text
FinalAssertionCeiling = min(Ceiling₁, Ceiling₂, ..., Ceilingₙ)
```

## 6.5 审批优先级固定

```text
DENY
  > REQUIRE_HUMAN
  > DEFER
  > REQUIRE_EVIDENCE
  > ALLOW
```

同时必须区分拒绝类型：

- 权限拒绝；
- 证据不足；
- 目标不清；
- 容量不足；
- 路线被否决；
- 配置不兼容；
- 发布上限不足。

## 6.6 变换采用显式 DAG

两个 Transformer 同时修改同一工件时，必须声明：

- 顺序；
- 是否交换律成立；
- 是否幂等；
- 冲突检测；
- 回滚方式。

没有明确关系时，组合编译失败，而不是采用加载顺序。

## 6.7 单调后果安全性质

若所有模块满足“不得自行扩大权限”，则在没有新签名授权的情况下：

```text
Capability(C ⊕ m) ⊆ Capability(C)
AssertionCeiling(C ⊕ m) ≤ AssertionCeiling(C)
EvidenceRequirements(C ⊕ m) ⊇ EvidenceRequirements(C)
```

内部搜索容量可以扩大；外部后果边界不能隐式扩大。

---

# 7. 模块不是同一类插件

```text
OBSERVER       观察并记录，不修改规范状态
GATE           可以阻断，不直接执行副作用
STATE_MACHINE  维护特定领域状态
TRANSFORMER    生成新工件，不直接覆盖旧工件
VERIFIER       产生证据和证据上限
ROUTER         在已授权路径中选择执行者
SCHEDULER      分配时间、预算和队列
ADAPTER        连接外部模型、工具、运行时
```

典型分类：

| 能力 | 类型 | 是否能阻断 | 是否能执行副作用 |
|---|---|---:|---:|
| Contract | Gate / Transformer | 是 | 否 |
| Evidence | Observer | A2/A3 日志失败时可阻断 | 否 |
| Telos | State Machine / Router | 可暂停 | 否 |
| Assertion | State Machine / Gate | 可阻止发布 | 否 |
| Trajectory | State Machine | 可阻止无谱系替换 | 否 |
| Assurance | Verifier framework | 只改变证据上限 | 通过内核请求 |
| Federation | Router | 可回退 | 否 |
| Capacity | Scheduler | 可延迟/缩减 | 否 |
| Portfolio | Scheduler / State Machine | 可停止开新目标 | 否 |
| Accommodation | Meta-controller | 只能提案 | 否 |

权限强制和真正执行始终由 K0 内核承担。

---

# 8. 重新审视“12 块积木”

## 8.1 12 只是产品表面，不是规范真理

可以保留 12 个易理解的用户入口，但内部应按能力接口实现。推荐的用户表面如下：

### Foundation

1. `contract`
2. `evidence`
3. `artifact`
4. `workspace`

### Governance

5. `telos`
6. `assertion`
7. `trajectory`
8. `assurance`

### Orchestration

9. `federation`
10. `capacity`
11. `portfolio`
12. `accommodation`

其中：

- 原 `permission` 的策略配置仍可作为安装包，但最终执行权移入 K0；
- 原 `partition` 扩展为 `workspace`，由不同运行时 Adapter 实现；
- 新增 `artifact`，补上文档、数据、代码、证明、报告和配置的一等身份；
- `claim` 规范名改为 `assertion`；
- `verifier` 规范名改为 `assurance`；
- `campaign` 规范名改为 `portfolio`；
- `schema-tournament` 规范名改为 `accommodation`。

## 8.2 用户别名与规范名称可以并存

```text
@sip/claim              用户熟悉的别名
@schemabox/assertion    psi.run 参考实现
assertion.registry      SIP 能力接口
```

协议、实现和产品命名必须分离。

---

# 9. ModuleManifest 规范

```yaml
ModuleManifest:
  moduleId: psi.schemabox.telos
  version: 1.0.0
  implementationRef: "@schemabox/telos"

  moduleKind:
    - STATE_MACHINE
    - ROUTER

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
    - GOAL_AND_CONTEXT_BINDING
    - PLAN_PROPOSAL
    - ASSERTION_EVALUATION
    - STAGNATION

  privileges:
    fsRead: []
    fsWrite: []
    network: []
    tools: []

  criticality: CLAIM_CRITICAL

  failureSemantics:
    onUnavailable: REQUIRE_HUMAN
    onTimeout: DEFER
    onInvalidState: FAIL_CLOSED

  state:
    schemaRef: schemas/telos_state_v1.json
    migrationRefs: []
    rebuildableFromJournal: true

  events:
    consumes:
      - plan.proposed
      - assertion.proposed
      - progress.window.closed
    emits:
      - telos.signal
      - goal.delta.proposed

  integrity:
    packageDigest: sha256:...
    signatureRef: ...
    sbomRef: ...

  guarantees:
    - guaranteeId: goal.lineage_preserved
      onlyIf:
        - kernel.event_journal.available
        - goal.anchor.sealed

  nonGuarantees:
    - mathematical_correctness
    - scientific_novelty

  conformance:
    fixtureRefs: []
    testReportRefs: []
```

依赖应绑定能力接口，不应硬绑定具体 npm 包。

---

# 10. 规范状态：事件溯源 + CQRS + 工件注册

## 10.1 事件日志是唯一事实来源

所有状态变化写成不可变事件：

```text
goal.bound
route.opened
candidate.generated
defect.found
assertion.downgraded
artifact.replaced
review.completed
release.authorized
```

## 10.2 模块状态是可重建投影

各模块可以维护：

- 目标图；
- 主张图；
- 路线图；
- 证据仪表盘；
- 审查覆盖矩阵；
- 容量与债务视图。

这些都是由事件流重建的读模型。

## 10.3 工件是一等对象

```yaml
ArtifactRecord:
  artifactId: ...
  artifactType: DOCUMENT | DATASET | CODE | MODEL |
                PROOF | CHECKER | REPORT | CONFIG |
                TEST_RESULT | SIMULATION | CAD | MEDIA
  contentHash: ...
  mediaType: ...
  producerRef: ...
  createdAt: ...
  sourceRefs: [...]
  lineageRefs: [...]
  accessPolicyRef: ...
  integrityStatus: ...
  supersedes: [...]
  contradictedBy: [...]
  retentionPolicyRef: ...
```

SchemaDocs 可以直接成为这个 Artifact Registry 的公共/企业实现。

---

# 11. Profile、Recipe、Pack、Adapter、Registry 的严格区分

## 11.1 Module

提供通用治理机制，例如：

```text
telos
assertion
trajectory
assurance
```

## 11.2 Adapter

连接外部模型、工具和运行时，例如：

```text
OpenAI adapter
LangGraph adapter
MCP adapter
Lean adapter
Browser adapter
WASI adapter
Enterprise DMS adapter
```

## 11.3 Profile

定义领域语义：

```text
GEO Profile
Decision Research Profile
Mathematical Research Profile
Legal Profile
Industrial Engineering Profile
Bio-Evidence Profile
```

每个 Profile 至少定义：

- 目标类型；
- 主张类型；
- 证据类型；
- 验证等级；
- 风险类别；
- 成熟度映射；
- 人类审批点；
- 允许发布的结论形式。

## 11.4 Recipe

定义一个经过测试的结果型组合：

```text
GEO Audit Recipe
Decision Research Dossier Recipe
Enterprise Evidence Room Recipe
AI Math Research Recipe
```

Recipe 必须包含：

- 组合 manifest；
- 模块版本；
- Profile；
- Adapter；
- 示例输入；
- 回归测试；
- 威胁测试；
- 预期证据；
- 性能范围；
- 非保证声明。

## 11.5 Pack

商业分发单元：

```text
Modules
+ Adapters
+ Profile
+ Recipes
+ Fixtures
+ Documentation
+ Signature
+ License
```

## 11.6 Registry

提供：

```text
发现
版本
签名
撤回
兼容性
许可证
授权
计费
安全状态
Conformance 报告
```

SchemaDocs 最适合承担 Registry 与 Artifact Exchange，而不是只做普通文档托管。

---

# 12. 三种“独立使用”状态

模块不能简单标记“可独立使用”。应区分：

## Standalone

能够提供局部功能。

## Degraded

缺少增强能力时仍可运行，但保证上限下降。

## Profile-Conformant

只有满足完整组合，才可以宣称某个 Profile 的保证。

| 缺失能力 | 仍可做 | 不可宣称 |
|---|---|---|
| Evidence | 临时处理 | 可审计、可重放 |
| Capability Authority | R0 内部推理 | 有外部行动安全边界 |
| Telos | 单轮任务 | 长程目标保持 |
| Assertion | 生成文本 | 分层主张治理 |
| Assurance | 候选输出 | 已验证结论 |
| Trajectory | 当前运行 | 路线替换、失败资产化 |
| Artifact Registry | 临时文件 | 可验证版本与谱系 |

---

# 13. 组合保证清单

每个 Recipe 编译后生成 `CompositionAssuranceManifest`：

```yaml
CompositionAssuranceManifest:
  recipeId: ...
  resolvedModules: [...]
  resolvedCapabilities: [...]
  dependencyGraphHash: ...
  lifecyclePlanHash: ...
  finalCapabilityScope: ...
  finalRiskClass: ...
  finalAssertionCeiling: ...
  requiredEvidence: [...]
  degradationModes: [...]
  unresolvedConflicts: [...]
  conformanceProfile: ...
  fixtureResults: [...]
  threatTestResults: [...]
  guarantees: [...]
  nonGuarantees: [...]
  upgradeAndRollbackPlanRef: ...
```

这份文件是企业采购、审计和保险真正关心的对象。

---

# 14. 模块失败与降级语义

| 能力 | 默认失败语义 |
|---|---|
| Contract | 外部输出 fail-closed；内部候选可保留 |
| Evidence | A2/A3 行为 fail-closed；A0 探索可降级 |
| Artifact | 不能确定身份时禁止发布和替换 |
| Workspace | 高风险执行 fail-closed |
| Telos | 事务任务可继续；长程研究暂停或询问人工 |
| Assertion | 禁止主张发布 |
| Trajectory | 禁止路线替换与成熟化声明 |
| Assurance | 主张保持候选状态 |
| Federation | 回退到签名的单模型路径 |
| Capacity | 只允许保持或缩减，不扩大 |
| Portfolio | 停止新开目标，不影响已验证目标 |
| Accommodation | 保持当前 Schema，不自动替换 |

---

# 15. 模块供应链安全

第三方模块进入的是专业 Agent 的控制平面，因此至少需要：

```text
发布者身份
内容签名
SBOM
权限声明
网络声明
生命周期阶段声明
状态路径声明
兼容范围
迁移脚本
回滚版本
威胁测试
许可证
撤回机制
漏洞通知
```

建议的发行形式：

- SDK：npm / Python 包；
- 可部署模块：签名 OCI artifact；
- 高风险第三方逻辑：WASM/WASI 或隔离 worker；
- 证据与工件：内容寻址对象存储；
- Registry：SchemaDocs。

治理模块自身也必须受能力授权约束，不能因为“负责安全”就获得无限权限。

---

# 16. Conformance 与成熟度

建议建立五级成熟度：

| 等级 | 含义 |
|---|---|
| M0 Experimental | 原型，接口可能变化，无保证 |
| M1 Packaged | 有 manifest、版本和基本测试 |
| M2 Composition-Tested | 通过组合、回归和故障测试 |
| M3 Signed & Profile-Conformant | 签名、SBOM、Profile 一致性、可重放 |
| M4 Independently Audited | 独立安全/证据审计和第三方复现 |

同时建立四类采用标签：

```text
Local Capability
Composition Compatible
Profile Conformant
Certified Recipe
```

---

# 17. 三个现有产品作为 Reference Recipes

## 17.1 SchemaDocs Evidence Room Recipe

```text
Contract
Evidence
Artifact
Assertion
Trajectory
Trust/Signing
```

核心能力：

- 文档护照；
- 主张—来源绑定；
- 版本、替换和撤回；
- 发布者身份；
- AI/MCP/API 可访问；
- 工件交换和授权。

## 17.2 GEO Audit Recipe

```text
Contract
Evidence
Artifact
Telos
Assertion
Trajectory
Assurance
Portfolio
Search/Browser Adapters
```

核心能力：

- Prompt 组合管理；
- AI 可见度观察；
- 引用来源图；
- 品牌错误主张；
- 修复前后对照；
- 证据包发布；
- 持续监测。

## 17.3 Decision Research Dossier Recipe

```text
Contract
Evidence
Artifact
Telos
Assertion
Trajectory
Assurance
Federation
Capacity
Portfolio
```

核心能力：

- 目标绑定；
- 多路线研究；
- 反方证据；
- 主张成熟度；
- 专家修订；
- 决策级报告；
- 更新与撤回。

这三个 Recipe 是 V34 的真实验证场，不应被视为与 Schema Sandbox 无关的外围产品。

---

# 18. 商业和开放策略

## 18.1 应开放

- SIP 核心字段与能力接口；
- ModuleManifest；
- 生命周期与决策代数；
- 基础 SDK；
- Conformance fixtures；
- 示例 Profile 和 Recipe；
- 基本签名和验证逻辑。

## 18.2 应保留为商业 IP

- 托管控制平面；
- 企业证据存储；
- 私有行业 Profile；
- 高价值 Recipe；
- GEO 诊断规则；
- 研究质量策略；
- 方法与失败模式库；
- 领域本体和历史效果数据；
- 企业 Adapter；
- 私有部署、审计与支持。

## 18.3 产品层次

```text
免费：SDK、基础模块、示例 Recipe
专业版：托管 Evidence / Artifact / Telos 控制平面
企业版：私有部署、SSO、策略、审计、数据连接
行业版：GEO、研究、法律、工业 Pack
生态版：SchemaDocs Registry 与能力市场
```

---

# 19. 开发优先级

## Phase 0：K0 微内核

必须先完成：

```text
ModuleManifest
固定生命周期
决策代数
事件日志
ArtifactRecord
能力授权与事务提交
状态投影与重放
```

## Phase 1：差异化治理核心

```text
Contract
Evidence
Artifact
Assertion
Trajectory
```

直接服务 SchemaDocs。

## Phase 2：研究系统核心

```text
Telos
Assurance
Portfolio
```

直接服务 GEO 与在线快研究。

## Phase 3：运行时适配

```text
OpenAI / LangGraph / MCP adapters
Browser / Database / DMS adapters
WASI / Container workspace adapters
```

不要先自造完整 Agent Loop 或容器平台。

## Phase 4：规模能力

```text
Federation
Capacity
```

## Phase 5：高风险元控制

```text
Accommodation
Schema competition
Equal-budget frame tournament
```

Accommodation 最后实现，因为它最难验证，也最容易被误用为自我改权。

---

# 20. 当前构想到 V34 的迁移表

| 当前模块化构想 | V34 处理 |
|---|---|
| `@sip/contract` | 保留能力；实现名改为 `@schemabox/contract` |
| `@sip/evidence` | 保留，连接规范事件日志和认识日志 |
| `@sip/permission` | 策略提供器可模块化，最终强制移入 K0 |
| `@sip/partition` | 改为 Workspace 能力与运行时 Adapter |
| `@sip/telos` | 保留 |
| `@sip/claim` | 规范名改为 Assertion |
| `@sip/trajectory` | 保留 |
| `@sip/verifier` | 规范名改为 Assurance，具体工具为 Adapter |
| `@sip/federation` | 保留 |
| `@sip/capacity` | 保留，但不能改变权限边界 |
| `@sip/campaign` | 规范名改为 Portfolio |
| `@sip/schema-tournament` | 规范名改为 Accommodation，仅可提案 |
| 任意 `compose()` 顺序 | 改为生命周期编译 + 决策代数 |
| 包名依赖 | 改为能力接口依赖 |
| “每个模块独立使用” | 改为 Standalone / Degraded / Conformant |
| 文档网站 | SchemaDocs 升级为 Artifact/Pack/Trust Registry |

---

# 21. 必须避免的反模式

1. **把模块数量当成理论完整性**；
2. **把 npm 安装成功当成安全保证**；
3. **让模块直接执行外部副作用**；
4. **依赖 hook 声明顺序决定权限**；
5. **让多个模块直接写同一规范状态**；
6. **缺少 Evidence 时仍宣称可审计**；
7. **缺少 Assurance 时仍宣称已验证**；
8. **把 Profile 语义硬编码进通用模块**；
9. **先建设空 Marketplace，再寻找供给**；
10. **用 JSON Schema 模块作为商业差异核心**；
11. **把 SIP 开放协议等同于 psi.run 私有 npm 包**；
12. **让 Accommodation 自行改变权限和发布标准**。

---

# 22. V34 最值得冻结的十项决策

1. S1–S10 永远是参考模型，不是包目录；
2. K0 微内核不可绕过；
3. 模块只提出决策和工件，不直接提交副作用；
4. 权限交集、风险最大、证据并集、主张上限最小；
5. 事件日志为唯一规范状态来源；
6. 工件为一等身份对象；
7. 模块依赖能力接口，不依赖包名；
8. Profile 定义领域语义，Recipe 定义产品结果；
9. 每个组合生成保证与非保证清单；
10. SchemaDocs 是 Registry 与 Artifact Exchange，而不只是文档站。

---

# 23. 最终建议

当前“12 块乐高积木”应当保留为开发者的认知入口，但不应直接成为底层规范。最稳健的路线是：

```text
乐高式产品表面
        +
可信微内核
        +
固定生命周期
        +
策略组合代数
        +
事件与工件双账本
        +
Profile / Recipe / Pack / Registry
```

这套结构同时解决：

- V33 理论过重；
- 模块采用门槛；
- 多模块安全组合；
- 企业审计；
- 第三方生态；
- SchemaDocs、GEO 和快研究的统一；
- 从方法论向“专业 AI 能力操作系统”的升级。

真正的护城河不在于拥有最多模块，而在于：

> **任何模块、模型、工具和人类专家进入系统后，其权限、目标、证据、主张、工件、修复和发布都能在同一个可重放的可信组合框架中工作。**

