from repository.userDB import UserDB

class RegisterService:
    @staticmethod
    def register_service(username, password):
        if UserDB.getUser(username):
            raise ValueError("Tài khoản này đã tồn tại")
        UserDB.createUser(username, password)