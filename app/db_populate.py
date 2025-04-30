import random
from datetime import datetime, timedelta
from faker import Faker
import psycopg
from db_info import DBUSER, DBPASS

fake = Faker()
conn = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={DBUSER} password={DBPASS}")
cursor = conn.cursor()

def insert_cities(n=5):
    for num in range(n):
        cname = fake.city()
        state = fake.state_abbr()
        cursor.execute("INSERT INTO cities (cname, state) VALUES (%s, %s)", (cname, state))

def insert_lots(n=3):
    for num in range(n):
        lot = {
            'num_handicap': random.randint(1, 5),
            'num_guest': random.randint(2, 10),
            'lot_name': fake.street_name(),
            'num_faculty': random.randint(2, 8),
            'num_students': random.randint(10, 30)
        }
        lot['num_total'] = lot['num_handicap'] + lot['num_guest'] + lot['num_faculty'] + lot['num_students']
        cursor.execute("""
            INSERT INTO lots (num_handicap, num_guest, lot_name, num_faculty, num_total, num_students)
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (lot['num_handicap'], lot['num_guest'], lot['lot_name'],
             lot['num_faculty'], lot['num_total'], lot['num_students']))

def insert_users(n=10):
    user_types = ['student', 'faculty', 'guest']
    for i in range(1, n + 1):
        cursor.execute("""
            INSERT INTO users (uid, first_name, last_name, email, password, is_admin, user_type, is_handicap)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (i, fake.first_name(), fake.last_name(), fake.email(), fake.password(),
             random.choice([True, False]), random.choice(user_types), random.choice([True, False])))

def insert_cars(n=10):
    for num in range(n):
        cursor.execute("""
            INSERT INTO cars (year, make, model, lplate, lstate)
            VALUES (%s, %s, %s, %s, %s)""",
            (random.randint(2000, 2024), fake.company(), fake.word(),
             fake.license_plate(), fake.state_abbr()))

def link_users_to_cars():
    cursor.execute("SELECT uid FROM users")
    users = cursor.fetchall()
    cursor.execute("SELECT lplate, lstate FROM cars")
    cars = cursor.fetchall()
    for i, uid in enumerate(users):
        if i < len(cars):
            car = cars[i]
            cursor.execute("""
                INSERT INTO user_car (uid, lstate, lplate) 
                VALUES (%s, %s, %s)
            """, (uid[0], car[1], car[0]))

def insert_colleges(n=3):
    cursor.execute("SELECT cid FROM cities")
    cities = cursor.fetchall()
    for num in range(n):
        colname = fake.company() + " College"
        cid = random.choice(cities)[0]
        cursor.execute("""
            INSERT INTO college (colname, cid, num_students)
            VALUES (%s, %s, %s)""",
            (colname, cid, random.randint(100, 10000)))

def link_users_to_attending():
    cursor.execute("SELECT uid FROM users")
    users = cursor.fetchall()
    cursor.execute("SELECT cid, colname FROM college")
    college = cursor.fetchall()
    for uid in users:
        cid, colname = random.choice(college)
        cursor.execute("SELECT state FROM cities where cid = %s", (cid,))
        state = cursor.fetchone()[0]
        cursor.execute("""
            INSERT INTO attending (uid, colname, state, cid) VALUES (%s, %s, %s, %s)""", (uid[0], colname, state, cid))

def link_lots_to_colleges():

    cursor.execute("SELECT lid FROM lots;")
    lot_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT colname, cid FROM college;")
    colleges = cursor.fetchall()

    if not lot_ids or not colleges:
        print("No lots or colleges available to link.")
        return

    for lid in lot_ids:
        colname, cid = random.choice(colleges)
        try:
            cursor.execute("""
                INSERT INTO college_lot (lid, colname, cid)
                VALUES (%s, %s, %s)
            """, (lid, colname, cid))
        except Exception as e:
            print(f"Error linking lot {lid} to college {colname} ({cid}): {e}")

