import csv
import mysql.connector
from mysql.connector import Error

# Database config
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password123',  # Replace with your MySQL password
    'database': 'cinemovies'
}

def create_table(cursor):
    """Create movies table if it doesn't exist."""
    create_query = """
    CREATE TABLE IF NOT EXISTS movies (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Series_Title VARCHAR(255) NOT NULL,
        Released_Year INT NULL,
        Genre VARCHAR(255),
        IMDB_Rating FLOAT NULL,
        Director VARCHAR(255),
        Star1 VARCHAR(255),
        Star2 VARCHAR(255),
        Star3 VARCHAR(255)
    )
    """
    cursor.execute(create_query)
    print("Table 'movies' created or already exists.")

def import_csv_to_db():
    """Read movies.csv and insert into MySQL."""
    try:
        # Connect to database
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Create table
        create_table(cursor)

        # Read CSV and insert rows
        with open('movies.csv', 'r', newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file, delimiter=',', quotechar='"')
            next(csv_reader)  # Skip header row
            row_count = 0
            bad_rows = []
            for i, row in enumerate(csv_reader, start=1):
                try:
                    # Validate row length (expect 8 columns)
                    if len(row) != 8:
                        raise ValueError(f"Expected 8 columns, got {len(row)}")

                    # Convert Released_Year to int or None
                    year = None
                    if row[1] and row[1].strip().isdigit() and len(row[1].strip()) == 4:
                        year = int(row[1])

                    # Convert IMDB_Rating to float or None
                    rating = None
                    if row[3] and row[3].strip().replace('.', '').isdigit():
                        rating = float(row[3])

                    # Prepare row data
                    row_data = (
                        row[0].strip(),  # Series_Title
                        year,            # Released_Year
                        row[2].strip(),  # Genre
                        rating,          # IMDB_Rating
                        row[4].strip(),  # Director
                        row[5].strip(),  # Star1
                        row[6].strip(),  # Star2
                        row[7].strip()   # Star3
                    )

                    insert_query = """
                    INSERT INTO movies (Series_Title, Released_Year, Genre, IMDB_Rating, Director, Star1, Star2, Star3)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, row_data)
                    row_count += 1

                except (ValueError, IndexError) as e:
                    bad_rows.append((i, row, str(e)))
                    continue
                except mysql.connector.Error as e:
                    bad_rows.append((i, row, f"DB Error: {e}"))
                    continue

        # Save changes
        conn.commit()
        print(f"Imported {row_count} rows successfully!")
        if bad_rows:
            print(f"Skipped {len(bad_rows)} bad rows:")
            for row_num, row_data, error in bad_rows:
                print(f"Row {row_num}: {row_data} - Error: {error}")

    except Error as e:
        print(f"Database Error: {e}")
    except FileNotFoundError:
        print("Error: movies.csv not found in project folder!")
    except Exception as e:
        print(f"Unexpected Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    import_csv_to_db()
