# App.py

from flask import Flask, jsonify, request
from Manager import BookDatabaseManager

app = Flask(__name__)
db_handler = BookDatabaseManager()

@app.route("/books", methods=["GET", "POST"])
def books_handler():
    db_handler.connect_to_database()
    if request.method == "GET":
        # Handle GET request to retrieve books
        db_handler.connect_to_database()
        user_input = request.args

        if not user_input:
            result = db_handler.retrieve_all_books()
            db_handler.disconnect_from_database()
            return jsonify(result)
        
        else:
            result = db_handler.filter_books(user_input)
            db_handler.disconnect_from_database()
            return jsonify(result)

    elif request.method == "POST":
        try:
            # Handle POST request to add a new book
            data = request.json
            db_handler.connect_to_database()
            db_handler.add_new_book(data['title'], data['author'], data['summary'], data['genre'])
            db_handler.disconnect_from_database()
            return jsonify({"message": "Book added successfully"}), 201
        except Exception as e:
            # Log the exception or handle it appropriately
            db_handler.disconnect_from_database()
            return jsonify({"error": "Internal Server Error"}), 500
        


@app.route("/books/<int:book_id>", methods=["GET", "PUT", "DELETE"])
def book_details_handler(book_id):
    if request.method == "GET":
        db_handler.connect_to_database()
        result = db_handler.select_book_by_id(book_id)
        db_handler.disconnect_from_database()
        return jsonify(result)

    elif request.method == "PUT":
        data = request.json
        db_handler.update_book_info(book_id, data['title'], data['author'], data['summary'], data['genre'])
        db_handler.disconnect_from_database()
        return jsonify({"message": "Book updated successfully"})

    elif request.method == "DELETE":
        db_handler.remove_book_by_id(book_id)
        db_handler.disconnect_from_database()
        return jsonify({"message": "Book removed successfully"})

@app.route("/reviews", methods=["GET", "POST"])
def reviews_handler():
    if request.method == "GET":
        db_handler.connect_to_database()
        result = db_handler.get_all_reviews()
        db_handler.disconnect_from_database()
        return jsonify(result)

    elif request.method == "POST":
        data = request.json
        db_handler.add_review(data['book_id'], data['user'], data['rating'], data['review_text'])
        db_handler.disconnect_from_database()
        return jsonify({"message": "Review added successfully"}), 201

@app.route("/reviews/<int:book_id>", methods=["GET"])
def reviews_by_book_handler(book_id):
    db_handler.connect_to_database()
    result = db_handler.get_reviews_by_book_id(book_id)
    db_handler.disconnect_from_database()
    return jsonify(result)

@app.route("/books/top", methods=["GET"])
def top_books_handler():
    db_handler.connect_to_database()
    result = db_handler.get_top_rated_books()
    db_handler.disconnect_from_database()
    return jsonify(result)

@app.route("/author", methods=["GET"])
def author_info_handler():
    author_name = request.args.get("name")
    db_handler.connect_to_database()
    result = db_handler.get_author_information(author_name)
    db_handler.disconnect_from_database()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
