import psycopg2

from appSetting import dbUser, dbPassword, database, host


def create_user_table():
    cur = None  # Initialize cur to None
    try:
        # Establish a connection to the database
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=dbUser,
            password=dbPassword,
            port=5433
        )

        # Create a cursor object
        cur = conn.cursor()

        # SQL command to create the user table
        cur.execute(""" 
             CREATE TABLE IF NOT EXISTS users (
                 id SERIAL PRIMARY KEY,
                 name VARCHAR(100),
                 job_id VARCHAR(50),
                 day DATE,
                 time TIME,
                 type VARCHAR(50),
                 door VARCHAR(250),
                 registration_type VARCHAR(50)
             )
         """)

        # Commit the transaction
        conn.commit()
        print("Table created successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the cursor and connection
        if cur:
            cur.close()
        if conn:
            conn.close()