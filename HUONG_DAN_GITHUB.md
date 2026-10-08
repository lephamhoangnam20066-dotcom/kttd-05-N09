# Hướng dẫn đưa bài lên GitHub – Nhóm N09

Repo: https://github.com/lephamhoangnam20066-dotcom/kttd-05-N09

## 1. Tạo Issue trên GitHub
Issues → New issue. Title: `T04 - Thực hành kiểm thử đăng nhập bằng Selenium`.
Description: Viết ba test case đăng nhập, chạy pytest, lưu ảnh, ghi chú. Giao cho chính bạn. Ghi lại số Issue (ví dụ #1).

## 2. Tải repo và tạo nhánh riêng (PowerShell)
```powershell
git clone https://github.com/lephamhoangnam20066-dotcom/kttd-05-N09.git
cd kttd-05-N09
git fetch origin
git switch Tuan-04
git pull origin Tuan-04
git switch -c t04-nam
```
Sao chép các file trong gói bài tập vào thư mục clone, giữ nguyên `.git` của repo đã clone. **Không** sao chép đè thư mục `.git`.

## 3. Hai commit minh họa
```powershell
git add requirements.txt README.md .gitignore tuan-04/testcases.md tuan-04/notes.md tuan-04/anh/README.md
git commit -m "T04: them test case va tai lieu"
git add tuan-04/test_login.py .github/pull_request_template.md HUONG_DAN_GITHUB.md
git commit -m "T04: them ba bai kiem thu Selenium"
git push -u origin t04-nam
```
Nếu file đã có hoặc bạn thay đổi cách chia commit, dùng `git status` để kiểm tra trước mỗi commit.

## 4. Pull Request từ nhánh cá nhân vào nhánh tuần
Trên GitHub: Pull requests → New pull request → base: `Tuan-04`, compare: `t04-nam`. Điền số Issue thực tế thay cho `#__` và mô tả cách chạy. Tự kiểm tra trước khi merge; nhóm một người không thể tự cung cấp reviewer độc lập.

## 5. Pull Request từ nhánh tuần vào main
Sau khi gộp PR đầu, tạo PR thứ hai: base `main`, compare `Tuan-04`. Kiểm tra lại file và kết quả chạy rồi merge. Giữ nhánh tuần theo tài liệu của cô.

## 6. Xử lý lỗi phổ biến
- 403: kiểm tra đăng nhập đúng tài khoản GitHub.
- Push bị từ chối: fetch/pull và giải quyết khác biệt trước khi push.
- PR nhầm base: sửa base về `Tuan-04`.
- Conflict: mở file, giữ nội dung đúng, xóa các dấu xung đột, commit rồi push.

**Lưu ý:** Đây là bộ bài chuẩn bị, không có kết quả PASS được xác nhận. Cần tự chạy Selenium trên máy trước khi nộp.
