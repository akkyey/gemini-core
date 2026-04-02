# Project Configuration (gemini-core)

本プロジェクトにおける論理名（Alias）と実体（Path/Tool ID）の最新定義です。
エージェントは高度なインフラ操作を行う際、本ファイルを参照してエイリアスを解決してください。

## 1. ツール・エイリアス (Tool Aliases)
| 論理名 (Logical Name) | 実体 (Physical ID) |
| :--- | :--- |
| `SAFETY_SHELL_TOOL` | `mcp_safe-shell-server_execute_safe` |

## 2. パス・エイリアス (Path Aliases)
| 論理名 (Logical Name) | 実体 (Absolute Path) |
| :--- | :--- |
| `DOCS_PROJECT_ROOT` | `/home/irom/dev/gemini-docs/projects/mcp-servers/safe-shell/` |
| `PROJECT_REPO_ROOT` | `/home/irom/dev/gemini-core/` |

## 3. インターロック規定 (Interlock Protocol)
- ワークフローおよびスキルの冒頭で「本構成情報の読み込み」を宣言せよ。
- 宣言後、上記論理名で規定された物理パス・ツールを使用して作業を完遂せよ。
