from flask import Flask, jsonify
import redis

app = Flask(__name__)
redis_cli = redis.Redis(host="localhost", port=6379, db=0)


@app.route("/")
def test_hello():
    return jsonify("hello")


@app.route("/get/<key>")
def redis_get(key):
    res = redis_cli.get(key)
    return jsonify(f"success: {res}")


@app.route("/set/<key>/<value>")
def redis_set(key, value):
    res = redis_cli.set(name=key, value=value, ex=10)
    return jsonify(f"success: {res}")
