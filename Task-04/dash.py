import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLineEdit,
                               QLabel, QComboBox)
from PySide6.QtCore import Qt
import mysql.connector
from mysql.connector import Error
import csv

# Database config
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password123',  # Replace with your MySQL password
    'database': 'cinemovies'
}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CineScope Dashboard")
        self.setGeometry(100, 100, 1000, 700)  # Slightly larger window

        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by title or director...")
        search_layout.addWidget(QLabel("Search:"))
        search_layout.addWidget(self.search_input)
        main_layout.addLayout(search_layout)

        # Search button
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.perform_search)
        main_layout.addWidget(self.search_button)

        # Genre filter
        filter_layout = QHBoxLayout()
        self.genre_combo = QComboBox()
        self.genre_combo.addItem("All Genres")
        self.populate_genres()  # Dynamically load genres
        filter_layout.addWidget(QLabel("Filter by Genre:"))
        filter_layout.addWidget(self.genre_combo)
        main_layout.addLayout(filter_layout)

        # Filter button
        self.filter_button = QPushButton("Apply Filter")
        self.filter_button.clicked.connect(self.apply_filter)
        main_layout.addWidget(self.filter_button)

        # Clear button
        self.clear_button = QPushButton("Clear Filters")
        self.clear_button.clicked.connect(self.load_all_data)
        main_layout.addWidget(self.clear_button)

        # Table for displaying movies
        self.table = QTableWidget()
        self.table.setColumnCount(5)  # id, Series_Title, Released_Year, Genre, IMDB_Rating
        self.table.setHorizontalHeaderLabels(["ID", "Title", "Year", "Genre", "Rating"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)  # Enable sorting by clicking headers
        self.table.resizeColumnsToContents()  # Auto-resize columns
        main_layout.addWidget(self.table)

        # Export button
        self.export_button = QPushButton("Export to CSV")
        self.export_button.clicked.connect(self.export_to_csv)
        main_layout.addWidget(self.export_button)

        # Load initial data
        self.load_all_data()

    def get_connection(self):
        """Connect to MySQL database."""
        try:
            return mysql.connector.connect(**DB_CONFIG)
        except Error as e:
            print(f"Connection Error: {e}")
            return None

    def populate_genres(self):
        """Load unique genres from database."""
        conn = self.get_connection()
        if not conn:
            return
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT DISTINCT Genre FROM movies ORDER BY Genre")
            genres = [row[0] for row in cursor.fetchall()]
            self.genre_combo.addItems(genres)
        except Error as e:
            print(f"Genre Query Error: {e}")
        finally:
            cursor.close()
            conn.close()

    def load_all_data(self):
        """Load all movies from database."""
        self.search_input.clear()  # Clear search bar
        self.genre_combo.setCurrentText("All Genres")  # Reset genre filter
        query = """
        SELECT id, Series_Title, Released_Year, Genre, IMDB_Rating
        FROM movies
        ORDER BY IMDB_Rating DESC
        """
        self.perform_query(query)

    def perform_search(self):
        """Search movies by title or director."""
        search_term = self.search_input.text().strip()
        if not search_term:
            self.load_all_data()
            return
        query = """
        SELECT id, Series_Title, Released_Year, Genre, IMDB_Rating
        FROM movies
        WHERE Series_Title LIKE %s OR Director LIKE %s
        ORDER BY IMDB_Rating DESC
        """
        params = (f'%{search_term}%', f'%{search_term}%')
        self.perform_query(query, params)

    def apply_filter(self):
        """Filter movies by genre."""
        selected_genre = self.genre_combo.currentText()
        if selected_genre == "All Genres":
            self.load_all_data()
            return
        query = """
        SELECT id, Series_Title, Released_Year, Genre, IMDB_Rating
        FROM movies
        WHERE Genre = %s
        ORDER BY IMDB_Rating DESC
        """
        params = (selected_genre,)
        self.perform_query(query, params)

    def perform_query(self, query, params=None):
        """Execute SQL query and update table."""
        conn = self.get_connection()
        if not conn:
            return
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            if not results:
                print("No results found!")
                self.table.setRowCount(0)
                return

            # Update table
            self.table.setRowCount(len(results))
            for row_idx, row in enumerate(results):
                for col_idx, value in enumerate(row):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value or '')))
            self.table.resizeColumnsToContents()  # Resize after data load
            print(f"Displayed {len(results)} rows.")
        except Error as e:
            print(f"Query Error: {e}")
        finally:
            cursor.close()
            conn.close()

    def export_to_csv(self):
        """Export current table data to CSV."""
        if self.table.rowCount() == 0:
            print("No data to export!")
            return
        with open('exported_movies.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write headers
            headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
            writer.writerow(headers)
            # Write rows
            for row in range(self.table.rowCount()):
                row_data = [self.table.item(row, col).text() for col in range(self.table.columnCount())]
                writer.writerow(row_data)
            print(f"Exported {self.table.rowCount()} rows to exported_movies.csv")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
