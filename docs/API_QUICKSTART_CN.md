# ProofFlow API 快速示例 — Alpha.8

启动服务后：

```bash
curl http://127.0.0.1:8000/health
```

完整 OpenAPI：

```text
http://127.0.0.1:8000/docs
```

## 0. 导入 `.smath.zip` 前预检

预检不会创建项目或改写工作区。只有返回的 `can_import` 为 `true` 时，再调用导入接口。

```bash
curl -X POST http://127.0.0.1:8000/api/v1/imports/preflight \
  -F "file=@project.smath.zip;type=application/zip"
```

## 1. 创建项目

```bash
curl -X POST http://127.0.0.1:8000/api/v1/projects \
  -H 'Content-Type: application/json' \
  -d '{
    "title":"开放数学探索",
    "description":"不强迫闭合",
    "problem":{"source_text":"在这里填写原始问题","author_notes":"","definitions":[],"assumptions":[]},
    "actor":{"type":"human","id":"researcher"}
  }'
```

## 2. 创建路线与分支

```bash
curl -X POST http://127.0.0.1:8000/api/v1/projects/PROJECT_ID/routes \
  -H 'Content-Type: application/json' \
  -d '{
    "title":"反例搜索路线",
    "description":"先检查小规模结构",
    "initial_state":"ACTIVE",
    "revival_conditions":[],
    "actor":{"type":"human","id":"researcher"}
  }'
```

```bash
curl -X POST http://127.0.0.1:8000/api/v1/projects/PROJECT_ID/branches \
  -H 'Content-Type: application/json' \
  -d '{
    "route_id":"ROUTE_ID",
    "title":"小参数枚举",
    "description":"先检查 n<=30",
    "initial_state":"ACTIVE",
    "actor":{"type":"human","id":"researcher"}
  }'
```

## 3. 创建 Challenge

```bash
curl -X POST http://127.0.0.1:8000/api/v1/projects/PROJECT_ID/challenges \
  -H 'Content-Type: application/json' \
  -d '{
    "route_id":"ROUTE_ID",
    "branch_id":"BRANCH_ID",
    "challenge_type":"BOUNDARY_CASE",
    "statement":"递推式在 n=1 可能失效",
    "test_plan":"精确枚举 n=1..30",
    "actor":{"type":"human","id":"researcher"}
  }'
```

## 4. 保存 BridgeResult

```bash
curl -X POST http://127.0.0.1:8000/api/v1/projects/PROJECT_ID/bridge-results \
  -H 'Content-Type: application/json' \
  -d '{
    "route_id":"ROUTE_ID",
    "branch_id":"BRANCH_ID",
    "title":"有限范围递推引理",
    "summary":"即使渐近路线失败，该有限引理仍可复用",
    "retained_value":["边界分类","有限递推"],
    "actor":{"type":"human","id":"researcher"}
  }'
```

## 5. 保存死路与重开条件

```bash
curl -X POST http://127.0.0.1:8000/api/v1/projects/PROJECT_ID/dead-ends \
  -H 'Content-Type: application/json' \
  -d '{
    "route_id":"ROUTE_ID",
    "title":"不要假设系数恒正",
    "description":"n=7 时出现负系数",
    "strength":"OBSERVED",
    "reopen_conditions":["找到新的归一化"],
    "actor":{"type":"human","id":"researcher"}
  }'
```

## 6. Chat 导入

```bash
curl -X POST \
  -F 'file=@conversation.md' \
  -F 'actor_id=researcher' \
  http://127.0.0.1:8000/api/v1/projects/PROJECT_ID/chat-imports/preview
```

确认候选节点见 `CHAT_IMPORT_GUIDE_CN.md`。

## 7. Python 插件

启用：

```bash
curl -X POST \
  -H 'Content-Type: application/json' \
  -d '{"type":"human","id":"researcher"}' \
  http://127.0.0.1:8000/api/v1/projects/PROJECT_ID/plugins/python.local/enable
```

运行：

```bash
curl -X POST \
  -H 'Content-Type: application/json' \
  -d '{
    "source_code":"print(2+2)",
    "timeout_seconds":10,
    "input_artifact_ids":[],
    "actor":{"type":"human","id":"researcher"}
  }' \
  http://127.0.0.1:8000/api/v1/projects/PROJECT_ID/plugin-runs/python
```

## 8. Research Packet、完整性与导出

```bash
curl -X POST \
  -H 'Content-Type: application/json' \
  -d '{"route_ids":[],"include_recent_events":60,"include_checkpoints":10}' \
  http://127.0.0.1:8000/api/v1/projects/PROJECT_ID/research-packets
```

```bash
curl http://127.0.0.1:8000/api/v1/projects/PROJECT_ID/integrity
curl -OJ http://127.0.0.1:8000/api/v1/projects/PROJECT_ID/export
```
