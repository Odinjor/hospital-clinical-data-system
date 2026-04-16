import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="StarMan#4490",
        db="hospital_db",
        autocommit=True
    )

def execute_query(query, params=None, fetch=False):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    result = None
    if fetch:
        result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result
