---
name: safe_commander
description: コマンド実行時のハングアップやゾンビプロセスを防止し、安全かつ追跡可能な実行環境を提供するスキル。
---

# Safe Commander Skill

このスキルは、ターミナルでのコマンド実行において「ハングアップ」「原因不明の失敗」「ゾンビプロセスによるロック競合」を防ぐための標準手順を提供します。
重要なコマンドや長時間実行されるプロセス（Git同期、サーバー起動、大規模ビルド等）を実行する際は、可能な限りこのスキルを使用してください。

## 原則

1.  **Clean First**: 実行前に「場をきれいにする」。古いプロセスやロックファイルは敵である。
2.  **Log Always**: 標準出力・エラー出力は全てファイルに残す。ターミナルバッファに頼らない。
3.  **Verify & Cleanup**: 成功を確認してからログを消す。失敗したらログを残す。

## 手順

### 1. プロセスのクリーンアップ (Cleanup Processes)

実行するコマンドに関連するプロセスが既に動いていないか確認し、強制終了します。

```bash
# 例: git 関連のプロセスを一掃する場合
pkill -f "git" || true
# 必要に応じて強力な kill
# pkill -9 -f "git" || true
```

### 2. コマンドの実行とログ記録 (Execute with Logging)

コマンドを実行し、その出力を一時ログファイルに保存します。
`tee` を使うことで、リアルタイムの出力確認とログ保存を両立します。

```bash
# ログファイル名の生成（ユニーク性が重要）
LOG_FILE="/tmp/cmd_$(date +%Y%m%d_%H%M%S).log"

# コマンド実行（set -o pipefail でパイプ途中のエラーも検知）
set -o pipefail
{
  echo "=== START: $(date) ==="
  # ここに実行したいコマンドを書く
  # 例:
  # git pull origin main
  your_command_here
  echo "=== END: $(date) ==="
} 2>&1 | tee "$LOG_FILE"
```

### 3. 結果の確認と後処理 (Verify & Teardown)

直前のコマンドの終了ステータス (`$?`) に基づいて判断します。

*   **成功 (`$? == 0`)**: ログファイルを削除します（またはアーカイブ）。
*   **失敗 (`$? != 0`)**: ログファイルのパスをユーザーに通知し、解析を促します。

## MCPでの使用例

エージェントが `run_command` でこれを行う場合のテンプレート：

```bash
# 1. Clean
pkill -f "target_process_name" || true

# 2. Exec & Log (コマンド連結せず、シェルスクリプトとして渡すか、単一行でしっかり書く)
# 以下のワンライナーは安全です（set -o pipefail を含むため）
bash -c 'set -o pipefail; your_command 2>&1 | tee /tmp/cmd_log.txt'
```

> [!TIP]
> 複雑な処理が必要な場合は、無理に `run_command` に詰め込まず、一時スクリプト (`safe_run.sh`) を作成してから実行することを推奨します。
