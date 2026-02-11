---
description: 新規または既存のプロジェクトをGemini管理下に追加する
---

# プロジェクト参加 (Join Gemini)

このワークフローは、指定されたディレクトリをGeminiプロジェクト化し、管理台帳(`gemini-core`)に登録します。

## 前提
*   対象となるディレクトリ名またはディレクトリパスを決めてください。
*   基本的には `$GEMINI_ROOT` (例: `/home/irom/dev`) 直下に配置することを推奨します。

## 実行手順

### 1. プロジェクトの初期化 (Target Project)

対象ディレクトリで以下のコマンドを実行します。

```bash
# ディレクトリ作成（存在しない場合）
mkdir -p <TARGET_PATH>
cd <TARGET_PATH>

# Git初期化（まだの場合）
if [ ! -d ".git" ]; then git init; fi

# Geminiシンボリックリンク作成（サブモジュールではない）
# 前提: ../gemini-core が存在すること
if [ ! -L ".gemini" ]; then
    ln -s ../gemini-core .gemini
    echo "✅ ./gemini -> ../gemini-core リンク作成完了"
fi

# .gitignore に .gemini を追記（ローカルパス依存のため追跡しない）
if ! grep -q "^\.gemini$" .gitignore 2>/dev/null; then
    echo -e "\n# gemini-core シンボリックリンク\n.gemini" >> .gitignore
    echo "✅ .gitignore に .gemini を追加"
fi

# ワークフローディレクトリ作成
mkdir -p .agent/workflows

# 必須ワークフローのコピー
CORE_ROOT=$(git rev-parse --show-toplevel)
# 注意: コピー元は .gemini/ 経由で取得
cp ".gemini/.agent/workflows/sync-gemini.md" .agent/workflows/
cp ".gemini/.agent/workflows/check-all-status.md" .agent/workflows/
```

### 2. ドキュメント環境の整備

新しいプロジェクト用のドキュメントフォルダを作成し、スコープ規約を更新します。

```bash
# gemini-docs のルートを特定
# gemini-core と gemini-docs は同階層にあると仮定
DOCS_ROOT=$(cd "../gemini-docs" && pwd)

# フォルダ作成
mkdir -p "${DOCS_ROOT}/projects/<PROJECT_NAME>"
touch "${DOCS_ROOT}/projects/<PROJECT_NAME>/README.md"

# スコープ規約の更新 (SCOPE_RULES.md に対応表を追記してください)
echo "| \`projects/<PROJECT_NAME>/\` | \`\$GEMINI_ROOT/<PROJECT_NAME>\` のみ |" >> "${DOCS_ROOT}/SCOPE_RULES.md"
```

### 3. 司令塔への登録 (Core Registration)

`gemini-core` 側の管理ファイルを更新し、このプロジェクトを認識させます。

**A. 台帳への登録**
ファイル: `gemini-core/projects.json`
*   プロジェクト名をリストに追加してください。

**B. 同期・確認リストへの追加**
*   `gemini-core/.agent/workflows/sync-gemini.md` に追記。
*   `gemini-core/.agent/workflows/check-all-status.md` に追記。

**C. ワークスペースへの追加**
ファイル: `gemini-core/../gemini.code-workspace`
*   `folders` 配列に新しいパスを追加してください。

### 4. 設定の反映

```bash
# gemini-core の変更を保存
cd ../gemini-core
git add .
git commit -m "chore: add <PROJECT_NAME> to gemini ecosystem"
git push origin main
```

### 5. プロジェクト側の変更を保存

```bash
cd <TARGET_PATH>
git add .
git commit -m "chore: initial commit with gemini-core symlink"
```

## 完了
これにてプロジェクトはGeminiの管理下に入りました。
以後、`/sync-gemini` や `/check-all-status` の対象となります。
