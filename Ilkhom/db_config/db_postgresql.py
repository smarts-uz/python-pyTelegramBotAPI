import psycopg2 as sql
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")


class Database:
    def __init__(self):
        self.db = sql.connect(
            database=DB_NAME,
            host=DB_HOST,
            password=DB_PASS,
            user=DB_USER,
            port=5432
        )
        self.cursor = self.db.cursor()

# Execute a command: create user_info table
    def create_user_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS user_info(
            user_id SERIAL PRIMARY KEY UNIQUE NOT NULL,
            user_name VARCHAR (50) NOT NULL,
            user_age VARCHAR (10) NOT NULL,
            user_sex VARCHAR (20) NOT NULL
            )"""
        self.execute(sql, commit=True)

    def insert_user(self, user_id, user_name, user_age, user_sex):
        sql = """
        INSERT INTO user_info(user_id, user_name, user_age, user_sex)
        VALUES(%s, %s, %s, %s)
        """
        self.execute(sql, user_id, user_name, user_age, user_sex, commit=True)

    def check_user_id(self, user_id):
        sql = """
        SELECT user_id FROM user_info 
        WHERE user_id = %s
        """
        return self.execute(sql, user_id, fetchone=True)

    def execute(self, sql, *args,
            fetchone: bool = False,
            fetchall: bool = False,
            fetchmany: bool = False,
            commit: bool = False):
        self.cursor.execute(sql, args)
        if commit:
            self.db.commit()
        if fetchone:
            self.cursor.fetchone()
        elif fetchall:
            self.cursor.fetchall()
        elif fetchmany:
            self.cursor.fetchmany()

    def close_db(self):
        self.db.close()

    def check_db(self):
        return self.cursor.closed

