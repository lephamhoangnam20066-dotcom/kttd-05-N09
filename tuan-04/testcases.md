# Test case kiểm thử đăng nhập

Website: https://the-internet.herokuapp.com/login

| Mã | Trường hợp | Dữ liệu | Bước thực hiện | Kết quả mong đợi |
|---|---|---|---|---|
| TC01 | Đăng nhập thành công | tomsmith / SuperSecretPassword! | Mở trang, nhập tài khoản, nhập mật khẩu, nhấn Login | Chuyển đến `/secure` và hiện `You logged into a secure area!` |
| TC02 | Sai mật khẩu | tomsmith / wrong-password | Thực hiện đăng nhập | Ở trang login, hiện `Your password is invalid!` |
| TC03 | Sai tên đăng nhập | wrong-user / SuperSecretPassword! | Thực hiện đăng nhập | Ở trang login, hiện `Your username is invalid!` |

**Lưu ý:** Đây là tài khoản công khai của website demo, không phải tài khoản cá nhân.
