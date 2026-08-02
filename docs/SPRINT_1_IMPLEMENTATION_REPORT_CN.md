# SchemaMath Sprint 1 实施报告
## `0.1.0-alpha.2`

## 1. 本阶段目标

Sprint 1 验证三个问题：

1. 数学研究过程能否从“路线”进一步细化为分支、挑战、桥接结果、死路约束和结构化检查点；
2. ChatGPT 等可见模型会话能否被完整保存、解析，并在**人类确认后**转化为研究节点；
3. 专业工具能否以按需插件方式运行，同时把成功、失败、日志和输出纳入同一条可回放研究轨迹。

Alpha.2 已实现这三个纵向闭环。

## 2. 已实现对象

### 2.1 Branch

分支是某条路线的具体实例、参数化或局部尝试。它有独立状态，但不能脱离所属路线存在。

```text
SEED → ACTIVE → CHALLENGED → DORMANT → REVIVED
                         ↘ BRIDGE_RESULT / SUPERSEDED / COMPLETED
```

### 2.2 Challenge

Challenge 表示异议或待检验问题。创建 Challenge 不自动关闭路线。支持：

- 一般异议；
- 反例搜索；
- 来源核查；
- 量词检查；
- 形式化测试；
- 计算测试；
- 边界情形。

Challenge 可以保持 OPEN、进入 TESTING、被 RESOLVED、WITHDRAWN 或保留为 INCONCLUSIVE。

### 2.3 BridgeResult

BridgeResult 保存“最终结果中可能消失、但对后续路线有帮助”的中间成果。它可以绑定路线/分支、工件、保留价值和被启用的后续路线。

### 2.4 DeadEndConstraint

DeadEndConstraint 不是普通删除标记。它记录：

- 哪条思路反复失败；
- 适用范围；
- 证据；
- 强度；
- 重新开放条件。

`CERTIFIED` 强度要求人类 actor 和证据引用。模型不可以单独宣布一条路线被证明关闭。

### 2.5 ResearchCheckpoint

Checkpoint 是主动外化的研究状态，不是隐藏思维链。它记录当前目标、准备采取的动作、已使用假设、本轮收获或失败、未完成义务、建议下一路线和置信状态。

## 3. 路线拆分与合并

### 路线拆分

一条混合路线可以拆分为两个或更多具有不同机制的子路线。源路线仍保留，子路线通过 `parent_route_id` 记录来源。

### 路线合并

两条或更多路线可以形成综合路线。默认可将来源路线标记为 `SUPERSEDED`，但来源历史、事件和工件不会被删除。

拆分与合并解决的是认识状态的结构变化，不是文件复制或聊天摘要。

## 4. ChatGPT Companion Import

支持：

- Markdown 角色段落；
- HTML 中的可见对话结构；
- 常见 JSON messages/mapping 结构；
- 纯文本角色行。

处理流程：

```text
上传会话
→ 原始字节保存为 CHAT_TRANSCRIPT 工件
→ 解析为候选片段
→ 人类逐条选择 disposition
→ 生成模型笔记 / Challenge / BridgeResult / Branch / Checkpoint
→ 未选择内容仍留在原始工件中
```

硬边界：

- 导入预览不会自动改变研究图；
- 只有人类 actor 可以确认；
- 模型输出默认不具有数学结论地位；
- 原始会话不可被派生节点覆盖。

## 5. Python 插件

Alpha.2 包含一个内置、默认禁用的 `python.local` 插件。

### 已实现

- 项目级启用/禁用；
- 独立 venv；
- 每次运行独立目录；
- 环境变量清理；
- `python -I -B`；
- wall-clock timeout；
- POSIX 下 best-effort CPU、内存和文件大小限制；
- 输出文件数量与大小限制；
- 保存源码、stdout、stderr、run metadata 和输出工件；
- 成功、失败、超时都进入事件流；
- 插件不能直接编辑 `events.jsonl`，由主服务追加规范事件。

### 没有实现

- 容器、WASM 或 microVM 强隔离；
- 网络阻断；
- 文件系统强约束；
- pip 包动态安装；
- 不可信代码安全执行。

因此该插件只适用于研究者自己信任的本地实验代码。

## 6. 浏览器原型

`/prototype/` 已支持：

- 项目、路线、分支；
- 路线拆分和合并；
- Challenge；
- BridgeResult；
- DeadEndConstraint；
- ResearchCheckpoint；
- Chat 导入预览和人工确认；
- Python 插件启用和运行；
- 手绘草图与工件上传；
- 研究事件时间线；
- Research Packet；
- 完整性检查和导出。

正式 React Flow + Excalidraw 前端仍为脚手架。本轮打包环境无法从 npm registry 取得全部依赖，因此没有声称 React 构建已验证。

## 7. 数据与可移植性

项目继续使用：

```text
project.json
事件源 events/events.jsonl
可重建 database/projections.sqlite3
内容寻址 blobs/sha256/
插件锁 plugins/plugins.lock.json
运行目录 runs/
导出 exports/
```

Alpha.2 导出的 `.smath.zip` 可在空工作区导入，随后从事件流重建全部 Alpha.2 对象和插件运行投影。

## 8. 验证结论

当前版本适合作为：

- 开源开发预览；
- 本地单用户研究原型；
- SchemaMath 对象模型和事件语义的实现基线；
- 下一阶段插件与模型角力功能的宿主。

当前版本不适合作为：

- 不可信代码执行服务；
- 多用户云服务；
- 数学正确性裁判；
- 自动解决开放问题的产品；
- 公开互联网 API。
