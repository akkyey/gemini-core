---
description: セッション開始の統合処理（Sync, Load State, Context Restore, Memory Recall）
---


> [!IMPORTANT]
> **⚠️ [Safety Interlock]**
> 本手順を開始する前に、必ず `.agent/project_config.md` を読み込み、`SAFETY_SHELL_TOOL` 等の論理名を物理的な実体（Path/Tool ID）へ解決せよ。規約を無視した直接的な `run_command` 等の使用はプロセス違反となる。
# `start` ワークフロー

このワークフローは、前回の作業内容を完璧に思い出し、即座に開発を再開するための「開店準備」コマンドです。

## 実行ステップ

### 0. 対象の特定と宣言
引数 `{{project_name}}` を確認（不明な場合は質問）し、宣言します。
> 🤖 **対象プロジェクト「{{project_name}}」のセッションを開始します。**

### 1. マスタ規約の強制配信と環境同期 (Broadcaster & Sync)

> [!CAUTION]
> **🤖 [Bootstrap Mode: Sentinel 起動チェック]**
> `list_resources` 等で `mcp_safe-shell-server` の不在（またはツールの消失）を検知した場合、エージェントは**唯一の例外**として復旧を試みる。ただし、以下のプロトコルを厳守せよ：
> 1.  **通知**: ユーザーに現在の「プロトコル不全」の状態を報告する。
> 2.  **提示**: `.agent/project_config.md` の `BOOTSTRAP_CMD` を読み込み、実行コマンドを明示する。
> 3.  **承認待ち**: **ユーザーからの明示的な許可（例: "OK", "実行して"）を得るまで、一切のコマンド発行を停止せよ。**
> 4.  **実行**: 承認後のみ `run_command` で起動スクリプトを実行し、復旧後は直ちに `execute_script` へ移行すること。

### 2. 環境同期 (Bootstrap)
ルートの `package.json` に基づき、依存関係を同期します。

```javascript
// ⚠️ Execute via SAFETY_SHELL_TOOL (execute_script)
SAFETY_SHELL_TOOL.execute_script({
  script: `
    # 🔄 基盤パッケージ間のリンク整合性の確認
    npm install
  `,
  cwd: "{{project_root}}"
});
```

### 3. 主権確保の確認とステータス監視
各サーバーが Highlander プロトコルに基づき、正常に「王座（ソケット）」を確保していることを確認します。

```javascript
// ⚠️ Execute via SAFETY_SHELL_TOOL (execute_script)
SAFETY_SHELL_TOOL.execute_script({
  script: "npm run mcp-status",
  cwd: "{{project_root}}"
});
```

### 4. コンテキストの復元と実態確認

```javascript
// ⚠️ Execute via SAFETY_SHELL_TOOL (execute_script)
SAFETY_SHELL_TOOL.execute_script({
  script: `
    # 💾 セッション状態の読み込み
    # 📄 全体コンテキストの読み込み
    # 🔍 物理的な実態確認 (Physical Artifact Verification)
    ls -R .agent/
  `,
  cwd: "{{project_root}}"
});
```

## 完了の定義
- [x] 冒頭に対象プロジェクトの宣言が行われていること
- [x] `execute_script` による同期・実態確認が完了していること
- [x] **実施内容が一覧化され、ユーザーから作業開始の合意を得ていること**
