#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#Necessary pip install: shapely and shapely_geojson
#sudo pip install shapely shapely_geojson
#sudo pip install git+https://github.com/alekzvik/shapely-geojson

from shapely.geometry.point import Point
from shapely_geojson import dumps, Feature
p = Point(-8.2918,41.4425) # (lon,lat) 41.4425° N, 8.2918° W

buffer = p.buffer(1.0)
feature = Feature(buffer, properties={'buffer_extent': '1'})
f1=open("./data/guimaraes_buffer.geojson","w")
f1.write(dumps(feature, indent=2))