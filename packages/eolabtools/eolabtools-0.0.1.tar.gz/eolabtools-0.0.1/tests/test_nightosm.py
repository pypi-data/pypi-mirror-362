from conftest import EOLabtoolsTestsPath
import subprocess
from test_utils import compare_files, clear_outdir, create_outdir, fill_config_nightosm
import pytest
import os
from pathlib import Path
import subprocess
import sys

@pytest.mark.ci
def test_nightosm_rasterize_radiance(eolabtools_paths: EOLabtoolsTestsPath) -> None:
    """
    TO DO
    """
    fill_config_nightosm(f"{eolabtools_paths.nightosm_datadir}/config/config1.yml", eolabtools_paths)
    create_outdir(f"{eolabtools_paths.nightosm_outdir}/test_nightosm_rasterize_radiance")

    command = [
        f"night_osm_image_registration",
        f"-o", f"{eolabtools_paths.nightosm_outdir}/test_nightosm_rasterize_radiance/",
        f"--config", f"{eolabtools_paths.nightosm_datadir}/config/config1.yml",
        f"--osm-config", f"{eolabtools_paths.nightosm_datadir}/osm-config/osm_config_subtracted.yml",
        f"{eolabtools_paths.nightosm_datadir}/Extrait1/Extract1-Radiance.tif"
    ]
    print(' '.join(command))

    result = subprocess.run(command, capture_output=True, text=True, check=True)

    compare_files(reference_dir = f"{eolabtools_paths.nightosm_ref}/TestRasterizeRadiance",
                  output_dir = f"{eolabtools_paths.nightosm_outdir}/test_nightosm_rasterize_radiance",
                  tool = "NightOSM")
    # clear_outdir(f"{eolabtools_paths.nightosm_outdir}/test_nightosm_rasterize_radiance")


@pytest.mark.ci
def test_nightosm_rasterize_rgb(eolabtools_paths: EOLabtoolsTestsPath) -> None:
    """
    TO DO
    """
    fill_config_nightosm(f"{eolabtools_paths.nightosm_datadir}/config/config2.yml", eolabtools_paths)
    create_outdir(f"{eolabtools_paths.nightosm_outdir}/test_nightosm_rasterize_rgb")

    command = [
        f"night_osm_image_registration",
        f"-o", f"{eolabtools_paths.nightosm_outdir}/test_nightosm_rasterize_rgb/",
        f"--config", f"{eolabtools_paths.nightosm_datadir}/config/config2.yml",
        f"--osm-config", f"{eolabtools_paths.nightosm_datadir}/osm-config/osm_config_subtracted.yml",
        f"{eolabtools_paths.nightosm_datadir}/Extrait2/Extract2-FakeRGB.tif"
    ]
    print(command)

    result = subprocess.run(command, capture_output=True, text=True, check=True)

    compare_files(reference_dir=f"{eolabtools_paths.nightosm_ref}/TestRasterizeRGB",
                  output_dir=f"{eolabtools_paths.nightosm_outdir}/test_nightosm_rasterize_rgb",
                  tool="NightOSM")
    clear_outdir(f"{eolabtools_paths.nightosm_outdir}/test_nightosm_rasterize_rgb")


@pytest.mark.ci
def test_nightosm_register_radiance(eolabtools_paths: EOLabtoolsTestsPath) -> None:
    """
    TO DO
    """
    fill_config_nightosm(f"{eolabtools_paths.nightosm_datadir}/config/config3.yml", eolabtools_paths)
    create_outdir(f"{eolabtools_paths.nightosm_outdir}/test_nightosm_register_radiance")

    command = [
        f"night_osm_image_registration",
        f"-o", f"{eolabtools_paths.nightosm_outdir}/test_nightosm_register_radiance/",
        f"--config", f"{eolabtools_paths.nightosm_datadir}/config/config3.yml",
        f"--osm-config", f"{eolabtools_paths.nightosm_datadir}/osm-config/osm_config_subtracted.yml",
        f"{eolabtools_paths.nightosm_datadir}/Extrait1/Extract1-Radiance.tif",
        f"{eolabtools_paths.nightosm_datadir}/Extrait1/Extract1-FakeRGB.tif"
    ]
    print(command)
    result = subprocess.run(command, capture_output=True, text=True, check=True)

    compare_files(reference_dir=f"{eolabtools_paths.nightosm_ref}/TestRegisterRadiance",
                  output_dir=f"{eolabtools_paths.nightosm_outdir}/test_nightosm_register_radiance",
                  tool="NightOSM")
    clear_outdir(f"{eolabtools_paths.nightosm_outdir}/test_nightosm_register_radiance")


