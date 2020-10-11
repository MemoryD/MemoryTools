# -*- coding: utf-8 -*-
"""
@name: count_code
@author: Memory
@date: 2020/10/11
@description: 统计项目中的py代码行数
"""

from pathlib import Path


def count_code(cwd: Path, count: dict):
    for py in cwd.glob("*.py"):
        count[str(py)] = len(py.read_text(encoding="utf-8").split('\n'))

    for p in cwd.iterdir():
        if p.is_dir():
            count_code(p, count)

    return count


count = count_code(Path(), {})
total = 0
for py, line in count.items():
    total += line
    print(py, line)

print(total)


