#!/bin/sh

# GDAL
wget http://download.osgeo.org/gdal/gdal-1.6.0.tar.gz
tar xzf gdal-1.6.0.tar.gz
cd gdal-1.6.0
./configure
make
sudo make install
