import csv
import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password123',  # Replace with your MySQL root password
    'database': 'cinemovies'
}

def create_table(cursor):
    """Create movies table if it doesn't exist."""
    create_query = """
    CREATE TABLE IF NOT EXISTS movies (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Series_Title VARCHAR(255) NOT NULL,
        Released_Year INT,
        Genre VARCHAR(100),
        IMDB_Rating FLOAT,
        Director VARCHAR(255),
        Star1 VARCHAR(255),
        Star2 VARCHAR(255),
        Star3 VARCHAR(255)
    )
    """
    cursor.execute(create_query)
    print("Table 'movies' created or already exists.")

def import_csv_to_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        create_table(cursor)
        with open('movies.csv', 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            for row_idx, row in enumerate(csv_reader, start=1):
                row = row + [None] * (8 - len(row))  # Pad incomplete rows
                # Convert Released_Year to int or None
                try:
                    row[1] = int(row[1]) if row[1] else None
                except ValueError:
                    print(f"Invalid Released_Year at row {row_idx+1}: {row[1]}")
                    row[1] = None
                # Convert IMDB_Rating to float or None
                try:
                    row[3] = float(row[3]) if row[3] else None
                except ValueError:
                    print(f"Invalid IMDB_Rating at row {row_idx+1}: {row[3]}")
                    row[3] = None
                insert_query = """
                INSERT INTO movies (Series_Title, Released_Year, Genre, IMDB_Rating, Director, Star1, Star2, Star3)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, row[:8])  # Use first 8 columns
        conn.commit()
        print(f"Imported {cursor.rowcount} rows successfully!")
    except Error as e:
        print(f"Error: {e}")
    except FileNotFoundError:
        print("Error: movies.csv not found in the project folder!")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    import_csv_to_db()

