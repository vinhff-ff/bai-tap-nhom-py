class Users:
    def __init__(self, id, username, password):
        self.__id = id
        self.__username = username
        self.__password = password

    def get_id(self):
        return self.__id

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password