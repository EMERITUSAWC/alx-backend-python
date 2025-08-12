# Python Generators – Task 0

This task sets up a MySQL database and loads user data from CSV using Python. It uses UUIDs and generator-friendly batch inserts for large data simulation.

## Files

- `seed.py`: Script to create DB, table, and load data.
- `0-main.py`: Test script to verify setup.
- `user_data.csv`: Sample user dataset.
- `README.md`: This documentation.

## Database

- **Name:** ALX_prodev  
- **Table:** user_data  
  - `user_id` (UUID, Primary Key)  
  - `name` (VARCHAR)  
  - `email` (VARCHAR)  
  - `age` (DECIMAL)

## Usage

1. Ensure MySQL is running.
2. Replace `your_mysql_password` in `seed.py`.
3. Run the test:
```bash
./0-main.py
