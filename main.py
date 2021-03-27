from flask import Flask, render_template, request, jsonify, make_response, send_from_directory
# Source https://realpython.com/python-memcache-efficient-caching/
from pymemcache.client import base
cache = base.Client(('127.0.0.1', 11211,))


def get_price_data():
    rv = cache.get('price_data')
    if rv is None:
        cache.set('price_data', [0])
        return [0]
    return rv


def get_user_data(user_id):
    rv = cache.get(user_id)
    if rv is None:
        cache.set(user_id, {"shares":0, "cash":100, "bid":{"price":0, "quantity":0}, "offer":{"price":0, "quantity":0}})
        return cache.get(user_id)
    else:
        return rv



app = Flask(__name__)


@app.route("/")
def index():
    """ Route to render the HTML """
    return render_template("index.html")


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('templates/js', path)


@app.route("/update", methods=["POST"])
def update():
    user_id = request.json()["user_id"]
    response = {"price_data": get_price_data(), "user_data":get_user_data(user_id)}
    return jsonify(response)


if __name__ == "__main__":
    app.run(port=8008, host="0.0.0.0")
