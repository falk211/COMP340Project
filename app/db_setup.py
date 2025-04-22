import psycopg
from db_info import *


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
            CREATE TABLE IF NOT EXISTS attending (
                Foreign Key (uid) references users (uid),
                Foreign Key (state) references cities(state),
                Foreign Key (cid) references cities(cid),
                Primary Key (uid, state, cid)
            );""")

        conn.commit()
        print('attending table created successfully')

        # User Responses Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS college_lot (
                Foreign key (lid) references lots(lid)
	            Foreign key (colname) references college(colname),
	            Foreign Key (cid) references cities(cid), 
	            Primary key(lid))

            );""")

        conn.commit()
        print("college lot table created successfully")


        # User Response to Free Response
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS parking (
                Foreign key (uid) references Users(uid),
	            Foreign key (lid) references Lots(lid),
                Foreign key (snum) references Parking(snum),
	            time_in datetime Not Null
	            time_out datetime Not Null
	            Primary key(uid,lid,snum,time_in,time_out)

            );""")

        conn.commit()
        print("parking table created successfully")


        # User Response to Multiple Choice
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS spaces (
                space_num Integer not null,
	            car_restrictions enum('electric', 'compact', 'regular') not null,
	            user_restiction enum('student', 'faculty', 'guest')  not null,
	            is_handicap bool Not Null, 
	            is_occupied bool Not Null,
	            Foreign Key (lid) references Lots(lid)
                Primary Key (space_num, lid))

            );""")

        conn.commit()
        print("spaces table created successfully")


        # User Response to Coding
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS college (
                colname TEXT not null,
	            Foreign Key (cid) references cities (cid),
	            Num_students Integer Not Null,
	            Primary Key (colname, cid))

            );""")

        conn.commit()
        print("college created successfully")



        conn.close()

    except Exception as e:
        print(f"Error creating table: {e}")


if __name__ == "__main__":
    create_table()
