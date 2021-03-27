from flask import Flask, render_template, request, jsonify, make_response, send_from_directory, abort
import json
# Source https://realpython.com/python-memcache-efficient-caching/
from pymemcache.client import base


def get_price_data(cache):
    rv = cache.get('price_data')
    if rv is None:
        cache.set('price_data', json.dumps([0]))
        return [0]
    return json.loads(rv)


def get_user_data(cache, user_id):
    rv = cache.get(str(user_id))
    if rv is None:
        cache.set(user_id, json.dumps({"shares":0, "cash":100, "bid":{"price":0, "quantity":0}, "offer":{"price":0, "quantity":0}}))
        return json.loads(cache.get(user_id))
    else:
        return json.loads(rv)


def update_user_data(cache, user_data):
    user_id = user_data["user_id"]
    if "bid" in user_data:
        # given the old user data variable becomes the new user data
        # a better name should probably be chosen
        old_user_data = json.loads(cache.get(str(user_id)))
        old_user_data["bid"] = user_data["bid"]
        cache.set(str(user_id), json.dumps(old_user_data))
    if "offer" in user_data:
        # given the old user data variable becomes the new user data
        # a better name should probably be chosen
        old_user_data = json.loads(cache.get(str(user_id)))
        old_user_data["offer"] = user_data["offer"]
        cache.set(str(user_id), json.dumps(old_user_data))
    
        
    



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
    # needs some extra validation on the structure of the payload
    try:
        payload = request.json
    except (TypeError) as ex:
        print(ex)
        abort(400)
    if payload.get("user_id") is None:
        abort(400)
    else:
        user_id = payload["user_id"]
    cache = base.Client(('127.0.0.1', 11211,))
    update_user_data(cache, payload)
    response = {"price_data": get_price_data(cache), "user_data":get_user_data(cache, user_id)}
    cache.close()
    return jsonify(response)


if __name__ == "__main__":
    app.run(port=8008, host="0.0.0.0")
