# Utility functions for PRM tools

def format_intensity_scientific(value):
    import numpy as np
    if value == 0:
        return '0'
    exponent = int(np.floor(np.log10(abs(value))))
    mantissa = value / (10 ** exponent)
    return f"{mantissa:.2f}E{exponent}"

def find_excel_files(directory):
    import os, glob
    patterns = [
        'prm_list.xlsx', 'prm_list.xls',
        'PRM_list.xlsx', 'PRM_list.xls',
        'prm_list*.xlsx', 'prm_list*.xls',
        'PRM_list*.xlsx', 'PRM_list*.xls'
    ]
    files = []
    for pattern in patterns:
        files.extend(glob.glob(os.path.join(directory, pattern)))
    return list(set(files))

def find_raw_files(directory):
    import os, glob
    return glob.glob(os.path.join(directory, '*.raw'))

def consolidate_fragments(fragments_data, ppm_tolerance=20):
    # Consolidate fragments by m/z within ppm tolerance
    if not fragments_data:
        return []
    fragments_data = sorted(fragments_data, key=lambda x: x['fragment_mz'])
    consolidated = []
    current_group = []
    current_mz = None
    for frag in fragments_data:
        mz = frag['fragment_mz']
        if current_mz is None:
            current_mz = mz
            current_group = [frag]
        elif abs(mz - current_mz) / current_mz * 1e6 <= ppm_tolerance:
            current_group.append(frag)
        else:
            sum_intensity = sum(f['intensity'] for f in current_group)
            consolidated.append({
                'fragment_mz': current_mz,
                'sum_intensity': sum_intensity,
                'consolidated_fragments': len(current_group),
                'rt': current_group[0]['rt'],
                'intensity': current_group[0]['intensity'],
                'precursor_mz': current_group[0]['precursor_mz'],
                'analyte': current_group[0]['analyte'],
                'raw_file': current_group[0]['raw_file'],
                'scan_number': current_group[0]['scan_number'],
                'precursor_mz_observed': current_group[0]['precursor_mz_observed']
            })
            current_mz = mz
            current_group = [frag]
    if current_group:
        sum_intensity = sum(f['intensity'] for f in current_group)
        consolidated.append({
            'fragment_mz': current_mz,
            'sum_intensity': sum_intensity,
            'consolidated_fragments': len(current_group),
            'rt': current_group[0]['rt'],
            'intensity': current_group[0]['intensity'],
            'precursor_mz': current_group[0]['precursor_mz'],
            'analyte': current_group[0]['analyte'],
            'raw_file': current_group[0]['raw_file'],
            'scan_number': current_group[0]['scan_number'],
            'precursor_mz_observed': current_group[0]['precursor_mz_observed']
        })
    return consolidated


