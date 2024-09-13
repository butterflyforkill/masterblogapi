from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    """
    Renders the home page template.

    Returns:
        flask.Response: The rendered HTML content of the 'index.html' template.
    """
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
