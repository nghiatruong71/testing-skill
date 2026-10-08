---
description: Rà soát bộ manual test cases theo Definition of Done — lint tự động + review nghiệp vụ, xuất báo cáo và đề xuất sửa.
skills:
  - testcase_reviewer
---

> **BẮT BUỘC (MANDATORY SKILL):** Bạn PHẢI nạp và đọc kỹ nội dung của skill **`testcase_reviewer`** (tại `.claude/skills/testcase_reviewer/SKILL.md`) trước khi bắt đầu thực hiện tác vụ này.

# Workflow: Rà soát Test Cases

## Đầu vào

- `$ARGUMENTS` — đường dẫn file test cases Markdown (ví dụ: `output/login/2026-10-03/test_cases_login.md`). Nếu trống → hỏi user.
- Tài liệu requirements (nếu user cung cấp) để kiểm tra độ bao phủ và truy vết.

## Các bước thực hiện

1. **Chạy lint:** `python3 scripts/testcases/lint_testcases.py <file>` — xác minh từng lỗi, loại false positive.
2. **Review nghiệp vụ:** Đánh giá theo tiêu chí R1–R11 trong skill.
3. **Xuất báo cáo** theo mẫu trong skill, lưu vào `output/<module>/<YYYY-MM-DD>/review_test_cases_<module>.md`.
4. **Hỏi user** có muốn sửa không. Nếu đồng ý → sửa file, chạy lại lint đến khi 0 ERROR.
5. **Gợi ý bước tiếp:** Xuất CSV để import Xray:
   `python3 scripts/testcases/md_to_xray_csv.py <file>`
