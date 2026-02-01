---
description: 全プロジェクトのGitステータスを一括確認する
---

# 全プロジェクト Gitステータス確認

// turbo-all

1. gemini-core のステータス
```bash
echo "=== gemini-core ===" && cd /home/irom/dev/gemini-core && git status -s -b
```

2. mcp-servers のステータス
```bash
echo "=== mcp-servers ===" && cd /home/irom/dev/mcp-servers && git status -s -b
```

3. project-stock2 のステータス
```bash
echo "=== project-stock2 ===" && cd /home/irom/dev/project-stock2 && git status -s -b
```

4. salesforce のステータス
```bash
echo "=== salesforce ===" && cd /home/irom/dev/salesforce && git status -s -b
```
