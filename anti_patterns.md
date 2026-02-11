# アンチパターン一覧 (Anti-Pattern Catalog)

本ファイルは、開発中に発見されたアンチパターンを蓄積する共通ファイルです。
**リファクタリング時およびコミット時に参照**し、同じ問題の再発を防止します。

> [!NOTE]
> 新しいアンチパターンを発見した場合、このファイルに追記してコミット＆プッシュしてください。

---

## 設定管理

### AP-001: 設定ロジックの重複
- **問題**: 同じ設定値（環境変数、CLI引数など）を複数箇所で参照している
- **影響**: 修正漏れ、不整合、保守困難
- **解決策**: 一箇所（CONFIG オブジェクト等）に集約する

```typescript
// ❌ 悪い例
const name1 = process.env.PROJECT_NAME || 'default';
// ... 100行後 ...
const name2 = process.env.PROJECT_NAME || 'default'; // コピペ

// ✅ 良い例
const CONFIG = {
  projectName: process.env.PROJECT_NAME || 'default',
} as const;
```

---

## プロセスライフサイクル

### AP-002: stdin 終了未監視（MCP サーバー）
- **問題**: MCPクライアントが接続を切断してもプロセスが終了しない
- **影響**: ゾンビプロセスの残留、リソースリーク
- **解決策**: stdin 終了イベントを監視して process.exit() する

```typescript
// ✅ 必須パターン
process.stdin.on('end', () => process.exit(0));
process.stdin.on('close', () => process.exit(0));
```

---

## セキュリティ

### AP-003: シークレットのハードコード
- **問題**: トークン、パスワード等がソースコードに直接記載されている
- **影響**: GitHub Push Protection でブロック、漏洩リスク
- **解決策**: 環境変数経由で渡す

```typescript
// ❌ 悪い例
const token = "MTQ2MzA0ODM3..."; // ハードコード

// ✅ 良い例
const token = process.env.DISCORD_BOT_TOKEN;
```

---

## ロギング

### AP-004: ログパスの分散
- **問題**: デバッグログのパスが複数箇所にハードコードされている
- **影響**: 変更時の修正漏れ、不整合
- **解決策**: ヘルパー関数または定数で一元管理

```typescript
// ✅ 良い例
const CONFIG = {
  debugLogPath: '/tmp/app_debug.log',
} as const;

function debugLog(message: string): void {
  fs.appendFileSync(CONFIG.debugLogPath, `[${new Date().toISOString()}] ${message}\n`);
}
```

---


---

## パス・環境依存

### AP-005: Absolute Path Hardcoding (絶対パスのハードコード)
- **問題**: ソースコード、設定ファイル、または起動スクリプト内に `/home/user/...` といった特定の環境に依存する絶対パスが直接記述されている
- **影響**: 開発者間やCI環境、サーバー移行時に動作しなくなる（ポータビリティの欠如）。設定ファイル（`mcp_config.json` 等）の修正漏れが発生する。
- **解決策**:
  - **環境変数での一元管理**: ルートの `.env` で `MCP_ROOT` 等を定義し、各所から参照する。**ただし、.env 内の値も可能な限りプロジェクトルートからの相対パス（例: `./admin`）にする。**
  - **相対パス解決**: 実行スクリプトの位置を基準にパスを動的に解決する。
  - **構成の自動生成**: `.env` を元に設定ファイル（JSON）をスクリプトで自動生成する。**ジェネレータ自体も `Path(__file__)` 等を利用して自身の位置から動的に絶対パスを特定する。**
  - **相対パスによるシンボリックリンク**: リンク作成時は絶対パスではなく、ターゲットまでの相対パス（例: `ln -s ./.config/... ./link`）を使用する。

> [!WARNING]
> **「外部化」と「相対化」の混同に注意**
> 絶対パスを設定ファイル（.env 等）に移動しただけでは、ハードコードの場所が移っただけで「ポータビリティ」は改善されていません。移動に強い構成にするには「相対パス」または「動的解決」が不可欠です。

```python
# ✅ Python: pathlib を使用
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
```

```typescript
// ✅ Node.js: process.env または path.resolve を使用
const root = process.env.MCP_ROOT || path.join(__dirname, '..');
```

