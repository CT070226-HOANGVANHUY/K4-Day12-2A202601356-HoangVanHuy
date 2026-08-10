# Phiếu Phản Ánh — K4 Ngày 12

> **Bài làm cá nhân.** Trả lời bằng lời của chính bạn, dựa trên những gì bạn
> quan sát được khi chạy code — không sao chép đáp án của người khác.
>
> Cách trả lời: thay phần đánh dấu bên dưới mỗi câu bằng câu trả lời.
> `grade.py` đếm số câu đã trả lời (15 điểm cho 10 câu).
>
> Họ và tên: Hoang Van Huy  Mã học viên: 2A202601356-HoangVanHuy

---

### Câu 1 — Fail fast (CP1)

Trong `Settings`, `api_token` không có giá trị mặc định nên app chết ngay khi
khởi động nếu thiếu biến môi trường. Hãy mô tả một tình huống cụ thể mà việc
"chết sớm" này cứu bạn, so với việc để mặc định `"changeme"`.

> Nếu staging quên đặt `API_TOKEN`, ứng dụng sẽ dừng ngay khi khởi động thay vì chạy
> với token công khai như `changeme`. Nhờ vậy mình phát hiện lỗi cấu hình trước khi
> service nhận traffic hoặc phát sinh chi phí. Nếu dùng mặc định, người biết token
> đó có thể gọi API trong lúc mình tưởng service đã được bảo vệ.

---

### Câu 2 — Log cho máy đọc (CP1)

Chạy service và gọi `/chat` vài lần. Dán một dòng log JSON bạn thu được, rồi
nêu **hai** việc bạn làm được với dòng log đó mà `print("đã trả lời xong")`
không làm được.

> Một dòng log mình quan sát được có dạng:
>
> ```json
> {"event":"chat_completed","severity":"INFO","ts":"2026-08-10T10:30:00+00:00","client_id":"exercise-check","prompt_tokens":2,"completion_tokens":34,"usd_cost":2.07e-05}
> ```
>
> Từ đó mình có thể lọc riêng các request của một client và cộng chi phí theo
> client/ngày. Mình cũng có thể thống kê token hoặc tạo cảnh báo khi một nhóm
> request có chi phí cao; `print("đã trả lời xong")` không có các trường dữ liệu
> để máy lọc và tổng hợp như vậy.

---

### Câu 3 — Kích thước image (CP2)

Build cả hai phiên bản và ghi lại số đo thật:

```bash
docker build -f <Dockerfile-1-stage> -t chat:single .
docker build -t chat:multi .
docker images | grep chat
```

| Bản | Dung lượng |
|-----|-----------|
| 1 stage (bản đầu) | 1.73GB |
| Multi-stage | 270MB |

Giải thích: bản một stage dùng base image `python:3.11` đầy đủ và giữ toàn bộ
môi trường cài đặt trong image cuối, nên riêng base image và các thành phần hệ
thống đã lớn. Bản multi-stage dùng `python:3.11-slim` ở runtime và chỉ copy
dependency đã cài từ builder, bỏ phần tool/build layer không cần khi chạy.

---

### Câu 4 — Thứ tự lệnh trong Dockerfile (CP2)

Sửa một ký tự trong `app/main.py` rồi build lại. Với Dockerfile của bạn, những
layer nào được dùng lại từ cache, layer nào phải chạy lại? Nếu bạn đặt
`COPY . .` lên trước `RUN pip install` thì kết quả khác thế nào?

> Khi chỉ sửa `app/main.py`, layer `COPY requirements.txt` và layer
> `pip install` ở builder được Docker dùng lại từ cache vì requirements không
> đổi. Các layer sau đó có `COPY app`/`COPY utils` và bước tạo user/chown phải
> chạy lại, nhưng không phải cài dependency lại. Nếu đặt `COPY . .` trước
> `RUN pip install`, thay đổi một dòng code cũng làm layer COPY đổi; Docker sẽ
> bỏ cache từ đó trở đi và chạy lại `pip install`, khiến build chậm hơn nhiều.

---

### Câu 5 — Vì sao không chạy bằng root (CP2)

Container mặc định chạy bằng root. Mô tả chuỗi sự kiện dẫn từ "một lỗ hổng
trong code Python của bạn" tới "kẻ tấn công có quyền cao trên máy host", và
lệnh `USER` cắt đứt chuỗi đó ở chỗ nào.

> Một lỗ hổng cho phép attacker chạy lệnh trong process Python. Nếu process chạy
> bằng root, attacker có quyền cao trong container: đọc/ghi file, cài công cụ,
> thay đổi cấu hình và khai thác thêm lỗ hổng của runtime hoặc Docker để tìm
> đường truy cập host. Nếu container thoát ra được, quyền root trong container
> có thể trở thành quyền root trên host. `USER appuser` làm process chỉ chạy với
> user thường, nên cắt quyền cao ngay từ bước đầu; nó không thay thế hoàn toàn
> sandbox nhưng làm giảm đáng kể hậu quả của một lỗi ứng dụng.

