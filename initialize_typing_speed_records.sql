-- Create the database table for typing speed records
CREATE TABLE IF NOT EXISTS typing_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    wpm REAL NOT NULL,
    mistakes INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Insert a new record into the typing_records table
-- Example usage:
-- INSERT INTO typing_records (username, wpm, mistakes) VALUES ('suyash', 18.0, 0);

-- Retrieve all records for a specific user
-- Example usage:
-- SELECT wpm, mistakes, timestamp FROM typing_records WHERE username = 'suyash';

-- Retrieve all records in the database
-- Example usage:
-- SELECT * FROM typing_records;

-- Delete all records for a specific user
-- Example usage:
-- DELETE FROM typing_records WHERE username = 'suyash';