```bash
# ✅ Shell: スクリプトの位置を取得して相対解決
SCRIPT_DIR=$(cd "$(dirname "$0")"; pwd)
BUILD_PATH="${SCRIPT_DIR}/build/index.js"
```

---

---

## 設計・アーキテクチャ

### AP-006: MCPハンドラーの密結合
- **問題**: MCPサーバーインスタンス（`Server`）内、またはクラスのプライベートメソッドにすべてのロジックが直接記述されている。
- **影響**: 
  - `Server` インスタンスが必要な `executeRequest` 等の内部メソッドに依存し、単体テストが困難になる。
  - テスト環境で SDK のモック化が必要になり、テストコードが複雑化する。
- **解決策**:
  - ツール実行ロジックをサーバーインスタンスから独立した非同期関数（例: `handleCallTool`）として定義・export する。
  - 外部依存（DB接続、外部APIクライアント等）は引数として渡す。


### AP-007: 設定ディレクトリの手動構築
- **問題**: エージェントが独自判断で `.gemini` ディレクトリや `GEMINI.md` をサブプロジェクト配下に手動で作成・構築する。
- **影響**: 
  - プロジェクト間でのルール不整合（Gitフックの動作不良等）が発生する。
  - グローバルな司令塔（`gemini-core`）からの変更が反映されない。
- **解決策**:
  - 新規プロジェクト管理開始時は必ず `/join-gemini` ワークフローを使用する。
  - プロジェクト固有の設定が必要な場合は、`GEMINI.md` の仕組みの範囲内で拡張する。

---

## 運用・保守

### AP-008: 実行時ディレクトリの欠落前提
- **問題**: DB保存用ディレクトリ（`dbs/`, `storage/` 等）が最初から存在することを前提にしたコード・構成になっている。
- **影響**: 
  - OS再起動や環境移行後のクリーンな状態で、ディレクトリ不足による書き込みエラー（例: `TypeError: Cannot open database because the directory does not exist`）が発生する。
- **解決策**:
  - サーバー起動ロジック内で、必要なディレクトリの存否確認と自動生成を行う。
  - または、空のディレクトリに `.gitkeep` を配置して Git 管理下に置く。

### AP-009: 知見登録失敗の黙殺（長期記憶）
- **問題**: `memory-server` への記憶保存がエラー（サーバー未起動、パス不備等）で失敗した際、それを無視して作業を続行する。
- **影響**: 
  - 重要な教訓やハマりどころが長期記憶に蓄積されず、将来の再発防止に繋がらない。
- **解決策**:
  - 記憶の保存に失敗した場合は、直ちに作業を停止し原因を解消するか、失敗した内容を一時ファイル（トラブルレポート等）に記録して、後から確実に登録する。

---

<<<<<<< HEAD
## データフロー

### AP-010: Ambiguous Resource Auto-Selection (不透明な自動リソース選択)
- **問題**: ファイル名やディレクトリ構造を走査し、最新のファイルを「推測（例: `max(files)`）」して処理の入力とする。
- **影響**: 
  - ファイル名の命名規則（アルファベット順 vs 数値順）の勘違いにより、意図しない古いデータが選ばれる。
  - 処理が暗黙的になり、データフローの追跡が困難になる。
- **解決策**:
  - 生成元プロセスから生成先プロセスへ、ファイルパスを**明示的な引数（Data Relay）**として渡す。
  - ファイルパスの不確実性を排除するインターフェース設計を行う。

```python
# ❌ 悪い例: 暗黙のファイル探索
files = glob.glob("data/output/*.csv")
target = max(files)  # アルファベット順で weekly が daily に勝つ

# ✅ 良い例: 明示的なパスリレー
report_paths = reporter.generate_reports(results)  # {"summary": Path, "detailed": Path}
tools.export_to_sheets(csv_path=str(report_paths["summary"]))
```

### AP-011: Truthless Success Notification (不実な完了通知)
- **問題**: サブプロセス（アップロード、連携など）が失敗しているにもかかわらず、メインプロセスが終了したことのみをもって「✅ 成功」として通知する。
- **影響**: 
  - ユーザーが不具合（データの未更新等）に気づくのが遅れる。
  - システムが「正常」を装うため、信頼性が損なわれる。
