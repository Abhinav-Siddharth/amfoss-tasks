import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem, QGridLayout, 
    QTextEdit, QSizePolicy, QLineEdit
)
from PySide6.QtGui import QFont
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

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CineScope – Dashboard")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet("background-color: #121212; color: white; padding: 20px;")
        self.search_mode = None
        self.selected_columns = ["title", "year", "genre", "rating", "director", "stars"]
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        # Header
        header = QLabel("🎬 CineScope Dashboard")
        header.setFont(QFont("Arial", 24, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setFixedHeight(80)
        main_layout.addWidget(header)

        split_layout = QHBoxLayout()

        # Left Panel
        left_container = QVBoxLayout()
        left_container.setSpacing(10)
        left_container.setAlignment(Qt.AlignTop)

        # Search buttons
        search_heading = QLabel("Search By")
        search_heading.setFont(QFont("Arial", 18, QFont.Bold))
        left_container.addWidget(search_heading)

        self.search_buttons = []
        search_modes = [
            ("Genre", "genre"),
            ("Year", "year"),
            ("Rating", "rating"),
            ("Director", "director"),
            ("Actor", "actor"),
        ]

        search_grid = QGridLayout()
        for index, (label, mode) in enumerate(search_modes):
            btn = QPushButton(label)
            btn.setStyleSheet(self.get_button_style(False))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.clicked.connect(lambda _, m=mode: self.set_search_mode(m))
            self.search_buttons.append(btn)
            row, col = divmod(index, 2)
            search_grid.addWidget(btn, row, col)
        left_container.addLayout(search_grid)

        # Search input
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Enter search term")
        self.query_input.setStyleSheet("background-color: #1e1e1e; color: white; padding: 5px; border: 1px solid #444;")
        self.query_input.hide()  # Hidden until search mode is set
        left_container.addWidget(self.query_input)

        # Send button for search
        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("background-color: #e50914; color: white; padding: 6px; border-radius: 5px;")
        self.send_button.clicked.connect(self.execute_search)
        self.send_button.hide()  # Hidden until search mode is set
        left_container.addWidget(self.send_button)

        # Column selection
        column_heading = QLabel("Select Columns")
        column_heading.setFont(QFont("Arial", 18, QFont.Bold))
        left_container.addWidget(column_heading)

        self.column_buttons = {}
        column_options = [
            ("Title", "title"),
            ("Year", "year"),
            ("Genre", "genre"),
            ("Rating", "rating"),
            ("Director", "director"),
            ("Stars", "stars"),
        ]

        column_grid = QGridLayout()
        for index, (label, col) in enumerate(column_options):
            btn = QPushButton(label)
            btn.setStyleSheet(self.get_button_style(True if col in self.selected_columns else False))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.clicked.connect(lambda _, c=col: self.toggle_column(c))
            self.column_buttons[col] = btn
            row, col = divmod(index, 2)
            column_grid.addWidget(btn, row, col)
        left_container.addLayout(column_grid)

        # Action buttons
        action_layout = QHBoxLayout()
        search_btn = QPushButton("Search All")
        search_btn.setStyleSheet("background-color: #e50914; color: white; padding: 6px; border-radius: 5px;")
        search_btn.clicked.connect(self.execute_search_all)
        action_layout.addWidget(search_btn)

        export_btn = QPushButton("Export CSV")
        export_btn.setStyleSheet("background-color: #1f1f1f; color: white; padding: 6px; border-radius: 5px;")
        export_btn.clicked.connect(self.export_csv)
        action_layout.addWidget(export_btn)
        left_container.addLayout(action_layout)

        # Right Panel
        right_side_layout = QVBoxLayout()
        right_side_layout.setSpacing(10)

        # Table
        self.table = QTableWidget()
        self.table.setStyleSheet("""
            QTableWidget {
                color: white;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: white;
                color: black;
                padding: 4px;
            }
        """)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_side_layout.addWidget(self.table)

        # Output console
        self.output_console = QTextEdit()
        self.output_console.setPlaceholderText("Results will appear here...")
        self.output_console.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: white;
                border: 1px solid #444;
                padding: 5px;
            }
        """)
        self.output_console.setFixedHeight(100)
        right_side_layout.addWidget(self.output_console)

        split_layout.addLayout(left_container, 2)
        split_layout.addLayout(right_side_layout, 8)
        main_layout.addLayout(split_layout)
        self.setLayout(main_layout)

        # Load initial data
        self.load_all_data()

    def get_button_style(self, is_selected):
        if is_selected:
            return """
                QPushButton {
                    background-color: #ffcc00;
                    border: 1px solid #ff9900;
                    border-radius: 3px;
                    padding: 6px;
                }
            """
        else:
            return """
                QPushButton {
                    background-color: #1f1f1f;
                    border: 1px solid #333;
                    border-radius: 3px;
                    padding: 6px;
                }
                QPushButton:hover {
                    background-color: #333;
                }
            """

    def set_search_mode(self, mode):
        """Set the search mode and show input/send button."""
        self.search_mode = mode
        self.query_input.setPlaceholderText(f"Enter {mode.capitalize()}...")
        self.query_input.show()
        self.send_button.show()
        for btn in self.search_buttons:
            btn.setStyleSheet(self.get_button_style(False))
        sender = self.sender()
        sender.setStyleSheet(self.get_button_style(True))
        self.output_console.append(f"Search mode set to: {mode}")

    def toggle_column(self, column):
        """Toggle column visibility."""
        if column in self.selected_columns:
            self.selected_columns.remove(column)
            self.column_buttons[column].setStyleSheet(self.get_button_style(False))
        else:
            self.selected_columns.append(column)
            self.column_buttons[column].setStyleSheet(self.get_button_style(True))
        self.update_table_columns()
        self.output_console.append(f"Column toggled: {column}")

    def load_all_data(self):
        """Load all movies from database."""
        conn = self.get_connection()
        if not conn:
            return
        cursor = conn.cursor()
        try:
            query = """
            SELECT id, Series_Title, Released_Year, Genre, IMDB_Rating, Director, CONCAT(Star1, ', ', Star2, ', ', Star3)
            FROM movies
            ORDER BY IMDB_Rating DESC
            """
            cursor.execute(query)
            results = cursor.fetchall()
            self.update_table(results)
        except Error as e:
            self.output_console.append(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

    def execute_search(self):
        """Execute search based on the selected mode and input."""
        if not self.search_mode:
            self.output_console.append("Please select a search mode first!")
            return
        value = self.query_input.text().strip()
        if not value:
            self.output_console.append("Please enter a value!")
            return

        conn = self.get_connection()
        if not conn:
            return
        cursor = conn.cursor()
        try:
            query = "SELECT id, Series_Title, Released_Year, Genre, IMDB_Rating, Director, CONCAT(Star1, ', ', Star2, ', ', Star3) FROM movies WHERE 1=1"
            params = []
            if self.search_mode == "year" and value.isdigit() and len(value) == 4:
                query += " AND Released_Year = %s"
                params.append(int(value))
            elif self.search_mode == "genre":
                query += " AND Genre LIKE %s"
                params.append(f'%{value}%')
            elif self.search_mode == "rating" and value.replace('.', '').isdigit():
                query += " AND IMDB_Rating >= %s"
                params.append(float(value))
            elif self.search_mode in ["director", "actor"]:
                field = "Director" if self.search_mode == "director" else "CONCAT(Star1, ', ', Star2, ', ', Star3)"
                query += f" AND {field} LIKE %s"
                params.append(f'%{value}%')
            query += " ORDER BY IMDB_Rating DESC"

            cursor.execute(query, params)
            results = cursor.fetchall()
            self.update_table(results)
            self.output_console.append("Query executed successfully")
            self.output_console.append(f"SQL: {query % tuple(params)}")
            self.query_input.hide()
            self.send_button.hide()
            self.search_mode = None
        except Error as e:
            self.output_console.append(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

    def execute_search_all(self):
        """Execute search using all input fields."""
        search_term = self.search_input.text().strip() if hasattr(self, 'search_input') else ""
        genre = self.genre_input.text().strip() if hasattr(self, 'genre_input') else ""
        year = self.year_input.text().strip() if hasattr(self, 'year_input') else ""
        rating = self.rating_input.text().strip() if hasattr(self, 'rating_input') else ""

        conn = self.get_connection()
        if not conn:
            return
        cursor = conn.cursor()
        try:
            query = "SELECT id, Series_Title, Released_Year, Genre, IMDB_Rating, Director, CONCAT(Star1, ', ', Star2, ', ', Star3) FROM movies WHERE 1=1"
            params = []
            if search_term:
                query += " AND (Series_Title LIKE %s OR Director LIKE %s OR Star1 LIKE %s OR Star2 LIKE %s OR Star3 LIKE %s)"
                params.extend([f'%{search_term}%'] * 5)
            if genre:
                query += " AND Genre LIKE %s"
                params.append(f'%{genre}%')
            if year and year.isdigit() and len(year) == 4:
                query += " AND Released_Year = %s"
                params.append(int(year))
            if rating and rating.replace('.', '').isdigit():
                query += " AND IMDB_Rating >= %s"
                params.append(float(rating))
            query += " ORDER BY IMDB_Rating DESC"

            cursor.execute(query, params)
            results = cursor.fetchall()
            self.update_table(results)
            self.output_console.append("Query executed successfully")
            self.output_console.append(f"SQL: {query % tuple(params)}")
        except Error as e:
            self.output_console.append(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

    def update_table(self, results):
        """Update the table with results and selected columns."""
        column_map = {
            "title": "Series_Title",
            "year": "Released_Year",
            "genre": "Genre",
            "rating": "IMDB_Rating",
            "director": "Director",
            "stars": "CONCAT(Star1, ', ', Star2, ', ', Star3)"
        }
        visible_columns = ["id"] + [col for col in self.selected_columns]
        header_labels = ["ID"] + [col.capitalize() for col in self.selected_columns]
        self.table.setColumnCount(len(visible_columns))
        self.table.setHorizontalHeaderLabels(header_labels)
        self.table.setRowCount(len(results))

        for row_idx, row in enumerate(results):
            for col_idx, col in enumerate(visible_columns):
                value = row[0] if col == "id" else row[list(column_map.keys()).index(col) + 1] if col in column_map else ""
                item = QTableWidgetItem(str(value or ''))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_idx, col_idx, item)
        self.table.resizeColumnsToContents()

    def export_csv(self):
        """Export current table data to CSV."""
        if self.table.rowCount() == 0:
            self.output_console.append("No data to export!")
            return
        with open('exported_movies.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
            writer.writerow(headers)
            for row in range(self.table.rowCount()):
                row_data = [self.table.item(row, col).text() for col in range(self.table.columnCount())]
                writer.writerow(row_data)
            self.output_console.append(f"Exported {self.table.rowCount()} rows to exported_movies.csv")

    def get_connection(self):
        """Connect to MySQL database."""
        try:
            return mysql.connector.connect(**DB_CONFIG)
        except Error as e:
            self.output_console.append(f"Connection Error: {e}")
            return None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec())
