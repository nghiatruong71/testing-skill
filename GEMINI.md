# CLAUDE AI - GLOBAL MANUAL TESTING RULES

> **Scope:** Áp dụng cho mọi tác vụ Phân tích Nghiệp vụ và Thiết kế Manual Test Cases do Claude (Claude Code) hoạt động trong dự án này.
> **Mục tiêu:** Sinh ra test cases chất lượng cao, bao phủ đầy đủ kịch bản, dễ hiểu, dễ thực thi và sẵn sàng Import lên Jira/Xray/Excel.

---

## Git Pull Restriction Rule

* Tuyệt đối KHÔNG dùng lệnh GIT làm thay đổi trạng thái code/tài liệu (như `git pull`, `git checkout`, `git merge`, `git rebase`, `git reset`) để lấy code hoặc thay đổi nhánh.
* Luôn giữ nguyên trạng thái tài liệu local hiện tại để làm việc.
* Nếu cần file hoặc nội dung mới, hãy yêu cầu người dùng cung cấp thay vì tự ý dùng git.
* **Được phép** dùng lệnh read-only: `git status`, `git diff`, `git log` — để kiểm tra trạng thái mà không thay đổi dự án.

---

## Cleanup & Delivery

### ✅ Điều kiện bàn giao (Definition of Done)

Tài liệu Test Cases chỉ được coi là **hoàn thành** khi đáp ứng **toàn bộ** các tiêu chí sau:

#### 🧹 Tài liệu Cleanup
- [ ] Không để lại ghi chú nháp hoặc ký tự placeholder thừa.
- [ ] Không có test data hardcoded chung chung (như "nhập email hợp lệ", "nhập tên bất kỳ" — email, username, ID phải có giá trị cụ thể, traceable).
- [ ] Không có các bước test lặp lại mơ hồ.

#### 🏗️ Cấu trúc & Định dạng
- [ ] Định dạng bảng Markdown chuẩn, sẵn sàng để copy sang Excel hoặc import lên Jira/Xray.
- [ ] Phân chia rõ ràng theo Module, Sub-module.
- [ ] Đặt ID Test Case theo đúng convention (ví dụ: `[PROJECT]_[MODULE]_TC_[NUMBER]`).

#### ✔️ Chất lượng Test Cases
- [ ] Bao phủ đầy đủ: Happy Path, Negative Path (dữ liệu sai/thiếu), Boundary Cases, và Edge Cases (lỗi hệ thống, mất kết nối nếu có).
- [ ] Từng Test Step và Expected Result phải được đánh số tương ứng (1, 2, 3...).
- [ ] Mỗi test case độc lập — không phụ thuộc vào kết quả của test case trước.

---

## 1. Ngôn Ngữ & Giao Tiếp

- Luôn giao tiếp, giải thích ý tưởng và báo cáo bằng **Tiếng Việt**.
- Diễn giải **ngắn gọn, rõ ràng, dễ hiểu**.
- Tránh suy đoán mơ hồ về nghiệp vụ mà cần hỏi rõ User hoặc đưa ra giả định (Assumption) cụ thể.

## 2. Quy Trình Làm Việc (Workflow)

- **Recon (Tìm hiểu):** Luôn đọc kỹ tài liệu yêu cầu (Requirements/User Stories) hoặc inspect giao diện web/ứng dụng thực tế để hiểu luồng nghiệp vụ.
- **Decomposition (Phân rã):** Chia nhỏ tính năng phức tạp thành các module/sub-module nhỏ hơn để thiết kế kịch bản kiểm thử không bị sót.
- **Traceability (Truy vết):** Lập ma trận truy vết (Traceability Matrix) để đảm bảo 100% yêu cầu được bao phủ bởi các kịch bản test.
- **RBT & Generation:** Áp dụng kiểm thử dựa trên rủi ro (Risk-Based Testing) để phân bổ mức độ ưu tiên và sinh test case chi tiết.

## 3. Công Cụ Hỗ Trợ Manual QA

