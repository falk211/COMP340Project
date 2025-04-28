import random
from datetime import datetime, timedelta
from faker import Faker
import psycopg
from db_info import DBUSER, DBPASS

fake = Faker()
conn = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user={DBUSER} password={DBPASS}")
cursor = conn.cursor()

def insert_cities(n=5):
    for _ in range(n):
        cname = fake.city()
        state = fake.state_abbr()
        cursor.execute("INSERT INTO cities (cname, state) VALUES (%s, %s)", (cname, state))

def insert_lots(n=3):
    for _ in range(n):
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
    for _ in range(n):
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


    random.shuffle(cars)


    for i, uid in enumerate(users):
        if i < len(cars):  # Only assign cars to users if there's a car available
            car = cars[i]  # Take the i-th car after shuffling
            cursor.execute("""
                INSERT INTO user_car (uid, lstate, lplate) 
                VALUES (%s, %s, %s)
            """, (uid[0], car[1], car[0]))

def insert_colleges(n=3):
    cursor.execute("SELECT cid FROM cities")
    cities = cursor.fetchall()
    for _ in range(n):
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
            INSERT INTO attending (uid, college, state, cid) VALUES (%s, %s, %s, %s)""", (uid[0], colname, state, cid))

def link_lots_to_colleges():

    # Get all existing lots and colleges
    cursor.execute("SELECT lid FROM lots;")
    lot_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT colname, cid FROM college;")
    colleges = cursor.fetchall()

    if not lot_ids or not colleges:
        print("No lots or colleges available to link.")
        return

    inserted = 0
    for lid in lot_ids:
        colname, cid = random.choice(colleges)

        try:
            cursor.execute("""
                INSERT INTO college_lot (lid, colname, cid)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING;
            """, (lid, colname, cid))
            inserted += 1
        except Exception as e:
            print(f"Error linking lot {lid} to college {colname} ({cid}): {e}")

def run():
    insert_cities()
    insert_lots()
    insert_users()
    insert_cars()
    link_users_to_cars()
    insert_colleges()
    link_users_to_attending()
    link_lots_to_colleges()
    conn.commit()
    print("Data inserted successfully.")

if __name__ == "__main__":
    run()
    conn.close()
