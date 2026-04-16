from utils.connectDB import get_connection
from res.schedule import Schedule

class ScheduleDB:
    @staticmethod
    def create_schedule(user_id, work_date, start_time, end_time, title, note):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            query = """
                        INSERT INTO schedules (user_id, work_date, start_time, end_time, title, note)
                        VALUES(%s, %s, %s, %s, %s, %s)
                    """
            cursor.execute(query, (user_id, work_date, start_time, end_time, title, note))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise RuntimeError(f"Lỗi database: {str(e)}")
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_schedules_by_user(user_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            query = """
                        SELECT id, user_id, work_date, start_time, end_time, title, note
                        FROM schedules
                        WHERE user_id = %s
                        ORDER BY work_date ASC, start_time ASC 
                    """
            cursor.execute(query, (user_id,))
            results = cursor.fetchall()

            ds = []
            for row in results:
                ds.append(
                    Schedule(
                        row[0], row[1], row[2], row[3], row[4], row[5], row[6]
                    )
                )
            return ds
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def has_conflict(user_id, work_date, start_time, end_time):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            query = """
                        SELECT id
                        FROM schedules
                        WHERE user_id = %s
                          AND work_date = %s
                          AND start_time < %s
                          AND end_time > %s
                        LIMIT 1
                    """
            cursor.execute(query, (user_id, work_date, end_time, start_time))
            result = cursor.fetchone()
            return result is not None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def has_conflict_excluding_id(schedule_id, user_id, work_date, start_time, end_time):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            query = """
                        SELECT id
                        FROM schedules
                        WHERE user_id = %s
                          AND work_date = %s
                          AND start_time < %s
                          AND end_time > %s
                          AND id <> %s
                        LIMIT 1
                    """
            cursor.execute(query, (user_id, work_date, end_time, start_time, schedule_id))
            result = cursor.fetchone()
            return result is not None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_schedule(schedule_id,user_id, work_date, start_time, end_time, title, note):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            update_query = """
                            UPDATE schedules
                            set work_date = %s,
                                start_time = %s,
                                end_time = %s,
                                title = %s,
                                note = %s
                            WHERE id = %s AND user_id = %s

                            """
            cursor.execute(update_query, (work_date, start_time, end_time, title, note, schedule_id, user_id))
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise RuntimeError(f"Lỗi database: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_schedule(schedule_id, user_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            delete_query = """
                            DELETE FROM schedules
                            WHERE id = %s AND user_id = %s
                           """
            cursor.execute(delete_query, (schedule_id, user_id))
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise RuntimeError(f"Lỗi database: {str(e)}")
        finally:
            cursor.close()
            conn.close()
