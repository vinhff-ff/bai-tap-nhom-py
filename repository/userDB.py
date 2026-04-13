from utils.connectDB import get_connection
from res.users import Users

from utils.connectDB import get_connection
from res.users import Users

class UserDB:
    @staticmethod
    def getUser(username):
        conn = get_connection()
        cursor = conn.cursor()

        query = "SELECT id, username, password FROM users WHERE username = %s LIMIT 1"
        cursor.execute(query, (username,))

        result = cursor.fetchone()

        conn.close()

        if result:
            id, username, password = result

            return Users(id, username, password)

        return None
    
    def createUser(username, password):
        conn = get_connection()
        cursor = conn.cursor()

        if UserDB.getUser(username):
            return "Tài khoản này đã tồn tại"

        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, password))

        conn.commit()
        conn.close()

        return "Tạo tài khoản thành công"