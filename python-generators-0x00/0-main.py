#!/usr/bin/python3

# Import the seed module (which contains database functions)
seed = __import__('seed')

# Attempt to connect to the MySQL server
connection = seed.connect_db()
if connection:
    # Create the database if it doesn't exist, then close this initial connection
    seed.create_database(connection)
    connection.close()
    print(f"connection successful (to server)")

    # Now, connect specifically to the ALX_prodev database
    connection = seed.connect_to_prodev()

    if connection:
        # Create the user_data table if it doesn't exist
        seed.create_table(connection)
        # Insert data from user_data.csv if the table is empty
        seed.insert_data(connection, 'user_data.csv')

        # Verify the database and fetch some data as specified in the brief
        cursor = connection.cursor()
        cursor.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
        result = cursor.fetchone()
        if result:
            print(f"Database ALX_prodev is present ")

        cursor.execute(f"SELECT * FROM user_data LIMIT 5;")
        rows = cursor.fetchall()
        print(rows) # Print the fetched rows

        cursor.close()
        connection.close() # Close the connection to ALX_prodev database
    else:
        print("Failed to connect to ALX_prodev database (after creation).")
else:
    print("Failed to establish initial connection to MySQL server.")