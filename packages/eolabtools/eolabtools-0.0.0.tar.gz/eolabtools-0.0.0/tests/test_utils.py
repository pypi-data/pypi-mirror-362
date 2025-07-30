from conftest import EOLabtoolsTestsPath
import geopandas as gpd
import rasterio
import numpy as np
import os
import yaml
from glob import glob

import shutil
import filecmp
import fiona
import pandas as pd

def clear_outdir(dir_path):
    for item in os.listdir(dir_path):
        full_path = os.path.join(dir_path, item)
        if os.path.isfile(full_path) or os.path.islink(full_path):
            os.unlink(full_path)  # delete file or symlink
        elif os.path.isdir(full_path):
            shutil.rmtree(full_path)  # delete folder

def create_outdir(dir_path):
    if not os.path.isdir(dir_path + '/'):
        os.makedirs(dir_path + '/')
    clear_outdir(dir_path)

def get_all_files(reference_dir):
    all_files = glob(os.path.join(reference_dir, "**", "*"), recursive=True)
    # Filter only files (exclude directories)
    just_files = [f.split(reference_dir + '/')[-1] for f in all_files if os.path.isfile(f)]
    return just_files

def compare_csv(file1, file2):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Sort both DataFrames by all columns
    df1_sorted = df1.sort_values(by=list(df1.columns)).reset_index(drop=True)
    df2_sorted = df2.sort_values(by=list(df2.columns)).reset_index(drop=True)

    if not df1_sorted.equals(df2_sorted):
        raise ValueError(f"CSV files differ: {file1} and {file2}")


def compare_shapefiles(file1, file2):
    """
    Compare two shapefiles.

    Raises:
        ValueError: If shapefiles are different
    """
    if not filecmp.cmp(file1, file2, shallow=False):
        raise ValueError(f"Error comparing {file1} and {file2}")


def compare_tif(file1, file2, atol=1e-10):
    with rasterio.open(file1) as src1, rasterio.open(file2) as src2:
        # Compare metadata
        if src1.meta != src2.meta:
            raise ValueError(f"TIFF metadata differs.")

        # Compare pixel data
        arr1 = src1.read()
        arr2 = src2.read()
        if not np.allclose(arr1, arr2, atol=atol):
            raise ValueError(f"TIFF pixel values differ.")

    print("TIFF files are identical.")
    return True


def compare_gpkg(file1, file2):
    layers1 = fiona.listlayers(file1)
    layers2 = fiona.listlayers(file2)

    common_layers = set(layers1).intersection(layers2)

    for layer in common_layers:
        gdf1 = gpd.read_file(file1, layer=layer)
        gdf2 = gpd.read_file(file2, layer=layer)

        # Sort by non-geometry columns for alignment
        sort_cols = [col for col in gdf1.columns if col != 'geometry']
        gdf1 = gdf1.sort_values(by=sort_cols).reset_index(drop=True)
        gdf2 = gdf2.sort_values(by=sort_cols).reset_index(drop=True)

        for idx, (row1, row2) in enumerate(zip(gdf1.itertuples(index=False), gdf2.itertuples(index=False))):
            geom1 = row1.geometry
            geom2 = row2.geometry

            for attr_name in gdf1.columns:
                if attr_name == 'geometry': # Geometry check
                    if geom1 is None and geom2 is None:
                        pass
                    elif (geom1 is None) != (geom2 is None) or not geom1.equals(geom2):
                        raise ValueError(f"GPKG files differ.")
                else : # Attribute check
                    val1 = getattr(row1, attr_name)
                    val2 = getattr(row2, attr_name)
                    if not((pd.isna(val1) and pd.isna(val2)) or (val1 == val2)):
                        print(f"  Row {idx}: Attribute '{attr_name}' mismatch")
                        print(f"    File1: {val1}")
                        print(f"    File2: {val2}")
                        raise ValueError(f"GPKG files differ.")


def compare_files(reference_dir : str, output_dir : str, tool : str):
    """
    TO DO
    """
    ref_files = get_all_files(reference_dir)
    out_test_files = get_all_files(output_dir)

    if ref_files == out_test_files:
        print("Both directories contain the same filenames.")
    else:
        raise Exception("Filenames differ between the directories.\n"
                            f"Only in {reference_dir} : {[item for item in ref_files if item not in out_test_files]}\n"
                            f"Only in {output_dir} : {[item for item in out_test_files if item not in ref_files]}")

    # Compare output files with references
    print("Output files :", ref_files)
    for f in ref_files :
        print(f)
        if ".tif" in f:
            # Compare tif files (pixel value and metadata)
            compare_tif(f"{output_dir}/{f}", f"{reference_dir}/{f}")
        elif ".gpkg" in f:
            # Compare gpkg files
            compare_gpkg(f"{output_dir}/{f}", f"{reference_dir}/{f}")
        elif ".shp" in f:
            # Compare shapefiles
            compare_shapefiles(f"{output_dir}/{f}", f"{reference_dir}/{f}")
        elif ".csv" in f :
            # Compare csv files
            if f in ["computation_time.csv", "processing_time.csv"]:
                continue
            compare_csv(f"{output_dir}/{f}", f"{reference_dir}/{f}")
    print("Both directories contain the same files.")


def fill_config_nightosm(config_file : str, eolabtools_paths: EOLabtoolsTestsPath) :
    '''
    Fill NightOSMRegistration config file with local paths
    '''
    # Open config file
    with open(config_file) as conf:
        conf_dict = yaml.safe_load(conf)

    for key in conf_dict.keys():
        if any(ext in str(conf_dict[key]) for ext in ['.shp', '.osm.pbf', '.tif']):
            conf_dict[key] = str(eolabtools_paths.referencedir) + "/tests/data" + conf_dict[key].split("tests/data")[-1]

    with open(config_file, 'w') as outfile:
        yaml.dump(conf_dict, outfile, default_flow_style=False)