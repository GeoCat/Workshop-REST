#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import flask

app = flask.Flask(__name__)

@app.route('/welcome')
def welcome():
    return 'Bem vindos a Guimaraes'

app.run(debug = True,host = "0.0.0.0", port = 5000)

