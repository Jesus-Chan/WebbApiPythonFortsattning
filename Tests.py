import unittest
from flask import Flask
from flask.testing import FlaskClient
from Manager import BookDatabaseManager

class TestAPIEndpoints(unittest.TestCase):
    def setUp(self):
        # Set up the Flask test client and BookDatabaseManager for testing
        from App import app
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.db_manager = BookDatabaseManager()

    def tearDown(self):
        # Disconnect from the database after each test
        if self.db_manager.connection:
            self.db_manager.disconnect_from_database()

    def test_retrieve_all_books(self):
        # Test the /books GET endpoint to retrieve all books
        response = self.client.get('/books')
        self.assertEqual(response.status_code, 200)
        # Check if the response contains the expected data
      

    def test_add_new_book(self):
        # Test the /books POST endpoint to add a new book
        data = {'title': 'Test Book', 'author': 'Test Author', 'summary': 'Test Summary', 'genre': 'Test Genre'}
        response = self.client.post('/books', json=data)
        self.assertEqual(response.status_code, 201)
        # Check if the book was added successfully in the database
        # (Add more assertions based on the actual response structure)

    def test_get_book_details(self):
        # Test the /books/<book_id> GET endpoint to get details of a specific book
        
        response = self.client.get('/books/1')
        self.assertEqual(response.status_code, 200)
        # Check if the response contains the expected data
       

    def test_update_book_info(self):
        # Test the /books/<book_id> PUT endpoint to update information of a specific book
        # (Assumes there is an existing book in the database with ID 1)
        data = {'title': 'Updated Title', 'author': 'Updated Author', 'summary': 'Updated Summary', 'genre': 'Updated Genre'}
        response = self.client.put('/books/1', json=data)
        self.assertEqual(response.status_code, 200)
        # Check if the book information was updated successfully in the database
      

    def test_remove_book(self):
        # Test the /books/<book_id> DELETE endpoint to remove a specific book
        # (Assumes there is an existing book in the database with ID 1)
        response = self.client.delete('/books/1')
        self.assertEqual(response.status_code, 200)
        # Check if the book was removed successfully from the database




if __name__ == '__main__':
    unittest.main()
