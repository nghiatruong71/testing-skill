#!/usr/bin/env python3
"""Kiểm tra tự động bộ test case Markdown theo Definition of Done trong CLAUDE.md.

Chỉ bắt các lỗi "cơ học" (định dạng, thiếu cột, placeholder, đánh số). Các lỗi cần hiểu
nghiệp vụ (thiếu kịch bản, gộp validation nhiều trường...) do skill testcase_reviewer đánh giá.

Cách dùng:
    python3 scripts/testcases/lint_testcases.py test_cases_login.md
    python3 scripts/testcases/lint_testcases.py test_cases_login.md --id-pattern '^CRM_[A-Z]+_TC_\\d{3}$'

Exit code: 0 = không có ERROR, 1 = có ERROR.
"""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tc_parser import parse_markdown, split_numbered  # noqa: E402

DEFAULT_ID_PATTERN = r"^[A-Z0-9]+_[A-Z0-9]+(_[A-Z0-9]+)*_TC_\d{3,}$"
PRIORITIES = {"critical", "high", "medium", "low"}
REQUIRED = [("title", "Test Title"), ("steps", "Test Steps"),
            ("expected", "Expected Result"), ("priority", "Priority")]

# Cụm từ placeholder / chung chung bị cấm trong Test Steps và Test Data (CLAUDE.md mục 8)
PLACEHOLDERS = [
    (r"\b(nhập|điền|chọn|upload|tải lên)\b[^.<\n]{0,40}\b(hợp lệ|không hợp lệ|bất kỳ|tùy ý|ngẫu nhiên|đúng định dạng|sai định dạng)\b",
     "Dữ liệu chung chung — ghi rõ giá trị cụ thể"),
    (r"\b(valid|invalid|any|random)\s+(data|value|email|name|input)\b", "Placeholder tiếng Anh — ghi rõ giá trị"),
    (r"\b(TBD|TODO|FIXME|N/?A)\b", "Còn ghi chú nháp / chưa điền"),
    (r"(\bx{3,}\b|\.\.\.|…)", "Ký tự placeholder thừa"),
    (r"<(email|username|password|value|name|id)>", "Placeholder dạng <...> chưa thay giá trị"),
    (r"\[(email|giá trị|tên|value)[^\]]*\]", "Placeholder dạng [...] chưa thay giá trị"),
]
DEPENDENCY = re.compile(r"(_TC_\d+|test case (trước|ở trên)|TC (trước|ở trên)|kết quả của TC)", re.IGNORECASE)


def lint(cases, id_pattern):
    issues = []  # (level, tc_id, line, rule, detail)
    id_re = re.compile(id_pattern)

    def add(level, case, rule, detail):
        issues.append((level, case.get("tc_id", "?"), case["_line"], rule, detail))

    for tc_id, count in Counter(c["tc_id"] for c in cases).items():
        if count > 1:
            dup = next(c for c in cases if c["tc_id"] == tc_id)
            add("ERROR", dup, "TC ID trùng", f"Xuất hiện {count} lần")

    for case in cases:
        if not id_re.match(case["tc_id"]):
            add("ERROR", case, "Sai convention TC ID", f"'{case['tc_id']}' không khớp {id_pattern}")

        for key, name in REQUIRED:
            if not case.get(key, "").strip():
                add("ERROR", case, "Thiếu cột bắt buộc", f"Cột '{name}' trống")

        if case.get("priority") and case["priority"].strip("* ").lower() not in PRIORITIES:
            add("WARN", case, "Priority lạ", f"'{case['priority']}' (dùng Critical/High/Medium/Low)")

        if "data" in case and not case["data"].strip():
            add("WARN", case, "Thiếu Test Data", "Cột Test Data trống")

        steps = split_numbered(case.get("steps", ""))
        expected = split_numbered(case.get("expected", ""))
        for col, items in (("Test Steps", steps), ("Expected Result", expected)):
            numbers = [n for n, _ in items]
            if items and None in numbers:
                add("ERROR", case, "Thiếu đánh số", f"{col} có dòng không đánh số (1, 2, 3...)")
            elif numbers and numbers != list(range(1, len(numbers) + 1)):
                add("ERROR", case, "Đánh số sai thứ tự", f"{col}: {numbers}")
        if steps and expected and len(steps) != len(expected):
            add("ERROR", case, "Step/Expected lệch nhau",
                f"{len(steps)} step nhưng {len(expected)} expected result")

        for key in ("steps", "data"):
            text = case.get(key, "")
            for pattern, msg in PLACEHOLDERS:
                m = re.search(pattern, text, re.IGNORECASE)
                if m:
                    add("ERROR", case, "Placeholder / dữ liệu chung chung", f"{msg}: \"{m.group(0)}\"")

        own_id = re.escape(case["tc_id"])
        pre = re.sub(own_id, "", case.get("precondition", ""))
        if DEPENDENCY.search(pre):
            add("WARN", case, "Phụ thuộc TC khác",
                "Pre-Condition tham chiếu TC khác — mỗi TC phải tự chuẩn bị dữ liệu")
    return issues


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input", help="File Markdown chứa bảng test case")
    parser.add_argument("--id-pattern", default=DEFAULT_ID_PATTERN, help="Regex convention TC ID")
    args = parser.parse_args()

    cases = parse_markdown(Path(args.input).read_text(encoding="utf-8"))
    if not cases:
        sys.exit(f"Không tìm thấy bảng test case (cần cột 'TC ID') trong {args.input}")

    issues = lint(cases, args.id_pattern)
    errors = sum(1 for i in issues if i[0] == "ERROR")
    warns = len(issues) - errors
    print(f"Đã kiểm tra {len(cases)} test case: {errors} ERROR, {warns} WARN\n")
    if issues:
        print("| Mức | TC ID | Dòng | Quy tắc | Chi tiết |")
        print("|---|---|---|---|---|")
        for level, tc_id, line, rule, detail in sorted(issues, key=lambda i: (i[0] != "ERROR", i[2])):
            print(f"| {level} | {tc_id} | {line} | {rule} | {detail.replace('|', '/')} |")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