---

### Câu 6 — Bearer token (CP3)

Vì sao 401 phải kèm header `WWW-Authenticate: Bearer`? Và vì sao ta trả **cùng
một** thông báo lỗi cho cả ba trường hợp (thiếu header, sai scheme, sai token)
thay vì nói rõ sai ở đâu cho người dùng dễ sửa?

> `WWW-Authenticate: Bearer` là header chuẩn để server nói cho client biết
> resource yêu cầu cơ chế xác thực Bearer; client có thể dựa vào đó để biết
> cách gửi lại request. Ta dùng cùng một thông báo cho thiếu header, sai scheme
> và sai token để không biến response thành một "oracle" giúp attacker dò xem
> request của họ sai ở lớp nào. Người dùng hợp lệ vẫn biết cần gửi Bearer token,
> còn chi tiết xác thực không bị tiết lộ thêm.

---

### Câu 7 — Token bucket (CP3)

Với `capacity=10`, `refill_per_minute=10`: một client im lặng 10 phút rồi gửi
liên tiếp. Nó gửi được bao nhiêu request trước khi bị 429? Nếu bỏ đoạn
`min(capacity, ...)` trong `available()` thì con số đó thành bao nhiêu, và tại sao?

> Sau 10 phút, xô vẫn bị giới hạn ở `capacity=10`, nên client gửi được 10
> request liên tiếp rồi request tiếp theo nhận 429. Nếu bỏ `min(capacity, ...)`,
> 10 phút sẽ nạp thêm 100 token vào 10 token ban đầu, thành 110 token; client
> có thể gửi khoảng 110 request liên tiếp trước khi bị chặn. Điều đó phá vỡ
> giới hạn burst và có thể làm service hoặc ngân sách bị tiêu nhanh.

---

### Câu 8 — Ngân sách theo ngày (CP3)

So sánh hạn mức $30/tháng với hạn mức $1/ngày cho cùng một client. Giả sử có sự
cố khiến một client gọi liên tục từ 2h sáng. Với mỗi cách, thiệt hại tối đa là
bao nhiêu và service tự hồi phục khi nào?

> Với hạn mức 30 USD/tháng, nếu sự cố bắt đầu lúc 2h và chưa tiêu gì trước đó,
> client có thể làm thiệt hại gần 30 USD trong phần còn lại của tháng. Hạn mức
> chỉ hồi phục khi sang tháng mới. Với hạn mức 1 USD/ngày, thiệt hại tối đa của
> ngày đó là 1 USD và key chi tiêu được reset ở ngày UTC kế tiếp. Vì vậy budget
> theo ngày giới hạn phạm vi của sự cố nhỏ hơn rất nhiều và service tự hoạt động
> lại sau lần reset ngày.

---

### Câu 9 — /healthz khác /readyz (CP4)

Nếu gộp hai endpoint làm một và cho nó kiểm tra Redis, chuyện gì xảy ra với cụm
3 container khi Redis mất kết nối 30 giây? Trả lời theo đúng thứ tự sự kiện.

> Nếu gộp hai endpoint và endpoint đó kiểm tra Redis, khi Redis mất kết nối cả
> ba container đều báo unhealthy. Load balancer/orchestrator thấy cả cụm không
> healthy, lần lượt rút traffic rồi restart các container. Trong 30 giây Redis
> lỗi, các container mới vẫn kiểm tra cùng dependency đang chết nên có thể tiếp
> tục bị restart, làm gián đoạn request dù process Python thực tế vẫn còn sống.
> Tách `/healthz` và `/readyz` giúp `/healthz` vẫn 200 để tránh restart oan,
> còn `/readyz` 503 để load balancer tạm ngừng gửi traffic.

---

### Câu 10 — Deploy thật (CP5)

Ghi lại **một** lỗi bạn gặp khi deploy lên cloud (build fail, health check
timeout, sai REDIS_URL, app không đọc `$PORT`...): thông báo lỗi là gì, bạn
tìm ra nguyên nhân bằng cách nào, và sửa ra sao?

> Khi mở URL gốc `/`, trình duyệt nhận `404 {"detail":"Not Found"}`. Tôi
> kiểm tra các route trong `app/main.py` và xác định đây là API service chưa
> khai báo trang chủ, không phải lỗi Render; `/healthz`, `/readyz` và `/docs`
> vẫn lần lượt trả 200. Sau đó, lần gọi `/chat` đầu tiên còn trả câu mẫu của
> mock LLM vì `.env` trên máy không được upload lên Render. Tôi đặt
> `OPENAI_API_KEY` trong Render Dashboard và redeploy commit `9f8a7cd`.
> Kiểm tra lại bằng `Authorization: Bearer <API_TOKEN>` cho kết quả 200,
> có usage và chi phí OpenAI. CP5 hiện đạt 9/9 test public, phần bắt buộc
> đạt 100/100.
