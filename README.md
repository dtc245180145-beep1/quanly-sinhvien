
# Hệ thống Quản lý Sinh viên

## 1. Giới thiệu
Dự án xây dựng hệ thống quản lý sinh viên bằng Flask, MySQL và Docker Compose.

## 2. Chức năng
- Quản lý thông tin sinh viên.
- Quản lý lớp học.
- Quản lý điểm sinh viên.
- Lưu trữ dữ liệu bằng MySQL.
- Quản trị cơ sở dữ liệu bằng phpMyAdmin.

## 3. Công nghệ sử dụng
- Python, Flask, Gunicorn.
- MySQL.
- Docker và Docker Compose.
- Prometheus, Grafana, Loki và Promtail.
- Nginx.

## 4. Khởi chạy
Kiểm tra cấu hình bằng `docker-compose config`.

Khởi động dịch vụ bằng `docker-compose up -d --build`.

Kiểm tra dịch vụ bằng `docker-compose ps`.

## 5. Bảo mật
- Không đưa file `.env` chứa mật khẩu thật lên GitHub.
- Sử dụng biến môi trường để cấu hình kết nối.
- Kiểm tra HTTPS và các dịch vụ giám sát trước khi nghiệm thu.

## 6. Tác giả
Sinh viên thực hiện: Nguyễn Thị Huyền Trang

