---
description: Safe-Shell V2
---


> [!IMPORTANT]
> **⚠️ [Safety Interlock]**
> 本手順を開始する前に、必ず `.agent/project_config.md` を読み込み、`SAFETY_SHELL_TOOL` 等の論理名を物理的な実体（Path/Tool ID）へ解決せよ。規約を無視した直接的な `run_command` 等の使用はプロセス違反となる。
`self_diagnostic.py`  `pytest` `safe-shell` 

## 

### 1. 
1. 
   - `macro_id`: `[project_name]_diag`
   - `cmd`: `python` ( `./venv/bin/python`)
   - `args`: `["self_diagnostic.py"]` ( `["-m", "pytest"]`)
   - `persist`: `False`

### 2. 
2. `execute_macro`  `background=True` 
   - `PYTHONPATH` 

### 3. 
3. `get_process_status` 
   - `RUNNING` 

### 4. 
4.  `DONE` 
   - `/safe-push`
