# Sprint 1 计划
## 目标版本：`0.1.0-alpha.2`

> 实施状态：已完成。验收结果见 `SPRINT_1_IMPLEMENTATION_REPORT_CN.md` 与 `ALPHA_2_ACCEPTANCE_MATRIX_CN.md`。

建议周期：3 周。

## P0-1 研究对象完整化

- `Branch`；
- `Challenge`；
- `BridgeResult`；
- `DeadEndConstraint`；
- `ResearchCheckpoint`；
- 新对象事件和 SQLite 投影；
- 路线合并、拆分和显式 supersede。

## P0-2 ChatGPT Companion Import

支持：

- 粘贴 Markdown；
- 上传 HTML；
- 上传 JSON；
- 保存原始会话工件；
- 人工选择段落并标注为 IDEA / OBJECTION / BRIDGE / CANDIDATE；
- 可选 LLM 结构化建议，但必须由人类确认后进入路线图。

## P0-3 Python Plugin Runner

- 根据 manifest 创建独立 venv；
- 项目级启用/禁用；
- 每次运行独立工作目录；
- 记录输入、命令、环境、stdout、stderr、exit code、时限；
- 失败运行也产生 `ToolRun` 和工件；
- 插件不得直接写 `events.jsonl`。

## P1 双画布 React 化

- React Flow 正式路线图；
- Excalidraw 原始画布；
- 图形节点和结构化节点双向引用；
- 原图与解释分离；
- 事件时间线与节点联动。

## Sprint 1 验收场景

1. 导入一个 ChatGPT Markdown 会话，保存原文，并人工抽取三条研究节点；
2. 将一条失败结果标记为 BridgeResult，并交给另一条路线；
3. 安装 Python 插件，运行一个失败脚本和一个成功脚本，二者都可回放；
4. 暂眠路线后重启服务，能够从检查点恢复；
5. 将项目导出后，在空工作区导入并保持事件链完整。
