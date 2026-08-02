# ChatGPT Companion Import 规范

## 1. 目的

ProofFlow 不自动控制 ChatGPT 网页。研究者可以从网页或其他模型产品中导出、复制或保存可见会话，再导入本地项目。导入模块解决的是“可见过程如何进入研究轨迹”，不是“如何取得模型隐藏思维”。

## 2. 支持格式

- Markdown：识别 `# User`、`# Assistant`、`User:`、`Assistant:` 等段落；
- HTML：优先识别 `data-message-author-role`，否则回退到可见文本；
- JSON：支持常见 `messages` 数组和 ChatGPT `mapping` 结构；
- Plain text：按角色行和段落进行保守拆分。

解析器保留：

- 顺序；
- 可见角色；
- 完整可见文本；
- 原始文件工件；
- 解析器名称与格式。

## 3. 两阶段模型

### Preview

上传后：

1. 原文件先进入内容寻址工件库；
2. 解析为 `ChatMessageCandidate`；
3. 为每段给出非权威的建议处置；
4. 不创建分支、挑战、桥接结果或检查点。

### Human Confirm

只有人类 actor 可以确认。每个片段可被处理为：

- `IGNORE`：只保留在原始会话；
- `MODEL_NOTE`：可见研究笔记；
- `NEW_BRANCH`：新分支；
- `CHALLENGE`：异议和检验计划；
- `BRIDGE_RESULT`：可复用中间结果；
- `RESEARCH_CHECKPOINT`：结构化状态快照。

## 4. 不做的事情

- 不推断导入文本为事实；
- 不自动声称模型贡献或自主性；
- 不把“助手说已证明”改成项目已证明；
- 不填补缺失回合；
- 不恢复系统提示；
- 不读取隐藏 chain-of-thought；
- 不自动发布会话。

## 5. API 示例

```bash
curl -F 'file=@conversation.md;type=text/markdown' \
  -F 'actor_id=researcher' \
  http://127.0.0.1:8000/api/v1/projects/$PROJECT/chat-imports/preview
```

确认：

```json
{
  "selections": [
    {
      "candidate_id": "...",
      "disposition": "CHALLENGE",
      "route_id": "...",
      "structured_payload": {
        "test_plan": "Enumerate n <= 30 exactly."
      }
    }
  ],
  "actor": {"type": "human", "id": "researcher"}
}
```

## 6. 数据边界

导入文件可能包含隐私、未公开数学内容或受版权保护文本。Alpha.2 不提供自动脱敏和访问控制；研究者必须自行决定是否导入和分享项目包。
