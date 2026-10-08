# Claude Testing Kit for Manual Testing 🚀

👋 Chào mừng bạn đến với **Claude Testing Kit** phiên bản chuyên biệt dành cho **Manual Testing**!

Đây là bộ Kit được thiết lập và phát triển để hỗ trợ tối đa cho các công việc của **Manual Tester / QA Engineer** trên nền tảng **Claude Code** hoặc **Antigravity**. Bộ Kit này tập trung 100% vào việc chuẩn hóa quy trình phân tích yêu cầu nghiệp vụ, thiết kế kịch bản kiểm thử (Test Cases) và quản lý dữ liệu kiểm thử.

Mục tiêu chính là giúp Manual Tester làm việc thông minh hơn, nhanh hơn và chính xác hơn nhờ sự hỗ trợ đắc lực từ AI Agent một cách có hệ thống.

---

## 🌟 Tính Năng Nổi Bật

- **📋 Quy Trình Thiết Kế Test Cases Chuẩn RBT:** Thiết kế test cases chuyên sâu dựa trên rủi ro nghiệp vụ (**Risk-Based Testing**), giúp phân loại và tối ưu hóa độ bao phủ của kịch bản kiểm thử.
- **🔍 Phân Tích Requirements Thông Minh:** AI tự động quét và phân tích để phát hiện các lỗ hổng nghiệp vụ, điểm mờ (Ambiguities), mâu thuẫn trong tài liệu yêu cầu.
- **🧬 Thiết Kế Dữ Liệu Kiểm Thử Phong Phú:** Tự động sinh Test Data đa dạng, có cấu trúc thực tế và đảm bảo tính truy vết (Traceable Test Data).
- **🇻🇳 Giao Tiếp Hoàn Toàn Bằng Tiếng Việt:** AI được cấu hình để trao đổi, đưa ra câu hỏi Q&A và kết xuất bảng Test Cases bằng tiếng Việt rõ ràng, mạch lạc.

---

## 📂 Cấu Trúc Thư Mục

```
claude-testing-kit/
├── .claude/
│   ├── commands/       # 8 lệnh tùy chỉnh (Slash Commands) cho manual
│   ├── rules/          # Quy tắc thiết kế Test Cases và phân tích yêu cầu
│   ├── skills/         # 4 kỹ năng chuyên biệt cho AI
│   └── settings.json   # Cấu hình quyền hạn hệ thống cho AI Agent
├── plans/
│   ├── manual/          # Quy trình 6 bước sinh Manual Test Cases (AI-RBT)
│   └── cross-module/    # Quy trình thiết kế kịch bản tích hợp đa module
├── prompt_templates/    # Prompt mẫu dùng nhanh cho manual (copy -> paste -> gửi)
└── CLAUDE.md            # Rule chung bắt buộc AI Agent tuân theo
```

### Chi Tiết Thư Mục `.claude/`

| Thư mục | Vai trò |
|---------|--------|
| `commands/` | Chứa 8 lệnh như `/generate_manual_testcases_rbt`, `/generate_testcases_from_requirements`, `/generate_requirements_from_website`, `/analyze_requirement_document`... |
| `rules/` | Quy tắc kiểm thử: quy chuẩn thiết kế test case (`testcase_design_rules.md`) và phương pháp phân tích yêu cầu (`requirements_analysis_rules.md`). |
| `skills/` | Các skill chuyên dụng: `rbt_manual_testing`, `requirements_analyzer`, `test_data_generator`, `jira_integration`, `design_analyzer`. |
| `settings.json` | Phân quyền bảo mật cho AI Agent khi hoạt động trong workspace. |

---

## 🧭 Hướng Dẫn Sử Dụng Nhanh

### Cách 1: Sử dụng trong Claude Code CLI hoặc Antigravity
1. Copy thư mục `.claude` và file `CLAUDE.md` vào thư mục gốc của dự án kiểm thử của bạn.
2. Khởi động AI Agent bằng lệnh `claude` (hoặc khởi động trong IDE).
3. Gõ `/` trong khung chat để xem các lệnh có sẵn. Ví dụ:
   * `/generate_manual_testcases_rbt` (để chạy quy trình AI-RBT 6 bước).
   * `/generate_testcases_from_requirements` (để sinh test case nhanh).

### Cách 2: Sử dụng Prompt Templates dùng nhanh
* Vào thư mục `prompt_templates/`, chọn prompt phù hợp với tác vụ.
* Thay đổi các thông tin trong dấu ngoặc vuông `[...]` bằng dữ liệu thực tế dự án của bạn.
* Sao chép toàn bộ nội dung và gửi cho AI.

### Cách 3: Thực hiện theo quy trình kế hoạch (Plans)
* Mở file `QUICK_START.md` trong `plans/manual/` hoặc `plans/cross-module/`.
* Thực hiện lần lượt từng bước theo hướng dẫn để thiết lập bối cảnh, phân tích yêu cầu và xuất Test Cases hoàn chỉnh.

---

## 🔄 So Sánh Antigravity vs Claude Code

| Tiêu chí | Antigravity (`.agent/`) | Claude Code (`.claude/`) |
|-----------|------------------------|--------------------------|
| Thư mục cấu hình | `.agent/` | `.claude/` |
| File quy tắc chính | `GEMINI.md` | `CLAUDE.md` |
| Slash commands | `.agent/workflows/` | `.claude/commands/` |
| Rules phụ | `.agent/rules/` | `.claude/rules/` |
| Skills chuyên biệt | `.agent/skills/` | `.claude/skills/` |

---

## 📄 Giấy phép (License)
Dự án được phân phối dưới giấy phép mã nguồn mở **MIT License**.
