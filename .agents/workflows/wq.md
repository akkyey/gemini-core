---
description: セッション終了の統合処理（Design Check, Commit, Push, Context Sync, Memory, Log Backup）
---


> [!IMPORTANT]
> **⚠️ [Safety Interlock]**
> 本手順を開始する前に、必ず `.agent/project_config.md` を読み込み、`SAFETY_SHELL_TOOL` 等の論理名を物理的な実体（Path/Tool ID）へ解決せよ。規約を無視した直接的な `run_command` 等の使用はプロセス違反となる。
# `wq` ワークフロー

このワークフローは、開発セッションを完璧に締めくくり、次回への情報を「プロトテコル準拠の状態」で引き継ぐための統合コマンドです。

## 実行ステップ

### 1. 最終監査と情報の引き継ぎ (Final Audit & Handover)

```javascript
// ⚠️ Execute via SAFETY_SHELL_TOOL (execute_script)
SAFETY_SHELL_TOOL.execute_script({
  script: `
    # 🤖 【スキル発動】 design_validator
    
    # 📄 全体コンテキストの生成 / 🧠 知見記録 / 💾 状態保存
    # (内部ツール呼び出しとして構成されるが、スクリプト内で順次実行を宣言)
    
    # 🔖 インデックス（etags）の更新
    if [ -f ".agent/scripts/update_etags.sh" ]; then
      bash .agent/scripts/update_etags.sh
    fi
    
    # 🤖 【スキル発動】 audit_analyzer
    python3 scripts/core/audit_analyzer.py
    
    # 🤖 【スキル発動】 log_rotator
    if [ -f "scripts/core/log_rotator.sh" ]; then
      bash scripts/core/log_rotator.sh
    fi
    
    # 📚 知識の資産化 (Knowledge Steward)
    # 今回の作業で得た教訓、回避したピットフォール、発見した新たなアンチパターンを特定せよ。
    # それらを memory-server (save_memory) および anti_patterns.md に物理反映し、次回のセッションの知能を底上げすること。
  `,
  cwd: "{{project_root}}"
});
```

### 2. 安全なコミットとプッシュ
```bash
# ⚠️ Execute via SAFETY_SHELL_TOOL
# 🤖 【スキル発動】 git_committer
# プロトコルに基づき、全成果を記録。
# ハイブリッド形式に基づき、gemini-core (Agents) と gemini-docs (Policy) の両方を最新状態に保つこと。
```

## 完了の定義
- [x] `design_validator` による監査が完了していること
- [x] `git_committer` によるリモートとの同期が完了していること
