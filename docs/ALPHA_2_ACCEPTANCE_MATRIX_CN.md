# Alpha.2 验收矩阵

| 目标 | 验收条件 | 当前状态 |
|---|---|---|
| Branch | 可创建、改状态、绑定路线、事件重放恢复 | 通过 |
| Challenge | 可创建、测试、解决，且不自动关闭路线 | 通过 |
| BridgeResult | 可绑定分支和保留价值并导出恢复 | 通过 |
| DeadEndConstraint | 可保存范围与重开条件；CERTIFIED 需人类和证据 | 通过 |
| ResearchCheckpoint | 可记录当前目标、动作、增量和未完成义务 | 通过 |
| Route split | 创建多个带父路线的子路线，源路线保留 | 通过 |
| Route merge | 创建综合路线，来源可被 supersede 但不删除 | 通过 |
| Markdown import | 解析角色段落并生成候选 | 通过 |
| HTML import | 解析可见角色结构或回退到可见文本 | 通过（解析器级） |
| JSON import | 支持 messages、mapping 和常见列表结构 | 通过（解析器级） |
| 原始会话保存 | 导入前先保存原始 CHAT_TRANSCRIPT 工件 | 通过 |
| 人工确认 | 模型 actor 不能确认导入候选 | 通过 |
| Python plugin | 项目级启用、独立 venv、运行记录 | 通过 |
| 成功运行 | stdout、stderr、源码、输出工件可追踪 | 通过 |
| 失败运行 | 非零退出、stderr 与事件仍保留 | 通过 |
| 工件限制 | 输出数量/大小和日志大小有限制 | 通过 |
| 事件链 | Alpha.2 对象和运行事件纳入 SHA-256 链 | 通过 |
| 投影重建 | 删除 SQLite 后从事件流恢复 | 通过 |
| Export/import | Alpha.2 对象和插件运行可跨工作区恢复 | 通过 |
| 浏览器原型 | 核心 Alpha.2 闭环可交互使用 | 通过 |
| React 构建 | 安装依赖并产出正式双画布构建 | 未验证；打包环境 registry 缺少依赖 |
| OS 级插件隔离 | 不可信代码不能访问主机 | 未实现；明确不作安全承诺 |
| 数学正确性判断 | 自动判定证明或反例正确 | 非目标 |
