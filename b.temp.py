#!/usr/bin/env python3
'''
	10.08.2023
	Robert Folkenberg Siro
	Nuclear Eng. & Thermal Physics, NRNU MEPhI
	Geospatial (Optical Multispectral & Hyperspectral RS), The Technical University of Kenya 2019
'''

from osgeo import gdal; import numpy;

band_no=input('ENTER BAND NUMBER: ');
band_no=int(band_no);
if band_no in(10,11):
  band="LC08_L1TP_170061_20190215_20200829_02_T1_B";
  met="LC08_L1TP_170061_20190215_20200829_02_T1_MTL.txt";
  MTL=open(met, 'r');

  def build_dict(MTL):
  	output={};
  	for var in MTL.readlines():
  		if '=' in var:
  			line=var.split('=');
  			output[line[0].strip()]=line[1].strip();
  	return output;
  data=build_dict(MTL);
  if band_no==10:
  	K_1=float(data['K1_CONSTANT_BAND_10']);
  	K_2=float(data['K2_CONSTANT_BAND_10']);
  else:
  	K_1=float(data['K1_CONSTANT_BAND_11']);
  	K_2=float(data['K2_CONSTANT_BAND_11']);
  from_dir="./input";
  xrad_ds=gdal.Open(from_dir+band+str(band_no)+'.TIF');
  xrad=xrad_ds.GetRasterBand(1);
  L=xrad.ReadAsArray();

  def rad_btemp(L,K_1,K_2):
  	return (((K_2)/(numpy.log((K_1/L)+1)))-273.15);
  L=L.astype(numpy.float64);
  btemp=rad_btemp(L,K_1,K_2);
  to_dir="./output/b.temperature/";
  new_btemp=gdal.GetDriverByName('GTiff').Create(\
  	to_dir+band+str(band_no)+'.TIF',\
  	xrad_ds.RasterXSize,xrad_ds.RasterYSize,1,\
  gdal.GDT_Float32);
  new_btemp.SetProjection(xrad_ds.GetProjection());
  new_btemp.SetGeoTransform(xrad_ds.GetGeoTransform());
  new_fil = new_btemp.GetRasterBand(1)
  new_fil.WriteArray(btemp);
  print ('CONVERSION COMPLETED...');
else:
  print ('Unrecognized user input');
