from services.Auth.login_service import LoginService

def login_routes(request_body):
    username = request_body.get("username")
    password = request_body.get("password")

    if not username or not password:
        return {"status": 400, "message": "Thiếu username hoặc password"}

    try:
        username, user_id = LoginService.login_service(username, password)
        return {"status": 200, "message": "Đăng nhập thành công", "username": username, "id": user_id}
    except ValueError as e:
        return {"status": 401, "message": str(e)}