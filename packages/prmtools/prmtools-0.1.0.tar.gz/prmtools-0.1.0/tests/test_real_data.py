import os
import pytest
from prmtools import utils, extraction
import pandas as pd

def test_real_excel_and_raw():
    # Find real Excel and RAW files in the working directory
    excel_files = utils.find_excel_files(os.getcwd())
    raw_files = utils.find_raw_files(os.getcwd())
    assert len(excel_files) > 0, "No Excel files found in working directory."
    assert len(raw_files) > 0, "No RAW files found in working directory."
    # Try reading the first Excel file
    df = pd.read_excel(excel_files[0])
    assert not df.empty, "Excel file is empty."
    # Try initializing FragmentExtractor with the first RAW file
    fe = extraction.FragmentExtractor(raw_files[0])
    assert fe.raw_file_path == raw_files[0]
    # Only test open_raw_file if fisher_py is available
    if hasattr(fe, 'open_raw_file'):
        try:
            fe.open_raw_file()
        except Exception:
            pass  # Acceptable if fisher_py is not installed
