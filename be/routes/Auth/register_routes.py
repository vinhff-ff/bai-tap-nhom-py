from services.Auth.register_service import RegisterService

def register_routes(request_body):
    username = request_body.get("username")
    password = request_body.get("password")
    if not username or not password:
        return {"status": 400, "message" : "Thiếu username hoặc password"}
    
    try:
        user = RegisterService.register_service(username, password)
        return {"status": 201, "message": "Đăng kí thành công"}
    except ValueError as e:
        return {"status": 401, "message": str(e)}