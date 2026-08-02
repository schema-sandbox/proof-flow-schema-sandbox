# `python.local` 插件运行器

## 1. 定位

`python.local` 是第一个按需数学工具插件，用于：

- 小规模枚举；
- 符号原型；
- 反例搜索；
- 数据和图形生成；
- 将模型建议转化为可执行实验。

它不是自动证明器，也不是不可信代码沙箱。

## 2. 安装与启用

插件清单位于：

```text
plugins/builtin/python.local/plugin.json
```

项目创建时默认关闭。启用后：

- 在插件根目录创建专用 venv；
- 写入项目 `plugins/plugins.lock.json`；
- 生成 `PLUGIN_ENABLED` 事件。

## 3. 每次运行

```text
runs/<run-id>/
├── main.py
├── inputs/
├── outputs/
├── tmp/
├── stdout.log
├── stderr.log
└── run.json
```

运行参数：

- `python -I -B main.py`；
- 清理后的环境变量；
- `SCHEMAMATH_INPUT_DIR`；
- `SCHEMAMATH_OUTPUT_DIR`；
- 用户指定的 1–60 秒时限；
- 最多 64 个输出文件；
- 单文件/日志默认最多 10 MiB；
- POSIX 下最佳努力 CPU、地址空间和文件大小限制。

## 4. 记录

每次运行至少保存：

- 源代码工件；
- 输入工件引用；
- 真实命令；
- Python 运行时；
- 隔离等级；
- 开始/结束时间；
- exit code；
- stdout/stderr；
- 输出文件；
- 超时与错误；
- `PLUGIN_RUN_STARTED` 和 `PLUGIN_RUN_COMPLETED` 事件。

失败与超时不会被删除，它们是研究轨迹的一部分。

## 5. 安全警告

Alpha.2 的隔离等级是：

```text
process-only
```

代码仍具有运行 ProofFlow 的本机用户权限。专用 venv、工作目录和资源限制只能减少误操作，不能防止恶意代码。不要运行不可信来源的脚本。

后续可增加：

- OCI/Podman runner；
- 无网络模式；
- 只读输入挂载；
- seccomp / gVisor；
- microVM；
- 插件签名和权限清单。
