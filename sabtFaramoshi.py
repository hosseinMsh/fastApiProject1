import psycopg2
from jinja2.filters import sync_do_sum

from appSetting import dbUser, dbPassword, database, host
from crateDb import create_user_table
from datetime import datetime
def addDataToDb(name, job_id, day, time, type_, door, registration_type):
    create_user_table()
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=dbUser,
        password=dbPassword,
        port=5433
    )
    cur = conn.cursor()

    try:
        # First, check if this exact time entry already exists
        cur.execute(
            "SELECT id FROM users WHERE name = %s AND job_id = %s AND day = %s::date AND time = %s::time",
            (name, job_id, day, time)
        )
        existing_record = cur.fetchone()

        # If record already exists, skip insertion
        if existing_record:
            print(f"Record already exists for {name} at {time} on {day}")
            return False

        # If record doesn't exist, proceed with normal logic
        cur.execute(
            "SELECT type FROM users WHERE name = %s AND job_id = %s AND day = %s::date ORDER BY time DESC LIMIT 1",
            (name, job_id, day)
        )
        last_record = cur.fetchone()

        # Determine if this should be an entry or exit
        if type_ != 0:
            if last_record is None or last_record[0] == 'exit':
                type_ = 'entry'
            else:
                type_ = 'exit'

        # Insert the new record
        cur.execute(
            "INSERT INTO users (name, job_id, day, time, type, door, registration_type) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (name, job_id, day, time, type_, door, registration_type)
        )
        conn.commit()
        print(f"Data inserted successfully. Type: {type_}")
        return True

    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()
        return False

    finally:
        cur.close()
        conn.close()