import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="vinh1234",
        database="py_ck2"
    )
