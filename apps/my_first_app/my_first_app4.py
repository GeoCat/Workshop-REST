#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import flask
from flask import request
app = flask.Flask(__name__)

@app.route('/welcome')
def welcome():
    name = request.args.get('name')
    return 'Bem vindos a Guimaraes. {}'.format(name)

app.run(debug = True,host = "0.0.0.0", port = 5000)

