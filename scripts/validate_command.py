#!/usr/bin/env python3
import sys
import re

def validate_command(cmd):
    """
    コマンドがGEMINI.mdの安全規定に準拠しているか検証する。
    """
    # 1. 連結演算子の禁止 (&&, ;, ||)
    # 文字列内の記号を考慮するため、単純な検索ではなく正規表現やパースが必要だが、
    # AIエージェントの抑止としては厳しめのチェックを行う。
    chaining_ops = [r'&&', r';', r'\|\|']
    
    # パイプ (|) は CLI Idioms (GEMINI.md 4.8) により、特定ケースを除き禁止
    forbidden_ops = chaining_ops + [r'\|']

    for op in forbidden_ops:
        if re.search(op, cmd):
            print(f"FAILED: Command chaining operator '{op}' detected.")
            print("REASON: GEMINI.md Section 4.1 & 4.8 prohibit command chaining and pipes.")
            return False

    # 2. 危険なシェルの使用 (bash -c 等)
    if re.search(r'bash\s+-c', cmd) or re.search(r'sh\s+-c', cmd):
        print("FAILED: Double shell execution (bash -c) detected.")
        print("REASON: Chaining within nested shells is an anti-pattern.")
        return False

    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: validate_command.py <command>")
        sys.exit(1)

    command_to_validate = " ".join(sys.argv[1:])
    if validate_command(command_to_validate):
        print("SUCCESS: Command is compliant with GEMINI.md safety rules.")
        sys.exit(0)
    else:
        sys.exit(1)
