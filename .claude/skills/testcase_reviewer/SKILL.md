---
name: testcase_reviewer
description: Rà soát bộ manual test cases (file Markdown) theo Definition of Done trong CLAUDE.md — chạy lint tự động (TC ID, đánh số, placeholder, cột thiếu) rồi đánh giá nghiệp vụ (độ bao phủ Happy/Negative/Boundary/Edge, gộp validation, phụ thuộc TC, truy vết REQ). Dùng khi user yêu cầu "review test case", "rà soát TC", "kiểm tra bộ test case", hoặc trước khi bàn giao/import lên Xray.
---

# Test Case Reviewer

## 1. Mục đích

Kiểm tra chất lượng bộ test cases **trước khi bàn giao hoặc import lên Jira/Xray**, đảm bảo đạt toàn bộ Definition of Done trong `CLAUDE.md`.

Skill chia làm 2 lớp:
- **Lớp 1 — Lint tự động (script):** Lỗi cơ học, kiểm tra được bằng quy tắc.
- **Lớp 2 — Review nghiệp vụ (Claude):** Lỗi cần hiểu requirements và ngữ cảnh.

---

## 2. Khi nào sử dụng

### ✅ Nên dùng khi:
- User yêu cầu "review test case", "rà soát TC", "kiểm tra bộ test case này".
- Ngay sau khi skill `rbt_manual_testing` sinh xong test cases (Bước 6 FULL RBT hoặc cuối QUICK).
- Trước khi xuất CSV import lên Xray.

### ❌ Không dùng khi:
- Chưa có test cases → dùng `rbt_manual_testing`.
- Cần review tài liệu yêu cầu → dùng `requirements_analyzer` hoặc `/analyze_requirement_document`.

---

## 3. Quy trình Review (4 bước)

### Bước 1: Thu thập đầu vào
- File test cases Markdown (bắt buộc).
- Tài liệu requirements / danh sách REQ (nếu có) — cần cho kiểm tra độ bao phủ.
- Convention TC ID của dự án (mặc định: `[DỰ_ÁN]_[MODULE]_TC_[SỐ]`, ví dụ `CRM_CUST_TC_001`).

### Bước 2: Chạy lint tự động

```bash
python3 scripts/testcases/lint_testcases.py <file_test_cases.md>
# Convention TC ID riêng:
python3 scripts/testcases/lint_testcases.py <file> --id-pattern '^CRM_[A-Z]+_TC_\d{3}$'
```

Script kiểm tra:

| Quy tắc | Mức |
|---|---|
| TC ID sai convention / trùng lặp | ERROR |
| Thiếu Test Title, Test Steps, Expected Result, Priority | ERROR |
| Test Steps / Expected Result không đánh số hoặc sai thứ tự | ERROR |
| Số step ≠ số expected result | ERROR |
| Placeholder / dữ liệu chung chung trong Test Steps, Test Data (`nhập email hợp lệ`, `TBD`, `...`, `<email>`) | ERROR |
| Test Data trống | WARN |
| Priority ngoài Critical/High/Medium/Low | WARN |
| Pre-Condition tham chiếu TC khác (phụ thuộc) | WARN |

> Script chỉ là lớp lọc đầu tiên. Có thể có **false positive** (ví dụ: `...` nằm trong một chuỗi test data hợp lệ) — Claude phải đọc lại từng lỗi và loại các trường hợp không đúng trước khi báo cáo.

### Bước 3: Review nghiệp vụ (Claude đọc từng test case)

