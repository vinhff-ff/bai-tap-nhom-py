class Schedule:
    def __init__(self, id, user_id, work_date, start_time, end_time, title, note):
        self.__id = id
        self.__user_id = user_id
        self.__work_date = work_date
        self.__start_time = start_time
        self.__end_time = end_time
        self.__title = title
        self.__note = note

    def get_id(self):
        return self.__id

    def get_user_id(self):
        return self.__user_id

    def get_work_date(self):
        return self.__work_date

    def get_start_time(self):
        return self.__start_time

    def get_end_time(self):
        return self.__end_time

    def get_title(self):
        return self.__title

    def get_note(self):
        return self.__note
