#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# http://0.0.0.0:5000/search?name=Jorge
import flask
from flask import request, make_response
app = flask.Flask(__name__)

@app.route('/search')
def search():
    name = request.args.get('name')
    if name in ["John","Josh"]:
        code = 200
        resp = make_response("Found", code)
    else:
        code = 404
        resp = make_response("Not Found", code)

    return resp

app.run(debug = True,host = "0.0.0.0", port = 5000)

