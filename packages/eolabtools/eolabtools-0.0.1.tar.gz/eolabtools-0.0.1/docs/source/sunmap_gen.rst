.. _sunmap_gen:

==================
Sun Map Generation
==================

SunMapGeneration generates a map per date with the percentage of sun exposure over the time range, as well as a vector file that
gives the transition times from shade to sun (and sun to shade) for each pixel at the first date.
It takes as inputs a Digital Surface Model (DSM) of the area of interest, a range of dates and a time range per date of your choice.
Shadow masks can also be produced at each step.

*Please note that the time range is given in the local time of the area of interest.*

If the area of interest is important, the DSM should be divided into tiles beforehand (typically 1km*1km). The list of tiles is
given as input. The tool will manage the shadow impact on adjacent tiles.


.. figure:: _static/sunmap/sunmap_illustration.png
   :alt:
   :width: 50.0%
   :align: center

   Example of sun exposure maps at winter and summer solstices


Steps of the algorithm
======================

Here are the main steps of the algorithm :

- Compute elevation and azimuth angles of the Sun at the center of each tile for each time step in the time range and date range.

- Compute the corresponding shadow masks.

- Generate the “sun map” at each date.

- Generate the sun to shade transitions vector file.


Single tool installation procedure
==================================

To install SunMapGeneration, please launch the following commands :

.. code-block:: console

    conda create -n sunmap_env python=3.12 libgdal=3.5.0 -c conda-forge -c defaults -y
    conda activate sunmap_env
    pip install georastertools --no-binary rasterio
    pip install eolabtools[SunMapGen] --force-reinstall --no-cache-dir


Code file contained in the directory
===============================

The file `sun_map_generation/SunMapGenerator.py` contains the main source code.


Compute a sun map with SunMapGeneration
=======================================

Command line
------------

To launch SunMapGeneration, please use the following command :

.. code-block:: python

    sun_map_generation --digital_surface_model /path_to_input_files/input_files.lst (or .tif)
                       --tiles_file /path_to_tiles_files/tiles.shp
                       --date YYYY-MM-DD YYYY-MM-DD 3
                       --time HH:MM HH:MM 30
                       --nb_cores 32
                       --occ_changes 4
                       --output_dir /path_to_output_directory/output_directory/
                       --save_temp
                       --save_masks


- `--digital_surface_model` : Path to the `.lst` file containing the names of the `.tif` files, an example can be found `here <https://github.com/CNES/eolabtools/blob/main/docs/source/sunmap_doc/listing_2tiles.lst>`_. When only one input file is necessary for the computation, the `.tif` file can be given. An example of `.tif` file can be downloaded `here <https://github.com/CNES/eolabtools/blob/main/tests/data/SunMapGen/test_data/test_1tile_low_res/75-2021-0659-6861-LA93-0M50.tif>`_.

- `--tiles_file` : Path to the `.shp` file containing the geometry of the tiles to be processed and at least the attribute `TILE_NAME` (name of the tile). An example can be downloaded `here <https://github.com/CNES/eolabtools/blob/main/tests/data/SunMapGen/test_data/test_1tile_low_res/1tile.shp>`_.

- `--date` : Date or date range (YYYY-MM-DD) and step (in days). The step value should be strictly positive and default value is 1 day.

- `--time` : Time or time range (HH:MM) and step (in minutes). The step value should be strictly positive and default value is 30 minutes.

- `--occ_changes` (should be >= 3) : Maximal number of sun/shade changes over the day of a pixel registered in the Sun appearance/disappearance vector file. Default value 4.

- `--nb_cores` : To launch parallel processing. Number of processes to be entered.

- `--output_dir` : Path to the output directory.

- `--save_temp` : To be filled in to obtain the file describing the calculation time per step in the processing chain (`processing_time.csv`).

- `--save_masks` : To save shadow masks calculated at each time step


Output files
------------

Files are stored in the directory given to `--output_dir` :

- **Percentage of sun exposure raster** : `[tile_name]-sun_map-[YYYYMMDD].tif` The algorithm calculates them for each tile and each day entered by the user.

- **Sun appearance/disappearance vector** : `[tile-sun_map-[YYYYMMDD].gpkg` The number of sun/shade changes per pixel registered in the file is limited by the `occ_changes` argument.

- **Shadow masks (--save_masks option)** : `[tile_name]-hillshade-[YYYYMMDD]-[HHMM].tif` The algorithm calculates them for each tile, day and time entered by the user.


QGIS processing of output files
-------------------------------

It is possible do “requests” on the `.gpkg` file.

For instance, to detect places that are shadowed between 12h00 and 14h00, you can view the file on QGIS and filter it with the
following expression :

.. code-block:: console

    "first_shadow_appearance" < '2024-08-31 11:55:00' AND "second_sun_appearance"  > '2024-08-31 14:05:00' OR "second_shadow_appearance"  < '2024-08-31 11:55:00'

