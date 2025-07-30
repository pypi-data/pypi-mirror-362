from conftest import EOLabtoolsTestsPath
from test_utils import compare_files, clear_outdir, create_outdir
import pytest
import os
import subprocess

@pytest.mark.ci
def test_sunmap_1tile_lst(eolabtools_paths: EOLabtoolsTestsPath) -> None:
    """
    TO DO
    """
    with open(f"{eolabtools_paths.sunmap_datadir}/test_1tile_low_res/listing_1tile.lst", "w") as f:
        f.write(f"{eolabtools_paths.sunmap_datadir}/test_1tile_low_res/75-2021-0659-6861-LA93-0M50.tif" + "\n")

    create_outdir(f"{eolabtools_paths.sunmap_outdir}/test_1tile_low_res_lst/")

    command = [
        f"sun_map_generation",
        f"--digital_surface_model", f"{eolabtools_paths.sunmap_datadir}/test_1tile_low_res/listing_1tile.lst",
        f"--tiles_file", f"{eolabtools_paths.sunmap_datadir}/test_1tile_low_res/1tile.shp",
        f"--date", f"2024-08-03", f"2024-08-04", f"1",
        f"--time", f"08:00", f"17:00", f"120",
        f"--nb_cores", f"32",
        f"--occ_changes", f"3",
        f"--output_dir", f"{eolabtools_paths.sunmap_outdir}/test_1tile_low_res_lst/"
    ]

    result = subprocess.run(command, capture_output=True, text=True, check=True)
    print(result.stderr)

    compare_files(reference_dir = f"{eolabtools_paths.sunmap_ref}/test_1tile_low_res",
                  output_dir = f"{eolabtools_paths.sunmap_outdir}/test_1tile_low_res_lst",
                  tool = "SunMapGen")

    os.remove(f"{eolabtools_paths.sunmap_datadir}/test_1tile_low_res/listing_1tile.lst")
    clear_outdir(f"{eolabtools_paths.sunmap_outdir}/test_1tile_low_res_lst/")


@pytest.mark.ci
def test_sunmap_1tile_tif(eolabtools_paths: EOLabtoolsTestsPath) -> None:
    """
    TO DO
    """
    create_outdir(f"{eolabtools_paths.sunmap_outdir}/test_1tile_low_res_tif/")

    command = [
        f"sun_map_generation",
        f"--digital_surface_model", f"{eolabtools_paths.sunmap_datadir}/test_1tile_low_res/75-2021-0659-6861-LA93-0M50.tif",
        f"--tiles_file", f"{eolabtools_paths.sunmap_datadir}/test_1tile_low_res/1tile.shp",
        f"--date", f"2024-08-03", f"2024-08-04", f"1",
        f"--time", f"08:00", f"17:00", f"120",
        f"--nb_cores", f"32",
        f"--occ_changes", f"3",
        f"--output_dir", f"{eolabtools_paths.sunmap_outdir}/test_1tile_low_res_tif/"
    ]

    result = subprocess.run(command, capture_output=True, text=True, check=True)
    print(result.stderr)

    compare_files(reference_dir = f"{eolabtools_paths.sunmap_ref}/test_1tile_low_res",
                  output_dir = f"{eolabtools_paths.sunmap_outdir}/test_1tile_low_res_tif",
                  tool = "SunMapGen")

    clear_outdir(f"{eolabtools_paths.sunmap_outdir}/test_1tile_low_res_tif/")


@pytest.mark.ci
def test_sunmap_2tiles(eolabtools_paths: EOLabtoolsTestsPath) -> None:
    """
    TO DO
    """
    with open(f"{eolabtools_paths.sunmap_datadir}/test_2tiles_low_res/listing_2tiles.lst", "w") as f:
        f.write(f"{eolabtools_paths.sunmap_datadir}/test_2tiles_low_res/75-2021-0648-6862-LA93-0M50.tif"
                + "\n"
                + f"{eolabtools_paths.sunmap_datadir}/test_2tiles_low_res/75-2021-0649-6862-LA93-0M50.tif" )

    create_outdir(f"{eolabtools_paths.sunmap_outdir}/test_2tiles_low_res/")

    command = [
        f"sun_map_generation",
        f"--digital_surface_model", f"{eolabtools_paths.sunmap_datadir}/test_2tiles_low_res/listing_2tiles.lst",
        f"--tiles_file", f"{eolabtools_paths.sunmap_datadir}/test_2tiles_low_res/2tiles.shp",
        f"--date", f"2024-08-31", f"2024-08-31", f"1",
        f"--time", f"08:00", f"9:00", f"60",
        f"--nb_cores", f"32",
        f"--occ_changes", f"3",
        f"--output_dir", f"{eolabtools_paths.sunmap_outdir}/test_2tiles_low_res/",
        f"--save_temp"
    ]

    result = subprocess.run(command, capture_output=True, text=True, check=True)
    print(result.stderr)

    compare_files(reference_dir = f"{eolabtools_paths.sunmap_ref}/test_2tiles_low_res",
                  output_dir = f"{eolabtools_paths.sunmap_outdir}/test_2tiles_low_res",
                  tool = "SunMapGen")

    os.remove(f"{eolabtools_paths.sunmap_datadir}/test_2tiles_low_res/listing_2tiles.lst")
    clear_outdir(f"{eolabtools_paths.sunmap_outdir}/test_2tiles_low_res/")