Thứ nhất ko được nghịch vô Main.py !!! 
Thứ hai viết code trong repository để kết nối với cơ sở dũ liệu
Thứ ba viết res để định nghĩa kiểu trả về trong repository
Thứ tư viết services để sử lý logic
Thứ năm viết routes để sủ lý lỗi trả về
Thứ sáu viết định nghĩa đầu API trong __init__.py
Thứ bảy là hoàn thành !

Vi du tao task moi (POST /schedule/create):

Body JSON:
Curl commands for Postman (Import -> Raw text)
Base URL: http://localhost:8000

Register
curl --location 'http://localhost:8000/register' \
--header 'Content-Type: application/json' \
--data '{
  "username": "test_user",
  "password": "123456"
}'

Login
curl --location 'http://localhost:8000/login' \
--header 'Content-Type: application/json' \
--data '{
  "username": "test_user",
  "password": "123456"
}'

Create task (/schedule/create)
curl --location 'http://localhost:8000/schedule/create' \
--header 'Content-Type: application/json' \
--data '{
  "user_id": 1,
  "title": "Learn Python",
  "description": "Practice API testing",
  "status": "pending",
  "deadline": "2026-04-30 23:59:59",
  "created_at": "2026-04-21 10:00:00",
  "is_overdue": false
}'

List tasks
curl --location 'http://localhost:8000/schedule/list' \
--header 'Content-Type: application/json' \
--data '{
  "user_id": 1
}'

Update task
curl --location 'http://localhost:8000/schedule/update' \
--header 'Content-Type: application/json' \
--data '{
  "task_id": 1,
  "user_id": 1,
  "title": "Learn Python Advanced",
  "description": "Update task content",
  "status": "in_progress",
  "deadline": "2026-05-01 23:59:59",
  "is_overdue": false
}'

Delete task
curl --location 'http://localhost:8000/schedule/delete' \
--header 'Content-Type: application/json' \
--data '{
  "task_id": 1,
  "user_id": 1
}'

List tasks by status
curl --location 'http://localhost:8000/schedule/list-by-status' \
--header 'Content-Type: application/json' \
--data '{
  "user_id": 1,
  "status": "pending"
}'

Overdue tasks
curl --location 'http://localhost:8000/schedule/overdue' \
--header 'Content-Type: application/json' \
--data '{
  "user_id": 1
}'
