---
description: 全プロジェクトのGitステータスを一括確認する
---

# 全プロジェクト Gitステータス確認

// turbo-all

### 各プロジェクトのステータスを一括表示します

```bash
# gemini-core のルートを特定
CORE_ROOT=$(git rev-parse --show-toplevel)
DEV_ROOT=$(cd "${CORE_ROOT}/.."; pwd)

# 司令塔のステータス
echo "=== gemini-core ===" && cd "${CORE_ROOT}" && git status -s -b

# projects.json に基づく各プロジェクトのステータス
# (AIは事前に projects.json を確認し、以下の各ディレクトリを巡回してください)

echo "=== mcp-servers ===" && cd "${DEV_ROOT}/mcp-servers" && git status -s -b
echo "=== project-stock2 ===" && cd "${DEV_ROOT}/project-stock2" && git status -s -b
echo "=== salesforce ===" && cd "${DEV_ROOT}/salesforce" && git status -s -b
echo "=== gemini-docs ===" && cd "${DEV_ROOT}/gemini-docs" && git status -s -b
```
