import sqlite3
import tkinter as tk
from tkinter import filedialog
import os

class DatabaseManager:

    def connect_to_database(self):
        """
        Connects to the SQLite database. If the database file doesn't exist,
        prompts the user to select a database file.
        """
        # Check if the database file exists
        if not os.path.exists(self.data_base):
            # Prompt user to select a database file
            self.root = tk.Tk()
            self.root.withdraw()
            self.data_base = filedialog.askopenfilename(title="Select Database File", filetypes=[("SQLite Database Files", "*.db")])
            self.root.destroy()

            if self.data_base:
                # If user selected a file, connect to the database
                self.connection = sqlite3.connect(self.data_base)
            else:
                print("File was not found!")
                exit()

        else:
            # If the database file exists, connect to it
            self.connection = sqlite3.connect(self.data_base)

        self.cursor = self.connection.cursor()
        return self.cursor
    
    def disconnect_from_database(self):
        """
        Disconnects from the database.
        """
        # Close the cursor and connection
        if self.cursor:
            self.cursor.close()

        if self.connection:
            self.connection.close()

    def show_all_books(self):
        """
        Retrieves all books from the database.
        """
        # Execute SQL query to select all books
        self.cursor.execute("SELECT * FROM Books")
        result = self.cursor.fetchall()
        return result

    def filter_books(self, filters):
        """
        Filters books based on user input parameters.

        Example: SELECT * FROM Books WHERE genre = 'biography'
        """
        # Construct and execute SQL query based on filters
        query = "SELECT * FROM Books WHERE "
        conditions = []

        for key, value in filters.items():
            conditions.append(f"{key} = '{value}'")

        query += " AND ".join(conditions)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def select_book_ID(self, book_id):
        """
        Selects a specific book by ID.
        """
        # Execute SQL query to select a book by ID
        self.cursor.execute("SELECT * FROM Books WHERE id = ?", (book_id,))
        result = self.cursor.fetchall()
        return result


    def add_book(self, title, author, summary, genre):
        """
        Adds a book to the database.
        """
        # Execute SQL query to insert a new book
        self.cursor.execute("INSERT INTO Books (title, author, summary, genre) VALUES (?, ?, ?, ?)",
                            (title, author, summary, genre))
        self.connection.commit()

    def edit_book(self, book_id, title, author, summary, genre):
        """
        Edits/update book information in the database.
        """
        # Execute SQL query to update book information
        self.cursor.execute("UPDATE Books SET title=?, author=?, summary=?, genre=? WHERE id=?",
                            (title, author, summary, genre, book_id))
        self.connection.commit()

    def remove_book(self, book_id):
        """
        Removes a book from the database.
        """
        # Execute SQL query to delete a book by ID
        self.cursor.execute("DELETE FROM Books WHERE id=?", (book_id,))
        self.connection.commit()

    def add_review(self, book_id, user, rating, review_text):
        """
        Adds a review for a specific book.
        """
        # Execute SQL query to insert a new review
        self.cursor.execute("INSERT INTO Reviews (book_id, user, rating, review_text) VALUES (?, ?, ?, ?)",
                            (book_id, user, rating, review_text))
        self.connection.commit()

    def show_all_reviews(self):
        """
        Retrieves all reviews from the database.
        """
        # Execute SQL query to select all reviews
        self.cursor.execute("SELECT * FROM Reviews")
        result = self.cursor.fetchall()
        return result

    def show_review_by_book(self, book_id):
        """
        Retrieves reviews for a specific book.
        """
        # Execute SQL query to select reviews for a specific book
        self.cursor.execute("SELECT * FROM Reviews WHERE book_id=?", (book_id,))
        result = self.cursor.fetchall()
        return result

    def show_top_books(self):
        """
        Retrieves the top-rated books.
        """
        # Execute SQL query to calculate average ratings and select top books
        self.cursor.execute("""
            SELECT Books.*, AVG(Reviews.rating) as avg_rating
            FROM Books LEFT JOIN Reviews ON Books.id = Reviews.book_id
            GROUP BY Books.id
            ORDER BY avg_rating DESC
            LIMIT 5
        """)
        result = self.cursor.fetchall()
        return result

    def show_author_info(self, author_name):
        """
        Retrieves information about the author from external APIs.
        """
        # Example: Use external API to get author summary
        author_summary_api = f"https://en.wikipedia.org/api/rest_v1/page/summary/{author_name}"
        # Use requests library or another method to make an API call
        # Example with requests library: response = requests.get(author_summary_api)
        # Extract relevant information from the API response
        # Return the extracted information




DatabaseManager()