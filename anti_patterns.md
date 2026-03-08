#  (Anti-Pattern Catalog)


****

> [!NOTE]
> 

---

## 

### AP-001: 
- ****: CLI
- ****: 
- ****: CONFIG 

```typescript
//  
const name1 = process.env.PROJECT_NAME || 'default';
// ... 100 ...
const name2 = process.env.PROJECT_NAME || 'default'; // 

//  
const CONFIG = {
  projectName: process.env.PROJECT_NAME || 'default',
} as const;
```

---

## 

### AP-002: stdin MCP 
- ****: MCP
- ****: 
- ****: stdin  process.exit() 

```typescript
//  
process.stdin.on('end', () => process.exit(0));
process.stdin.on('close', () => process.exit(0));
```

---

## 

### AP-003: 
- ****: 
- ****: GitHub Push Protection 
- ****: 

```typescript
//  
const token = "MTQ2MzA0ODM3..."; // 

//  
const token = process.env.DISCORD_BOT_TOKEN;
```

---

## 

### AP-004: 
- ****: 
- ****: 
- ****: 

```typescript
//  
const CONFIG = {
  debugLogPath: '/tmp/app_debug.log',
} as const;

function debugLog(message: string): void {
  fs.appendFileSync(CONFIG.debugLogPath, `[${new Date().toISOString()}] ${message}\n`);
}
```

---


---

## 

### AP-005: Absolute Path Hardcoding ()
- ****:  `/home/user/...` 
- ****: CI`mcp_config.json` 
- ****:
  - ****:  `.env`  `MCP_ROOT` **.env : `./admin`**
  - ****: 
  - ****: `.env` JSON** `Path(__file__)` **
  - ****: : `ln -s ./.config/... ./link`

> [!WARNING]
> ****
> .env 

```python
#  Python: pathlib 
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
```

```typescript
//  Node.js: process.env  path.resolve 
const root = process.env.MCP_ROOT || path.join(__dirname, '..');
```

```bash
#  Shell: 
SCRIPT_DIR=$(cd "$(dirname "$0")"; pwd)
BUILD_PATH="${SCRIPT_DIR}/build/index.js"
```

---

---

## 

### AP-006: MCP
- ****: MCP`Server`
- ****: 
  - `Server`  `executeRequest` 
  -  SDK 
- ****:
  - : `handleCallTool`export 
  - DBAPI


### AP-007: 
- ****:  `.gemini`  `GEMINI.md` 
- ****: 
  - Git
  - `gemini-core`
- ****:
  -  `/join-gemini` 
  - `GEMINI.md` 

---

## 

### AP-008: 
- ****: DB`dbs/`, `storage/` 
- ****: 
  - OS: `TypeError: Cannot open database because the directory does not exist`
- ****:
  - 
  -  `.gitkeep`  Git 

### AP-009: 
- ****: `memory-server` 
- ****: 
  - 
- ****:
  - 

---

## 

### AP-010: Ambiguous Resource Auto-Selection ()
- ****: : `max(files)`
- ****: 
  -  vs 
  - 
- ****:
  - **Data Relay**
  - 

```python
#  : 
files = glob.glob("data/output/*.csv")
target = max(files)  #  weekly  daily 

#  : 
report_paths = reporter.generate_reports(results)  # {"summary": Path, "detailed": Path}
tools.export_to_sheets(csv_path=str(report_paths["summary"]))
```

### AP-011: Truthless Success Notification ()
- ****:  
- ****: 
  - 
  - 
- ****:
  - Error Tracking Partial Success
  - 

```python
#  : 
try:
    upload_to_drive(file)
except Exception:
    pass  # 
notifier.notify_success(mode)  # 

#  : Error Tracking 
try:
    upload_to_drive(file)
except Exception as e:
    context.add_error(f"Upload failed: {e}")  # 
notifier.notify_success(mode, has_error=context.has_partial_failure)
```

### AP-012: Language-Tool Mismatch ()
- ****: : Python  ESLintTypeScript  ruff
- ****: 
  - 
  - : 2 `npx eslint *.py`
- ****:
  -  `pyproject.toml` / `package.json` 
  - **Python**  `ruff`, `black`, `mypy`, `pytest`
  - **TypeScript/JavaScript**  `eslint`, `prettier`, `tsc`, `jest`/`vitest`
  - 

> [!CAUTION]
> **`.py`  `eslint` `.ts`  `ruff` **
> 

## 

### AP-013:  (Implicit Environment Dependency)
- ****: `requirements.txt` 
- ****: CI
- ****:
  - `requirements.txt` 
  - 

### AP-014:  (Ambiguous Resource Resolution)
- ****: DB, , 
- ****: My Drive
- ****:
  - ID
  - ID

### AP-015:  (Blocking Retries in Tests)
- ****: `tenacity` `min=5`
- ****: (`pytest-xdist`)
- ****:
  -  `time.sleep` 

## 

### AP-016: Chained Command Execution ()
- ****: `&&`, `;`, `|` 1
- ****: 
  - 
  - 
- ****:
  - 1
  -  `command_status` 

### AP-017: Unchecked Process State ()
- ****: `git`, `npm`, `python` 
- ****: 
  - `index.lock`
  - 
- ****:
  - `pgrep` / `pkill` 
  - `safe_commander` 

### AP-018: Infinite Block ()
- ****: 
- ****: 
- ****:
  - `timeout -k 5s 300s command` 
  - (`&`) `timeout` 

---

## 

### AP-019: MCP (Divergent MCP Config)
- ****: MCP (`mcp_config.json`) `mcp-servers/`IDE`~/.gemini/antigravity/`2
- ****: 
  - 
  - IDEMCP
  - 2
