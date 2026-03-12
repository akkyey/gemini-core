# Safe Commander Skill (V2)

このスキルは、Safe-Shell V2 の強固な隔離基盤と自律監視能力を最大限に引き出し、AI エージェントが実行するタスクの「安全性」と「継続性」を担保するための標準手順を提供します。

## 原則

1.  **Direct Execution**: 可能な限りシェル演算子（`&&` 等）を使わず、`execute_safe` またはマクロを使用する。
2.  **Autonomous Monitoring**: 長時間タスクは背景実行 (`background=True`) に逃がし、`get_process_status` で定期定期に内省監視を行う。
3.  **Survival First**: サーバー再起動や通信断絶が発生しても、`State Persistence` によりプロセスを再補足するレジリエンスを維持する。
4.  **Clean First**: 実行前に「場をきれいにする」。古いプロセスやロックファイルは敵である。
5.  **Predictive Resources**: 実行前に必要なリソース（CPU, メモリ, 時間）を予測し、天井ではなく枠として宣言する。
6.  **Log Always**: 標準出力・エラー出力はすべてファイルに残す。ターミナルバッファに頼らない。

## 手順

### 1. 実行環境のクリーンアップ (Pre-flight Cleanup)

実行前に、競合するプロセスが残っていないか Safe-Shell を通じて確認します。

1.  **プロセス確認**:
    - `get_process_status` を実行し、既存のロックや実行中プロセスがないか確認する。
2.  **ゾンビパージ**:
    - 予期せぬ残留がある場合は、`cleanup` ツールを使用して「場」を物理的に浄化する。

### 2. インテリジェント実行 (Smart Execution)

タスクの特性に応じて、最適な実行方法を選択します。

#### A. 短時間タスク (単発コマンド)
- `execute_safe` を同期実行（`background=False`）で使用。
- `AUTO PYTHONPATH` により、サブモジュール内でもパス設定なしで実行可能。

#### B. 長時間タスク (テスト、ビルド)
1.  **背景への委ね**:
    - `execute_safe` または `execute_macro` を `background=True` で呼び出す。
2.  **監視プロセスの確立**:
    - 返された `pid` を保持し、一定間隔で `get_process_status` を実行する。
3.  **内省的パース**:
    - `log_tail` の内容を読み取り、進捗をユーザーに報告する。

### 3. レジリエンス復旧 (Recovery)

通信断絶 (EOF) やサーバー再起動が発生した場合の復元手順。

1.  **沈黙の掌握**:
    - 接続が回復次第、`get_process_status` を実行する（引数は不要。Lockから自動特定される）。
2.  **物理証跡の確認**:
    - `/tmp/safe_shell_logs/macro_history.log` 等を直接覗き、断絶中の挙動を確定させる。

## 使用例

```python
# 長時間テストの例
mcp.execute_macro(macro_id="run_tests", background=True)
# -> { "pid": 1234, ... }

# 定期監視
mcp.get_process_status(pid=1234)
# -> { "running": True, "log_tail": "..." }
```

> [!TIP]
> 複雑な環境が必要な場合は、まず `macro_forger` スキルで武器を「鍛造」してから実行することを強く推奨します。
