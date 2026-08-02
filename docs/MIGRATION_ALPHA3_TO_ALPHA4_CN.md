# Alpha.3 到 Alpha.4 迁移说明

Alpha.4 保留 Alpha.3 的 `.smath.zip` 与 JSONL 读取兼容性。不会修改导入包中的
历史事件；旧事件可与新的 `schema_version: "0.4"` 事件共存。

## 导入前检查

先调用 `POST /api/v1/imports/preflight`，或在 API 文档页上传压缩包。只有
`can_import: true` 时才建议执行 `POST /api/v1/imports`。预检不会创建项目、复制
工件或改变现有工作区。

## 投影迁移

打开项目时，SQLite 会记录迁移版本并补齐兼容列。它始终是可删除、可从 JSONL
重建的投影；不要把 SQLite 当作规范历史。

## 受损事件链

若完整性报告为 `valid: false`，Alpha.4 会拒绝新的写入。请保留原始目录，导出
诊断材料，并从可靠的 `.smath.zip` 或事件备份恢复；不要通过编辑历史 JSONL
来“修复”链。
