---
description: Safe-Shell V2 を使用して、安全かつ自律的にプッシュを完遂する
---

このワークフローは、`GEMINI.md` の安全規定に基づき、`safe_commander` スキルと `safe-shell-server` を駆使してプッシュを完工させます。

## 前提条件
- `safe-shell-server` が稼働していること
- コミット内容が確定していること

## 手順

### 1. 武器（マクロ）の登録
// turbo
1. 現在のプロジェクトとブランチに対応したプッシュマクロを登録する。
   - `macro_id`: `[repo_name]_safe_push`
   - `cmd`: `bash`
   - `args`: `["-c", "git add . && git commit -F /tmp/commit_msg && git push origin [branch]"]`
   - `persist`: `False` (セッション限定で良い)

### 2. 背景実行の開始
// turbo
2. 登録したマクロを `background=True` で実行し、通信断絶に備える。
   - `execute_macro(macro_id="[repo_name]_safe_push", background=True)`

### 3. 自律監視の開始
// turbo
3. `get_process_status` を使用して、プッシュの進行状況を確認する。
   - ループによる監視を行い、`DONE` になるまで追跡する。
   - 通信エラーが発生した場合は、再起動後に PID から状態を復旧する。

### 4. 証跡の確認
// turbo
4. `read_recent_messages` または `git log` で、リモートに反映されたことを視認確認する。

## 注意事項
- **ハングアップ防止**: 手順 2 で必ず `background=True` を使用すること。
- **連結コマンドの局所化**: マクロ内部でのみ連結を許可し、`run_command` での連結は厳禁とする。
