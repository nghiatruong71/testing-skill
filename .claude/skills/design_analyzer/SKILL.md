---
name: design_analyzer
description: Phân tích thiết kế (mockup, screenshot, wireframe; Figma cần Figma MCP) để trích xuất UI components, layout, trường dữ liệu, trạng thái UX và phát hiện rủi ro/lệch pha so với PRD. Dùng khi user gửi ảnh giao diện hoặc yêu cầu "phân tích thiết kế", "review UI/UX", "so sánh design với PRD".
---

# Kỹ năng Phân tích Thiết kế (UI/UX Design Analyzer)

## 1. Mô tả
Kỹ năng này cung cấp các nguyên tắc, quy trình và biểu mẫu chuẩn giúp AI (Claude) phân tích chuyên sâu các bản thiết kế (Figma, Mockup, Wireframe, Screenshot) nhằm phục vụ đắc lực cho công việc của QA, Tester và Developer. 

Mục tiêu chính là **phát hiện sớm lỗi thiết kế (Design Defect), kiểm tra tính khả dụng kiểm thử (Testability), trích xuất đặc tả UI/UX và đối chiếu với tài liệu yêu cầu (PRD/User Story)** để đảm bảo sản phẩm được build chính xác nhất.

---

## 2. Khi nào sử dụng

### ✅ Nên sử dụng khi:
- Người dùng cung cấp ảnh chụp màn hình (Screenshot), mockup UI hoặc đường dẫn Figma và yêu cầu "phân tích thiết kế", "review UI/UX".
- Cần đối chiếu, so sánh sự nhất quán giữa tài liệu yêu cầu (PRD/Jira ticket) với giao diện thiết kế thực tế.
- Cần lập bản đồ thành phần giao diện (UI elements mapping) phục vụ cho Automation Testing (xác định locators) hoặc Manual Testing (thiết kế test case giao diện).
- Cần chuẩn bị kịch bản kiểm thử giao diện (UI/UX Testing, Responsive Testing, Accessibility).

### ❌ KHÔNG sử dụng khi:
- Chỉ phân tích tài liệu dạng văn bản đơn thuần mà không có hình ảnh/giao diện thiết kế kèm theo (sử dụng skill `requirements_analyzer`).
- Mục tiêu chính là viết test cases chi tiết ngay lập tức (sử dụng skill `rbt_manual_testing` hoặc `/generate_testcases_from_requirements`).
- Cần sinh mã nguồn tự động hoặc viết kịch bản kiểm thử tự động (Automation Test Script).

---

## 3. Quy trình Phân tích Thiết kế (6 Bước)

Quy trình phân tích thiết kế được thực hiện tuần tự để tránh bỏ sót chi tiết:

### Bước 1: Khám phá Tổng quan Giao diện (Layout & Structure Analysis)
- **Phân vùng giao diện:** Chia nhỏ thiết kế thành các khu vực lớn như Header, Navigation Bar, Sidebar, Main Content Area, Footer, Drawer (Menu kéo), Modals (Popup), Floating Buttons.
- **Bố cục & Grid:** Xác định kiểu layout (Single column, Two-column, Grid, Flexbox, Fixed width, Full width).
- **Responsive Behavior:** Đánh giá hành vi co giãn của giao diện trên các kích thước màn hình khác nhau (Mobile, Tablet, Desktop) dựa trên thiết kế được cung cấp.

### Bước 2: Bản đồ Thành phần & Trường dữ liệu (UI Component & Field Mapping)
Lập bảng kê chi tiết toàn bộ các thành phần tương tác (interactive elements) có mặt trên thiết kế:
- **Tên trường/Thành phần (Label/Name):** Nhãn hiển thị của trường.
- **Loại UI (UI Component Type):** Text Input, Password, Select/Dropdown, Multi-select, Date Picker, Checkbox, Radio Button, Toggle Switch, Button, Tooltip, Tab, File Uploader...
- **Thuộc tính hiển thị mặc định:** Trạng thái mặc định (Default value), gợi ý nhập liệu (Placeholder text).
- **Quy tắc Validation (nếu hiển thị trên UI):** Ký tự bắt buộc (dấu sao đỏ `*`), định dạng hiển thị, độ dài giới hạn được gợi ý.

