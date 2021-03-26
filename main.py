from flask import Flask, render_template, request, jsonify, make_response
# Source https://realpython.com/python-memcache-efficient-caching/
from pymemcache.client import base
cache = base.Client(('127.0.0.1', 11211,))


def get_my_item():
    rv = cache.get('my-item')
    if rv is None:
        cache.set('my-item', "1")
    else:
        rv = int(rv)
        rv += 1
        cache.set('my-item', str(rv))
    return rv

app = Flask(__name__)

@app.route("/")
def index():
    """ Route to render the HTML """
    return render_template("index.html")



if __name__ == "__main__":
    app.run(port=8008, host="0.0.0.0")