| # | Tiêu chí | Cách kiểm tra |
|---|---|---|
| R1 | **Độ bao phủ loại kịch bản** | Mỗi module có đủ Happy Path, Negative, Boundary, Edge Case (timeout, mất kết nối, double-click Submit) chưa? |
| R2 | **Field-Level Validation** | Liệt kê mọi field trong requirements → mỗi field có TC validation riêng theo đúng loại (bảng Field-Level Validation trong `rbt_manual_testing`) chưa? |
| R3 | **Gộp validation** | Có TC nào kiểm tra nhiều field trong cùng 1 TC không? → Tách. |
| R4 | **BVA đúng giá trị biên** | Với field có Min/Max, đã có test tại `Min-1`, `Min`, `Max`, `Max+1` chưa? Giá trị biên có tính đúng không (ví dụ: max 255 → test 255 và 256 ký tự)? |
| R5 | **Expected Result kiểm chứng được** | Expected có mô tả cụ thể (nội dung message, URL chuyển hướng, trạng thái dữ liệu) hay chỉ ghi chung chung "hệ thống hoạt động đúng"? |
| R6 | **Độc lập** | Mỗi TC có tự chuẩn bị dữ liệu trong Pre-Condition, không dựa vào kết quả TC khác? |
| R7 | **Test data đúng quy ước** | Dữ liệu unique dùng format traceable (`test_<chức_năng>_<timestamp>@manual.test`), không chứa PII thật? |
| R8 | **Thực thể động** | Tính năng phụ thuộc Event/Campaign/Promo đã có TC cho trạng thái chưa bắt đầu, đã kết thúc, kết thúc giữa chừng chưa? |
| R9 | **Bảo mật** | Text/Textarea field đã có TC cho XSS và SQL Injection chưa? |
| R10 | **Truy vết** | Nếu có danh sách REQ: mọi REQ có ít nhất 1 TC? Có TC nào không map về REQ nào? |
| R11 | **Priority / Risk hợp lý** | Luồng liên quan tiền, bảo mật, dữ liệu có Priority/Risk High trở lên? |

### Bước 4: Báo cáo & đề xuất sửa

Xuất báo cáo theo mẫu ở mục 4 và lưu vào `output/<module>/<YYYY-MM-DD>/review_test_cases_<module>.md`. Sau khi user đồng ý, Claude sửa trực tiếp file test cases, chạy lại lint đến khi **0 ERROR**.

---

## 4. Mẫu Báo cáo Review

```markdown
# 🔍 Review Test Cases: [Tên Module]

## 1. Tổng quan
- **File:** output/login/2026-10-03/test_cases_login.md
- **Số test case:** 24
- **Lint:** 3 ERROR, 2 WARN
- **Kết luận:** ❌ Chưa đạt DoD / ✅ Đạt DoD

## 2. Lỗi Lint (đã xác minh)
| Mức | TC ID | Quy tắc | Chi tiết | Đề xuất sửa |
|---|---|---|---|---|
| ERROR | SHOP_LOGIN_TC_005 | Placeholder | "Nhập email hợp lệ" | Nhập email: `test_login_1712049200@manual.test` |

## 3. Vấn đề Nghiệp vụ
| Mã | Tiêu chí | TC / Module | Vấn đề | Đề xuất |
|---|---|---|---|---|
| REV-01 | R2 | Login / Password | Thiếu TC Max length cho Password | Thêm TC: nhập 65 ký tự (max 64) |
| REV-02 | R3 | SHOP_LOGIN_TC_008 | Gộp validation Email + Password | Tách thành 2 TC |

## 4. Độ bao phủ
| Module | Happy | Negative | Boundary | Edge | Ghi chú |
|---|---|---|---|---|---|
| Login | 2 | 6 | 4 | 0 | ⚠️ Thiếu Edge Case (timeout, double-click) |

## 5. Truy vết (nếu có REQ)
| REQ | Số TC | Trạng thái |
|---|---|---|
| REQ-001 | 5 | ✅ |
| REQ-004 | 0 | ❌ Chưa có TC |
```

---

## 5. Quy tắc

1. Luôn viết bằng **Tiếng Việt**.
2. Mã vấn đề nghiệp vụ đánh `REV-XX`, kèm mã tiêu chí `R1`–`R11`.
3. Mỗi đề xuất sửa phải **cụ thể** (giá trị test data thật, TC cần thêm/tách) — không ghi "cần bổ sung thêm".
4. **Không tự sửa file** khi chưa được user đồng ý.
5. Không đánh giá được tiêu chí nào (ví dụ: không có requirements để kiểm R10) → ghi rõ "Không đủ dữ liệu để đánh giá", không bỏ qua im lặng.
