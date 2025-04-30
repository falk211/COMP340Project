import os
import string
import random
import time
import psycopg
from psycopg.rows import dict_row
from db_info import *


class CarFuncs:
    def __init__(self, db_filename="pico.db"):
        """Initialize the connection to the database."""
        self.db_url = f"host=dbclass.rhodescs.org dbname=practice user={DBUSER} password={DBPASS}"

    def add_car(self, uid, year, make, model, lplate, lstate):
        try:
            # Connect to the database
            connection = psycopg.connect(self.db_url)
            cursor = connection.cursor()

            # Insert the car into the cars table if it doesn't already exist
            cursor.execute("""
                INSERT INTO cars (year, make, model, lplate, lstate)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (lplate, lstate) DO NOTHING
            """, (year, make, model, lplate, lstate))

            # Link the car to the user in the user_car table
            cursor.execute("""
                INSERT INTO user_car (uid, lstate, lplate)
                VALUES (%s, %s, %s)
                ON CONFLICT (uid, lstate, lplate) DO NOTHING
            """, (uid, lstate, lplate))

            # Commit the transaction
            connection.commit()
            print(f"Car {make} {model} ({year}) added successfully for user {uid}.")
            connection.close()

        except Exception as e:
            print(f"Error adding car: {e}")



    def get_lots(self, uid):
        conn = psycopg.connect(self.db_url, row_factory=dict_row)
        cursor = conn.cursor()
        cursor.execute('''with user_lots as (select lot_name, l.lid, num_total from lots l join college_lot cl on l.lid = cl.lid where cl.colname in (select colname from attending where uid = %s))
        select lot_name, num_total, count(*) from spaces join user_lots on spaces.lid = user_lots.lid where is_occupied = false group by lot_name, num_total;
        ''', (uid,))
        lots = cursor.fetchall()
        conn.close()
        return lots


    def reserve_space(self, uid, lot_name):
        try:
            conn = psycopg.connect(self.db_url, row_factory=dict_row)
            cursor = conn.cursor()
            cursor.execute('''select lid from lots where lot_name = %s''', (lot_name,))
            lid = cursor.fetchone()['lid']
            cursor.execute('''select space_num from spaces where lid = %s''', (lid,))
            space_num = cursor.fetchone()['space_num']
            cursor.execute('''update spaces set is_occupied = true where lid = %s and space_num = %s''', (lid, space_num,))
            conn.commit()
            cursor.execute('''insert into parking (uid, lid, space_num, time_in, time_out) values (%s, %s, %s, now(), null)''', (uid, lid, space_num,))
            conn.commit()
            conn.close()

            return True
        except Exception as e:
            print(f"Error reserving space: {e}")
            return False

    

    def get_cars(self, uid):
        try:
            # Connect to the database
            connection = psycopg.connect(self.db_url, row_factory=dict_row)
            cursor = connection.cursor()

            # Fetch the cars associated with the user
            cursor.execute("""
                SELECT cars.year, cars.make, cars.model, cars.lplate, cars.lstate
                FROM cars
                JOIN user_car ON cars.lplate = user_car.lplate AND cars.lstate = user_car.lstate
                WHERE user_car.uid = %s
            """, (uid,))
            cars = cursor.fetchall()

            connection.close()
            return cars

        except Exception as e:
            print(f"Error fetching cars: {e}")
            return []