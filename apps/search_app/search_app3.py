#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# http://0.0.0.0:5000/search?name=Jorge
import flask
from flask import request, make_response
app = flask.Flask(__name__)
from webargs import fields
from webargs.flaskparser import use_args

def is_valid_string(val):
    """You can cast '1234' to a number but not the way around"""
    try:
        float(val)
        return False
    except:
        return True

hello_args = {"name": fields.Str(required=True,validate=is_valid_string)} #It has to be a string
@app.route('/search')
@use_args(hello_args)
def search(name):
    if name in ["John","Josh"]:
        code = 200
        resp = make_response("Found", code)
    else:
        code = 404
        resp = make_response("Not Found", code)

    return resp

app.run(debug = True,host = "0.0.0.0", port = 5000)

