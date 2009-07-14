# Proj.4
wget http://download.osgeo.org/proj/proj-4.6.1.tar.gz
wget http://download.osgeo.org/proj/proj-datumgrid-1.4.tar.gz
tar xzf proj-4.6.1.tar.gz
cd proj-4.6.1/nad
tar xzf ../../proj-datumgrid-1.4.tar.gz
cd ..
./configure --prefix=/usr
make && sudo make install
