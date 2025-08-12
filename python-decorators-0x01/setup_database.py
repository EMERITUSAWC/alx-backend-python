import sqlite3
import os

DATABASE_NAME = 'users.db'

def setup_database():
    """
    Connects to the SQLite database, creates the users table if it doesn't exist,
    and populates it with sample data if the table is empty.
    """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                age INTEGER
            )
        """)
        conn.commit()
        print(f"Table 'users' created or already exists in {DATABASE_NAME}.")

        # Check if table is empty
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            # Insert sample data
            sample_users = [
                ('Alice Smith', 'alice.smith@example.com', 30),
                ('Bob Johnson', 'bob.j@example.com', 25),
                ('Charlie Brown', 'charlie.b@example.com', 40),
                ('Diana Prince', 'diana.p@example.com', 28),
                ('Ethan Hunt', 'ethan.h@example.com', 35),
                ('Fiona Glenanne', 'fiona.g@example.com', 50),
                ('George Costanza', 'george.c@example.com', 60),
                ('Hannah Montana', 'hannah.m@example.com', 18),
                ('Ivy Pepper', 'ivy.p@example.com', 20),
                ('Jack Reacher', 'jack.r@example.com', 45),
                ('Kelly Clarkson', 'kelly.c@example.com', 38),
                ('Liam Neeson', 'liam.n@example.com', 65)
            ]
            cursor.executemany("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", sample_users)
            conn.commit()
            print("Sample data inserted into 'users' table.")
        else:
            print("Table 'users' already contains data. Skipping insertion.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    setup_database()
    print(f"Database setup complete for {DATABASE_NAME}.")
    # Optional: Verify data
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users LIMIT 3")
    print("\nFirst 3 users:")
    for row in cursor.fetchall():
        print(row)
    conn.close()