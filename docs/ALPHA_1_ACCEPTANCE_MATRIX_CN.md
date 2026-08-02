# Alpha.1 验收矩阵

| 设计承诺 | 实现状态 | 验证方法 | 结论 |
|---|---|---|---|
| 不保证答案 | 无自动 `SOLVED` 状态 | 代码和状态枚举检查 | 通过 |
| 原始问题不被工作目标覆盖 | 独立 `original_problem` | manifest 检查 | 通过 |
| 研究历史追加保存 | JSONL event store | 单元测试 | 通过 |
| 事件可检测篡改 | SHA-256 hash chain | integrity API | 通过，单机 alpha |
| 路线可暂停和复活 | 状态机 | API 测试 | 通过 |
| 路线不易正式关闭 | 人类确认 + 证据引用 | 负向测试 | 通过，证据内容不自动判断 |
| SQLite 可重建 | 事件重放 | 删除 DB 后测试 | 通过 |
| 原始工件内容寻址 | SHA-256 blob path | 工件测试 | 通过 |
| 人类可随时加入思考 | notes endpoint + UI | API/原型测试 | 通过 |
| ChatGPT 网页伴侣 | Research Packet | 服务测试 | 初步通过 |
| 专业工具按需插件 | 仅有 manifest schemas | 无 runner | 未完成 |
| 双画布 | 原生原型 + React 源码 | 手工检查 | 部分完成 |
| 完整项目导出恢复 | zip export/import | 测试 export，import 代码 | 部分通过 |
| 模型会话导入 | 无 | — | 未完成 |
| 多模型角力 | 只有 schema/设计 | — | 未完成 |
