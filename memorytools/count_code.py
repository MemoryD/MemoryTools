# -*- coding: utf-8 -*-
from pathlib import Path


def count_code(cwd: Path, count: dict):
    for py in cwd.glob("*.py"):
        count[str(py)] = len(py.read_text(encoding="utf-8").split('\n'))

    for p in cwd.iterdir():
        if p.is_dir():
            count_code(p, count)

    return count

all_py = []
count = count_code(Path(), {})
total = 0
for py, line in count.items():
    total += line
    print(py, line)

print(total)
print(list(count.keys()))


