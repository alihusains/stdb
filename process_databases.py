import os
import sqlite3
import pandas as pd

# Directory where the .db files are stored
database_dir = 'database'

# List all .db files in the database directory
db_files = [f for f in os.listdir(database_dir) if f.endswith('.db')]

# Process each .db file
for db_file in db_files:
    db_path = os.path.join(database_dir, db_file)
    db_name = os.path.splitext(db_file)[0]
    
    # Create a directory for the database in the root directory
    output_dir = db_name
    os.makedirs(output_dir, exist_ok=True)
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    
    # Get the list of tables
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    # Export each table to a CSV file
    for table_name in tables:
        table_name = table_name[0]
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        csv_path = os.path.join(output_dir, f"{table_name}.csv")
        df.to_csv(csv_path, index=False)
    
    # Close the database connection
    conn.close()
