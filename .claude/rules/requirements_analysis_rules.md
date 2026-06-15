# Quy tắc Phân tích Yêu cầu & Phát hiện Điểm mờ Nghiệp vụ (Ambiguity)

> **Mục tiêu:** Giúp Agent chủ động phát hiện các lỗ hổng, mâu thuẫn hoặc điểm chưa rõ ràng trong tài liệu yêu cầu (Requirements/User Stories) trước khi bắt tay vào thiết kế test cases.

---

## 1. Các điểm cần lưu ý khi đọc tài liệu yêu cầu

Khi tiếp nhận tài liệu yêu cầu từ người dùng, Agent phải chủ động rà soát các khía cạnh sau:

### 1.1 Tính thiếu sót (Omissions)
* Tài liệu có quy định giới hạn độ dài ký tự tối đa/tối thiểu cho các textbox không?
* Tài liệu có mô tả các trường hợp lỗi (Error handling) khi người dùng nhập sai không?
* Có quy định về hành vi của hệ thống khi mất kết nối mạng, timeout, hoặc khi click đúp liên tục vào nút Submit không?

### 1.2 Tính mâu thuẫn (Contradictions)
* Mô tả ở phần biểu đồ UI có khớp với mô tả nghiệp vụ bằng chữ ở dưới không?
* Có yêu cầu nào mâu thuẫn với các tính năng hiện hữu của hệ thống đã được định nghĩa từ trước không?

### 1.3 Tính mơ hồ (Ambiguities)
* Tránh các từ ngữ chung chung không định lượng được như: *nhanh chóng*, *giao diện đẹp*, *dễ sử dụng*, *thời gian hợp lý*, *dữ liệu lớn*...
* Cần làm rõ các thông số kỹ thuật cụ thể (Ví dụ: *"thời gian phản hồi dưới 2 giây"*, *"hỗ trợ tải file kích thước tối đa 10MB"*).

---

## 2. Quy trình đặt câu hỏi Q&A

Nếu phát hiện điểm chưa rõ ràng trong tài liệu yêu cầu, Agent **BẮT BUỘC** phải lập danh sách câu hỏi Q&A gửi tới người dùng. Quy chuẩn đặt câu hỏi như sau:

1. **Đánh số thứ tự câu hỏi:** Định dạng `Q1`, `Q2`, `Q3`... để người dùng dễ theo dõi và trả lời theo từng mục.
2. **Nêu ngữ cảnh (Context):** Trích dẫn cụ thể dòng hoặc phần nào trong tài liệu yêu cầu gây ra thắc mắc.
3. **Đưa ra Giả định (Assumption):** Với mỗi câu hỏi, Agent nên đề xuất một giả định logic/hợp lý nhất (Ví dụ: *"Nếu không có quy định độ dài tối đa, chúng tôi giả định độ dài tối đa là 255 ký tự"*). Điều này giúp người dùng dễ dàng đồng ý hoặc điều chỉnh nhanh chóng.

---

## 3. Quản lý Traceability Matrix (Ma trận truy vết)

* Đảm bảo mọi dòng yêu cầu (Requirement Line) được gán một mã định danh duy nhất (Ví dụ: `REQ-001`, `REQ-002`...).
* Trong danh sách test cases, bắt buộc phải có cột tham chiếu ngược lại mã yêu cầu để đảm bảo tính bao phủ (100% requirements đều có test cases tương ứng).
