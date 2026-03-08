---
description: .gemini () HooksMCP
---

# MCP 

 `.gemini`HooksMCP
`git pull`  `gemini-core` 

## 

`projects.json` 

1.  `mcp-servers`
2.  `project-stock2`
3.  `salesforce`
4.  `gemini-docs`
5.  ( `projects.json` )

## 

// turbo-all

### 1.  Git Hooks 

`.gemini` Git Hooks 

```bash
# gemini-core 
CORE_ROOT=$(git rev-parse --show-toplevel)
DEV_ROOT=$(cd "${CORE_ROOT}/.."; pwd)

# projects.json AI
# 
# 1. 
# 2. git hooks 

# : mcp-servers 
dir="${DEV_ROOT}/mcp-servers"; [ -L "${dir}/.gemini" ] && cp "${dir}/.gemini/scripts/git-hooks/pre-commit" "${dir}/.git/hooks/" && chmod +x "${dir}/.git/hooks/pre-commit" && echo " mcp-servers: Hooks" || echo " mcp-servers: .gemini"

# : project-stock2 
dir="${DEV_ROOT}/project-stock2"; [ -L "${dir}/.gemini" ] && cp "${dir}/.gemini/scripts/git-hooks/pre-commit" "${dir}/.git/hooks/" && chmod +x "${dir}/.git/hooks/pre-commit" && echo " project-stock2: Hooks" || echo " project-stock2: .gemini"

# : salesforce 
dir="${DEV_ROOT}/salesforce"; [ -L "${dir}/.gemini" ] && cp "${dir}/.gemini/scripts/git-hooks/pre-commit" "${dir}/.git/hooks/" && chmod +x "${dir}/.git/hooks/pre-commit" && echo " salesforce: Hooks" || echo " salesforce: .gemini"

# : gemini-docs 
dir="${DEV_ROOT}/gemini-docs"; [ -L "${dir}/.gemini" ] && cp "${dir}/.gemini/scripts/git-hooks/pre-commit" "${dir}/.git/hooks/" && chmod +x "${dir}/.git/hooks/pre-commit" && echo " gemini-docs: Hooks" || echo " gemini-docs: .gemini"
```

### 2. MCP

 `mcp_config.json` IDE

```bash
# MCP
MCP_MASTER="${DEV_ROOT}/mcp-servers/mcp_config.json"
MCP_IDE="${HOME}/.gemini/antigravity/mcp_config.json"

if [ -f "${MCP_MASTER}" ]; then
  cp "${MCP_MASTER}" "${MCP_IDE}"
  echo " MCP: ${MCP_MASTER}  ${MCP_IDE}"
else
  echo " : ${MCP_MASTER}"
fi
```

> [!NOTE]
> - ****: `mcp-servers/mcp_config.json`
> - ****: `~/.gemini/antigravity/mcp_config.json`IDE 
> - IDE
> - : AP-019MCP

### 3. 

Discord :
```
mcp_discord_send_message({ channel_name: "notifications", content: " .gemini HooksMCP" })
```

## 

- `.gemini`  `../gemini-core` 
