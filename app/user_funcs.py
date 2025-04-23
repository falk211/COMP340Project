
import os
import string
import random
import time
import psycopg
from psycopg.rows import dict_row
from db_info import *


class UserFuncs:

    def __init__(self, db_filename="pico.db"):
        """Initialize the connection to the SQLite database located one directory above."""
        self.db_url = f"host=dbclass.rhodescs.org dbname=practice user={DBUSER} password={DBPASS}"

    ########################################
    ########## CREATING NEW USERS ##########
    ########################################

    def generate_unique_uid(self, cursor):
        while True:
            uid = random.randint(10000, 99999)
            # Check if the UID already exists in the database
            cursor.execute("SELECT 1 FROM users WHERE uid = %s", (uid,))
            if not cursor.fetchone():
                return uid


    def check_user_exists(self, uid):
        connection = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={'falwt-25'} password={'falwt-25'}")
        cursor = connection.cursor()
        cursor.execute("SELECT 1 FROM users WHERE uid = %s", (uid,))
        result = cursor.fetchone()
        connection.close()
        return result

    def add_user(self, first_name, last_name, email, hashed_password, user_type, is_handicap):
        try:
            connection = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={'falwt-25'} password={'falwt-25'}")
            cursor = connection.cursor()

            # Generate a unique UID
            uid = self.generate_unique_uid(cursor)

            # Insert the new user
            cursor.execute(
                "INSERT INTO users (uid, first_name, last_name, email, password, is_admin, user_type, is_handicap) VALUES (%s, %s, %s, %s, %s, False, %s, %s)",
                (uid, first_name, last_name, email, hashed_password, user_type, is_handicap,))

            connection.commit()
            print(f"User {email} added successfully with UID: {uid}")
            connection.close()
            return uid

        except Exception as e:
            print(f"Error adding user: {e}")

    def get_users(self):
        try:
            connection = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={'falwt-25'} password={'falwt-25'}")
            cursor = connection.cursor()

            cursor.execute("SELECT uid, first_name, last_name, uemail FROM users")

            names = cursor.fetchall()
            connection.close

            return names

        except Exception as e:
            print(f"Error fetching list of users: {e}")

    ##################################################
    ########## AUTHENTICATING CURRENT USERS ##########
    ##################################################

    def get_user_by_credentials(self, email, hashed_password):
        connection = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={'falwt-25'} password={'falwt-25'}")
        cursor = connection.cursor()

        cursor.execute("SELECT uid, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user:
            print(f"User not found in database: {email}")
            connection.close()
            return -1

        db_uid, db_password = user
        print(f"Database password hash: {db_password}")
        print(f"Provided password hash: {hashed_password}")

        if db_password == hashed_password:
            print(f"Password match: returning UID {db_uid}")
            connection.close()
            return db_uid
        else:
            print("Password mismatch")
            connection.close()
            return 0

    ##################################################
    ##########        ADMIN CHECK           ##########
    ##################################################
    def is_admin(self, uid):
        """Check if a user is an admin"""
        if not uid:
            return False

        try:
            connection = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={'falwt-25'} password={'falwt-25'}")
            cursor = connection.cursor()

            cursor.execute("SELECT is_admin FROM users WHERE uid = %s", (uid,))
            result = cursor.fetchone()

            is_admin = result[0]

            connection.close()
            return is_admin

        except Exception as e:
            print(f"Error checking admin status: {e}")
            return False




if __name__ == '__main__':
    service = UserFuncs()




