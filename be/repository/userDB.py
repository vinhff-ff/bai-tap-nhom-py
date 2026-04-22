from config.connectDB import get_connection
from res.users import Users

class UserDB:
    @staticmethod
    def getUser(username):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            query = "SELECT id, username, password, created_at FROM users WHERE username = %s LIMIT 1"
            cursor.execute(query, (username,))

            result = cursor.fetchone()
            if result:
                user_id, username, password, created_at = result
                return Users(user_id, username, password, created_at)
            return None
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def createUser(username, password):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(query, (username, password))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise RuntimeError(f"Lỗi database: {str(e)}")
        finally:
            cursor.close()
            conn.close()