# Thông Tin Deploy — Checkpoint 5

## Thông Tin Học Viên

| Mục | Nội dung |
|-----|----------|
| Họ và tên | Học viên |
| Mã học viên | 2A202601356-HoangVanHuy |
| Repo | K4-Day12-Cloud-Services-And-Deployment |

## Service

| Mục | Nội dung |
|-----|----------|
| Public URL | Chưa triển khai public |
| Platform | Docker Compose local fallback; cấu hình Railway và Render đã có sẵn |
| Ngày deploy | 2026-08-10 |
| Local URL | http://localhost:8000 |

## Trạng Thái

Máy hiện dùng phương án dự phòng `LOCAL_FALLBACK=true` vì chưa có tài khoản hoặc
quyền truy cập cloud để triển khai public. Docker Compose đang chạy hai service
`chat` và `redis`, cả hai đều healthy.

## Biến Môi Trường Đã Set

Chỉ ghi tên biến, không ghi giá trị secret:

| Biến | Đã set | Ghi chú |
|------|--------|---------|
| `PORT` | Có | 8000 ở local, cloud tự gán khi deploy |
| `API_TOKEN` | Có | đọc từ `.env`, không lưu trong tài liệu |
| `REDIS_URL` | Có | `redis://redis:6379/0` trong Compose |
| `BUCKET_CAPACITY` | Có | 10 |
| `REFILL_PER_MINUTE` | Có | 10 |
| `DAILY_BUDGET_USD` | Có | 1.0 |
| `LOG_LEVEL` | Có | INFO |

## Kết Quả Kiểm Tra Local

```text
docker compose ps: chat healthy, redis healthy
GET /healthz: 200 {"status":"ok"}
GET /readyz: 200 {"status":"ready","redis":true}
POST /chat không có token: 401
POST /chat có token: 200
Docker image: 270MB
```

## Ảnh Chụp Minh Chứng

- `screenshots/dashboard.png` — trang Swagger UI của service local.
- `screenshots/healthz.png` — kết quả endpoint `/healthz`.

## Cấu Hình Cloud Đã Chuẩn Bị

- Railway: `railway.toml`
- Render: `render.yaml`
- Docker image bind `0.0.0.0` và đọc biến `PORT`.

Khi có tài khoản cloud, chỉ cần tạo service từ repository, đặt các biến môi
trường ở trên trong dashboard, tạo Redis managed service, rồi thay Public URL
và kết quả kiểm tra bằng URL public thật.
