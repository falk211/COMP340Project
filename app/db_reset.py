import psycopg
from db_info import *


def reset_tables():
    try:
        with psycopg.connect(
                f"host=dbclass.rhodescs.org dbname=practice user={DBUSER} password={DBPASS}") as conn:
            with conn.cursor() as cursor:  # Use 'with' to auto-close cursor

                print(f"Database: {conn.info.dbname}")
                print(f"User: {conn.info.user}")
                print(f"Host: {conn.info.host}")
                print(f"Port: {conn.info.port}")
                print(f"Backend PID: {conn.info.backend_pid}")
                print(f"Server version: {conn.info.server_version}")
                print(f"Default client encoding: {conn.info.encoding}")

                # List of tables (drop in the correct order to avoid FK issues)
                tables = [
                    "users", "cities", "lots", "cars", "user_car", "attending", "college", "college_lot", "parking","spaces"
                ]

                # Drop tables with CASCADE to remove dependencies
                for table in tables:
                    #cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
                    cursor.execute(f"DROP TABLE if exists {table} CASCADE")
                    print(f"Dropped table: {table}")

                # Commit changes
                conn.commit()
                print(f"Tables dropped")

    except Exception as e:
        print(f"Error dropping tables: {e}")


if __name__ == "__main__":
    reset_tables()
