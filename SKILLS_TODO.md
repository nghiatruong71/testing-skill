# Skills — Các vấn đề còn tồn đọng

> Cập nhật: 2026-10-03. Danh sách các điểm chưa sửa sau đợt rà soát skills trong `.claude/skills/` và `.agent/skills/`.

## 1. Thiếu script Jira/Xray — skill `jira_integration` chưa chạy được

- Skill tham chiếu các file **không có trong repo**:
  - `scripts/integrations/jira/jira_fetcher.js`
  - `scripts/integrations/jira/xray_auth.js`
  - `scripts/integrations/jira/xray_importer.js`
  - `scripts/integrations/jira/utils.js`
  - `scripts/integrations/package.json`
  - `.env.example`
- **Cần làm:** Bổ sung các file trên, hoặc đánh dấu skill là "chưa sẵn sàng" / gỡ khỏi CLAUDE.md.

## 2. `.claude/settings.json` sai cú pháp — các rule quyền không có hiệu lực

- Các rule hiện tại (`"Read project files"`, `"Push to remote repositories"`, `"Run playwright tests"`...) là mô tả bằng chữ, không phải cú pháp quyền của Claude Code → bị bỏ qua, **không có gì thực sự bị chặn**.
- Claude không tự sửa được file này (bị chặn vì là file cấu hình quyền của chính Claude). Người dùng cần sửa tay.
- **Đề xuất nội dung thay thế** (bám theo CLAUDE.md — cấm git làm thay đổi trạng thái):

```json
{
  "permissions": {
    "allow": [
      "Read(./.env)"
    ],
    "ask": [
      "Bash(rm:*)"
    ],
    "deny": [
      "Bash(git push:*)",
      "Bash(git pull:*)",
      "Bash(git checkout:*)",
      "Bash(git merge:*)",
      "Bash(git rebase:*)",
      "Bash(git reset:*)",
      "Bash(npm install -g:*)",
      "Bash(npm i -g:*)",
      "Bash(npx playwright test:*)",
      "Bash(mvn:*)"
    ]
  }
}
```

- Rule gốc `"Execute shell commands for testing"` quá mơ hồ để chuyển thành rule cụ thể — cần xác định rõ lệnh nào muốn chặn.

## 3. `.claude/settings.local.json` chứa rule rác từ máy Windows

- Chứa các lệnh PowerShell với đường dẫn `d:\ANHTESTER\ClaudeCode\claude-testing-kit` — không dùng được trên máy khác.
- File này đang được **commit vào git** (thường nên nằm trong `.gitignore` vì là cấu hình cá nhân).
- **Cần làm:** Xóa nội dung (hoặc xóa file) và thêm `.claude/settings.local.json` vào `.gitignore`.

## 4. Thiếu MCP server — một số tính năng skill chưa dùng được

Repo chưa có `.mcp.json`. Các tính năng sau chỉ chạy được khi cài MCP tương ứng:

| Skill | Tính năng | MCP cần cài |
|---|---|---|
| `log_bug` | Tự tạo Bug ticket trên Jira (`createJiraIssue`) | Atlassian MCP |
| `design_analyzer` | Đọc trực tiếp link Figma | Figma MCP |
| `requirements_analyzer` | Mở browser thật để chụp/inspect giao diện | Playwright MCP |

Khi chưa cài: `log_bug` xuất báo cáo Markdown; `design_analyzer` dùng screenshot; `requirements_analyzer` dùng HTML/tài liệu người dùng cung cấp.

## 5. Quy ước test data chưa thống nhất ở lệnh combinatorial

- `generate_test_data` và skill `test_data_generator` đã chuyển sang `test_...@manual.test` theo CLAUDE.md.
- `.claude/commands/generate_combinatorial_test_data.md`, `generate_cross_module_test_plan.md` và phần "Multi-Step / Combinatorial" trong skill `test_data_generator` vẫn dùng prefix `auto_combo{XX}` / `auto_c{XX}`.
- **Cần quyết định:** Giữ `auto_combo` riêng cho dữ liệu ma trận kết hợp, hay đổi thống nhất sang prefix manual.

## 6. Tính năng mới chỉ có ở bản Claude (`.claude/`)

- Skill `testcase_reviewer`, lệnh `/review_testcases`, và bước lint + xuất CSV trong `rbt_manual_testing` **chỉ thêm vào `.claude/`**, không đồng bộ sang `.agent/` (Gemini) và `GEMINI.md`.
- Scripts dùng chung: `scripts/testcases/` (`tc_parser.py`, `lint_testcases.py`, `md_to_xray_csv.py`).

## 7. CSV Xray chưa thử import trên Xray thật

- `md_to_xray_csv.py` đã chạy thử với file mẫu, nhưng **chưa import thử** lên Xray Cloud/Server của dự án.
- Khi import lần đầu: trong wizard Xray Test Case Importer, map `TCID` → Test Case Identifier, `Action` / `Data` / `Expected Result` → các trường Step tương ứng; các cột còn lại map theo cấu hình project. Lưu cấu hình map để dùng lại.
