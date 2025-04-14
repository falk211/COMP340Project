import psycopg
from app.db_info import *


def create_table():
    try:
        # Creating questions table
        conn = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={DBUSER} password={DBPASS}")
        print(f"Database: {conn.info.dbname}")
        print(f"User: {conn.info.user}")
        print(f"Host: {conn.info.host}")
        print(f"Port: {conn.info.port}")
        print(f"Backend PID: {conn.info.backend_pid}")
        print(f"Server version: {conn.info.server_version}")
        print(f"Default client encoding: {conn.info.encoding}")
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cities (
                cid SERIAL PRIMARY KEY,
                cname TEXT NOT NULL,
                state TEXT NOT NULL
            );""")

        conn.commit()
        print("cities table created successfully")


        # Creating True/False Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lots (
                lid serial PRIMARY KEY,
                num_handicap Integer NOT NULL,
                num_guest Integer NOT NULL,
                lot_name TEXT NOT NULL,
                num_faculty Integer NOT NULL,
                num_total Integer NOT NULL,
                num_students Integer NOT NULL
            );""")

        conn.commit()
        print("lots table created successfully")


        # Creating Multiple Choice Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                uid INTEGER PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL,
                is_admin boolean NOT NULL,
                user_type enum('student', 'faculty', 'guest') not null,
                is_handicap boolean NOT NULL,
                FOREIGN KEY (qid) REFERENCES questions(qid) ON DELETE CASCADE
            );""")

        conn.commit()
        print("users table created successfully")


        # Creating Code Blocks Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cars (
                year Integer NOT NULL,
                make TEXT NOT NULL,
                model TEXT NOT NULL,
                lplate TEXT NOT NULL,
                lstate TEXT NOT NULL,
                Primary KEY (lplate, state)
            );""")

        conn.commit()
        print("cars table created successfully")


        # Creating Free Response Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_car (
                Foreign Key (uid) references users (uid),
	            Foreign Key (lstate) references Car (lstate), 
	            Foreign Key (lplate) references Car(lplate),
                Primary key (uid,lstate,lplate))
            );""")

        conn.commit()
        print("user cars table created successfully")


        # Creating Coding Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS coding (
                qid INTEGER PRIMARY KEY,
                starter TEXT NOT NULL,
                testcases TEXT NOT NULL,
                correctcode TEXT NOT NULL,
                FOREIGN KEY (qid) REFERENCES questions(qid) ON DELETE CASCADE
            );""")

        conn.commit()


        ##############################################
        ##########  STORING USER RESPONSES  ##########
        ##############################################

        # User Responses Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_responses (
                uid TEXT NOT NULL,
                qid INTEGER NOT NULL,
                PRIMARY KEY (uid, qid)
            );""")

        conn.commit()
        print("user_response table created successfully")


        # User Response to Free Response
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_free_response (
                uid TEXT NOT NULL,
                qid INTEGER NOT NULL,
                uanswer TEXT NOT NULL,
                profanswer TEXT NOT NULL,
                PRIMARY KEY (uid, qid)
            );""")

        conn.commit()
        print("user free_response table created successfully")


        # User Response to Multiple Choice
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_multiple_choice (
                uid TEXT NOT NULL,
                qid INTEGER NOT NULL,
                response INTEGER NOT NULL,
                correct INTEGER CHECK (correct BETWEEN 1 AND 4),
                PRIMARY KEY (uid, qid)
            );""")

        conn.commit()
        print("user multiple_choice table created successfully")


        # User Response to Coding
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_coding (
                uid TEXT NOT NULL,
                qid INTEGER NOT NULL,
                usercode TEXT NOT NULL,
                compile_status TEXT NOT NULL,
                run_status TEXT NOT NULL,
                PRIMARY KEY (uid, qid)
            );""")

        conn.commit()
        print("user coding table created successfully")


        # User Response to Code Blocks
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_code_blocks (
                uid TEXT NOT NULL,
                qid INTEGER NOT NULL,
                submission TEXT NOT NULL,
                correct TEXT NOT NULL,
                PRIMARY KEY (uid, qid)
            );""")

        conn.commit()
        print("user_code_blocks table created successfully")


        # User Response to True/False
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_true_false (
                uid TEXT NOT NULL,
                qid INTEGER NOT NULL,
                response INTEGER NOT NULL,
                correct BOOLEAN NOT NULL,
                PRIMARY KEY (uid, qid)
            );""")

        conn.commit()
        print("user true false table created successfully")


        # Users Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                uid TEXT PRIMARY KEY,
                uname TEXT NOT NULL,
                uemail TEXT NOT NULL,
                upassword TEXT NOT NULL,
                ustreak INTEGER NOT NULL,
                ulastanswertime FLOAT NOT NULL,
                uincorrect INTEGER NOT NULL,
                ucorrect INTEGER NOT NULL,
                upoints INTEGER NOT NULL,
                uadmin INTEGER CHECK (uadmin BETWEEN 0 AND 1)
            );""")

        conn.commit()
        print("users table created successfully")


        # Question Analytics Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS question_analytics (
                id SERIAL PRIMARY KEY,
                qid INTEGER NOT NULL,
                uid TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_correct BOOLEAN NOT NULL
            );""")

        conn.commit()
        print("question_analytics table created successfully")


        conn.close()

    except Exception as e:
        print(f"Error creating table: {e}")


if __name__ == "__main__":
    create_table()
