import pytest
from prmtools import plotting
import numpy as np
import os

def test_create_analyte_eic_plot_improved(tmp_path):
    valid_fragments = [
        {
            'fragment_mz': 150.0,
            'EIC_Points': [(1.0, 10), (1.1, 20), (1.2, 30)],
            'EIC_Points_Window': [(1.0, 10), (1.1, 20), (1.2, 30)],
            'apex_rt': 1.1,
            'apex_intensity': 20,
            'EIC_Area': 60,
            'peak_quality': {'peak_height': 20, 'SNR': 10}
        }
    ]
    analyte = "TestAnalyte"
    target_rt = 1.1
    integration_window = 0.2
    output_dir = str(tmp_path)
    plotting.create_analyte_eic_plot_improved(valid_fragments, analyte, target_rt, integration_window, output_dir)
    eic_dir = os.path.join('Figures', 'EIC')
    found = False
    for f in os.listdir(eic_dir):
        if f.endswith("EIC_plot.svg"):
            found = True
    assert found
