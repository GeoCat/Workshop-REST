#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#http://0.0.0.0:5000/buffer?lon=41.4425&lat=-8.2918&range=1

import flask
from flask import request, make_response
from webargs import fields
from webargs.flaskparser import use_args

from shapely.geometry.point import Point
from shapely_geojson import dumps, Feature

from flasgger import Swagger,swag_from

import copy

import time

from osgeo import gdal
import struct

app = flask.Flask(__name__)

#Need to update the app to support swagger
Swagger(app)

input_args_pixel = {
        'lat': fields.Float(
            required=True,
            validate=lambda x:  -90.000 <= x <= 90.000
        ),
        'lon' : fields.Float(
            required=True,
            validate=lambda x:  -180.000 <= x <= 180.00
        )
}
range_input ={
    'range' : fields.Float(
            required=True
            )
    }


input_args_buffer =  copy.deepcopy(input_args_pixel).update(range_input) 


@app.route('/buffer')
@use_args(input_args_buffer)
@swag_from("buffer.yml")
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




@app.route('/query')
@use_args(input_args_pixel)
@swag_from("query.yml")
def query(input_args):
    
    datatype_2_struct = {1:'B',3:'h',5:'i',6:'f'} 
    raster_file = "PHIHOX_M_sl1_10km_ll.tif"

    lon = float(input_args["lon"])
    lat = float(input_args["lat"])
     
    data_source = gdal.Open(raster_file)

    geo_transform = data_source.GetGeoTransform() #array with information on coordinate system and orientation of image

    x_pixel = int((lon - geo_transform[0]) / geo_transform[1]) #x pixel
    y_pixel = int((lat - geo_transform[3]) / geo_transform[5])
    raster_data = data_source.GetRasterBand(1)

    structval=raster_data.ReadRaster(x_pixel,y_pixel,1,1,buf_type=raster_data.DataType) #reading only one pixel
    intval = struct.unpack(datatype_2_struct[raster_data.DataType] , structval) #transform from binary to integer
    intval = intval[0]
    
    data_dic={}
    data_dic["pixel_value"] = intval
    data_dic["source"] = raster_file
    data_dic["time"] = time.time()
    
    resp = flask.jsonify(**data_dic)
    
    return resp

