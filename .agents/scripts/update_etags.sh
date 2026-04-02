#!/bin/bash
# Hierarchy of Reliability (Layer 1) 用のインデックスを生成
# -maxdepth 4 で主要ファイルをカバーし、隠しファイルやvenv等を除外
find . -maxdepth 4 -not -path '*/.*' -not -path './venv*' -not -path './node_modules*' -printf "%M %n %u %g %s %TY-%Tm-%Td %TT %p\n" > etags_snapshot.txt
echo "✅ etags_snapshot.txt generated."
python3 generate_etags.py

# MCP Server Startup Validation
echo "Validating safe-shell startup..."
cd ../mcp-servers/safe-shell
/home/irom/dev/mcp-servers/safe-shell/bin/safe-shell --version || { echo "ERROR: safe-shell failed to start!"; exit 1; }
cd - > /dev/null
