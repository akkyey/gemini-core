---
description: プロジェクトの自己診断を Safe-Shell V2 経由で安全に実行する
---

このワークフローは、実行に時間がかかる傾向にある診断スクリプト（`self_diagnostic.py` や `pytest`）を `safe-shell-server` の背景実行モードで走らせ、チャットの停滞を防ぎつつ結果を正確に回収します。

## 手順

### 1. 診断用武器の鍛造
// turbo
1. 現在のディレクトリにある診断スクリプトをマクロとして登録する。
   - `macro_id`: `[project_name]_diag`
   - `cmd`: `python` (または `./venv/bin/python`)
   - `args`: `["self_diagnostic.py"]` (または `["-m", "pytest"]`)
   - `persist`: `False`

### 2. 安全な「試射」（背景実行）
// turbo
2. `execute_macro` を `background=True` で実行する。
   - インテリジェント・パス解決により、`PYTHONPATH` は自動的に調整される。

### 3. 進捗監視
// turbo
3. `get_process_status` で結果を待機する。
   - `RUNNING` 状態の間は、前回の出力から変化があるか確認し、適宜ユーザーへ中間報告を行う。

### 4. 最終確認
// turbo
4. プロセスが `DONE` になったら、完全なログを確認し、全ての品質ゲートがパスしたかを判定する。
   - パスした場合のみ、コミット・プッシュ（`/safe-push`）へ移行する。
