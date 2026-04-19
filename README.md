Thứ nhất ko được nghịch vô Main.py !!! 
Thứ hai viết code trong repository để kết nối với cơ sở dũ liệu
Thứ ba viết res để định nghĩa kiểu trả về trong repository
Thứ tư viết services để sử lý logic
Thứ năm viết routes để sủ lý lỗi trả về
Thứ sáu viết định nghĩa đầu API trong __init__.py
Thứ bảy là hoàn thành !

Vi du tao task moi (POST /schedule/create):

Body JSON:
{
	"user_id": 1,
	"title": "Hoan thanh bai tap nhom",
	"description": "Lam phan Schedule module",
	"status": "pending",
	"deadline": "2026-04-25 18:00:00",
	"created_at": "2026-04-20 09:30:00",
	"is_overdue": false
}

Phan hoi thanh cong (vi du):
{
	"status": 201,
	"message": "Them task thanh cong",
	"task_id": 12
}
