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
        #cursor.execute("Create type user_type as enum('student', 'faculty', 'guest');")
        #conn.commit()
       # cursor.execute("create type car_restrictions as enum('electric', 'compact', 'regular');")
       # conn.commit()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cities (
                cid SERIAL PRIMARY KEY,
                cname TEXT NOT NULL,
                state TEXT NOT NULL
            );""")

        conn.commit()
        print("cities table created successfully")


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


        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                uid serial PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                is_admin boolean NOT NULL,
                user_type user_type not null,
                is_handicap boolean NOT NULL
            );""")

        conn.commit()
        print("users table created successfully")


        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cars (
                year Integer NOT NULL,
                make TEXT NOT NULL,
                model TEXT NOT NULL,
                lplate TEXT NOT NULL,
                lstate TEXT NOT NULL,
                Primary KEY (lplate, lstate)
            );""")

        conn.commit()
        print("cars table created successfully")


        cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_car (
    uid INTEGER NOT NULL,
    lstate TEXT NOT NULL,
    lplate TEXT NOT NULL,
    PRIMARY KEY (uid, lstate, lplate),  
    FOREIGN KEY (uid) REFERENCES users(uid),
    FOREIGN KEY (lstate, lplate) REFERENCES cars(lstate, lplate),
    CONSTRAINT unique_car_per_user UNIQUE (lstate, lplate) 
);""")

        conn.commit()
        print("user cars table created successfully")

        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS college (
            colname      TEXT NOT NULL,
            cid          INTEGER NOT NULL,
            num_students INTEGER NOT NULL,
            PRIMARY KEY (colname, cid),
            FOREIGN KEY (cid) REFERENCES cities(cid)
        );
        """)

        conn.commit()
        print("college created successfully")


        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attending (
    uid   INTEGER NOT NULL,
    colname TEXT NOT NULL,
    state TEXT NOT NULL,
    cid   INTEGER NOT NULL,
    PRIMARY KEY (uid, colname, state, cid),
    FOREIGN KEY (uid) REFERENCES users(uid),
    FOREIGN KEY (colname, cid) REFERENCES college(colname, cid)
);""")

        conn.commit()
        print('attending table created successfully')


        cursor.execute("""
            CREATE TABLE IF NOT EXISTS college_lot (
    lid      INTEGER NOT NULL,
    colname  TEXT NOT NULL,
    cid      INTEGER NOT NULL,
    PRIMARY KEY (lid),
    FOREIGN KEY (lid) REFERENCES lots(lid),
    FOREIGN KEY (colname, cid) REFERENCES college(colname, cid)
);
""")

        conn.commit()
        print("college lot table created successfully")


        cursor.execute("""
           CREATE TABLE IF NOT EXISTS parking (
    uid      INTEGER NOT NULL,
    lid      INTEGER NOT NULL,
    snum     INTEGER NOT NULL,
    res_time TIMESTAMP NOT NULL,
    time_in  TIMESTAMP,
    time_out TIMESTAMP,
    PRIMARY KEY (uid, lid, snum, res_time),
    FOREIGN KEY (uid) REFERENCES users(uid),
    FOREIGN KEY (lid) REFERENCES lots(lid)
);

""")

        conn.commit()
        print("parking table created successfully")


        cursor.execute("""
            CREATE TABLE IF NOT EXISTS spaces (
    snum       INTEGER NOT NULL,
    lid             INTEGER NOT NULL,  
    user_restriction user_type NOT NULL,  
    is_handicap     BOOLEAN NOT NULL,
    is_occupied     BOOLEAN NOT NULL,
    PRIMARY KEY (snum, lid),
    FOREIGN KEY (lid) REFERENCES lots(lid)
);
""")

        conn.commit()
        print("spaces table created successfully")






        conn.close()

    except Exception as e:
        print(f"Error creating table: {e}")


if __name__ == "__main__":
    create_table()
