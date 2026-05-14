# hermes-napcat-platform

`hermes-napcat-platform` 是一个 Hermes gateway platform 插件，用于通过 NapCat 的 OneBot v11 接口接入 QQ 账号。

这个项目的目标是用 Hermes 原生的 platform + toolset 设计，替代 `nanobot-channel-anon` 中依赖上下文格式化的妥协方案：

- 通过 NapCat 接收 QQ 私聊、群聊和 Notice 事件
- 暴露 QQ 专用能力为 `hermes-napcat` toolset
- 让 Agent 通过结构化工具使用 @、引用回复、表情回应、媒体发送和群管操作
- 将 OneBot message_id、QQ 号和路由细节保留在 adapter/tool 层，而不是塞进主聊天上下文

## 初始范围

- NapCat WebSocket platform adapter
- 最近事件索引，用于解析用户和消息
- 回复准备工具，用于设置 @ 和引用回复
- 基于 NapCat HTTP API 的受保护群管工具

## 开发

```bash
uv sync
uv run hermes-napcat-platform
```