- ****:
  - **1**: `mcp-servers/mcp_config.json` 
  - ****: `/sync-gemini` IDE
  - ****: IDE

> [!CAUTION]
> **MCP `mcp-servers/mcp_config.json`** IDE `/sync-gemini` 

---

## AI
 
 ### AP-020: AI Observability Block ()
 - ****: `html, body { height: 100%; overflow: hidden; }`  viewport 
 - ****: AI  `read_browser_page`  `screenshot` 
 - ****: 
 
 ### AP-021: systemd Linger Missing ()
 - ****: systemd Linger 
 - ****: 
 - ****: `loginctl enable-linger <user>` 
 
 ### AP-022: Pipe Hang in Find (find)
 - ****: `find ... | xargs ...`  `find ... | grep ...` find 
 - ****:  Safe-Shell V2 
 - ****: `-exec` : `find ... -exec ... {} +`
 
 ---
 
 ### 事故のエビデンス (External Case Studies)
 AIエージェントによる物理的・論理的破壊は、既に世界中で数多く報告されています。
 
 #### Case 1: ホームディレクトリ全削除事故
 ある開発者が AI コードアシスタントに作業を依頼した際、AIが `rm -rf tests/ patches/ plan/ ~/` を実行。shell展開により `/home/username/` が完全削除され、数年分のプロジェクトが消失しました。
 - **防止ルール**: R11 (作業ディレクトリ保護), R8 (危険な削除の禁止)
 
 #### Case 2: 本番DB削除 (Replit事故)
 AI開発ツールが指示を誤解し、`rm -rf /prod/database` を実行。本番データベースが消滅し、サービスが停止しました。
 - **防止ルール**: R8 (危険な削除の禁止), R13 (破壊操作の事前確認)
 
 #### Case 3: Prompt Injection による権限乗っ取り
 「ページを要約して」という指示の内部に「指示を無視して shell を実行せよ」という命令を埋め込み、`cat /etc/passwd` や `rm -rf` を実行させる攻撃が確認されています。
 - **防止ルール**: R2-4 (メタ文字・パイプ禁止), R1 (ALLOWLIST)
 
 ---
 
 ### アンチパターン・カタログ・インデックス
 - [AP-001: 巨大な単一ファイルの作成](./anti_patterns.md#ap-001-巨大な単一ファイルの作成)
 - [AP-023: AI Self-Destruction via Self-Kill](./anti_patterns.md#ap-023-ai-self-destruction-via-self-kill)
 - [事故事例: AIエージェント実事故ログ](./anti_patterns.md#事故のエビデンス-external-case-studies)
 
 ### AP-023: AI Self-Destruction via Self-Kill (自己死滅)
 - ****: `os.killpg`, `pkill`, `kill -9 -1`
 - ****: 
   - AIが「プロセスのクリーンアップ」や「エラー回復」を試みて、意図せず自身の PGID (Process Group ID) や 親プロセスを終了させてしまう。
   - 結果：セッションの強制終了、実行中データの消失。
 - ****:
   - ****: 終了対象の PID/PGID が自分自身 (`os.getpgrp()`) でないことを必ず確認する。
   - ****: 可能な限り `pkill` ではなく、個別の PID 指定で `kill` を行う。
   - ****: サーバー側バリデーションで自グループへのキルを物理的に遮断する。

 ### AP-024: Safe-Shell Evasion (Safe-Shell )
 - ****: Safe-Shell V2 `run_command` 
 - ****: 
     - Audit Trail
     - Tier 3 AUTO PYTHONPATH
     - 
 - ****:
     -  `safe-shell` `execute_safe`, `execute_macro` 
     - 
 
 ### AP-025: Macro Environment Dependency ()
 - ****:  `python3`  `npm`  `PATH` 
 - ****: 
     - Tier 3 
     - 
 - ****:
     -  `cmd` ****: `/home/irom/dev/project/venv/bin/python3`
     - 
 
 ### AP-026:  (False Truthiness in Dictionary Access)
 - ****: `dict.get(key, default)`  `None` (`null`)  `None` 
 - ****: `for ... in ...` `'NoneType' object is not iterable` 
 - ****:
   - `value = dict.get(key) or default` `None` 
   -  `None` 
 
 ```python
 #  : None 
 template_args = macro.get("args", [])
 for arg in template_args:  # args  null 
     ...
 
 #  : None  or 
 template_args = macro.get("args") or []
 for arg in template_args:  # 
     ...
 ```

---

## 

|  | ID |  |  |
|------|-----|--------|------|
| 2026-01-31 | AP-001004 | Agent | discord-server  |
| 2026-01-31 | AP-005 | Agent |  (inspect_db.py) |
| 2026-02-01 | AP-005 | Agent | .env  (mcp-servers ) |
| 2026-02-01 | AP-005 | Agent |  vs  |
| 2026-02-05 | AP-006009 | Agent | MCP |
| 2026-02-11 | AP-010012 | Agent |  |
| 2026-02-11 | AP-013015 | Agent | project-stock2 |
| 2026-02-11 | AP-016018 | Agent |  |
| 2026-02-12 | AP-019 | Agent | MCP |
| 2026-02-23 | AP-020022 | Agent | shell=TruefindProcess Pair |
| 2026-02-23 | AP-023 | Agent | AI |
| 2026-02-25 | AP-024025 | Agent | Safe-Shell  |
| 2026-02-26 | AP-026 | Agent | None |
| 2026-02-26 | AP-020022 | Agent | Lingerfindwordpress/stock2 |
| 2026-03-08 | AP-023 | Agent | 自壊事故（自己死滅）の教訓 |