@pytest.mark.ci
def test_nightosm_register_rgb(eolabtools_paths: EOLabtoolsTestsPath) -> None:
    """
    TO DO
    """
    fill_config_nightosm(f"{eolabtools_paths.nightosm_datadir}/config/config4.yml", eolabtools_paths)
    create_outdir(f"{eolabtools_paths.nightosm_outdir}/test_nightosm_register_rgb")

    command = [
        f"night_osm_image_registration",
        f"-o", f"{eolabtools_paths.nightosm_outdir}/test_nightosm_register_rgb/",
        f"--config", f"{eolabtools_paths.nightosm_datadir}/config/config4.yml",
        f"--osm-config", f"{eolabtools_paths.nightosm_datadir}/osm-config/osm_config_subtracted.yml",
        f"{eolabtools_paths.nightosm_datadir}/Extrait2/Extract2-FakeRGB.tif"
    ]
    print(command)

    result = subprocess.run(command, capture_output=True, text=True, check=True)

    compare_files(reference_dir=f"{eolabtools_paths.nightosm_ref}/TestRegisterRGB",
                  output_dir=f"{eolabtools_paths.nightosm_outdir}/test_nightosm_register_rgb",
                  tool="NightOSM")
    clear_outdir(f"{eolabtools_paths.nightosm_outdir}/test_nightosm_register_rgb")

@pytest.mark.ci
def test_nightosm_vector(eolabtools_paths: EOLabtoolsTestsPath) -> None:
    """
    TO DO
    """
    create_outdir(f"{eolabtools_paths.nightosm_outdir}/test_nightosm_vector")

    command = [
        f"night_osm_vector_registration",
        f"-o", f"{eolabtools_paths.nightosm_outdir}/test_nightosm_vector/",
        f"-n Extract2_radiance_peaks_shifted",
        f"{eolabtools_paths.nightosm_datadir}/Extrait2/Extract2_RadiancePeaks.gpkg",
        f"{eolabtools_paths.nightosm_datadir}/Extrait2/Extract2-displacement_grid.tif"
    ]
    print(command)

    result = subprocess.run(command, capture_output=True, text=True, check=True)

    compare_files(reference_dir=f"{eolabtools_paths.nightosm_ref}/TestRegisterVector",
                  output_dir=f"{eolabtools_paths.nightosm_outdir}/test_nightosm_vector",
                  tool="NightOSM")
    clear_outdir(f"{eolabtools_paths.nightosm_outdir}/test_nightosm_vector")


@pytest.mark.ci
def test_nightosm_simple_config(eolabtools_paths: EOLabtoolsTestsPath) -> None:
    """
    TO DO
    """
    fill_config_nightosm(f"{eolabtools_paths.nightosm_datadir}/config/config5.yml", eolabtools_paths)
    create_outdir(f"{eolabtools_paths.nightosm_outdir}/test_nightosm_simple_config")

    command = [
        f"night_osm_image_registration",
        f"-o", f"{eolabtools_paths.nightosm_outdir}/test_nightosm_simple_config/",
        f"--config", f"{eolabtools_paths.nightosm_datadir}/config/config5.yml",
        f"--osm-config", f"{eolabtools_paths.nightosm_datadir}/osm-config/osm_config_simple.yml",
        f"{eolabtools_paths.nightosm_datadir}/Extrait2/Extract2-FakeRGB.tif"
    ]
    print(command)

    subprocess.run(command, capture_output=True, text=True, check=True)

    compare_files(reference_dir=f"{eolabtools_paths.nightosm_ref}/TestSimpleConfig",
                  output_dir=f"{eolabtools_paths.nightosm_outdir}/test_nightosm_simple_config",
                  tool="NightOSM")
    clear_outdir(f"{eolabtools_paths.nightosm_outdir}/test_nightosm_simple_config")
