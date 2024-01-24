# Manager.py

import sqlite3
import tkinter as tk
from tkinter import filedialog
import os

class BookDatabaseManager:

    def __init__(self):
        self.connection = None
        self.cursor = None
        # Initialize the manager with a flag to track whether a disconnect attempt has been made
        self.disconnect_attempted = False

    def connect_to_database(self):
        # Establish a connection to the SQLite database
        if not self.connection:
            self.connection = sqlite3.connect('Book_Reviews.db')
            self.cursor = self.connection.cursor()

        if not os.path.exists(self.data_base):
            self.root = tk.Tk()
            self.root.withdraw()
            self.data_base = filedialog.askopenfilename(
                title="Select Database File", filetypes=[("SQLite Database Files", "*.db")]
            )
            self.root.destroy()

            if self.data_base:
                self.connection = sqlite3.connect(self.data_base)
            else:
                print("File was not found!")
                exit()
        else:
            self.connection = sqlite3.connect(self.data_base)

        self.cursor = self.connection.cursor()
        return self.cursor

    def disconnect_from_database(self):
        # Disconnect from the database, and reset connection and cursor attributes
        if self.cursor:
            try:
                self.cursor.close()
            except sqlite3.ProgrammingError:
                pass  # Cursor was already closed

        if self.connection:
            try:
                self.connection.close()
            except sqlite3.ProgrammingError:
                pass  # Connection was already closed

    def retrieve_all_books(self):
        # Retrieve all books from the database
        self.cursor.execute("SELECT Books.*, AVG(Reviews.Rating) AS AvgRating "
                            "FROM Books LEFT JOIN Reviews ON Books.BookID = Reviews.BookID "
                            "GROUP BY Books.BookID")
        result = self.cursor.fetchall()
        return result

    def filter_books(self, filters):
        # Filter books based on user-provided conditions
        query = "SELECT Books.*, AVG(Reviews.Rating) AS AvgRating FROM Books " \
                "LEFT JOIN Reviews ON Books.BookID = Reviews.BookID " \
                "WHERE "
        conditions = []

        for key, value in filters.items():
            conditions.append(f"{key} = ?", (value,))

        query += " AND ".join(conditions)
        query += " GROUP BY Books.BookID"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result


    def select_book_by_id(self, book_id):
        self.connect_to_database()
        self.cursor.execute("SELECT Books.*, AVG(Reviews.Rating) AS AvgRating "
                            "FROM Books LEFT JOIN Reviews ON Books.BookID = Reviews.BookID "
                            "WHERE Books.BookID = ? "
                            "GROUP BY Books.BookID", (book_id,))
        result = self.cursor.fetchall()
        self.disconnect_from_database()
        return result

    def update_book_info(self, book_id, title, author, summary, genre):
        self.connect_to_database()
        self.cursor.execute("UPDATE Books SET Title=?, Author=?, Summary=?, Genre=? WHERE BookID=?",
                            (title, author, summary, genre, book_id))
        self.connection.commit()
        self.disconnect_from_database()

    def add_new_book(self, title, author, summary, genre):
        self.connect_to_database()
        self.cursor.execute("INSERT INTO Books (Title, Author, Summary, Genre) VALUES (?, ?, ?, ?)",
                            (title, author, summary, genre))
        self.connection.commit()
        self.disconnect_from_database()

    def remove_book_by_id(self, book_id):
        self.connect_to_database()
        self.cursor.execute("DELETE FROM Books WHERE BookID=?", (book_id,))
        self.connection.commit()
        self.disconnect_from_database()

    def add_review(self, book_id, user, rating, review_text):
        self.connect_to_database()
        self.cursor.execute("INSERT INTO Reviews (BookID, User, Rating, ReviewText) VALUES (?, ?, ?, ?)",
                            (book_id, user, rating, review_text))
        self.connection.commit()
        self.disconnect_from_database()

    def get_all_reviews(self):
        self.connect_to_database()
        self.cursor.execute("SELECT * FROM Reviews")
        result = self.cursor.fetchall()
        self.disconnect_from_database()
        return result

    def get_reviews_by_book_id(self, book_id):
        self.connect_to_database()
        self.cursor.execute("SELECT * FROM Reviews WHERE BookID=?", (book_id,))
        result = self.cursor.fetchall()
        self.disconnect_from_database()
        return result

    def get_top_rated_books(self):
        self.connect_to_database()
        self.cursor.execute("""
            SELECT Books.*, AVG(Reviews.Rating) AS AvgRating
            FROM Books LEFT JOIN Reviews ON Books.BookID = Reviews.BookID
            GROUP BY Books.BookID
            ORDER BY AvgRating DESC
            LIMIT 5
        """)
        result = self.cursor.fetchall()
        self.disconnect_from_database()
        return result

    def get_author_information(self, author_name):
        author_summary_api = f"https://en.wikipedia.org/api/rest_v1/page/summary/{author_name}"
    
        return None

BookDatabaseManager()
