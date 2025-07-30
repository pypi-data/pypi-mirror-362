import numpy as np
from prmtools import quality

def test_assess_peak_quality_good():
    rt = np.linspace(1, 2, 11)
    intensity = np.array([1, 2, 5, 10, 20, 30, 20, 10, 5, 2, 1])
    result = quality.assess_peak_quality(rt, intensity)
    assert result['is_good_peak']
    assert result['SNR'] > 0

def test_assess_peak_quality_bad():
    rt = np.linspace(1, 2, 5)
    intensity = np.array([1, 1, 1, 1, 1])
    result = quality.assess_peak_quality(rt, intensity)
    assert not result['is_good_peak']
    assert result['SNR'] == 0
