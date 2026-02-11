---
description: .gemini (シンボリックリンク) のHooksとMCP設定を同期する
---

# MCP 最新化ワークフロー

このワークフローは `.gemini`（シンボリックリンク）配下のHooksを適用し、MCP設定を同期します。
以前のサブモジュール方式とは異なり、`git pull` は不要です（リンク先 `gemini-core` が正であれば常に最新です）。

## 対象プロジェクト

`projects.json` に登録されているすべてのプロジェクトが対象となります。

1.  `mcp-servers`
2.  `project-stock2`
3.  `salesforce`
4.  `gemini-docs`
5.  (その他 `projects.json` に追記されたもの)

## 実行手順

// turbo-all

### 1. 各プロジェクトの Git Hooks を適用

`.gemini` がシンボリックリンクとして正しく存在することを確認し、Git Hooks をコピーします。

```bash
# gemini-core のルートを特定
CORE_ROOT=$(git rev-parse --show-toplevel)
DEV_ROOT=$(cd "${CORE_ROOT}/.."; pwd)

# projects.json を読み込み（AIは事前に内容を確認してください）
# 各プロジェクトに対して以下の処理を繰り返します：
# 1. リンク確認
# 2. git hooks 適用

# 例: mcp-servers の場合
dir="${DEV_ROOT}/mcp-servers"; [ -L "${dir}/.gemini" ] && cp "${dir}/.gemini/scripts/git-hooks/pre-commit" "${dir}/.git/hooks/" && chmod +x "${dir}/.git/hooks/pre-commit" && echo "✅ mcp-servers: Hooks適用" || echo "⚠️ mcp-servers: .geminiリンク不在またはディレクトリ不正"

# 例: project-stock2 の場合
dir="${DEV_ROOT}/project-stock2"; [ -L "${dir}/.gemini" ] && cp "${dir}/.gemini/scripts/git-hooks/pre-commit" "${dir}/.git/hooks/" && chmod +x "${dir}/.git/hooks/pre-commit" && echo "✅ project-stock2: Hooks適用" || echo "⚠️ project-stock2: .geminiリンク不在またはディレクトリ不正"

# 例: salesforce の場合
dir="${DEV_ROOT}/salesforce"; [ -L "${dir}/.gemini" ] && cp "${dir}/.gemini/scripts/git-hooks/pre-commit" "${dir}/.git/hooks/" && chmod +x "${dir}/.git/hooks/pre-commit" && echo "✅ salesforce: Hooks適用" || echo "⚠️ salesforce: .geminiリンク不在またはディレクトリ不正"

# 例: gemini-docs の場合
dir="${DEV_ROOT}/gemini-docs"; [ -L "${dir}/.gemini" ] && cp "${dir}/.gemini/scripts/git-hooks/pre-commit" "${dir}/.git/hooks/" && chmod +x "${dir}/.git/hooks/pre-commit" && echo "✅ gemini-docs: Hooks適用" || echo "⚠️ gemini-docs: .geminiリンク不在またはディレクトリ不正"
```

### 2. MCP設定ファイルの同期

リポジトリ側の `mcp_config.json` をマスター（唯一の正解）とし、IDE側へコピーします。

```bash
# MCP設定ファイルの同期
MCP_MASTER="${DEV_ROOT}/mcp-servers/mcp_config.json"
MCP_IDE="${HOME}/.gemini/antigravity/mcp_config.json"

if [ -f "${MCP_MASTER}" ]; then
  cp "${MCP_MASTER}" "${MCP_IDE}"
  echo "✅ MCP設定を同期しました: ${MCP_MASTER} → ${MCP_IDE}"
else
  echo "⚠️ マスター設定が見つかりません: ${MCP_MASTER}"
fi
```

> [!NOTE]
> - **マスター**: `mcp-servers/mcp_config.json`（リポジトリ管理、サーバー追加・パス変更はここで行う）
> - **コピー先**: `~/.gemini/antigravity/mcp_config.json`（IDE が読み込む設定）
> - 同期後はIDEのリロードが必要です
> - 参照: AP-019（MCP設定ファイル二重管理の禁止）

### 3. 完了通知

Discord に通知を送信:
```
mcp_discord_send_message({ channel_name: "notifications", content: "✅ .gemini Hooks適用＋MCP設定を同期しました" })
```

## 備考

- `.gemini` は `../gemini-core` へのシンボリックリンクである必要があります
