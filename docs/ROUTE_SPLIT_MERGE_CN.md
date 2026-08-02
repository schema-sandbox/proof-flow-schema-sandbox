# 路线拆分与合并

## 拆分

拆分用于把一条过宽路线显式分成两个或更多不同机制。它不会自动认定源路线错误，也不会关闭源路线。

```text
Source Route
├── Child Route A
└── Child Route B
```

接口：

```text
POST /api/v1/projects/{project_id}/routes/{route_id}/split
```

至少需要两个 child。每个 child 保存 `parent_route_id`。

## 合并

合并用于把多条路线中互补的结构形成一条综合路线。

```text
Route A ─┐
         ├── Synthesis Route
Route B ─┘
```

接口：

```text
POST /api/v1/projects/{project_id}/routes/merge
```

默认将源路线标记为 `SUPERSEDED`，但不删除它们的事件、分支或工件。若源路线的状态不允许替代，合并在写入前失败。

## 语义边界

- `SUPERSEDED` 不等于错误；
- 拆分不等于否定；
- 合并不等于证据自动合并；
- 源路线的挑战和死路不会无条件转移到新路线；
- 研究者应为综合路线重新检查假设和适用范围。
