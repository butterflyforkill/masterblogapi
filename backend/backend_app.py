from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.exceptions import BadRequest
import json_parcer
from datetime import date, datetime
import time
import random


FILE_PATH = 'backend/data.json'
# USER_PATH = 'backend/users.json'

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

blog_posts = json_parcer.load_data(FILE_PATH)

SWAGGER_URL="/api/docs"  # (1) swagger endpoint e.g. HTTP://localhost:5002/api/docs
API_URL="/static/masterblog.json" # (2) ensure you create this dir and file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Masterblog API' # (3) You can change this if you like
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


def generate_timestamp_id():
    """
    Generate a unique timestamp-based ID for a new blog post.

    Returns:
    int: A unique ID based on the current timestamp and a random component.
    """
    timestamp = int(time.time() * 1000)  # Milliseconds
    random_part = random.randint(0, 999)  # Adjust range as needed
    return timestamp * 1000 + random_part


def parse_date(date_string):
    """
    Parse a date string into a date object.

    Args:
    date_string (str): The date string to be parsed.

    Returns:
    datetime.date: The parsed date object.
    """
    try:
        return datetime.datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        return date_string


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Retrieve all blog posts, with optional sorting parameters.

    Returns:
    flask.Response: A JSON response containing the sorted or unsorted blog posts.
    """
    sort_by = request.args.get('sort')
    direction_sort = request.args.get('direction', 'asc')

    if sort_by:
        if sort_by not in ['title', 'content', 'author', 'date']:
            raise BadRequest('Invalid sort field. Valid sort fields are: title, content, author, date')

        if sort_by == 'date':
            sorted_posts = sorted(blog_posts, key=lambda x: datetime.strptime(x.get('date'), '%Y-%m-%d'), reverse=(direction_sort=='desc'))
        else:
            sorted_posts = sorted(blog_posts, key=lambda x: x[sort_by], reverse=(direction_sort=='desc'))
    else:
        sorted_posts = blog_posts  # Return all posts without sorting

    return jsonify(sorted_posts)


@app.route('/api/posts', methods=['POST'])
def add_post():
    """
    Add a new blog post to the collection.

    Returns:
    flask.Response: A JSON response containing the newly added blog post,
    or an error message if the request is invalid.
    """
    data = request.get_json()
    if 'title' not in data or 'content' not in data or 'author' not in data:
        return jsonify({'error': 'Title, content and author are required'}), 400

    new_post = {
        'id': generate_timestamp_id(),
        'title': data['title'],
        'content': data['content'],
        'author': data['author'],
        'date': date.today().isoformat()
    }
    blog_posts.append(new_post)
    json_parcer.write_file(FILE_PATH, blog_posts)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
@cross_origin()
def delete_post(id):
    """
    Delete a blog post by its ID.

    Args:
    id (int): The ID of the post to be deleted.

    Returns:
    flask.Response: A JSON response confirming the deletion,
    or an error message if the post is not found.
    """
    for post in blog_posts:
        if post['id'] == id:
            blog_posts.remove(post)
            json_parcer.write_file(FILE_PATH, blog_posts)
            return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200
    return jsonify({"message": f"Post with id {id} was not found."}), 404


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    """
    Update a blog post by its ID.

    Args:
    id (int): The ID of the post to be updated.

    Returns:
    flask.Response: A JSON response containing the updated blog post,
    or an error message if the post is not found.
    """
    data = request.get_json()
    for post in blog_posts:
        if post['id'] == id:
            if "title" in data:
                post['title'] = data['title']
                json_parcer.write_file(FILE_PATH, blog_posts)
            if "content" in data:
                post['content'] = data['content']
                json_parcer.write_file(FILE_PATH, blog_posts)
            if "author" in data:
                post['author'] = data['author']
                json_parcer.write_file(FILE_PATH, blog_posts)
            response = {
                "id": post['id'],
                "title": post['title'],
                "content": post['content'],
                "author": post['author'],
                "date": date.today().isoformat()
            }
            return jsonify(response), 200
    return jsonify({"message": f"Post with id {id} was not found."}), 404    


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """
    Search for blog posts based on various criteria.

    Returns:
    flask.Response: A JSON response containing the matching blog posts.
    """
    search_title = request.args.get('title', '')
    search_content = request.args.get('content', '')

    matching_posts = []
    for post in blog_posts:
        is_title = (search_title and search_title.lower() in post['title'].lower()) 
        is_content = (search_content and search_content.lower() in post['content'].lower())
        if is_title or is_content:
            matching_posts.append(post)

    return jsonify(matching_posts)


@app.errorhandler(400)
def handle_bad_request(e):
    """
    Handle bad request errors.

    Args:
    e (werkzeug.exceptions.BadRequest): The BadRequest exception.

    Returns:
    flask.Response: A JSON response containing the error message for the bad request.
    """
    return jsonify({'error': 'Bad Request', 'message': str(e.description)}), 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
