# -*- coding: utf-8 -*-
"""
功能: 自动为 Markdown 文件中的二级/三级标题添加连续编号，并输出带编号的新文件
用法: `python number_title.py <input.md>`，会在同目录生成 `<input_numbered.md>`
"""
import re
import sys
from pathlib import Path

def clean_path(path_str: str) -> Path:
    """去掉命令行传入路径两端可能的引号"""
    path_str = path_str.strip().strip('"').strip("'")
    return Path(path_str)

def number_markdown_headings(md_path: Path):
    text = md_path.read_text(encoding='utf-8-sig')
    lines = text.splitlines()
    newline = "\r\n" if "\r\n" in text else "\n"

    section_counter = 0
    subsection_counter = 0
    result = []
    in_code = False
    subsubsection_counter = 0

    for line in lines:
        # 代码块保护
        if re.match(r'^\s*(```|~~~)', line):
            in_code = not in_code
            result.append(line)
            continue
        if in_code:
            result.append(line)
            continue

        # ## 处理
        if re.match(r'^##\s', line):
            section_counter += 1
            subsection_counter = 0
            subsubsection_counter = 0
            title = re.sub(r'^##\s*', '', line).strip()
            title = re.sub(r'^\d+(\.\d+)*\s+', '', title)
            expected = f"## {section_counter} {title}"
            if line.strip() == expected:
                result.append(line)
            else:
                result.append(expected)
            continue

        # ### 处理
        if re.match(r'^###\s', line):
            if section_counter == 0:
                result.append(line)
                continue
            subsection_counter += 1
            subsubsection_counter = 0
            title = re.sub(r'^###\s*', '', line).strip()
            title = re.sub(r'^\d+(\.\d+)*\s+', '', title)
            expected = f"### {section_counter}.{subsection_counter} {title}"
            if line.strip() == expected:
                result.append(line)
            else:
                result.append(expected)
            continue

        # #### 处理
        if re.match(r'^####\s', line):
            if section_counter == 0 or subsection_counter == 0:
                result.append(line)
                continue
            subsubsection_counter += 1
            title = re.sub(r'^####\s*', '', line).strip()
            title = re.sub(r'^\d+(\.\d+)*\s+', '', title)
            expected = f"#### {section_counter}.{subsection_counter}.{subsubsection_counter} {title}"
            if line.strip() == expected:
                result.append(line)
            else:
                result.append(expected)
            continue

        result.append(line)

    out_path = md_path.with_name(md_path.stem + "_numbered.md")
    out_path.write_text(newline.join(result) + newline, encoding='utf-8')
    print(f"已生成: {out_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python number.py <input.md>")
        sys.exit(1)

    input_path = clean_path(sys.argv[1])
    if not input_path.exists():
        print(f"错误: 找不到文件 {input_path}")
        sys.exit(1)

    number_markdown_headings(input_path)
