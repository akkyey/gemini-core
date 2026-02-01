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

## 更新履歴

| 日付 | ID | 追加者 | 概要 |
|------|-----|--------|------|
| 2026-01-31 | AP-001〜004 | Agent | 初期登録（discord-server リファクタリングより） |
| 2026-01-31 | AP-005 | Agent | 絶対パスのハードコード禁止 (inspect_db.py調査より) |
| 2026-02-01 | AP-005 | Agent | .env 一元管理と自動設定生成パターンを追記 (mcp-servers 移行プロジェクトより) |
| 2026-02-01 | AP-005 | Agent | 「外部化 vs 相対化」の注意点と相対シンボリックリンクについて追記 |
