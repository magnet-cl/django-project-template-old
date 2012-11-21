#!/bin/bash
# from https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/geolibs/

#django recomended to install this libraries, but I have no idea what they do
sudo apt-get install binutils libproj-dev gdal-bin

# GEOS is a C++ library for performing geometric operations, and is the default
# internal geometry representation used by GeoDjango (it's behind the "lazy"
# geometries). Specifically, the C API library is called (e.g., libgeos_c.so)
# directly from Python using ctypes.
wget http://download.osgeo.org/geos/geos-3.3.5.tar.bz2
tar xjf geos-3.3.5.tar.bz2
cd geos-3.3.5
./configure
make
sudo make install
cd ..
rm -rf geos-3.3.5.tar.bz2
rm -rf geos-3.3.5


# REQUIRED BY POSTGRES
echo "Are you going to use postgre for your database? [N/y]"
read INSTALL_POSTGRE
if [[ "$INSTALL_POSTGRE" == "y" ]]
then
    #PROJ.4 is a library for converting geospatial data to different coordinate
    #reference systems.
    wget http://download.osgeo.org/proj/proj-4.8.0.tar.gz
    wget http://download.osgeo.org/proj/proj-datumgrid-1.5.tar.gz
    # Next, untar the source code archive, and extract the datum shifting files
    # in the nad subdirectory. This must be done prior to configuration:
    tar xzf proj-4.8.0.tar.gz
    cd proj-4.8.0/nad
    tar xzf ../../proj-datumgrid-1.5.tar.gz
    cd ..
    #Finally, configure, make and install PROJ.4:
    ./configure
    make
    sudo make install
    cd ..
    rm -rf proj-4.8.0.tar.gz
    rm -rf proj-4.8.0
    rm -rf roj-datumgrid-1.5.tar.gz
    rm -rf roj-datumgrid-1.5
else
    echo "Are you going to use sqlite for your database? [N/y]"
    read INSTALL_SQLITE
fi

if [[ "$INSTALL_POSTGRE" == "y" || "$INSTALL_SQLITE" == "y" ]]
then
    #!!!GEOS, PROJ.4 and GDAL should be installed prior to building PostGIS

    # GDAL is an excellent open source geospatial library that has support for
    # reading most vector and raster spatial data formats. Currently, GeoDjango
    # only supports GDAL's vector data capabilities [2]. GEOS and PROJ.4 should
    # be installed prior to building GDAL.

    # First download the latest GDAL release version and untar the archive:
    wget http://download.osgeo.org/gdal/gdal-1.9.1.tar.gz
    tar xzf gdal-1.9.1.tar.gz
    cd gdal-1.9.1
    ./configure
    make
    sudo make install
    cd ..
    rm -rf gdal-1.9.1.tar.gz
    rm -rf gdal-1.9.1
fi

###https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/postgis/ ##
if [[ "$INSTALL_POSTGRE" == "y" ]]
then
    wget http://postgis.refractions.net/download/postgis-2.0.1.tar.gz
    tar xzf postgis-2.0.1.tar.gz
    cd postgis-2.0.1
    ./configure
    make
    sudo make install
    cd ..
    rm -rf postgis-2.0.1.tar.gz
    rm -rf postgis-2.0.1
fi

###https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/postgis/ ##
if [[ "$INSTALL_SQLITE" == "y" ]]
then
    # !!! GEOS and PROJ.4 should be installed prior to building SpatiaLite.
    echo "Not implemented yet :'("
fi