### Bước 3: Phân tích Trạng thái Thành phần (Component States Analysis)
Mỗi thành phần UI cần được phân tích đầy đủ các trạng thái tương tác để Developer và Tester nắm rõ:
1. **Default/Normal:** Trạng thái bình thường khi chưa tương tác.
2. **Hover:** Trạng thái khi di chuột qua (chỉ dành cho Web/Desktop).
3. **Focus:** Trạng thái khi click chuột hoặc dùng phím Tab di chuyển vào trường nhập liệu.
4. **Active/Pressed:** Trạng thái khi đang click giữ chuột hoặc chạm tay (Tap).
5. **Disabled:** Trạng thái bị khóa không cho tương tác.
6. **Selected/Checked:** Trạng thái được chọn (áp dụng cho Checkbox, Radio, Dropdown option).
7. **Loading:** Trạng thái đang tải dữ liệu (ví dụ nút Submit xoay vòng tròn).
8. **Error/Validation:** Trạng thái khi nhập sai dữ liệu (border đỏ, xuất hiện dòng text báo lỗi).
9. **Empty State:** Trạng thái khi màn hình/danh sách chưa có dữ liệu hiển thị.

### Bước 4: Luồng Tương tác & Điều hướng (UX Interaction & Navigation)
- **Luồng chuyển trang:** Nhấp vào nút/link nào thì điều hướng đi đâu?
- **Hành vi Popup/Modal:** Khi nào Modal xuất hiện? Nút đóng (Close/X/Cancel) hoạt động như thế nào? Bấm ra ngoài vùng Modal (overlay) có tắt modal hay không?
- **Thông báo phản hồi (Toasts/Banners/Dialogs):** Các thông báo thành công (Success toast), thông báo lỗi (Error banner) xuất hiện ở đâu, tồn tại trong bao lâu, và có nút đóng hay tự tắt?

### Bước 5: Đối chiếu Thiết kế với Tài liệu (Design-PRD Gap Analysis)
Tìm kiếm và ghi nhận tất cả điểm lệch pha (Inconsistencies) giữa thiết kế trực quan và tài liệu nghiệp vụ (PRD/User Story/Jira Ticket):
- **Trường dữ liệu thừa/thiếu:** PRD yêu cầu nhập Trường A nhưng thiết kế không có; hoặc thiết kế vẽ thêm Trường B nhưng PRD không mô tả.
- **Sai lệch nhãn/tên gọi:** Nhãn trên thiết kế khác với mô tả trong PRD (ví dụ: PRD ghi là "Mã khách hàng", thiết kế ghi "Mã định danh").
- **Mâu thuẫn logic nghiệp vụ:** PRD yêu cầu nút Submit bị disabled khi chưa nhập đủ, nhưng thiết kế lại vẽ nút Submit active bình thường.

### Bước 6: Phát hiện Điểm Mơ Hồ & Rủi Ro Thiết Kế (UI/UX Ambiguities & Testing Risks)
Đóng vai trò QA để "bới lông tìm vết" những trường hợp thiết kế bị thiếu hoặc không tối ưu:
- **Thiếu thiết kế Edge Cases:** Không có thiết kế cho trường hợp mất mạng (Offline), lỗi kết nối API (API Error), dữ liệu trống (Empty State).
- **Rủi ro về dữ liệu thực tế (Data Overflow):** Text quá dài hiển thị trên thiết kế như thế nào? (Có bị tràn, xuống dòng làm vỡ khung, hay bị cắt bớt bằng dấu ba chấm `...` và hiển thị tooltip?).
- **Vấn đề khả dụng (Accessibility - WCAG):** Độ tương phản màu sắc giữa text và nền có đạt chuẩn không? Kích thước vùng click của button trên Mobile có đủ lớn (tối thiểu 44x44px) để dễ tap không?
- **Rủi ro về vị trí (UI Overlap):** Các nút FAB (nút nổi), menu sticky có che khuất các nút tương tác khác khi scroll trang không?

---

## 4. Cấu trúc Tài liệu Phân Tích Thiết Kế Đầu Ra (Output Template)

Khi thực hiện phân tích thiết kế, kết quả đầu ra **bắt buộc** phải được lưu thành một **file Markdown** (đường dẫn: `output/<module>/<YYYY-MM-DD>/design_analysis_<feature_name>.md`) tuân thủ cấu trúc sau:

