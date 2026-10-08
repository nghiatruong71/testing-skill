"""Đọc bảng test case Markdown (output của skill rbt_manual_testing) thành danh sách dict.

Nhận diện bảng có header chứa cột "TC ID". Tên cột được chuẩn hóa về key cố định
để các script khác (xuất CSV, lint) dùng chung.
"""
import re

# Header trong file Markdown -> key chuẩn
COLUMN_ALIASES = {
    "tc id": "tc_id",
    "module": "module",
    "sub-module": "module",
    "risk level": "risk",
    "risk": "risk",
    "test title": "title",
    "test scenario": "title",
    "test case title": "title",
    "title": "title",
    "requirement": "req",
    "req id": "req",
    "req": "req",
    "pre-condition": "precondition",
    "pre-conditions": "precondition",
    "precondition": "precondition",
    "test steps": "steps",
    "steps": "steps",
    "test data": "data",
    "expected result": "expected",
    "expected results": "expected",
    "priority": "priority",
}

_BR = re.compile(r"<br\s*/?>", re.IGNORECASE)
_NUM_PREFIX = re.compile(r"^\s*(\d+)[.)]\s*")


def _split_row(line):
    """Tách 1 dòng bảng Markdown thành các cell, hỗ trợ ký tự `\\|` đã escape."""
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|") and not line.endswith("\\|"):
        line = line[:-1]
    cells = re.split(r"(?<!\\)\|", line)
    return [c.strip().replace("\\|", "|") for c in cells]


def _is_separator(cells):
    return all(re.fullmatch(r":?-{3,}:?", c) for c in cells if c)


def split_numbered(cell):
    """'1. A<br>2. B' -> [(1, 'A'), (2, 'B')]. Dòng không đánh số có số thứ tự None."""
    items = []
    for part in _BR.split(cell or ""):
        part = part.strip()
        if not part:
            continue
        m = _NUM_PREFIX.match(part)
        if m:
            items.append((int(m.group(1)), part[m.end():].strip()))
        else:
            items.append((None, part))
    return items


def parse_markdown(text):
    """Trả về list test case. Mỗi phần tử: dict các key chuẩn + '_line' (số dòng trong file)."""
    lines = text.splitlines()
    cases = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.lstrip().startswith("|") and i + 1 < len(lines):
            header = _split_row(line)
            sep = _split_row(lines[i + 1])
            keys = [COLUMN_ALIASES.get(h.lower().strip("* ")) for h in header]
            if "tc_id" in keys and _is_separator(sep):
                i += 2
                while i < len(lines) and lines[i].lstrip().startswith("|"):
                    cells = _split_row(lines[i])
                    row = {"_line": i + 1}
                    for key, value in zip(keys, cells):
                        if key:
                            row[key] = value
                    if row.get("tc_id"):
                        cases.append(row)
                    i += 1
                continue
        i += 1
    return cases
