class Users:
    def __init__(self, user_id, username, password, created_at=None):
        self.__user_id = user_id
        self.__username = username
        self.__password = password
        self.__created_at = created_at

    def get_id(self):
        return self.__user_id

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_created_at(self):
        return self.__created_at