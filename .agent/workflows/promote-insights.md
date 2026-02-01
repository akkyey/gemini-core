---
description: 各プロジェクトの知見を一括収集し、グローバルルールへ昇格させる
---

# 知見の昇格 (Promote Insights)

このワークフローは、各プロジェクトの `.agent/local_insights.md` に蓄積された知見を収集し、`gemini-core` の各ファイル（GEMINI.md, anti_patterns.md等）への反映案を作成します。

## 実行手順

### 1. 各プロジェクトの知見を収集

以下のコマンドを実行して、各プロジェクトの `local_insights.md` の内容を表示します。

```bash
# gemini-core のルートを特定
CORE_ROOT=$(git rev-parse --show-toplevel)
DEV_ROOT=$(cd "${CORE_ROOT}/.."; pwd)

# 収集対象リスト (AIは事前に projects.json を確認し、以下の巡回を自動で行ってください)
echo "=== [mcp-servers] ===" && cat "${DEV_ROOT}/mcp-servers/.agent/local_insights.md" 2>/dev/null || echo "(no file)"
echo "=== [project-stock2] ===" && cat "${DEV_ROOT}/project-stock2/.agent/local_insights.md" 2>/dev/null || echo "(no file)"
echo "=== [salesforce] ===" && cat "${DEV_ROOT}/salesforce/.agent/local_insights.md" 2>/dev/null || echo "(no file)"
```

### 2. 内容の精査と分類

AIエージェントは、収集した内容を以下の3つに分類します。

1.  **共通ルール案**: `GEMINI.md` に追記すべき全社的方針。
2.  **新規アンチパターン案**: `anti_patterns.md` に追加すべき禁止事項。
3.  **スキル改善案**: 各スキルの `SKILL.md` に反映すべき具体的な手順。

### 3. マスタへの反映

分類された情報を `gemini-core` 内の該当ファイル（原本）に反映します。
原本ディレクトリは `$(git rev-parse --show-toplevel)` で動的に特定してください。

### 4. 反映後のクリーンアップ

マスタへの反映（コミット・Push）が完了したら、各プロジェクトの `local_insights.md` をリセットして空にします。

```bash
CORE_ROOT=$(git rev-parse --show-toplevel)
DEV_ROOT=$(cd "${CORE_ROOT}/.."; pwd)

truncate -s 0 "${DEV_ROOT}/mcp-servers/.agent/local_insights.md" 2>/dev/null
truncate -s 0 "${DEV_ROOT}/project-stock2/.agent/local_insights.md" 2>/dev/null
truncate -s 0 "${DEV_ROOT}/salesforce/.agent/local_insights.md" 2>/dev/null
```

### 5. 全軍同期

`/sync-gemini` ワークフローを実行し、最新のルールを配布します。

---

## 完了の定義
- `gemini-core` へ情報が移行されていること。
- 各プロジェクトの `local_insights.md` が空になっていること。
- 全プロジェクトで `/sync-gemini` が完了していること。
