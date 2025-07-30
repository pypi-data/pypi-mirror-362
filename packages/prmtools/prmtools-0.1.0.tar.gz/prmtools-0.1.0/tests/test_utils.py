import pytest
from prmtools import utils

def test_format_intensity_scientific():
    assert utils.format_intensity_scientific(0) == "0"
    assert utils.format_intensity_scientific(1000) == "1.00E3"
    assert utils.format_intensity_scientific(1.99e6) == "1.99E6"

def test_find_excel_files(tmp_path):
    # Create dummy files
    (tmp_path / "PRM_list.xlsx").write_text("")
    (tmp_path / "prm_list.xls").write_text("")
    files = [f.lower() for f in utils.find_excel_files(str(tmp_path))]
    assert any("prm_list.xlsx" in f for f in files)
    assert any("prm_list.xls" in f for f in files)

def test_find_raw_files(tmp_path):
    (tmp_path / "file1.raw").write_text("")
    (tmp_path / "file2.RAW").write_text("")
    files = utils.find_raw_files(str(tmp_path))
    assert any("file1.raw" in f for f in files)
    assert any("file2.RAW" in f for f in files)

def test_consolidate_fragments():
    fragments = [
        {'analyte': 'A', 'target_rt': 1.0, 'precursor_mz': 100.0, 'raw_file': 'file.raw', 'scan_number': 1, 'rt': 1.0, 'precursor_mz_observed': 100.0, 'fragment_mz': 150.0, 'intensity': 100},
        {'analyte': 'A', 'target_rt': 1.0, 'precursor_mz': 100.0, 'raw_file': 'file.raw', 'scan_number': 2, 'rt': 1.1, 'precursor_mz_observed': 100.0, 'fragment_mz': 150.0002, 'intensity': 200},
        {'analyte': 'A', 'target_rt': 1.0, 'precursor_mz': 100.0, 'raw_file': 'file.raw', 'scan_number': 3, 'rt': 1.2, 'precursor_mz_observed': 100.0, 'fragment_mz': 151.0, 'intensity': 50},
    ]
    consolidated = utils.consolidate_fragments(fragments, ppm_tolerance=10)
    assert len(consolidated) == 2
    assert consolidated[0]['sum_intensity'] == 300
    assert consolidated[1]['sum_intensity'] == 50
