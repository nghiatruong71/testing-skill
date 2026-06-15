# Prompt Templates dành cho Manual Testing

Thư mục này chứa các prompt mẫu hỗ trợ đắc lực cho các tác vụ kiểm thử thủ công (Manual Testing). Các prompt này đã được tinh chỉnh để bạn sử dụng trực tiếp bằng cách copy-paste vào khung chat của AI Agent.

---

## Danh Sách Prompt Templates Hỗ Trợ

| # | File | Lệnh Slash Command tương ứng | Kỹ năng AI (Skill) | Mục tiêu |
|---|------|-----------------------------|--------------------|----------|
| 01 | `prompt_01_generate_requirements.txt` | `/generate_requirements_from_website` | `requirements_analyzer` | Thu thập và sinh tài liệu Requirements từ website nghiệp vụ |
| 02 | `prompt_02_generate_test_cases.txt` | `/generate_manual_testcases_rbt` | `rbt_manual_testing` | Sinh bộ Test Cases theo kỹ thuật phân tích rủi ro |
| 07 | `prompt_07_generate_test_data.txt` | `/generate_test_data` | `test_data_generator` | Sinh dữ liệu kiểm thử (Test Data) phong phú, có cấu trúc |

---

## Cách Sử Dụng

1. Mở file `.txt` tương ứng với tác vụ bạn cần thực hiện.
2. Sao chép nội dung prompt.
3. Thay thế các phần trong dấu ngoặc vuông `[...]` bằng thông tin thực tế của dự án của bạn.
4. Gửi nội dung đã chỉnh sửa vào khung chat với AI Agent để bắt đầu thực hiện theo đúng quy trình.
