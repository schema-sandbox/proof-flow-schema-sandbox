# Alpha.2 到 Alpha.3 迁移说明

## 不需要覆盖升级

Alpha.3 可以直接导入 Alpha.2 导出的 `.smath.zip`。推荐先保留 Alpha.2
工作区和导出包，再在 Alpha.3 中导入副本。不要复制 Alpha.1 源码覆盖任何目录。

## 兼容约定

- Alpha.2 的 `schema_version: "0.2"` 继续可读。
- Alpha.3 新项目和新事件使用 `schema_version: "0.3"`。
- 旧事件 JSONL 不改写；缺失的认识增量类型在读取时推断。
- `schemamath_api` Python 模块名和 `/api/v1` 路径保持不变。
- `SCHEMAMATH_*` 环境变量仍被接受，新的 `PROOFFLOW_*` 名称优先。
- Alpha.2 无依赖原型继续位于 `/prototype/`，新生产界面位于 `/app/`。

## 投影迁移

首次打开项目时会为 SQLite 投影添加 Alpha.3 列和记录表，包括模型会话、
交接工件、Arena 配方和视觉工件。SQLite 仍不是规范历史；如有疑问，可以从
`events/events.jsonl` 重建投影。

## 插件迁移

Alpha.2 的 `python.local` 调用接口继续有效。Alpha.3 会把旧式“启用”调用
映射为显式安装后启用，并写入版本锁。新插件不会静默下载依赖；缺少工具时，
先由人决定是否安装，再重新执行健康检查。

## 回滚边界

Alpha.3 不会修改已经导出的 Alpha.2 包，但含有 Alpha.3 新事件/对象的项目
不应假设旧版程序能够完整理解。需要与旧版交换时，请保留原 Alpha.2 导出包，
不要删除或重写任何历史事件。
