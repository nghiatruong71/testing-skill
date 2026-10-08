---
name: log_bug
description: Viết báo cáo lỗi (Bug Report) chuẩn: tiêu đề, môi trường, bước tái hiện, actual/expected, severity, evidence; tạo ticket Jira qua Atlassian MCP nếu có, ngược lại xuất Markdown. Dùng khi user yêu cầu "log bug", "viết bug report", "tạo issue lỗi", hoặc khi phát hiện lỗi trong lúc test.
---

# Log Bug Skill

## 1. Mô Tả

Skill này hướng dẫn quy trình phát hiện, phân tích, phân loại và báo cáo lỗi (log bug) một cách chuẩn hóa, rõ ràng và dễ tái hiện nhất. Hỗ trợ cả hai hình thức:
- **Tự động (Jira MCP Integration):** Sử dụng các API của Jira qua MCP Server để tạo trực tiếp issue loại `Bug`.
- **Thủ công (Markdown Export):** Tạo báo cáo lỗi chi tiết định dạng Markdown chuẩn để copy-paste lên các công cụ tracking khác.

---

## 2. Khi Nào Sử Dụng

Sử dụng skill này khi:
- Phát hiện lỗi trong quá trình thực thi test (manual test hoặc automation test).
- User yêu cầu: "log bug này lên Jira", "viết bug report cho lỗi đăng nhập", "tạo issue lỗi UI".
- Cần chuẩn hóa thông tin lỗi để gửi cho đội phát triển (Developers).

---

## 3. Quy Trình Log Bug Chuẩn (4 Bước)

### Bước 1: Xác Định Lỗi & Thu Thập Thông Tin
Trước khi log bug, Agent phải thu thập đầy đủ thông tin:
1. **Tiêu đề lỗi (Summary):** Ngắn gọn, nêu bật được lỗi xảy ra ở đâu, lúc nào (Format: `[Module] Hành động -> Lỗi xảy ra`).
2. **Môi trường (Environment):** Hệ điều hành, Trình duyệt, Thiết bị, Môi trường test (Staging/Production).
3. **Dữ liệu kiểm thử (Test Data):** Dữ liệu cụ thể dùng để tái hiện lỗi. Tuân thủ **Test Data Rules** (ngẫu nhiên nhưng traceable).
4. **Các bước tái hiện (Steps to Reproduce):** Rõ ràng, đánh số tuần tự.
5. **Kết quả thực tế (Actual Result) vs Kết quả mong đợi (Expected Result).**
6. **Bằng chứng (Evidence):** Link screenshot, video hoặc API payload/log lỗi.

### Bước 2: Phân Loại Mức Độ Nghiêm Trọng (Severity) & Độ Ưu Tiên (Priority)

| Mức độ | Định nghĩa | Ví dụ |
|---|---|---|
| **Blocker / Critical** | Lỗi làm crash hệ thống, mất dữ liệu, hoặc chặn đứng hoàn toàn luồng nghiệp vụ chính (Happy Path) mà không có cách giải quyết thay thế (workaround). | Không thể bấm nút "Thanh toán", trắng trang sau khi đăng nhập. |
| **Major** | Lỗi ảnh hưởng lớn đến nghiệp vụ chính nhưng vẫn có workaround, hoặc lỗi chặn đứng luồng nghiệp vụ phụ. | Không thể tải file PDF hóa đơn (nhưng vẫn xem được online). |
| **Minor** | Lỗi nhỏ, không ảnh hưởng đến chức năng nghiệp vụ, chủ yếu là lỗi giao diện (UI), chính tả, hoặc lỗi trải nghiệm người dùng (UX). | Sai font chữ, lệch nút bấm 5px, sai lỗi chính tả tiếng Việt. |
| **Trivial** | Lỗi cực nhỏ, hầu như không ảnh hưởng. | Thiếu dấu chấm ở cuối câu thông báo. |

### Bước 3: Soạn Thảo Nội Dung (Mẫu Bug Report)

#### Mẫu 1: Lỗi Chức Năng / Giao Diện (Functional & UI Bug)
```markdown
*   **Tiêu đề:** [Login] Nhập mật khẩu sai quá 5 lần không bị khóa tài khoản
*   **Môi trường:** macOS 14.5, Chrome v125, Staging Environment
*   **Tài khoản test:** manual_user_1712049200@manual.test
*   **Các bước tái hiện:**
    1. Truy cập trang Đăng nhập [Đăng nhập](http://staging.example.com/login).
    2. Nhập email: `manual_user_1712049200@manual.test`.
    3. Nhập mật khẩu sai: `WrongPass123!`.
    4. Nhấn nút "Đăng nhập".
    5. Lặp lại bước 3 & 4 liên tục 6 lần.
*   **Kết quả thực tế:** Tài khoản không bị khóa, người dùng vẫn có thể tiếp tục thử đăng nhập tiếp.
*   **Kết quả mong đợi:** Tài khoản phải bị tạm khóa trong 15 phút sau 5 lần đăng nhập sai liên tiếp, hệ thống hiển thị thông báo lỗi rõ ràng.
*   **Bằng chứng:** [screenshot_login_fail.png](file:///path/to/screenshot)
```

#### Mẫu 2: Lỗi API / Tích Hợp (API Bug)
```markdown
*   **Tiêu đề:** [API] API POST `/api/v1/checkout` trả về lỗi 500 khi thiếu trường `discount_code`
*   **Endpoint:** `POST https://api-staging.example.com/api/v1/checkout`
*   **Request Payload:**
    ```json
    {
      "cart_id": "cart_checkout_1712049200",
      "payment_method": "COD"
    }
    ```
*   **Kết quả thực tế:** API trả về HTTP Status Code `500 Internal Server Error` với body: `{"error": "NullPointerException at..."}`.
*   **Kết quả mong đợi:** Trường `discount_code` là optional. Nếu thiếu, API phải xử lý checkout bình thường và trả về HTTP Status `200 OK`.
```

### Bước 4: Thực Thi Log Bug Lên Jira

Sử dụng tool `createJiraIssue` của `atlassian-mcp-server` để đẩy lỗi lên Jira.

#### Ví dụ tham số truyền vào tool:
```json
{
  "cloudId": "your-jira-site-url-or-uuid",
  "projectKey": "PROJ",
  "issueTypeName": "Bug",
  "summary": "[Login] Nhập mật khẩu sai quá 5 lần không bị khóa tài khoản",
  "description": "...", // Sử dụng định dạng Markdown/ADF mô tả các bước tái hiện
  "additional_fields": {
    "priority": {
      "name": "High"
    },
    "labels": ["bug", "security", "sprint-1"]
  }
}
```

---

## 4. Các Quy Tắc Quan Trọng (Anti-Patterns cần tránh)

- ❌ **Không log bug chung chung:** Tiêu đề như "Chức năng đăng nhập bị lỗi" là không hợp lệ. Phải nêu rõ hành động và lỗi xảy ra.
- ❌ **Không dùng dữ liệu hardcoded mơ hồ:** Tránh ghi "Nhập tài khoản bất kỳ". Phải cung cấp email/username cụ thể, tuân thủ traceable test data rules.
- ❌ **Không gộp nhiều bug khác nhau vào 1 ticket:** Mỗi hành vi lỗi khác nhau phải được log thành các ticket riêng biệt để dev dễ theo dõi và đóng ticket.
- ❌ **Thiếu bằng chứng (Evidence):** Không đính kèm log lỗi API hoặc ảnh chụp màn hình khi log các lỗi liên quan đến UI/API.
