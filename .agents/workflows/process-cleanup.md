---
description: 孤立プロセス (bash, sleep等) の一覧表示と一括Kill
---


> [!IMPORTANT]
> **⚠️ [Safety Interlock]**
> 本手順を開始する前に、必ず `.agent/project_config.md` を読み込み、`SAFETY_SHELL_TOOL` 等の論理名を物理的な実体（Path/Tool ID）へ解決せよ。規約を無視した直接的な `run_command` 等の使用はプロセス違反となる。
## 孤立プロセスのクリーンアップ

このワークフローは、親プロセスを失い（PPID 1）システムに残存している不要なプロセス（bash, sleep, node, python 等）を一掃するためのものです。

### 1. 孤立プロセスの一覧表示
以下のコマンドを実行し、削除対象となるプロセスを確認します。
```bash
# ⚠️ Execute via SAFETY_SHELL_TOOL
python3 /home/irom/dev/mcp-servers/safe-shell/scripts/cleanup_orphans.py
```

### 2. 孤立プロセスの一括Kill
一覧を確認し、問題なければ以下のコマンドで一括削除を実行します。
```bash
# ⚠️ Execute via SAFETY_SHELL_TOOL
python3 /home/irom/dev/mcp-servers/safe-shell/scripts/cleanup_orphans.py --kill
```

---
> [!WARNING]
> この操作は、親が init (1) である特定のプログラムを強制終了します。
> 自身が意図してバックグラウンドで動かしているプロセスが含まれていないか、ステップ1のリストで必ず確認してください。
