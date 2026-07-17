import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user = "root",
            password = os.getenv("DATABASE_PASSWORD"),
            database = "doctor_scraper"
        )
        if conn.is_connected():
            print("Connection OK!")
        return conn
    except Error as e:
        print(f"Connection failed ! : {e}")
        return None

conn = get_connection()


