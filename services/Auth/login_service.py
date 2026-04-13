from repository.userDB import UserDB

class LoginService:
    @staticmethod
    def login_service(username, password):
        user = UserDB.getUser(username)
        if not user:
            raise ValueError("Sai tài khoản hoặc mật khẩu")
        if user.get_password() != password:
            raise ValueError("Sai tài khoản hoặc mật khẩu") 
        return user.get_username() 