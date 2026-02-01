---
description: 新規または既存のプロジェクトをGemini管理下に追加する
---

# プロジェクト参加 (Join Gemini)

このワークフローは、指定されたディレクトリをGeminiプロジェクト化し、管理台帳(`gemini-core`)に登録します。

## 前提
*   対象となるディレクトリパスを決めてください（例: `/home/irom/dev/new-project`）。

## 実行手順

### 1. プロジェクトの初期化 (Target Project)

対象ディレクトリで以下のコマンドを実行します。

```bash
# ディレクトリ作成（存在しない場合）
mkdir -p <TARGET_PATH>
cd <TARGET_PATH>

# Git初期化（まだの場合）
if [ ! -d ".git" ]; then git init; fi

# Geminiサブモジュール追加
if [ ! -d ".gemini" ]; then
    git submodule add https://github.com/akkyey/gemini-core.git .gemini
    git submodule update --init --recursive
fi

# ワークフローディレクトリ作成
mkdir -p .agent/workflows

# 必須ワークフローのコピー
cp /home/irom/dev/gemini-core/.agent/workflows/sync-gemini.md .agent/workflows/
cp /home/irom/dev/gemini-core/.agent/workflows/check-all-status.md .agent/workflows/
```

### 2. 司令塔への登録 (Core Registration)

`gemini-core` 側の管理ファイルを更新し、このプロジェクトを認識させます。

**A. 同期リストへの追加**
ファイル: `/home/irom/dev/gemini-core/.agent/workflows/sync-gemini.md`
*   `## 対象プロジェクト` のリストに追記してください。
*   `cp` コマンド等の処理ブロックを追記してください。

**B. ステータス確認への追加**
ファイル: `/home/irom/dev/gemini-core/.agent/workflows/check-all-status.md`
*   `git status` 確認用コマンドを追記してください。

**C. ワークスペースへの追加**
ファイル: `/home/irom/dev/gemini.code-workspace`
*   `folders` 配列に新しいパスを追加してください。

### 3. 設定の反映

```bash
# Core側の変更を保存
cd /home/irom/dev/gemini-core
git add .
git commit -m "chore: add <PROJECT_NAME> to gemini ecosystem"
git push origin main

# プロジェクト側の変更を保存
cd <TARGET_PATH>
git add .
git commit -m "chore: initial commit with gemini-core submodule"
```

## 完了
これにてプロジェクトはGeminiの管理下に入りました。
以後、`/sync-gemini` や `/check-all-status` の対象となります。
