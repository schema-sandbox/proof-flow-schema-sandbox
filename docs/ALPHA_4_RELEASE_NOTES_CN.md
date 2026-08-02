# ProofFlow Schema Sandbox `0.1.0-alpha.4` 发布说明

发布日期：2026-07-30

## 目标

Alpha.4 先加固研究历史和导入边界，不扩大为自动解题系统。Alpha.3、Alpha.2
和 Alpha.1 均保留原状；本版本在独立 Alpha.4 副本中开发。

## 新能力

- `POST /api/v1/imports/preflight` 在导入前只读检查 `.smath.zip`。
- 检查 ZIP 路径穿越、符号链接、重复成员、数量、压缩/展开大小、项目清单、
  事件链、项目 ID 一致性和内容寻址工件是否齐全。
- Alpha.2/Alpha.3 包会得到兼容性提示而不是改写历史事件。
- SQLite 投影使用登记的迁移版本；`/integrity` 返回投影 Schema 版本。
- 事件 JSONL 哈希链失败时，任何新事件追加均被拒绝，项目保持只读，供人工诊断
  和恢复，而不是在已损坏历史之后继续写入。

## 不改变的边界

- JSONL 仍是规范历史，SQLite 仍可重建。
- `UNRESOLVED` 仍是一等状态。
- 人类仍可随时插入笔记、挑战、交接和画布映射。
- 关闭路线仍需要人类与证据；系统不自动标记 solved。
- 不访问或声称访问隐藏模型思维链。
- 原始工件和失败路线不被覆盖或删除。

## 验证

- 33 项 pytest 回归，含 Alpha.2 包预检、篡改链、路径穿越、只读锁定和旧投影迁移。
- 25 个运行时 Schema、29 份 JSON Schema 文档和 47 条 OpenAPI 路径。
- React/Vite 生产构建和 npm 高危审计通过。
