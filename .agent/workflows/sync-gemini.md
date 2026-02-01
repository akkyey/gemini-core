---
description: .gemini サブモジュールを最新化する
---

# MCP 最新化ワークフロー

このワークフローは `.gemini` サブモジュールをすべてのプロジェクトで最新化します。

## 対象プロジェクト

1. `/home/dev/mcp-servers` (メイン)
2. `/home/dev/project-stock2` (または現在のディレクトリ)
3. `/home/dev/salesforce`

## 実行手順

// turbo-all

### 1. mcp-servers の .gemini を更新

```bash
cd /home/dev/mcp-servers/.gemini && git pull origin main
```

### 2. project-stock2 の .gemini を更新

```bash
# プロジェクトルートに移動
cd "$(git rev-parse --show-toplevel)/.gemini" && git pull origin main 2>/dev/null || echo "サブモジュール未設定"
```

### 3. salesforce の .gemini を更新

```bash
cd /home/dev/salesforce/.gemini && git pull origin main 2>/dev/null || echo "サブモジュール未設定"
```

### 4. 完了通知

Discord に通知を送信:
```
mcp_discord_send_message({ channel_name: "notifications", content: "✅ .gemini サブモジュールを最新化しました" })
```

## 備考

- サブモジュールが未設定の場合はエラーメッセージが表示されます
- 初回設定には `sync_gemini` または `join_project` ツールを使用してください