```markdown
# 🎨 Phân Tích Thiết Kế UI/UX: [Tên Màn Hình/Tính Năng]
## Design Analysis Report

## 1. Tổng Quan & Cấu Trúc Layout
- **Đường dẫn/Nguồn thiết kế:** [Figma Link / Tên file ảnh]
- **Mục tiêu màn hình:** (Màn hình này dùng làm gì?)
- **Cấu trúc phân vùng chính:**
  - Header: (Các phần tử trong Header)
  - Main Content: (Bố cục nội dung chính)
  - Modals/Drawers kèm theo: (Nếu có)

## 2. Bản Đồ Thành Phần Giao Diện (UI Elements Map)
| STT | Tên Trường (Label) | Loại UI | Trạng Thái Mặc Định | Validation Rules Hiển Thị | Ghi Chú |
|---|---|---|---|---|---|
| 1 | Email | Text Input | Placeholder: "nhập email..." | Bắt buộc (Có dấu * đỏ) | |
| 2 | Đăng Ký | Button | Active | N/A | |

## 3. Đặc Tả Trạng Thái Tương Tác (UX States)
- **Trạng thái Nút/Input:**
  - Mặc định: ...
  - Hover / Focus: ...
  - Disabled: (Khi nào bị disabled?)
  - Loading: (Hiển thị ra sao khi chờ xử lý?)
  - Error: (Màu sắc, vị trí hiển thị text báo lỗi khi validation fail)
- **Trạng thái Trang/Danh sách:**
  - Trạng thái rỗng (Empty State): ...
  - Trạng thái lỗi (Error/Offline State): ...

## 4. Điểm Lệch Pha Giữa Thiết Kế Và PRD (Design-PRD Gap Analysis)
| Mã Gap | Chi tiết sai lệch | Nguồn PRD | Nguồn Thiết kế | Đề xuất xử lý |
|---|---|---|---|---|
| **GAP-01** | Thiếu nút "Hủy bỏ" trên popup xác nhận xóa | PRD mục 3.2 yêu cầu có nút Cancel | Thiết kế chỉ vẽ nút Delete | Thêm nút Cancel màu xám cạnh nút Delete |

## 5. Điểm Mơ Hồ & Rủi Ro UI/UX (Ambiguities & Risks)
### 5.1. Điểm Mơ Hồ (UI Ambiguities)
| Mã | Câu hỏi / Vấn đề cần làm rõ | Nguy cơ / Ảnh hưởng | Mức độ (High/Medium/Low) |
|---|---|---|---|
| **AMB-UI-01** | Khi nội dung tên sản phẩm quá dài (trên 100 ký tự) | UI bị tràn dòng gây vỡ layout thẻ sản phẩm | 🟡 Medium |
| **AMB-UI-02** | Hành vi khi click ra ngoài vùng Modal (Overlay click) | Người dùng vô tình tắt Modal khi đang nhập form dở dang gây mất dữ liệu | 🔴 High |

### 5.2. Rủi Ro Kiểm Thử UI/UX (Testing Risks)
- **RISK-UI-01 [Responsive Collision]:** Thiết kế layout dạng 4 cột trên desktop có thể bị bóp nghẹt trên các màn hình có độ phân giải thấp (1024px) dẫn đến các text bị đè lên nhau.
- **RISK-UI-02 [Loading State Lack]:** Thiếu màn hình skeleton/loading khi tải danh sách sản phẩm lớn từ API có thể khiến người dùng tưởng ứng dụng bị đơ và click liên tục.

## 6. Khuyến Nghị Cho Kiểm Thử UI/UX (QA Test Recommendations)
*(Liệt kê các vùng cần tập trung test kỹ, ví dụ: kiểm tra responsive, kiểm tra độ tương phản màu sắc, kiểm tra khả năng tương tác phím tab, kiểm tra độ dài dữ liệu, kiểm tra hiển thị khi zoom 200%,...)*
```

---

## 5. Quy Tắc Vàng (Strict Rules)
1. **Luôn viết bằng Tiếng Việt.**
2. **Không tự suy diễn thiết kế:** Nếu không có màn hình mô tả hoặc thiết kế cho một trạng thái cụ thể, **bắt buộc** phải đưa vào mục **"Điểm Mơ Hồ (Ambiguities)"** dưới dạng câu hỏi làm rõ. Không được tự ý đưa ra giả định ngầm mà không có ghi chú rõ ràng.
3. **Phân tích chi tiết kích thước & khoảng cách khi cần thiết:** Đối với các giao diện mobile app, cần đặc biệt lưu ý kiểm tra khoảng cách an toàn (Safe Area) ở tai thỏ (Notch) và thanh điều hướng dưới cùng của OS (Home Indicator).
4. **Nhất quán mã định danh:** Các lỗi lệch pha đánh mã `GAP-XX`, các điểm mơ hồ thiết kế đánh mã `AMB-UI-XX`, rủi ro kiểm thử giao diện đánh mã `RISK-UI-XX`.
