from flask import Flask, jsonify, request
from Manager import DatabaseManager

app = Flask(__name__)
db_handler = DatabaseManager()

@app.route("/books", methods=["GET", "POST"])
def books_handler():
    if request.method == "GET":
        db_handler.connect_to_database()
        user_input = request.args

        if not user_input:
            result = db_handler.show_all_books()
            db_handler.disconnect_from_database()
            return jsonify(result)
        
        else:
            result = db_handler.filter_books(user_input)
            db_handler.disconnect_from_database()
            return jsonify(result)

    elif request.method == "POST":
        # Implement logic for adding books to the database
        pass

@app.route("/books/<int:book_id>", methods=["GET", "PUT", "DELETE"])
def book_details_handler(book_id):
    if request.method == "GET":
        db_handler.connect_to_database()
        result = db_handler.select_book_ID(book_id)
        db_handler.disconnect_from_database()
        return jsonify(result)

    elif request.method == "PUT":
        # Implement logic for updating book information
        pass

    elif request.method == "DELETE":
        # Implement logic for deleting a book
        pass

@app.route("/reviews", methods=["GET", "POST"])
def reviews_handler():
    if request.method == "GET":
        # Implement logic for fetching all reviews
        pass

    elif request.method == "POST":
        # Implement logic for adding a review
        pass

# Implement other endpoints (GET /reviews, GET /reviews/{book_id}, GET /books/top, GET /author)

if __name__ == "__main__":
    app.run(debug=True)
