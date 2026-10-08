---
name: test_data_generator
description: Sinh test data cụ thể, unique, traceable cho manual test cases (positive, negative, boundary, edge, API payload, dữ liệu đa module/ma trận kết hợp). Dùng khi user yêu cầu "sinh test data", "dữ liệu test cho form", "data biên", hoặc khi test case cần giá trị cụ thể thay cho placeholder.
---

# Test Data Generator

Mục đích: Sinh test data cụ thể, đáng tin cậy để điền trực tiếp vào cột **Test Data** của manual test cases (không dùng placeholder chung chung).

---

## Khi nào sử dụng

Sử dụng skill này khi:

- Cần test data cho test cases mới
- Sinh dữ liệu cho các trường hợp biên (boundary) và ngoại lệ (edge case)
- Chuẩn bị bộ dữ liệu cho data-driven testing (nhiều bộ input cho cùng 1 kịch bản)
- Chuẩn bị API request payload để test bằng Postman

---

## Phạm vi

Sinh test data cho:

- Form đăng ký
- Thông tin đăng nhập
- Form nhập liệu (submit)
- API payload
- Từ khóa tìm kiếm
- File upload

---

## Quy tắc dữ liệu

Mọi dữ liệu sinh ra phải:

- **Unique** — Không trùng lặp trong cùng bộ test
- **Deterministic** — Cùng seed cho ra cùng dữ liệu (khi cần tái hiện)
- **Traceable** — Nhìn dữ liệu là biết test case nào tạo ra

---

## Pattern dữ liệu unique

Theo CLAUDE.md (mục 7): `tên_chức_năng + timestamp + suffix`

```
<prefix>_<tên_chức_năng>_<timestamp>
```

Ví dụ:

```
manual_register_1712049200
test_login_1712049200
```

---

## Các loại dữ liệu thường gặp

### Email
```
test_<tên_chức_năng>_<timestamp>@manual.test
```
Ví dụ: `test_register_1712049200@manual.test`

### Username
```
manual_<tên_chức_năng>_<timestamp>
```
Ví dụ: `manual_user_1712049200`

### Mã / ID
```
TC_<MODULE>_<timestamp>
```
Ví dụ: `TC_REG_1712049200`

### Số điện thoại
```
10 chữ số, bắt đầu bằng đầu số nhà mạng Việt Nam hợp lệ
```
Ví dụ: `0912345678`

### Mật khẩu
```
Kết hợp chữ hoa, chữ thường, chữ số, ký tự đặc biệt
```
Ví dụ: `Test@12345`

---

## Phân loại dữ liệu

### Dữ liệu hợp lệ (Positive — Happy Path)
- Đúng định dạng, nằm trong giới hạn cho phép
- Điền đủ các trường bắt buộc
- Giá trị nghiệp vụ thông thường

### Dữ liệu sai (Negative)
- Thiếu trường bắt buộc
- Sai định dạng (email sai, mật khẩu quá ngắn)
- Ký tự không hợp lệ
- Giá trị đã tồn tại (kiểm tra trùng lặp)

### Giá trị biên (Boundary)
- Độ dài tối thiểu (ví dụ: 1 ký tự)
- Độ dài tối đa (ví dụ: 255 ký tự)
- Min - 1, Min + 1, Max - 1, Max + 1
- Chuỗi rỗng vs null
- Số 0, số âm

### Trường hợp ngoại lệ (Edge Cases)
- Unicode / ký tự đặc biệt / Emoji
- Chuỗi rất dài
- Mẫu SQL injection (`' OR 1=1--`) — phục vụ kiểm thử bảo mật
- Thẻ HTML / XSS (`<script>alert(1)</script>`)
- Khoảng trắng đầu/cuối

---

## Ràng buộc

Test data phải:

- Tuân thủ validation rules của từng trường (lấy từ requirements hoặc inspect DOM)
- Đúng định dạng input (định dạng ngày, số điện thoại)
- Không trùng lặp giữa các lần chạy test
- Không chứa dữ liệu cá nhân thật (PII)

---

## Định dạng đầu ra

Trình bày dữ liệu có cấu trúc:

