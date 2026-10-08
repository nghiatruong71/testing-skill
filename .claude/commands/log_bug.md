---
description: Log bug chi tiết lên Jira/Xray (tự động) hoặc tạo báo cáo lỗi mẫu dưới dạng Markdown.
skills:
  - log_bug
---

> **BẮT BUỘC (MANDATORY SKILL):** Bạn PHẢI nạp và đọc kỹ nội dung của skill **`log_bug`** (tại `.claude/skills/log_bug/SKILL.md`) trước khi bắt đầu thực hiện tác vụ này.

# Workflow: Quy Trình Báo Cáo Lỗi (Log Bug)

Workflow này hướng dẫn bạn thu thập thông tin và thực hiện báo cáo lỗi (log bug) lên Jira (thông qua MCP Server) hoặc tạo một mẫu báo cáo lỗi Markdown chuyên nghiệp để gửi cho đội ngũ phát triển.

## Các bước thực hiện:

### Bước 1: Tiếp nhận và làm rõ thông tin lỗi (Clarify Bug Info)
1. **Thu thập thông tin từ người dùng:**
   - Hành vi lỗi xảy ra là gì?
   - Module/Chức năng bị lỗi.
   - Các bước dẫn tới lỗi (Steps to Reproduce).
   - Kết quả thực tế (Actual Result) vs Kết quả mong đợi (Expected Result).
   - Môi trường chạy lỗi (OS, Browser, App Version, URL, Account...).
   - Bằng chứng lỗi (Screenshot, log API, video, payload).
2. **Kiểm tra thông tin:** Đảm bảo tất cả các dữ liệu test được cung cấp cụ thể, không sử dụng các placeholder mơ hồ (tuân thủ **Test Data Rules**).

### Bước 2: Phân loại mức độ nghiêm trọng (Severity & Priority)
Xác định mức độ ảnh hưởng của lỗi dựa trên bảng phân loại trong skill `log_bug`:
- **Critical / Blocker:** Trắng trang, sập ứng dụng, chặn đứng luồng nghiệp vụ chính.
- **Major:** Nghiệp vụ chính bị ảnh hưởng nhưng có workaround, hoặc lỗi chức năng phụ.
- **Minor:** Lỗi giao diện (UI), chính tả, hoặc lỗi trải nghiệm (UX).
- **Trivial:** Lỗi hiển thị cực nhỏ.

### Bước 3: Soạn thảo báo cáo lỗi (Draft Bug Report)
Tạo bản nháp báo cáo lỗi định dạng Markdown chi tiết theo đúng mẫu tương ứng (Lỗi chức năng/giao diện hoặc Lỗi API/tích hợp) trong skill `log_bug`.

### Bước 4: Đẩy lỗi lên hệ thống quản lý (Jira Integration)
1. **Nếu dự án có tích hợp Jira:**
   - Sử dụng MCP tool `createJiraIssue` của `atlassian-mcp-server`.
   - Chọn loại issue (`issueTypeName`) là `Bug`.
   - Truyền đầy đủ các thông tin: `summary` (tiêu đề), `description` (nội dung chi tiết), `priority` và các `labels` (ví dụ: `bug`) trong trường `additional_fields`.
2. **Nếu không sử dụng Jira:**
   - Xuất báo cáo lỗi thành một file Markdown lưu tại `output/<module>/<YYYY-MM-DD>/bugs/bug_<mô_tả_ngắn>_<timestamp>.md` để người dùng sao chép thủ công.

---

## Output mong muốn:
- Một issue `Bug` được tạo thành công trên Jira (kèm Issue Key).
- HOẶC Một file Markdown báo cáo lỗi chi tiết chuyên nghiệp gửi tới người dùng.
