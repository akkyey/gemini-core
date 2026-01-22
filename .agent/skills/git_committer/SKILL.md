---
name: git_committer
description: GEMINI.mdの安全規定に準拠し、一時ファイルを経由して安全にGitコミットを行うためのスキル。
---

# Git Committer Skill

GEMINI.md 第7章「コマンド実行の安全性」に基づき、シェルインジェクションを防ぐ安全なコミット手順を提供します。
エージェントは変更をコミットする際、直接 `git commit -m` を使用せず、必ずこのスキルを使用してください。

> [!WARNING]
> **本スキルの使用は「絶対義務」である。**
> いかなる「軽微な修正」や「緊急対応」であっても、この手順（診断実行→一時ファイル作成→コミット）を省略することは許されない。
> 直接 `git commit` コマンドを発行した時点で、それは**プロセス違反**とみなされる。


## 作業フロー

### 1. メッセージの準備 (Prepare Message)

1.  **メッセージの構成**:
    - ユーザーからコミットメッセージを受け取るか、変更内容に基づいて生成します。
    - **Prefixの使用**: 以下のConventionに従ってください。
        - `feat:` 機能追加
        - `fix:` バグ修正
        - `docs:` ドキュメントのみの変更
        - `style:` コードの意味に影響しない変更（空白、フォーマットなど）
        - `refactor:` バグ修正も機能追加も行わないコード変更
        - `test:` テストの追加・修正
        - `chore:` ビルドプロセスやツール、ライブラリの変更

### 2. コミット前処理 (Pre-commit Hooks)

1.  **ステージングの確認 (Staging Check)**:
    - 修正がサブモジュール（例: `stock-analyzer4/`）に及ぶ場合、サブモジュール側でのコミット後に、親リポジトリ側でもその変更がステージング (`git add <submodule_path>`) されているか必ず確認してください。

<!-- (Step Removed: self_diagnostic is now enforced by Git Hook) -->

2.  **コンテキスト更新 (Context Update)**:
    - 重要な変更（src/ docs/ config.yaml等）を含む場合、コンテキストを最新化します。
      ```bash
      python3 full_context/generate_full_context.py
      ```
    - 更新されたファイルをステージングに追加します。
      ```bash
      git add full_context/
      ```

### 3. コミット実行 (Execute Commit)

### 3. コミット実行 (Execute Commit)

1.  **コミットの実行**:
    - 以下のMCPツールを呼び出し、コミットを実施します。
      - `tool: git_task.git_commit`
      - `message`: "[Prefix]: [Title]\n\n[Details]"
    - ※このツールは自動的に一時ファイル作成と安全なコミット処理を行います。

### 4. プッシュと完了確認（Push & Verify）

1.  **リモートへのプッシュ**:
    - リモートにプッシュします（これまで通り `run_command` を使用、または将来的に `git_push` ツール実装時はそちらを使用）。
      ```bash
      git push origin <branch_name>
      ```

2.  **最終ステータス確認**:
    - `tool: git_task.git_status` を呼び出し、変更が残っていないことを確認してください。

3.  **Discord通知と確認 (Notify & Verify)**:
    - コミット完了を通知し、**必ず送信成功を確認してください**。
    - `tool: discord.send_message`
    - `channel_name`: "notifications"
    - `content`: "✅ **[Commit]** `<Title>`\nブランチ `<branch_name>` にプッシュしました。"
    - **確認手順**:
        - ツール実行後、戻り値を確認し、エラーが出ていないことをチェックする。
        - ユーザーへの最終報告 (`notify_user`) に、必ず **「Discord通知: 送信確認済み」** と明記すること。