```json
{
  "positive": [
    { "email": "test_register_1712049200@manual.test", "password": "Test@12345" }
  ],
  "negative": [
    { "email": "", "password": "Test@12345", "expectedError": "Email là bắt buộc" },
    { "email": "test_register_1712049201.manual.test", "password": "Test@12345", "expectedError": "Email không đúng định dạng" }
  ],
  "boundary": [
    { "email": "test_register_1712049202@manual.test", "password": "Abc@1234", "note": "Mật khẩu đúng độ dài tối thiểu (8 ký tự)" }
  ]
}
```

---

## Multi-Step Data Pipeline (Cross-Module)

> Mở rộng cho bài toán: test data cần đi qua **nhiều modules nối tiếp** mới tạo ra được data hoàn chỉnh cho module cuối.

### Khi nào dùng

- Tính năng đi qua chuỗi N modules (VD: Đối tác → Thanh toán → Thuế → Biên bản)
- Data module sau **phụ thuộc** output module trước (Reference fields)
- Cần tạo data thật trên hệ thống qua browser

### Data Chain Pattern

```
Module 1 → Output: {id_1, code_1}
    ↓ (Reference)
Module 2 → Input: {id_1} → Output: {id_2}
    ↓ (Reference)
Module 3 → Input: {id_1, id_2} → Output: {id_3}
    ↓ (Reference)
Module N → Input: {id_1..id_N-1} → Output: Final Result
```

### Field Classification

| Loại field | Mô tả | Cách sinh data |
|-----------|-------|----------------|
| **Dimension field** | Giá trị thuộc chiều kết hợp trong ma trận | Lấy chính xác từ bộ combo — KHÔNG random |
| **Supporting field** | Bắt buộc nhưng không phải dimension | Random + unique + traceable |
| **Reference field** | ID/code từ output module trước | Copy từ output module trước trong chuỗi |
| **Computed field** | Tự tính từ formula/business rules | Tính theo formula — phải verify |

### Data Chain Tracing Format

```
auto_combo{XX}_{module_short}_{timestamp}
```

Ví dụ cho combo 01:
```
Module 1: partner_name  = "auto_c01_partner_1712049200"
Module 2: payment_desc  = "auto_c01_payment_1712049200"
Module 3: tax_note      = "auto_c01_tax_1712049200"
→ Có thể trace: combo 01 tạo ra những data nào ở mỗi module
```

---

## Combinatorial Data Generation

> Sinh bộ data cho **ma trận kết hợp đa chiều** — mỗi bộ kết hợp = 1 bộ data hoàn chỉnh.

### Khi nào dùng

- Đã có ma trận kết hợp (từ `/generate_cross_module_test_plan`)
- Cần sinh N bộ data tương ứng N bộ kết hợp
- Mỗi bộ data phải có expected output (template, formula, computed values)

### Combinatorial Data Structure

```json
{
  "combination_id": "COMBO_01",
  "dimensions": {
    "D1": "value_from_matrix",
    "D2": "value_from_matrix"
  },
  "module_data": {
    "module_1": { "field1": "...", "field2": "..." },
    "module_2": { "ref_from_module1": "...", "field3": "..." }
  },
  "expected_output": {
    "template": "EXPECTED_TEMPLATE_CODE",
    "formula": "Amount × Rate",
    "computed_values": { "total": 110000000 }
  }
}
```

### Rules cho Combinatorial Data

| # | Rule |
|---|------|
| 1 | Dimension values PHẢI đúng 100% so với ma trận — KHÔNG random |
| 2 | Mỗi combo dùng data riêng (unique per combo) |
| 3 | Computed values phải đúng theo formula |
| 4 | Mỗi combo PHẢI có expected output |
| 5 | Traceable: prefix `auto_combo{XX}` |

### Workflow tham chiếu

- `/generate_cross_module_test_plan` → Sinh ma trận kết hợp (input cho skill này)
- `/generate_combinatorial_test_data` → Workflow chính dùng skill này cho combinatorial data

---

## Tham chiếu quy tắc

- `CLAUDE.md` — Mục 7: Test Data Rules
- `.claude/rules/testcase_design_rules.md` — Mục 2: Checklist kiểm thử theo loại trường (EP/BVA)