- **解決策**:
  - 処理の全ステップの結果を収集（Error Tracking）し、一つでも例外や警告があれば「⚠️ Partial Success（一部失敗）」等のステータスで通知する。
  - 通知の色やタイトルをステータスに応じて動的に変更する。

```python
# ❌ 悪い例: 例外を握りつぶして成功通知
try:
    upload_to_drive(file)
except Exception:
    pass  # 失敗を無視
notifier.notify_success(mode)  # 常に成功

# ✅ 良い例: Error Tracking の活用
try:
    upload_to_drive(file)
except Exception as e:
    context.add_error(f"Upload failed: {e}")  # エラーを記録
notifier.notify_success(mode, has_error=context.has_partial_failure)
```

### AP-012: Language-Tool Mismatch (言語とツールの不一致)
- **問題**: プロジェクトの主要言語と異なるエコシステムのツール（例: Python プロジェクトに ESLint、TypeScript プロジェクトに ruff）を実行する。
- **影響**: 
  - ツールが対象言語を解析できず、永久にハングまたは無意味な結果を返す。
  - 実行時間が無限に浪費される（実例: 2時間近くハングした `npx eslint *.py`）。
- **解決策**:
  - プロジェクトの `pyproject.toml` / `package.json` を確認し、対応するツールのみを使用する。
  - **Python** → `ruff`, `black`, `mypy`, `pytest`
  - **TypeScript/JavaScript** → `eslint`, `prettier`, `tsc`, `jest`/`vitest`
  - ツール実行前に対象ファイルの拡張子を確認するガードを設ける。

> [!CAUTION]
> **`.py` ファイルに `eslint` を、`.ts` ファイルに `ruff` を実行してはならない。**
> ツールがハングし、数時間のリソース浪費を招く。

## 環境・リソース管理

### AP-013: 実行環境への暗黙的依存 (Implicit Environment Dependency)
- **問題**: `requirements.txt` に未記載のライブラリが偶然インストールされていたため動作していたが、環境再構築時に動作不能になる。
- **影響**: 環境移行やCIでのビルド失敗。「昨日まで動いていた」現象の発生。
- **解決策**:
  - `requirements.txt` への完全な記載。
  - テスト時の自動インポート監査による「環境の自己診断」。

### AP-014: 名前ベースの外部リソース解決 (Ambiguous Resource Resolution)
- **問題**: クラウド上のリソース（DB, ストレージ, フォルダ）を「名前」で検索・特定している。
- **影響**: 同名の別リソース（個人のMy Drive等）へ誤出力し、情報漏洩やデータ消失のリスクがある。
- **解決策**:
  - リソースは名前ではなく「一意のID」で解決することを原則とする。
  - 名前検索はIDが不明な場合のフォールバック（かつ警告付き）に留める。

### AP-015: テスト時のブロッキング待機 (Blocking Retries in Tests)
- **問題**: `tenacity` 等のリトライロジックでデフォルトの待機時間（`min=5`秒など）がテスト実行時にも有効になっている。
- **影響**: 並列実行(`pytest-xdist`)時にスレッドをブロックし、テスト全体のハングアップや実行時間の肥大化を招く。
- **解決策**:
  - テスト環境では `time.sleep` をモック化するか、待機時間ゼロの設定を注入する。

---

## 更新履歴

| 日付 | ID | 追加者 | 概要 |
|------|-----|--------|------|
| 2026-01-31 | AP-001〜004 | Agent | 初期登録（discord-server リファクタリングより） |
| 2026-01-31 | AP-005 | Agent | 絶対パスのハードコード禁止 (inspect_db.py調査より) |
| 2026-02-01 | AP-005 | Agent | .env 一元管理と自動設定生成パターンを追記 (mcp-servers 移行プロジェクトより) |
| 2026-02-01 | AP-005 | Agent | 「外部化 vs 相対化」の注意点と相対シンボリックリンクについて追記 |
| 2026-02-05 | AP-006〜009 | Agent | MCPハンドラー抽出、設定構築ルール、ディレクトリ生成、記憶登録失敗対応を追加 |
| 2026-02-11 | AP-010〜012 | Agent | 不透明な自動リソース選択、不実な完了通知、言語ツール不一致を追加 |
| 2026-02-11 | AP-013〜015 | Agent | 環境依存、リソース解決、テスト待機に関するアンチパターンを追加（project-stock2統合） |
