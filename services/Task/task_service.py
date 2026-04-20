from repository.taskDB import TaskDB


class TaskService:
    @staticmethod
    def _build_task_response(task):
        return {
            "id": task.get_id(),
            "user_id": task.get_user_id(),
            "title": task.get_title(),
            "description": task.get_description(),
            "status": task.get_status(),
            "deadline": str(task.get_deadline()),
            "is_overdue": bool(task.get_is_overdue()),
            "created_at": str(task.get_created_at()) if task.get_created_at() else None,
            "updated_at": str(task.get_updated_at()) if task.get_updated_at() else None,
        }

    @staticmethod
    def _normalize_status(status):
        if not status:
            raise ValueError("Thieu status")

        normalized = status.strip().lower()
        allowed = {"pending", "in_progress", "completed"}
        if normalized not in allowed:
            raise ValueError("Trang thai khong hop le")
        return normalized

    @staticmethod
    def create_task(user_id, title, description, status, deadline, created_at, is_overdue=False):
        if not user_id or not title or not status or not deadline or not created_at:
            raise ValueError("Thieu du lieu bat buoc")

        normalized_status = TaskService._normalize_status(status)
        task_id = TaskDB.create_task(
            user_id,
            title,
            description or "",
            normalized_status,
            deadline,
            created_at,
            is_overdue,
        )
        return task_id

    @staticmethod
    def get_tasks(user_id):
        if not user_id:
            raise ValueError("Thieu user_id")

        tasks = TaskDB.get_tasks_by_user(user_id)
        result = []
        for task in tasks:
            result.append(TaskService._build_task_response(task))
        return result

    @staticmethod
    def update_task(task_id, user_id, title, description, status, deadline, is_overdue):
        if not task_id or not user_id or not title or not status or not deadline:
            raise ValueError("Thieu du lieu bat buoc")

        normalized_status = TaskService._normalize_status(status)
        if TaskDB.update_task(
            task_id,
            user_id,
            title,
            description or "",
            normalized_status,
            deadline,
            is_overdue,
        ) == 0:
            raise ValueError("Khong tim thay task hoac khong co quyen sua")
        return True

    @staticmethod
    def delete_task(task_id, user_id):
        if not task_id or not user_id:
            raise ValueError("Thieu du lieu bat buoc")

        if TaskDB.delete_task(task_id, user_id) == 0:
            raise ValueError("Khong tim thay task hoac khong co quyen xoa")

        return True

    '''============================================================================================================='''
    
    @staticmethod
    def get_tasks_by_status(user_id, status):
        if not user_id:
            raise ValueError("Thieu user_id")

        normalized_status = TaskService._normalize_status(status)
        tasks = TaskService.get_tasks(user_id)
        return [task for task in tasks if task["status"] == normalized_status]

    @staticmethod
    def get_overdue_tasks(user_id):
        if not user_id:
            raise ValueError("Thieu user_id")

        tasks = TaskService.get_tasks(user_id)
        return [task for task in tasks if task["is_overdue"]]