| Công cụ | Mục đích |
|---------|----------|
| Chrome DevTools | Inspect giao diện, xem cấu trúc HTML, kiểm tra API Request/Response. |
| Postman | Kiểm thử và xác thực các API endpoints. |
| Jira / Xray | Quản lý Requirements, lưu trữ Test Cases và ghi nhận kết quả thực thi. |

## 4. Tham Chiếu Rules Chi Tiết

Agent phải tham chiếu quy tắc chi tiết trong `.claude/rules/`:

- [Quy tắc Thiết kế Test Case](.claude/rules/testcase_design_rules.md) — Phân vùng tương đương, phân tích giá trị biên, bảng quyết định.
- [Quy tắc Phân tích Yêu cầu](.claude/rules/requirements_analysis_rules.md) — Cách phân tích tài liệu và phát hiện điểm mờ nghiệp vụ.

## 5. Tham Chiếu Skills

Agent sử dụng các skills chuyên biệt trong `.claude/skills/` tùy theo nhiệm vụ:

| Skill | Vai trò |
|-------|---------|
| `rbt_manual_testing` | Master skill cho manual testing — Sinh test cases theo chế độ QUICK hoặc quy trình FULL RBT 6 bước. |
| `requirements_analyzer` | Phân tích requirements sâu từ website/tài liệu nghiệp vụ. |
| `test_data_generator` | Sinh test data phong phú, có cấu trúc rõ ràng. |
| `jira_integration` | Kết nối lấy yêu cầu hoặc đẩy kết quả kiểm thử lên Jira/Xray. |

## 6. Kế Hoạch Kiểm Thử (Plan Templates)

Các bộ prompt template sẵn dùng trong `plans/`:

- **`plans/manual/`** — Quy trình sinh Manual Test Cases (QUICK + FULL RBT). Xem `plans/manual/QUICK_START.md` để bắt đầu.
- **`plans/cross-module/`** — Quy trình phân tích Cross-Module & Ma trận kết hợp. Xem `plans/cross-module/QUICK_START.md` để bắt đầu.

## 7. Test Data Rules

- Tất cả các trường yêu cầu **unique** (Email, Username, Code/ID) bắt buộc dùng dữ liệu ngẫu nhiên nhưng **traceable** (truy vết được).
- Định dạng khuyến nghị: `tên_chức_năng + timestamp + suffix`.
- Ví dụ:
  - Email: `test_register_1712049200@manual.test`
  - Username: `manual_user_1712049200`
  - Code: `TC_REG_1712049200`

## 8. Anti-Patterns (NGHIÊM CẤM)

| ❌ Anti-Pattern | ✅ Thay thế đúng |
|-----------------|------------------|
| Tự đoán nghiệp vụ khi chưa rõ | Đặt câu hỏi Q&A cho User / đưa ra Assumption rõ ràng |
| Viết các bước test chung chung (ví dụ: "nhập dữ liệu hợp lệ") | Chỉ rõ dữ liệu cần nhập (ví dụ: "nhập email: user@test.com") |
| Gộp validation nhiều trường vào 1 test case | Tách biệt validation cho từng trường |
| Thiếu kịch bản Negative/Boundary | Luôn bao phủ các trường hợp biên và dữ liệu sai |
| Dùng placeholder test data chung chung | Sinh test data thực tế và cụ thể |

## 9. Tham Chiếu Workflows (Slash Commands)

Agent sử dụng các workflows trong `.claude/commands/` qua slash commands:

| Workflow | Mô tả |
|----------|-------|
| `/generate_requirements_from_website` | Sinh requirements từ việc phân tích website/module thực tế |
| `/analyze_requirement_document` | Phân tích tài liệu yêu cầu (Jira/.doc) để phát hiện lỗ hổng nghiệp vụ |
| `/generate_manual_testcases_rbt` | Sinh manual test cases theo quy trình AI-RBT 6 bước |
| `/generate_testcases_from_requirements` | Sinh test cases nhanh từ requirements |
| `/generate_cross_module_test_plan` | Thiết kế test plan tích hợp đa module |
| `/generate_test_data` | Sinh test data có cấu trúc phục vụ manual test |
| `/fetch_jira_requirements` | Lấy requirements/user stories từ Jira |
| `/import_test_results_xray` | Đẩy kết quả test lên Xray |
