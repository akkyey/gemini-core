---
description: .gemini サブモジュールを最新化する
---

# MCP 最新化ワークフロー

このワークフローは `.gemini` サブモジュールをすべてのプロジェクトで最新化します。

## 対象プロジェクト

`projects.json` に登録されているすべてのプロジェクトが対象となります。

1.  `mcp-servers`
2.  `project-stock2`
3.  `salesforce`
4.  (その他 `projects.json` に追記されたもの)

## 実行手順

// turbo-all

### 1. 各プロジェクトの .gemini サブモジュールを同期

原本（`gemini-core`）から各プロジェクトへルールとHooksを配布・適用します。

```bash
# gemini-core のルートを特定
CORE_ROOT=$(git rev-parse --show-toplevel)
DEV_ROOT=$(cd "${CORE_ROOT}/.."; pwd)

# projects.json を読み込み（AIは事前に内容を確認してください）
# 各プロジェクトに対して以下の処理を繰り返します：
# 1. git pull
# 2. chmod -R a-w
# 3. git hooks 適用

# 例: mcp-servers の場合
cd "${DEV_ROOT}/mcp-servers/.gemini" && git pull origin main && chmod -R a-w . && cp scripts/git-hooks/pre-commit ../.git/hooks/ && chmod +x ../.git/hooks/pre-commit 2>/dev/null || echo "mcp-servers: サブモジュール未設定またはフォルダ不在"

# 例: project-stock2 の場合
cd "${DEV_ROOT}/project-stock2/.gemini" && git pull origin main && chmod -R a-w . && cp scripts/git-hooks/pre-commit ../.git/hooks/ && chmod +x ../.git/hooks/pre-commit 2>/dev/null || echo "project-stock2: サブモジュール未設定またはフォルダ不在"

# 例: salesforce の場合
cd "${DEV_ROOT}/salesforce/.gemini" && git pull origin main && chmod -R a-w . && cp scripts/git-hooks/pre-commit ../.git/hooks/ && chmod +x ../.git/hooks/pre-commit 2>/dev/null || echo "salesforce: サブモジュール未設定またはフォルダ不在"
```

### 4. 完了通知

Discord に通知を送信:
```
mcp_discord_send_message({ channel_name: "notifications", content: "✅ .gemini サブモジュールを最新化しました" })
```

## 備考

- サブモジュールが未設定の場合はエラーメッセージが表示されます
- 初回設定には `sync_gemini` または `join_project` ツールを使用してください
