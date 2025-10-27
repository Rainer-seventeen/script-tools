# -*- coding: utf-8 -*-
"""
功能：
    在 Markdown 文件中，为所有中文与英文单词/字母/数字之间自动添加空格。
    英文与中文符号之间不加空格，保留代码块与行内代码不处理。
用法: python spacing.py file.md
"""

import re
import sys
from pathlib import Path

# 匹配中文（CJK）和英文字母/数字
CJK = r"[\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF\u2E80-\u2EFF\u31C0-\u31EF\u2F00-\u2FDF\u3000-\u303F]"
ALNUM = r"[A-Za-z0-9]"

# 模式：CJK 与 ALNUM 相邻
_re_cjk_alnum = re.compile(rf"({CJK})({ALNUM})")
_re_alnum_cjk = re.compile(rf"({ALNUM})({CJK})")

def add_spacing(s: str) -> str:
    s = _re_cjk_alnum.sub(r"\1 \2", s)
    s = _re_alnum_cjk.sub(r"\1 \2", s)
    s = re.sub(r" {2,}", " ", s)
    return s

def process_inline_code_aware(line: str) -> str:
    parts = re.split(r"(`)", line)
    in_code = False
    out = []
    for token in parts:
        if token == "`":
            in_code = not in_code
            out.append(token)
        else:
            out.append(token if in_code else add_spacing(token))
    return "".join(out)

def format_markdown(text: str) -> str:
    lines = text.splitlines()
    out = []
    in_fence = False
    fence_marker = None
    fence_re = re.compile(r"^(\s*)(`{3,}|~{3,})")

    for line in lines:
        if not in_fence:
            m = fence_re.match(line)
            if m:
                in_fence = True
                fence_marker = m.group(2)
                out.append(line)
                continue
            out.append(process_inline_code_aware(line))
        else:
            out.append(line)
            if re.match(rf"^\s*{re.escape(fence_marker)}\s*$", line):
                in_fence = False
                fence_marker = None
    return "\n".join(out) + "\n"

def main():
    if len(sys.argv) != 2:
        print("用法: python spacing.py file.md")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"错误: 文件 {file_path} 不存在。")
        sys.exit(1)

    text = file_path.read_text(encoding="utf-8")
    result = format_markdown(text)

    output_path = file_path.with_name(file_path.stem + "_spaced.md")
    output_path.write_text(result, encoding="utf-8")
    print(f"已生成: {output_path}")

if __name__ == "__main__":
    main()
