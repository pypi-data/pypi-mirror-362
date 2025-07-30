.. _night_osm:

======================
Night OSM Registration
======================

This tool performs night visible data registration based on OSM reference.

Single tool installation procedure
===============================

To install NightOsmRegistration, please launch the following commands :

.. code-block:: console

    conda create -n nightosm_env python=3.12 libgdal=3.11.0 markupsafe -c conda-forge
    conda activate nightosm_env
    pip install eolabtools[NightOsmReg]


Steps of the algorithm
======================

A city seen from above at night can be compared to a city map.

Here are the main steps of the algorithm :

1 - Radiance image thresholding and binarization.

2 - Extraction of OpenStreetMap layers (buildings, streets, bridges...) and binarization.

The resulting OSM raster should be as close as possible to the binarized input image.

3 - Tiling of the two rasters and computation of a row and column offset for each tile using spectral cross correlation.

4 - Computation of a global registration grid with the same geometry as the input file by interpolation of the shift values of
each tile. It is possible to keep the shift values at the center of the subtiles and force the interpolation at the subtile edges
or to interpolate on all the subtiles.

5 - Application of the grid on the radiance image.


Input files and configuration
==========================

Main configuration file
-----------------------

A main configuration file is needed to run the tool. A template is available `here <https://github.com/CNES/eolabtools/blob/main/docs/source/nightosm_doc/ex_config.yml>`_.


OSM extraction configuration
----------------------------

OSM layer extraction is handled by a configuration file.
See two examples with `simple <https://github.com/CNES/eolabtools/blob/main/docs/source/nightosm_doc/ex_osm_config_simple.yml>`_
and `subtracted <https://github.com/CNES/eolabtools/blob/main/docs/source/nightosm_doc/ex_osm_config_subtracted.yml>`_
methods.

**Simple :** Road vectors are simply rasterized (small memory footprint)

**Subtracted :** Everything else is rasterized and subtracted to obtain roads (huge memory footprint)

Using night_osm_image_registration
==================================

Input file
----------

*night_osm_image_registration* takes as input a RGB image or an image with total radiance information. In the first case, the algorithm computes the
total radiance via a composition of RGB bands.

Command line
------------

Use the command ``night_osm_image_registration`` with the following arguments :

.. code-block:: console

    night_osm_image_registration /path_to_input_files/input_file_1.tif [/path_to_input_files/input_file_2.tif] [...]
                                 -o /path_to_output_directory/output_directory/
                                 --config /path_to_config_directory/config_file_name
                                 --osm-config /path_to_config_directory/osm_config_file_name

Arguments are the following :

- ``infile`` : Reference input image to compute shift grid

- ``auxfiles`` : Optional list of additional images to shift based on the same grid

- ``-o``, ``--outdir`` : Output files location

- ``--config`` : Path to the main configuration file

- ``--osm-config`` : Path to the OSM configuration file with tags to keep in binary raster


Output files
------------

The following files are generated (XXXX being the reference image) :

    - ``XXXX_cropped.tif`` : Radiance raster cropped to the ROI

    - ``XXXX_binary.tif`` : Binarized cropped input raster

    - ``XXXX_osm.tif`` : Binarized OSM raster with same extent as input image

    In a directory `XXXX_MS_WS_SS/` (MS=max shift, WS=windows size, SS=sub sampling) :

    - ``XXXX_shifted.tif`` : Input ref or aux image shifted in x and y using displacement_grid.tif. Band 1 of the displacement grid corresponds to X shift, and band 2 to Y shift.

    - ``row/column_offset_position/value.csv`` : Value and position (center of subtile) of shifts before MS filtering.

    - ``shift_mask.tif`` : Mask with a shift arrow in the center of each subtile before filtering

    - ``filtered_shift_mask.tif`` : Mask with a shift arrow in the center of each subtile after filtering


Using night_osm_vector_registration
==================================

Input file
----------

The *night_osm_vector_registration* command allows to apply a displacement grid on vectors, for instance, on radiance peaks
(only geometry of type "Point" is handled at the moment).

Command line
------------

Use the command ``night_osm_vector_registration`` with the following arguments :

.. code-block:: console

    night_osm_vector_registration /path_to_points/points.gpkg
                                  /path_to_displacement_grid/displacement_grid.tif
                                  -o /path_to_output_directory/output_directory/
                                  -n output_file_basename


Arguments are the following :

- ``invector`` : Path to the input vector file.

- ``grid`` : Path to the displacement grid (band1 : shift along X in pixels, band 2 : shift along Y in pixels).

- ``-o``, ``--outdir`` : Output directory.

- ``-n``, ``--name`` : Basename for the output file.

Output files
------------

The following file is generated (XXXX being the basename) :

- ``XXXX.gpkg`` : It contains the geometries of the input file shifted in X and Y according to the input displacement grid.

Advices
=======

Dataset not available in pyrosm
-------------------------------

If the chosen city_name is not directly available in pyrosm, you can download the OSM "Protocolbuffer Binary Format" file (`.pbf`)
you need in the free `Geofabrik server <https://download.geofabrik.de/>`_. As the minimum distribution level for these files is
the region, you can use the `Osmium <https://osmcode.org/osmium-tool/index.html>`_
library to crop the `.pbf` file in the desired zone. Once `Osmium installation <https://osmcode.org/osmium-tool/manual.html>`_
is done, you can use the following command:

.. code-block:: console

    osmium extract -p zone.geojson region.osm.pbf -o zone.osm.pbf


- ``zone.geojson`` contains the polygon defining the zone to crop. Must be a geojson file.

- ``region.osm.pbf`` is the `.pbf` file downloaded from Geofabrik server.

- ``zone.osm.pbf`` is the output path of the cropped `.pbf` file.


Water shapefile
---------------

By default, an extraction of water osm layers is done with pyrosm, however the result is not satisfactory.
A better water layer can be computed with the following procedure using QuickOSM in QGIS:

- QuickOSM : get a water-river layer with the request ``natural=water + water=river``.

- QuickOSM : get a residential layer with the request ``landuse = residential``

- Compute a islands layer = intersection(water-river, residential). May need to clean manually polygons.

- Compute a layer ``river = water_river - islands``.

- Compute the final water layer as : ``(natural = water) - water_river + river``.
