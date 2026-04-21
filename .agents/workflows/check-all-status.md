---
description: Gitステータス一括確認
---


> [!IMPORTANT]
> **⚠️ [Safety Interlock]**
> 本手順を開始する前に、必ず `.agent/project_config.md` を読み込み、`SAFETY_SHELL_TOOL` 等の論理名を物理的な実体（Path/Tool ID）へ解決せよ。規約を無視した直接的な `run_command` 等の使用はプロセス違反となる。
#  Git


### 

```bash
# ⚠️ Execute via SAFETY_SHELL_TOOL
# gemini-core 
CORE_ROOT=$(git rev-parse --show-toplevel)
DEV_ROOT=$(cd "${CORE_ROOT}/.."; pwd)

# 
echo "=== gemini-core ===" && cd "${CORE_ROOT}" && git status -s -b

# projects.json 
# (AI projects.json )

echo "=== mcp-servers ===" && cd "${DEV_ROOT}/mcp-servers" && git status -s -b
echo "=== project-stock2 ===" && cd "${DEV_ROOT}/project-stock2" && git status -s -b
echo "=== salesforce ===" && cd "${DEV_ROOT}/salesforce" && git status -s -b
echo "=== gemini-docs ===" && cd "${DEV_ROOT}/gemini-docs" && git status -s -b
```
