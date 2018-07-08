#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# GDAL is already install in osgeo
# PHIHOX_M_sl1_10km_ll.tif soil ph at 10km resolution
# geotranform --> (-180.0, 0.1, 0.0, 83.99916720600001, 0.0, -0.1) --> pixel resolution:0.1
# datatype_2_struct From GDAL codes 1--> Byte,Int16-->3, Float32-->6  http://www.gdal.org/gdal_8h.html
# we need to convert the binary code into an integer number we need struct for it

from osgeo import gdal
import struct

datatype_2_struct = {1:'B',3:'h',5:'i',6:'f'} 

x_coord = -8.2918
y_coord = 41.4425
raster_file = "./data/PHIHOX_M_sl1_10km_ll.tif" 

data_source = gdal.Open(raster_file)

geo_transform = data_source.GetGeoTransform() #array with information on coordinate system and orientation of image

x_pixel = int((x_coord - geo_transform[0]) / geo_transform[1]) #x pixel
y_pixel = int((y_coord - geo_transform[3]) / geo_transform[5])

raster_data = data_source.GetRasterBand(1)

structval=raster_data.ReadRaster(x_pixel,y_pixel,1,1,buf_type=raster_data.DataType) #reading only one pixel
intval = struct.unpack(datatype_2_struct[raster_data.DataType] , structval) #transform from binary to integer

print(intval)
