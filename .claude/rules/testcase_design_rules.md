# Quy tắc Thiết kế Manual Test Case

> **Mục tiêu:** Đảm bảo mọi kịch bản kiểm thử được thiết kế khoa học, đạt độ bao phủ tối đa và giảm thiểu số lượng test cases trùng lặp.

---

## 1. Kỹ thuật Thiết kế Bắt buộc

Khi thiết kế test cases, Agent phải áp dụng các kỹ thuật thiết kế chuẩn sau:

### 1.1 Phân vùng tương đương (Equivalence Partitioning)
* Chia tập dữ liệu đầu vào thành các phân vùng dữ liệu hợp lệ (Valid Partition) và không hợp lệ (Invalid Partition).
* Với mỗi phân vùng, chỉ cần thiết kế tối thiểu 1 test case đại diện.

### 1.2 Phân tích giá trị biên (Boundary Value Analysis - BVA)
* Áp dụng cho các trường dữ liệu dạng số, độ dài chuỗi ký tự, ngày tháng...
* Luôn xác định giá trị biên tối thiểu (Min) và tối đa (Max).
* Thiết kế các test cases tại biên: `Min - 1`, `Min`, `Min + 1`, `Max - 1`, `Max`, `Max + 1` (hoặc cấu trúc 2-point boundary: `Min`, `Max`, và các giá trị ngoài biên ngay sát).

### 1.3 Bảng quyết định (Decision Table)
* Áp dụng khi nghiệp vụ có sự kết hợp của nhiều điều kiện logic đầu vào để tạo ra các hành động/kết quả khác nhau.
* Lập bảng liệt kê tất cả các tổ hợp True/False (hoặc Yes/No) của các điều kiện và xác định kết quả tương ứng của từng tổ hợp.

### 1.4 Chuyển đổi trạng thái (State Transition Testing)
* Áp dụng khi đối tượng kiểm thử có vòng đời chuyển đổi trạng thái (ví dụ: Đơn hàng: *Mới tạo -> Đang xử lý -> Đang giao -> Đã giao -> Hoàn thành* hoặc *Đã hủy*).
* Thiết kế kịch bản kiểm thử cho tất cả các bước chuyển đổi hợp lệ và các bước chuyển đổi không được phép (Ví dụ: từ *Mới tạo* không thể chuyển thẳng sang *Đã giao*).

---

## 2. Checklist Kiểm thử các Trường Nhập liệu (Field-Level Validation)

Khi gặp form hoặc các input fields, Agent phải tạo danh sách kiểm thử chi tiết cho từng trường dựa trên loại dữ liệu của trường đó:

| Loại Field | Kịch bản kiểm thử cần có |
|------------|-------------------------|
| **Text/Chuỗi ký tự** | 1. Để trống (nếu là trường bắt buộc).<br>2. Nhập dưới độ dài tối thiểu (Min length).<br>3. Nhập vượt quá độ dài tối đa (Max length).<br>4. Nhập chỉ toàn khoảng trắng (whitespace).<br>5. Nhập các ký tự đặc biệt nguy hiểm (`<`, `>`, `&`, `"`, `'`).<br>6. Kiểm tra lỗi bảo mật SQL Injection (`' OR 1=1--`) và XSS (`<script>alert(1)</script>`). |
| **Email** | 1. Định dạng đúng (`user@domain.com`).<br>2. Thiếu ký tự `@`.<br>3. Thiếu phần tên miền (domain).<br>4. Chứa nhiều ký tự `@`.<br>5. Nhập email đã tồn tại trong hệ thống (kiểm tra tính duy nhất). |
| **Số điện thoại** | 1. Chỉ nhập chữ cái.<br>2. Nhập đúng đầu số nhà mạng và số lượng ký tự theo quy định nước sở tại.<br>3. Nhập quá ngắn hoặc quá dài so với chuẩn thông thường. |
| **Ngày tháng** | 1. Ngày không hợp lệ trong thực tế (Ví dụ: `31/02/2026`).<br>2. Năm nhuận (Ví dụ: `29/02/2024` - Hợp lệ, `29/02/2025` - Không hợp lệ).<br>3. Ngày trong quá khứ hoặc tương lai (dựa trên nghiệp vụ yêu cầu). |
| **Số / Tiền tệ** | 1. Nhập số âm.<br>2. Nhập số 0 (nếu trường yêu cầu lớn hơn 0).<br>3. Nhập số thập phân.<br>4. Nhập ký tự không phải số.<br>5. Nhập số cực lớn vượt quá giới hạn lưu trữ dữ liệu (Overflow). |

---

## 3. Tiêu chuẩn Nội dung Test Case

* **Tiêu đề (Title):** Phải nêu rõ hành động và mục đích kiểm thử (Ví dụ: `Xác thực đăng ký tài khoản thành công với email hợp lệ`).
* **Các bước thực hiện (Test Steps):** Phải rõ ràng, đánh số tuần tự, không viết chung chung. Chỉ rõ dữ liệu cần nhập vào đâu.
* **Kết quả mong đợi (Expected Result):** Phải tương ứng với từng bước thực hiện, ghi rõ hệ thống phản hồi như thế nào (Ví dụ: Hiển thị thông báo thành công, chuyển hướng trang, gửi email kích hoạt...).
* **Dữ liệu kiểm thử (Test Data):** Tuyệt đối không dùng dữ liệu chung chung. Hãy cung cấp ví dụ dữ liệu thật, có cấu trúc cụ thể.
