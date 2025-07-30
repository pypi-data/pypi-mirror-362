.. _install:

======================
Installation
======================

Each tools can be use in separate virtual environnements.
The single tool installation is provided below and in each tool page.

SunMapGeneration installation
==============================

To install SunMapGeneration, please launch the following commands :

.. code-block:: console

    conda create -n sunmap_env python=3.12 libgdal=3.5.0 -c conda-forge -c defaults -y
    conda activate sunmap_env
    pip install georastertools --no-binary rasterio
    pip install eolabtools[SunMapGen] --force-reinstall --no-cache-dir


NightOsmRegistration installation
=================================

To install NightOsmRegistration, please launch the following commands :

.. code-block:: console

    conda create -n nightosm_env python=3.12 libgdal=3.11.0 markupsafe -c conda-forge
    conda activate nightosm_env
    pip install eolabtools[NightOsmReg]

DetectionOrientationCulture installation
=================================

To install DetectionOrientationCulture, please launch the following commands :

.. code-block:: console

    conda create -n orcult_env python=3.12 libgdal=3.11.0 -c conda-forge -c defaults -y
    conda activate orcult_env
    pip install eolabtools[DetecOrCult]