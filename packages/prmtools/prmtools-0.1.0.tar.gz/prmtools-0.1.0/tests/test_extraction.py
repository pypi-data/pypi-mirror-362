import pytest
from prmtools import extraction
import pandas as pd

def test_fragment_extractor_init():
    fe = extraction.FragmentExtractor('dummy.raw')
    assert fe.raw_file_path == 'dummy.raw'
    assert fe.rt_tolerance == 0.2
    assert fe.ppm_tolerance == 20
    assert fe.intensity_threshold == 1000
    assert fe.integration_window == 0.05

# More tests would require a real or mock raw file and fisher_py
