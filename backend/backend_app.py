from flask import Flask, jsonify, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import uuid
from werkzeug.exceptions import BadRequest
import json_parcer

FILE_PATH = 'backend/data.json'
# USER_PATH = 'backend/users.json'

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

blog_posts = json_parcer.load_data(FILE_PATH)
users = []

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


# User class for Flask-Login
class User(UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    user = next((u for u in users if u.id == user_id), None)
    return user

# User Registration Endpoint
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = User(username, password)
    users.append(user)
    return 'User registered successfully', 201

# User Login Endpoint
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = next((u for u in users if u.id == username and u.password == password), None)
    if user:
        login_user(user)
        return 'Login successful', 200
    else:
        return 'Invalid username or password', 401


# Logout Endpoint
@app.route('/api/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return 'Logged out successfully', 200


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(blog_posts)


@app.route('/api/posts', methods=['POST'])
@login_required
def add_post():
    data = request.get_json()
    if 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Title and content are required'}), 400

    new_post = {
        'id': int(uuid.uuid4().int),
        'title': data['title'],
        'content': data['content']
    }
    blog_posts.append(new_post)
    json_parcer.write_file(FILE_PATH, blog_posts)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
@login_required
def delete_post(id):
    for post in blog_posts:
        if post['id'] == id:
            blog_posts.remove(post)
            json_parcer.write_file(FILE_PATH, blog_posts)
            return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200
    return jsonify({"message": f"Post with id {id} was not found."}), 404


@app.route('/api/posts/<int:id>', methods=['PUT'])
@login_required
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
            response = {
                "id": post['id'],
                "title": post['title'],
                "content": post['content']
            }
            return jsonify(response), 200
    return jsonify({"message": f"Post with id {id} was not found."}), 404    


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    search_title = request.args.get('title')
    search_content = request.args.get('content')

    matching_posts = []
    for post in blog_posts:
        if (search_title and search_title.lower() in post['title'].lower()) or (search_content and search_content.lower() in post['content'].lower()):
            matching_posts.append(post)

    return jsonify(matching_posts)


@app.errorhandler(400)
def handle_bad_request(e):
    return jsonify({'error': 'Bad Request', 'message': str(e.description)}), 400


@app.route('/api/posts', methods=['GET'])
def sort_posts():
    sort_by = request.args.get('sort')
    direction_sort = request.args.get('direction')
    sorted_posts = blog_posts

    if direction_sort not in ['asc', 'desc']:
        raise BadRequest('Invalid direction. Direction must be "asc" or "desc"')

    if sort_by not in ['title', 'content']:
        raise BadRequest('Invalid sort field. Valid sort fields are: title, content')

    if sort_by and direction_sort:
        if direction_sort == 'desc':
            sorted_posts = sorted(blog_posts, key=lambda x: x[sort_by], reverse=True)
        else:
            sorted_posts = sorted(blog_posts, key=lambda x: x[sort_by], reverse=False)

    return jsonify(sorted_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
