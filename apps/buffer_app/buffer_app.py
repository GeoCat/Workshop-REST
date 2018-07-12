#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#http://0.0.0.0:5000/buffer?lon=41.4425&lat=-8.2918&range=1

import flask
from flask import request, make_response
from webargs import fields
from webargs.flaskparser import use_args

from shapely.geometry.point import Point
from shapely_geojson import dumps, Feature



app = flask.Flask(__name__)

input_args = {
        'lat': fields.Float(
            required=True,
            validate=lambda x:  -90.000 <= x <= 90.000
        ),
        'lon' : fields.Float(
            required=True,
            validate=lambda x:  -180.000 <= x <= 180.00
        ),
        'range' : fields.Float(
            required=True
            )
}


@app.route('/buffer')
@use_args(input_args)
def buffer(input_args):
    
    #Casting to float
    lat = float(input_args["lat"])
    lon = float(input_args["lon"])
    range = float(input_args["range"])
    
    
    p = Point(lon,lat)

    buffer = p.buffer(1.0)
    feature = Feature(buffer, properties={'buffer_extent': '1'})
    json_response = dumps(feature, indent=2)
    resp = make_response(json_response, 200)
    
    resp.mimetype = "application/vnd.geo+json" # So that browser knows what is the content type
    
    return resp
app.run(debug = True,host = "0.0.0.0", port = 5000)