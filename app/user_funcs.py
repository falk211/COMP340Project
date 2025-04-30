import os
import string
import random
import time
import psycopg
from psycopg.rows import dict_row
from db_info import *


class UserFuncs:

    def __init__(self, db_filename="practice.db"):
        """Initialize the connection to the SQLite database located one directory above."""
        self.db_url = f"host=dbclass.rhodescs.org dbname=practice user={DBUSER} password={DBPASS}"



    def generate_unique_uid(self, cursor):
        while True:
            uid = random.randint(10000, 99999)
            cursor.execute("SELECT uid FROM users WHERE uid = %s", (uid,))
            if not cursor.fetchone():
                return uid


    def check_user_exists(self, uid):
        connection = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={'falwt-25'} password={'falwt-25'}")
        cursor = connection.cursor()
        cursor.execute('''SELECT  first_name FROM users WHERE uid = %s''', (uid,))
        result = cursor.fetchone()
        if result is None:
            return False
        connection.close()
        return True

    def add_user(self, first_name, last_name, email, hashed_password, user_type, is_handicap):
        try:
            connection = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={'falwt-25'} password={'falwt-25'}")
            cursor = connection.cursor()


            uid = self.generate_unique_uid(cursor)


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





    def get_all_colleges(self):
        connection = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={'falwt-25'} password={'falwt-25'}", row_factory=dict_row)
        cursor = connection.cursor()
        cursor.execute("SELECT colname, cname, state FROM college co join cities ci on co.cid = ci.cid")
        colleges = cursor.fetchall()
        connection.close()
        return colleges

    def get_user_noncolleges(self, uid):
        connection = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={'falwt-25'} password={'falwt-25'}")
        cursor = connection.cursor()
        cursor.execute("""SELECT co.colname, ci.cname, ci.state
            FROM college co
            JOIN cities ci ON co.cid = ci.cid
            WHERE NOT EXISTS (SELECT * FROM attending a WHERE a.uid = %s AND a.colname = co.colname AND a.cid = co.cid
            );""", (uid,))
        colleges = cursor.fetchall()
        connection.close()
        return colleges

    def get_user_colleges(self,uid):
        connection = psycopg.connect(
            f"host=dbclass.rhodescs.org dbname=practice user={'falwt-25'} password={'falwt-25'}")
        cursor = connection.cursor()
        cursor.execute("""SELECT co.colname, ci.cname, ci.state
                    FROM college co
                    JOIN cities ci ON co.cid = ci.cid
                    WHERE EXISTS (SELECT * FROM attending a WHERE a.uid = %s AND a.colname = co.colname AND a.cid = co.cid
                    );""", (uid,))
        colleges = cursor.fetchall()
        connection.close()
        return colleges


    def add_college(self, uid, college, city, state):
        connection = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={'falwt-25'} password={'falwt-25'}")
        cursor = connection.cursor()
        cursor.execute("SELECT cid FROM cities WHERE cname = %s AND state = %s", (city, state,))
        cid = cursor.fetchone()[0]
        cursor.execute("INSERT INTO attending (uid, colname, cid, state) VALUES (%s, %s, %s, %s)", (uid, college, cid, state,))
        connection.commit()
        cursor.execute("SELECT uid FROM attending where uid = %s and colname = %s", (uid,college,))
        result = cursor.fetchone()
        connection.close()
        if result is None:
            return False
        return True
    
    def check_is_admin(self, uid):
        try:
            connection = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={'falwt-25'} password={'falwt-25'}")
            cursor = connection.cursor()
            cursor.execute("SELECT is_admin FROM users WHERE uid = %s", (uid,))
            result = cursor.fetchone()
            connection.close()

            # Ensure the result is a boolean
            if result is not None:
                return result[0]  # Return the value of is_admin (True/False)
            return False  # Default to False if no record is found
        except Exception as e:
            print(f"Error in check_is_admin: {e}")
            return False  # Default to False in case of an error

    def get_user_statistics(self):
        try:
            connection = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={'falwt-25'} password={'falwt-25'}")
            cursor = connection.cursor()

            # Count users by user type
            cursor.execute("SELECT user_type, COUNT(*) FROM users GROUP BY user_type")
            user_types = cursor.fetchall()

            # Count users by handicap status
            cursor.execute("SELECT is_handicap, COUNT(*) FROM users GROUP BY is_handicap")
            handicap_status = cursor.fetchall()

            # Count users by college
            cursor.execute("SELECT colname, COUNT(*) FROM attending GROUP BY colname")
            colleges = cursor.fetchall()

            # Count global occupancy
            cursor.execute("SELECT COUNT(*) FILTER (WHERE is_occupied = TRUE) AS occupied, COUNT(*) FILTER (WHERE is_occupied = FALSE) AS unoccupied FROM spaces")
            global_occupancy = cursor.fetchall()

            # Count occupancy by college
            cursor.execute("SELECT college_lot.colname, COUNT(*) FILTER (WHERE spaces.is_occupied = TRUE) AS occupied_count FROM spaces JOIN lots ON spaces.lid = lots.lid JOIN college_lot ON lots.lid = college_lot.lid GROUP BY college_lot.colname ORDER BY occupied_count DESC")
    
            college_occupancy = cursor.fetchall()

            connection.close()
            return {
                "user_types": user_types,
                "handicap_status": handicap_status,
                "colleges": colleges,
                "global_occupancy": global_occupancy,
                "college_occupancy": college_occupancy,
            }
        except Exception as e:
            print(f"Error fetching statistics: {e}")
            return {}

    def remove_college(self,uid, college, city, state ):
        connection = psycopg.connect(
            f"host=dbclass.rhodescs.org dbname=practice user={'falwt-25'} password={'falwt-25'}")
        cursor = connection.cursor()
        cursor.execute("SELECT cid FROM cities WHERE cname = %s AND state = %s", (city, state,))
        cid = cursor.fetchone()[0]
        cursor.execute("DELETE FROM attending WHERE uid = %s AND colname = %s AND cid=%s AND state=%s ",
                       (uid, college, cid, state,))
        connection.commit()
        cursor.execute("SELECT uid FROM attending where uid = %s and colname = %s", (uid, college,))
        result = cursor.fetchone()
        connection.close()
        if result is None:
            return True
        return False
    
    def get_all_cities(self):
        connection = psycopg.connect(self.db_url)
        cursor = connection.cursor()
        cursor.execute("SELECT cid, cname, state FROM cities ORDER BY cname")
        return cursor.fetchall()

    def insert_college(self, colname, cid, num_students):
        connection = psycopg.connect(self.db_url)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO college (colname, cid, num_students) VALUES (%s, %s, %s)",
            (colname, cid, num_students)
        )
        connection.commit()
        connection.close()

    

if __name__ == '__main__':
    service = UserFuncs()




