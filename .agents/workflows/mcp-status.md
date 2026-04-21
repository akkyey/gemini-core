---
description: MCPシステム全体のステータス確認
---

> [!IMPORTANT]
> **⚠️ [Safety Interlock]**
> 本手順を開始する前に、必ず `.agent/project_config.md` を読み込み、`SAFETY_SHELL_TOOL` 等の論理名を物理的な実体（Path/Tool ID）へ解決せよ。規約を無視した直接的な `run_command` 等の使用はプロセス違反となる。
# MCP System Status Check

物理分離された Brain と Shell の状態を一括確認します。

## 1. サーバー稼働状況の確認
1. `brain_get_system_status` ツールを実行します。
   - すべてのサーバーが `ACTIVE` であることを確認してください。
   - `OFFLINE` のサーバーがある場合は `/mcp-start` を実行してください。

## 2. プロセスログの確認
- ハングが発生している場合は、以下のログを確認してください。
  - `/home/irom/dev/mcp-servers/brain-mcp.log`
  - `/home/irom/dev/mcp-servers/safe-shell.log`
