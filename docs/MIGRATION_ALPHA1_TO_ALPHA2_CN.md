# 从 Alpha.1 迁移到 Alpha.2

Alpha.2 保留对 Alpha.1 项目 manifest 和事件的读取支持。旧项目第一次打开时不会改写既有事件。

建议步骤：

1. 备份整个 `.smath` 目录；
2. 使用 Alpha.2 启动本地服务；
3. 调用 `/integrity` 检查事件链；
4. 调用 `/rebuild-projection` 重建 SQLite；
5. 如需使用 Python 插件，在项目级显式启用；
6. 重新导出一个 Alpha.2 `.smath.zip` 作为迁移快照。

Alpha.2 新增事件和投影表不会改变 Alpha.1 原始问题、路线、工件或历史哈希。
