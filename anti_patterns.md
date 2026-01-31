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

## 更新履歴

| 日付 | ID | 追加者 | 概要 |
|------|-----|--------|------|
| 2026-01-31 | AP-001〜004 | Agent | 初期登録（discord-server リファクタリングより） |
