import mysql.connector

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='password123',  # Replace with your MySQL root password
        database='cinemovies'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT DATABASE();")
    print(cursor.fetchone())  # Should print ('cinemovies',)
    cursor.close()
    conn.close()
except mysql.connector.Error as e:
    print(f"Error: {e}")
