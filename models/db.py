import mysql.connector

def get_db_connection():
    db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="StarMan#4490",
    database="hospital_db"
)
    return db