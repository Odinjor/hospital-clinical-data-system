import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="StarMan#4490",
        database="hospital_db"
    )
    
def execute_query(query, params=None, fetch=False):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    if fetch:
        result = cursor.fetchall()
    else:
        db.commit()
        result = None
    cursor.close()
    db.close()
    return result