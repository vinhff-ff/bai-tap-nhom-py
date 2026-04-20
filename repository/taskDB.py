from utils.connectDB import get_connection
from res.task import Task


class TaskDB:
    @staticmethod
    def create_task(user_id, title, description, status, deadline, created_at, is_overdue=False):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            query = """
                        INSERT INTO tasks (user_id, title, description, status, deadline, is_overdue, created_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
            cursor.execute(query, (user_id, title, description, status, deadline, int(bool(is_overdue)), created_at))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise RuntimeError(f"Lỗi database: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_task(user_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            query = """
                        SELECT id, user_id, title, description, status, deadline, is_overdue, created_at, updated_at
                        FROM tasks
                        WHERE user_id = %s
                        ORDER BY deadline ASC, created_at ASC
                    """
            cursor.execute(query, (user_id,))
            results = cursor.fetchall()

            tasks = []
            for row in results:
                tasks.append(
                    Task(
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                        row[4],
                        row[5],
                        row[6],
                        row[7],
                        row[8],
                    )
                )
            return tasks
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_task(task_id, user_id, title, description, status, deadline, is_overdue):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            update_query = """
                            UPDATE tasks
                            SET title = %s,
                                description = %s,
                                status = %s,
                                deadline = %s,
                                is_overdue = %s,
                                updated_at = NOW()
                            WHERE id = %s AND user_id = %s
                            """
            cursor.execute(
                update_query,
                (title, description, status, deadline, int(bool(is_overdue)), task_id, user_id),
            )
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise RuntimeError(f"Lỗi database: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_task(task_id, user_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            delete_query = """
                            DELETE FROM tasks
                            WHERE id = %s AND user_id = %s
                           """
            cursor.execute(delete_query, (task_id, user_id))
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise RuntimeError(f"Lỗi database: {str(e)}")
        finally:
            cursor.close()
            conn.close()
