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
    timestamp = int(time.time() * 1000)  # Milliseconds
    random_part = random.randint(0, 999)  # Adjust range as needed
    return timestamp * 1000 + random_part


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(blog_posts)


@app.route('/api/posts', methods=['POST'])
def add_post():
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
    for post in blog_posts:
        if post['id'] == id:
            blog_posts.remove(post)
            json_parcer.write_file(FILE_PATH, blog_posts)
            return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200
    return jsonify({"message": f"Post with id {id} was not found."}), 404


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
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
    search_title = request.args.get('title')
    search_content = request.args.get('content')
    search_author = request.args.get('author')
    search_date = request.args.get('date')

    matching_posts = []
    for post in blog_posts:
        is_title = (search_title and search_title.lower() in post['title'].lower()) 
        is_content = (search_content and search_content.lower() in post['content'].lower())
        is_author = (search_author and search_author.lower() in post['author'].lower())
        is_date = (search_date in post['date'].lower())
        if is_title or is_content or is_author or is_date:
            matching_posts.append(post)

    return jsonify(matching_posts)


@app.errorhandler(400)
def handle_bad_request(e):
    return jsonify({'error': 'Bad Request', 'message': str(e.description)}), 400


# this sorting thing doesn't work proparly, need to think about  it !!!!!!
@app.route('/api/posts', methods=['GET'])
def sort_posts():
    sort_by = request.args.get('sort')
    direction_sort = request.args.get('direction')
    sorted_posts = blog_posts

    if direction_sort not in ['asc', 'desc']:
        raise BadRequest('Invalid direction. Direction must be "asc" or "desc"')

    if sort_by not in ['title', 'content', 'author', 'date']:
        raise BadRequest('Invalid sort field. Valid sort fields are: title, content, author, date')

    if sort_by and direction_sort:
        if sort_by == 'date':
            sorted_posts = sorted(blog_posts, key=lambda x: datetime.strptime(x.get('date'), '%Y-%m-%d'), reverse=(direction_sort=='desc'))
        else:
            sorted_posts = sorted(blog_posts, key=lambda x: x[sort_by], reverse=(direction_sort=='desc' and True or False))

    return jsonify(sorted_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
