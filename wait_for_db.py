import time
import psycopg2
from psycopg2 import OperationalError

def wait_for_db(host="db", port=5432, user="admin", password="password", dbname="newsportal"):
    print("Waiting for database...")
    while True:
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                dbname=dbname,
                connect_timeout=3
            )
            conn.close()
            print("Database is ready!")
            return
        except OperationalError:
            print("Database is unavailable, waiting 2 seconds...")
            time.sleep(2)

if __name__ == "__main__":
    wait_for_db()