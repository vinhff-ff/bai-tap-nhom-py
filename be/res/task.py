class Task:
    def __init__(
        self,
        task_id,
        user_id,
        title,
        description,
        status,
        deadline,
        is_overdue,
        created_at=None,
        updated_at=None,
    ):
        self.__task_id = task_id
        self.__user_id = user_id
        self.__title = title
        self.__description = description
        self.__status = status
        self.__deadline = deadline
        self.__is_overdue = is_overdue
        self.__created_at = created_at
        self.__updated_at = updated_at

    def get_id(self):
        return self.__task_id

    def get_user_id(self):
        return self.__user_id

    def get_title(self):
        return self.__title

    def get_description(self):
        return self.__description

    def get_status(self):
        return self.__status

    def get_deadline(self):
        return self.__deadline

    def get_is_overdue(self):
        return self.__is_overdue

    def get_created_at(self):
        return self.__created_at

    def get_updated_at(self):
        return self.__updated_at
