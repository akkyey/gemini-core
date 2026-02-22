---
description: 任意のコマンドを Safe-Shell V2 経由で安全に実行する
---

「5秒ルール」に基づき、実行時間が予想されるコマンドを Safe-Shell のセキュアな身体（Execve / Isolation / Persistence）に委託します。

## 実行基準
- 実行予想時間が **5秒** を超える場合
- `PYTHONPATH` の設定などの環境構築が複雑な場合
- ネットワークや高負荷な I/O を伴う場合

## 手順

### 1. 実行環境の設計
// turbo
1. `ls` 等で現在のコンテキストを確認し、実行バイナリのパスを特定する。

### 2. 即時実行 (Short Task) または 武器化 (Long Task)
// turbo
2. 判断基準に従い、適切なツールを選択する。
   - **5秒以内**: `execute_safe` を使用。
   - **5秒超**: `register_macro` でマクロ化し、`background=True` で `execute_macro` を実行。

### 3. 追跡と回収
// turbo
3. 背景実行の場合は `get_process_status` で生存を確認し、証跡が適切に物理ファイルに残されていることを確認する。

## 注意事項
- **利点の優先**: 自分で `export` を手書きするより、Safe-Shell にパス解決を任せたほうが「楽である」ことを意識せよ。
