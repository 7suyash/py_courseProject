import sqlite3
import os  # Import os module to check file existence

def initialize_database(db_path):
    # Create a database connection and initialize the table if it doesn't exist
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS typing_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            wpm REAL NOT NULL,
            mistakes INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def update_record(db_path, username, wpm, mistakes):
    username = username.strip().lower()  # Normalize username
    # Insert a new record into the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO typing_records (username, wpm, mistakes)
        VALUES (?, ?, ?)
    ''', (username, wpm, mistakes))
    conn.commit()
    conn.close()

def show_records(db_path, username):
    username = username.strip().lower()  # Normalize username
    # Retrieve and display all records for the specified user
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT wpm, mistakes FROM typing_records
        WHERE username = ?
    ''', (username,))
    records = cursor.fetchall()
    conn.close()

    if records:
        print(f"Records for {username}:")
        for record in records:
            print(f"WPM: {record[0]}, Mistakes: {record[1]}")
    else:
        print(f"No records found for user: {username}")

def check_database_exists(db_path):
    # Check if the database file exists
    if os.path.exists(db_path):
        print(f"Database '{db_path}' exists.")
    else:
        print(f"Database '{db_path}' does not exist.")

# Example usage
db_path = "c:\\Users\\suyash\\py project\\typing_speed_records.db"
check_database_exists(db_path)  # Check if the database exists
initialize_database(db_path)
username = "suyash"
update_record(db_path, username, wpm=15.0, mistakes=1)
show_records(db_path, username)
