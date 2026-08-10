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
| Public URL | https://day12-chat-y28x.onrender.com |
| Platform | Render |
| Ngày deploy | 2026-08-10 |
| Local URL | http://localhost:8000 |

## Trạng Thái

Service đã được triển khai public trên Render. Render đang chạy web service
`day12-chat` và Render Key Value `day12-chat-redis`.

## Biến Môi Trường Đã Set

Chỉ ghi tên biến, không ghi giá trị secret:

| Biến | Đã set | Ghi chú |
|------|--------|---------|
| `PORT` | Có | 8000 ở local, cloud tự gán khi deploy |
| `API_TOKEN` | Có | đọc từ `.env`, không lưu trong tài liệu |
| `REDIS_URL` | Có | Render Key Value tự cấp connection string |
| `BUCKET_CAPACITY` | Có | 10 |
| `REFILL_PER_MINUTE` | Có | 10 |
| `DAILY_BUDGET_USD` | Có | 1.0 |
| `LOG_LEVEL` | Có | INFO |

## Kết Quả Kiểm Tra Public

```text
GET https://day12-chat-y28x.onrender.com/healthz: 200 {"status":"ok"}
GET https://day12-chat-y28x.onrender.com/readyz: 200 {"status":"ready","redis":true}
POST /chat không có token: 401
```

## Ảnh Chụp Minh Chứng

- `screenshots/dashboard.png` — trang Swagger UI của service local.
- `screenshots/healthz.png` — kết quả endpoint `/healthz`.

## Cấu Hình Cloud Đã Chuẩn Bị

- Railway: `railway.toml`
- Render: `render.yaml`
- Docker image bind `0.0.0.0` và đọc biến `PORT`.

API_TOKEN được đặt trong Render Dashboard và không được ghi vào repository.
