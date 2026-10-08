#!/usr/bin/env python3
"""Chuyển bảng test case Markdown sang CSV để import vào Xray (Test Case Importer) hoặc mở bằng Excel.

Mỗi Test Step là 1 dòng CSV; các dòng cùng TCID thuộc cùng 1 test case (Xray dùng cột TCID để gom).
File ghi bằng UTF-8 có BOM để Excel hiển thị đúng tiếng Việt.

Cách dùng:
    python3 scripts/testcases/md_to_xray_csv.py test_cases_login.md
    python3 scripts/testcases/md_to_xray_csv.py test_cases_login.md -o out/login_xray.csv
"""
import argparse
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tc_parser import parse_markdown, split_numbered  # noqa: E402

HEADER = ["TCID", "Summary", "Test Type", "Priority", "Labels", "Component",
          "Description", "Step", "Action", "Data", "Expected Result"]

_BR = re.compile(r"<br\s*/?>", re.IGNORECASE)


def _plain(cell):
    """Đổi <br> thành xuống dòng, bỏ backtick Markdown."""
    return _BR.sub("\n", cell or "").replace("`", "").strip()


def _label(value):
    return re.sub(r"\s+", "-", value.strip().lower()) if value else ""


def build_rows(case):
    steps = split_numbered(case.get("steps", ""))
    expected = split_numbered(case.get("expected", ""))
    data = split_numbered(case.get("data", ""))
    # Test Data đánh số khớp với steps -> gán theo từng step; ngược lại gán toàn bộ vào step 1
    data_by_step = len(data) == len(steps) and all(n is not None for n, _ in data)

    description = []
    if case.get("req"):
        description.append(f"Requirement: {_plain(case['req'])}")
    if case.get("risk"):
        description.append(f"Risk Level: {_plain(case['risk'])}")
    if case.get("precondition"):
        description.append(f"Pre-Condition:\n{_plain(case['precondition'])}")

    labels = " ".join(filter(None, [_label(case.get("module", "")),
                                    "risk-" + _label(case["risk"]) if case.get("risk") else ""]))
    rows = []
    for idx in range(max(len(steps), len(expected), 1)):
        action = steps[idx][1] if idx < len(steps) else ""
        result = expected[idx][1] if idx < len(expected) else ""
        if data_by_step:
            step_data = data[idx][1]
        else:
            step_data = _plain(case.get("data", "")) if idx == 0 else ""
        first = idx == 0
        rows.append([
            case["tc_id"],
            _plain(case.get("title", "")) if first else "",
            "Manual" if first else "",
            _plain(case.get("priority", "")) if first else "",
            labels if first else "",
            _plain(case.get("module", "")) if first else "",
            "\n\n".join(description) if first else "",
            idx + 1,
            _plain(action),
            _plain(step_data),
            _plain(result),
        ])
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input", help="File Markdown chứa bảng test case")
    parser.add_argument("-o", "--output", help="File CSV đầu ra (mặc định: cùng tên, đuôi _xray.csv)")
    args = parser.parse_args()

    src = Path(args.input)
    cases = parse_markdown(src.read_text(encoding="utf-8"))
    if not cases:
        sys.exit(f"Không tìm thấy bảng test case (cần cột 'TC ID') trong {src}")

    out = Path(args.output) if args.output else src.with_name(src.stem + "_xray.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    total_steps = 0
    with out.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
        for case in cases:
            rows = build_rows(case)
            total_steps += len(rows)
            writer.writerows(rows)
    print(f"Đã xuất {len(cases)} test case / {total_steps} step -> {out}")


if __name__ == "__main__":
    main()
