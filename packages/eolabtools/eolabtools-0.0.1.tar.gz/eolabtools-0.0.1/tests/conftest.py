# -*- coding: utf-8 -*-
"""
    Dummy conftest.py for s2shores.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""
from dataclasses import dataclass

import pytest
from pathlib import Path

@dataclass
class EOLabtoolsTestsPath():
    project_dir: Path
    def __post_init__(self):

        test_data = self.project_dir / "tests" / "data"

        self.referencedir = self.project_dir

        self.sunmap_ref = test_data / "SunMapGen" / "reference_results"
        self.sunmap_outdir = test_data / "SunMapGen" / "test_out"
        self.sunmap_datadir = test_data / "SunMapGen" / "test_data"

        self.plotor_ref = test_data / "DetecOrCult" / "reference_results"
        self.plotor_outdir = test_data / "DetecOrCult" / "test_out"
        self.plotor_datadir = test_data / "DetecOrCult" / "test_data"

        self.nightosm_ref = test_data / "NightOSMReg" / "reference_results"
        self.nightosm_outdir = test_data / "NightOSMReg" / "test_out"
        self.nightosm_datadir = test_data / "NightOSMReg" / "test_data"


@pytest.fixture
def eolabtools_paths(request) -> EOLabtoolsTestsPath:
    return EOLabtoolsTestsPath(Path(__file__).parent.parent)
