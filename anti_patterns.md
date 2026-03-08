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

## 

### AP-020: String-Based Command Execution (shell=True)
- ****:  1 
- ****: `;`, `&`, `|` 2 OS
- ****:
  - `List[str]` `execve` `shell=False`
  - 

### AP-021: find Result Piping (find)
- ****: `find . -name "*.log" | xargs rm` find 
- ****:  AI 
- ****:
  - find  `-exec` : `find ... -exec rm {} +`
  - 

### AP-022: Sensory Isolation in Long-Running Tasks ()
- ****: Request/Response 
- ****: AI 
- ****:
  - **Process Pair **: `get_process_status` AI 

### AP-023: Deep Nesting / Avoidance of Early Return ()
- ****: Nested Ifs
- ****: 
    - ****: AI 
    - ****: AI 
- ****:
    - **Guard Clauses**:  `return`  `continue` 
    - ****:  2 

```python
#  : 
def process_data(data):
    if data is not None:
        if "user" in data:
            if data["user"].is_active:
                # 
                return do_actual_work(data)
    return False

#  : 
def process_data(data):
    if not data or "user" not in data:
        return False
    
    if not data["user"].is_active:
        return False
        
    # 
    return do_actual_work(data)
```

---

## 

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