def link_spaces_to_lots():
    cursor.execute("SELECT lid from lots;")
    lot_ids = [row[0] for row in cursor.fetchall()]

    for lid in lot_ids:
        cursor.execute("SELECT num_handicap, num_guest, num_faculty, num_students, num_total FROM lots WHERE lid = %s", (lid,))
        att = cursor.fetchall()
        num_handicap = att[0][0]
        num_guest = att[0][1]
        num_faculty = att[0][2]
        num_students = att[0][3]
        num_total = att[0][4]

        for i in range(num_total):
            decider = random.choice(range(1, 4))
            if decider >1:
                if num_handicap > 0:
                    cursor.execute("INSERT INTO spaces (snum, lid,user_restriction, is_handicap, is_occupied) VALUES (%s, %s, %s, %s, %s)",(i, lid, "student",True, False))
                    num_handicap -= 1
                elif num_guest > 0:
                    cursor.execute(
                        "INSERT INTO spaces (snum, lid,user_restriction, is_handicap, is_occupied) VALUES (%s, %s, %s, %s, %s)",
                        (i, lid, "guest",False,False))
                    num_guest -= 1
                elif num_faculty > 0:
                    cursor.execute(
                        "INSERT INTO spaces (snum, lid,user_restriction, is_handicap, is_occupied) VALUES (%s, %s, %s, %s, %s)",
                        (i, lid, "faculty",False, False))
                    num_faculty -= 1
                else:
                    cursor.execute(
                        "INSERT INTO spaces (snum, lid,user_restriction, is_handicap, is_occupied) VALUES (%s, %s, %s, %s, %s)",
                        (i, lid, "student",False, False))
            else:
                if num_handicap > 0:
                    cursor.execute("INSERT INTO spaces (snum, lid,user_restriction, is_handicap, is_occupied) VALUES (%s, %s, %s, %s, %s)",(i, lid, "student", True, True))
                    num_handicap -= 1
                elif num_guest > 0:
                    cursor.execute(
                        "INSERT INTO spaces (snum, lid,user_restriction, is_handicap, is_occupied) VALUES (%s, %s, %s, %s, %s)",
                        (i, lid, "guest",False,True))
                    num_guest -= 1
                elif num_faculty > 0:
                    cursor.execute(
                        "INSERT INTO spaces (snum, lid,user_restriction, is_handicap, is_occupied) VALUES (%s, %s, %s, %s, %s)",
                        (i, lid, "faculty",False,True))
                    num_faculty -= 1
                else:
                    cursor.execute(
                        "INSERT INTO spaces (snum, lid,user_restriction, is_handicap, is_occupied) VALUES (%s, %s, %s, %s, %s)",
                        (i, lid, "student",False,True))


def insert_parking_data(num =10):
    cursor.execute("SELECT uid FROM users;")
    user_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(num):
        cursor.execute("""
                    SELECT lid, snum FROM spaces
                    WHERE is_occupied = FALSE
                """)
        spaces = cursor.fetchall()

        uid = random.choice(user_ids)
        lid, snum = random.choice(spaces)

        time_in = fake.date_time_between(start_date='-30d', end_date='now')

        if random.random() < 0.7:
            duration = timedelta(minutes=random.randint(15, 300))
            time_out = time_in + duration
            still_parked = False
        else:
            time_out = None
            still_parked = True

        cursor.execute("""
                        INSERT INTO parking (uid, lid, snum, time_in, time_out)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (uid, lid, snum, time_in, time_out))

        if still_parked:
                cursor.execute("""
                            UPDATE spaces
                            SET is_occupied = TRUE
                            WHERE lid = %s AND snum = %s
                        """, (lid, snum))
def run():
    insert_cities()
    insert_lots()
    insert_users()
    insert_cars()
    link_users_to_cars()
    insert_colleges()
    link_users_to_attending()
    link_lots_to_colleges()
    link_spaces_to_lots()
    insert_parking_data()
    conn.commit()
    print("Data inserted successfully.")

if __name__ == "__main__":
    run()
    conn.close()
