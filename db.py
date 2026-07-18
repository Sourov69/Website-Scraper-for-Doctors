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


def insert_product(therapist_name, sub_title, Bio, therapist_url, Specialty, style):
    conn = get_connection()
    cusror = conn.cursor()

    query = """
            INSERT IGNORE INTO doctor_scraper.therapists_list
            ( therapist_name, sub_title, Bio, therapist_url, Specialty, style)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

    values = (therapist_name, sub_title, Bio, therapist_url, Specialty, style)
    cusror.execute(query, values)
    conn.commit()
    cusror.close()
    conn.close()

insert_product("Mr Sourov", "Engineer", "Hey i am sourov", "https://sourovtalukder.com", "Data Science", "Pro")


    

