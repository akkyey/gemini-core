---
description: Safe-Shell V2
---


> [!IMPORTANT]
> **⚠️ [Safety Interlock]**
> 本手順を開始する前に、必ず `.agent/project_config.md` を読み込み、`SAFETY_SHELL_TOOL` 等の論理名を物理的な実体（Path/Tool ID）へ解決せよ。規約を無視した直接的な `run_command` 等の使用はプロセス違反となる。
`GEMINI.md` `safe_commander`  `safe-shell` 

## 
- `safe-shell` 
- 

## 

### 1. 
1. 
   - `macro_id`: `[repo_name]_safe_push`
   - `cmd`: `bash`
   - `args`: `["-c", "git add . && git commit -F /tmp/commit_msg && git push origin [branch]"]`
   - `persist`: `False` ()

### 2. 
2.  `background=True` 
   - `execute_macro(macro_id="[repo_name]_safe_push", background=True)`

### 3. 
3. `get_process_status` 
   - `DONE` 
   -  PID 

### 4. 
4. `read_recent_messages`  `git log` 

## 
- ****:  2  `background=True` 
- ****: `run_command` 
