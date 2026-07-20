import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()


class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        
        # Making the connection with mysql
        self.conn = mysql.connector.connect(
            host= self.host,
            user = self.user,
            password = self.password,
            database = self.database
        )

        self.cursor = self.conn.cursor(dictionary=True)
    
    # Checking the connection
    def check_connection(self):
        if self.conn.is_connected():
            print("Connection OK !")
        else:
            print("Connection Failed !!")

    # Single row data insertion function 
    def insert_single_row(self, therapist_name, sub_title, Bio, therapist_url, Specialty, style):
        query = """
                INSERT IGNORE INTO doctor_scraper.therapists_list
                ( therapist_name, sub_title, Bio, therapist_url, Specialty, style)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

        values = (therapist_name, sub_title, Bio, therapist_url, Specialty, style)
        self.cursor.execute(query, values)
        self.conn.commit()

    ## Insert many rows onec
    def inser_many_rows(self, data):
        query = """
            INSERT INTO doctor_scraper.therapists_list
                ( therapist_name, sub_title, Bio, therapist_url, Specialty, style)
                VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.cursor.executemany(query, data)
        self.conn.commit()

        print(f"{self.cursor.rowcount} rows inserted.")
    
    def close_connection(self):
        self.cursor.close()
        self.conn.close()


db = Database(
    host="localhost",
    user = "root",
    password = os.getenv("DATABASE_PASSWORD"),
    database = "doctor_scraper"
)

db.check_connection()

    
# db.insert_single_row("Hridhy", "Moharani", "Sourov's Love", "Farihatasmin@gmail.com", "Silent", "Angel")
db.close_connection()