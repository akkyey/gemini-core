---
description: .gemini環境同期
---


> [!IMPORTANT]
> **⚠️ [Safety Interlock]**
> 本手順を開始する前に、必ず `.agent/project_config.md` を読み込み、`SAFETY_SHELL_TOOL` 等の論理名を物理的な実体（Path/Tool ID）へ解決せよ。規約を無視した直接的な `run_command` 等の使用はプロセス違反となる。
# `sync-gemini` ワークフロー

このワークフローは、規約の正典である `gemini-docs` と、実行ツールの正典である `gemini-core` の最新状態を作業プロジェクトへ強制同期させるためのものです。

## 実行ステップ

### 1. マスタ規約の強制配信と環境同期 (Broadcaster & Sync)

```javascript
// ⚠️ Execute via SAFETY_SHELL_TOOL (execute_script)
SAFETY_SHELL_TOOL.execute_script({
  script: `
    # gemini-docs の最新状態を各プロジェクトへ反映
    python3 /home/irom/dev/gemini-core/scripts/broadcast_core.py

    # Git Hooks の同期
    cp /home/irom/dev/gemini-core/.gemini/scripts/git-hooks/pre-commit .git/hooks/
    chmod +x .git/hooks/pre-commit
  `,
  cwd: "{{project_root}}"
});
```

### 2. MCP 設定の同期
物理的な実態確認 (Physical Artifact Verification)
```javascript
// ⚠️ Execute via SAFETY_SHELL_TOOL (execute_script)
# 🔍 読み込んだドキュメントや ADR の記述が、現在のディレクトリやファイルの状態を物理的に確認。
```
