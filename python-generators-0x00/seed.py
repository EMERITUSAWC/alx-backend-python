#!/usr/bin/python3
import mysql.connector
from mysql.connector import errorcode
import csv
import uuid

# MySQL connection configuration
# IMPORTANT: Update these with your MySQL server details
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root', # Your MySQL username
    'password': '', # Your MySQL password (often empty if not set, or a specific one)
    'database': 'ALX_prodev' # The database name for the project
}

def connect_db():
    """Connects to the MySQL database server."""
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        print("Connection successful (to MySQL server)")
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Something is wrong with your MySQL username or password. Please check DB_CONFIG in seed.py.")
        elif err.errno == errorcode.CR_CONN_HOST_ERROR:
            print(f"Error: Cannot connect to MySQL server at {DB_CONFIG['host']}. Is MySQL running and accessible?")
        else:
            print(f"Error: {err}")
        return None

def create_database(connection):
    """Creates the database ALX_prodev if it does not exist."""
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        print(f"Database {DB_CONFIG['database']} created successfully (if it didn't exist).")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
    finally:
        cursor.close()

def connect_to_prodev():
    """Connects to the ALX_prodev database in MySQL."""
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database']
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Failed to connect to database {DB_CONFIG['database']}: {err}")
        return None

def create_table(connection):
    """Creates a table user_data if it does not exists with the required fields."""
    cursor = connection.cursor()
    table_creation_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        age DECIMAL(5, 2) NOT NULL
    )
    """
    try:
        cursor.execute(table_creation_query)
        print("Table user_data created successfully (if it didn't exist).")
    except mysql.connector.Error as err:
        print(f"Failed creating table: {err}")
    finally:
        cursor.close()

def insert_data(connection, data_file):
    """Inserts data from a CSV file into the user_data table if it does not exist."""
    cursor = connection.cursor()

    # Check if table is empty to prevent re-inserting data on every run
    cursor.execute("SELECT COUNT(*) FROM user_data")
    if cursor.fetchone()[0] > 0:
        print("Table 'user_data' already contains data. Skipping insertion.")
        cursor.close()
        return

    try:
        with open(data_file, mode='r', newline='', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            insert_query = "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)"

            for row in csv_reader:
                # Convert UUID string to a standard UUID object, then to string for MySQL VARCHAR
                user_id_str = str(uuid.UUID(row['user_id']))
                data = (user_id_str, row['name'], row['email'], float(row['age']))
                try:
                    cursor.execute(insert_query, data)
                except mysql.connector.IntegrityError as e:
                    if e.errno == errorcode.ER_DUP_ENTRY:
                        print(f"Skipping duplicate entry for email: {row['email']}")
                    else:
                        raise e # Re-raise other integrity errors
            connection.commit()
            print(f"Data from {data_file} inserted successfully.")
    except FileNotFoundError:
        print(f"Error: {data_file} not found. Make sure user_data.csv is in the same directory.")
    except Exception as err:
        connection.rollback()
        print(f"Error inserting data: {err}")
    finally:
        cursor.close()

# This __main__ block is for direct testing of seed.py, not for 0-main.py itself.
if __name__ == "__main__":
    print("--- Running seed.py directly for testing database setup ---")
    conn = connect_db()
    if conn:
        create_database(conn)
        conn.close() # Close initial connection, then connect to specific database

        conn_prodev = connect_to_prodev()
        if conn_prodev:
            create_table(conn_prodev)
            insert_data(conn_prodev, 'user_data.csv')
            conn_prodev.close()
        else:
            print("Could not connect to ALX_prodev database (after creation).")
    else:
        print("Could not establish initial connection to MySQL server for direct seed.py test.")
    print("--- Finished direct seed.py test ---")
