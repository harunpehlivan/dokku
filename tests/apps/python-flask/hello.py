import os
from flask import Flask, abort

app = Flask(__name__)

@app.route('/')
def hello():
        return 'python/flask'


@app.route('/<env>')
def get_enc(env):
        if val := os.environ.get(env, None):
                return val
        else:
                abort(404)
