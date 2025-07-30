# Plotting functions for PRM tools


import numpy as np
import matplotlib.pyplot as plt
import os
from .utils import format_intensity_scientific

def create_analyte_eic_plot_improved(valid_fragments, analyte, target_rt, integration_window=0.2, output_dir='.', x_extension=0.0, raw_file=None):
    # ...existing code from PRM_script.py (see attachment, function create_analyte_eic_plot_improved)...
    # (Full function body as previously provided)
    if not valid_fragments:
        return
    valid_fragments.sort(key=lambda f: f.get('peak_quality', {}).get('peak_height', 0), reverse=True)
    top_fragments = valid_fragments[:25]
    fig, ax = plt.subplots(figsize=(10, 6))
    cmap = plt.get_cmap('tab10')
    colors = cmap(np.linspace(0, 1, len(top_fragments)))
    global_max_intensity = 0
    for fragment in top_fragments:
        eic_points = fragment.get('EIC_Points', [])
        if eic_points:
            intensities = [point[1] for point in eic_points]
            fragment_max = max(intensities) if intensities else 0
            global_max_intensity = max(global_max_intensity, fragment_max)
    legend_handles = []
    for idx, fragment in enumerate(top_fragments):
        color = colors[idx % len(colors)]
        mz = fragment['fragment_mz']
        eic_points = fragment.get('EIC_Points', [])
        if not eic_points:
            continue
        rt_values = np.array([point[0] for point in eic_points])
        intensity_values = np.array([point[1] for point in eic_points])
        if global_max_intensity > 0:
            relative_intensity = (intensity_values / global_max_intensity) * 100
        else:
            relative_intensity = intensity_values
        sort_idx = np.argsort(rt_values)
        sorted_rt = rt_values[sort_idx]
        sorted_intensity = relative_intensity[sort_idx]
        line = ax.plot(sorted_rt, sorted_intensity, color=color, linewidth=2, alpha=0.8)[0]
        integration_points = fragment.get('EIC_Points_Window', [])
        if integration_points:
            int_rt = np.array([point[0] for point in integration_points])
            int_intensity = np.array([point[1] for point in integration_points])
            if global_max_intensity > 0:
                int_relative = (int_intensity / global_max_intensity) * 100
            else:
                int_relative = int_intensity
            int_sort_idx = np.argsort(int_rt)
            int_sorted_rt = int_rt[int_sort_idx]
            int_sorted_intensity = int_relative[int_sort_idx]
            ax.fill_between(int_sorted_rt, int_sorted_intensity, color=color, alpha=0.3)
        apex_rt = fragment.get('apex_rt', target_rt)
        apex_intensity = fragment.get('apex_intensity', 0)
        if global_max_intensity > 0:
            apex_relative = (apex_intensity / global_max_intensity) * 100
        else:
            apex_relative = apex_intensity
        area = fragment.get('EIC_Area', 0)
        legend_label = f"{idx+1}. m/z {mz:.4f} (Area: {area:.0f})"
        legend_handles.append((line, legend_label))
    ax.set_xlabel('Retention Time (min)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Relative Abundance (%)', fontsize=14, fontweight='bold')
    ax.set_title(f'{analyte} - Fragment EICs', fontsize=14, fontweight='bold')
    ax.text(target_rt, 101, f'{target_rt:.1f}', ha='center', va='bottom', fontsize=12, fontweight='bold', color='black')
    ax.set_ylim(0, 105)
    ax.tick_params(axis='both', labelsize=12, width=2)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontweight('bold')
    buffer = integration_window * 0.5
    x_min = target_rt - integration_window - buffer - x_extension
    x_max = target_rt + integration_window + buffer + x_extension
    ax.set_xlim(x_min, x_max)
    total_area = sum(f.get('EIC_Area', 0) for f in top_fragments)
    ax.text(0.02, 0.98, f"Max Intensity: {format_intensity_scientific(global_max_intensity)}", transform=ax.transAxes, fontsize=12, va='top', fontweight='bold')
    ax.text(0.02, 0.92, f"Total Area: {format_intensity_scientific(total_area)}", transform=ax.transAxes, fontsize=12, va='top', fontweight='bold')
    ax.text(0.02, 0.86, f"Valid Fragments: {len(valid_fragments)}", transform=ax.transAxes, fontsize=12, va='top', fontweight='bold')
    if legend_handles:
        lines = [h[0] for h in legend_handles]
        labels = [h[1] for h in legend_handles]
        legend = ax.legend(lines, labels, loc='center left', fontsize=10, bbox_to_anchor=(1.05, 0.5))
        for text in legend.get_texts():
            text.set_fontweight('bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['left'].set_linewidth(1.5)
    plt.tight_layout()
    plt.subplots_adjust(right=0.75)
    safe_analyte_name = "".join(c for c in analyte if c.isalnum() or c in (' ', '-', '_')).rstrip()
    if raw_file:
        raw_base = os.path.splitext(os.path.basename(raw_file))[0]
        filename = f"{raw_base}_{safe_analyte_name}_EIC_plot.svg"
    else:
        filename = f"{safe_analyte_name}_EIC_plot.svg"
    eic_dir = os.path.join('Figures', 'EIC')
    os.makedirs(eic_dir, exist_ok=True)
    filepath = os.path.join(eic_dir, filename)
    plt.savefig(filepath, format='svg', bbox_inches='tight')
    plt.close()
    print(f"EIC plot saved: {filepath}")

def plot_ms2_best_scan(raw_file_path, analyte, target_rt, precursor_mz, valid_fragments, output_dir='.', rt_tolerance=0.5, ppm_tolerance=20):
    try:
        import fisher_py
    except ImportError:
        print("fisher_py not available. Cannot plot MS2 spectrum.")
        return
    try:
        raw_file = fisher_py.RawFile(raw_file_path)
    except Exception as e:
        print(f"Error opening raw file: {e}")
        return
    first_scan = raw_file.first_scan
    last_scan = raw_file.last_scan
    best_scan = None
    best_rt_diff = float('inf')
    for scan_num in range(first_scan, last_scan + 1):
        try:
            scan_event = raw_file.get_scan_event_str_from_scan_number(scan_num)
            if 'ms2' in scan_event.lower():
                rt = raw_file.get_retention_time_from_scan_number(scan_num)
                rt_diff = abs(rt - target_rt)
                if rt_diff > rt_tolerance:
                    continue
                if '@' in scan_event:
                    precursor_part = scan_event.split('@')[0]
                    scan_precursor_mz = float(precursor_part.split()[-1])
                else:
                    continue
                ppm_tol = (precursor_mz * 20) / 1e6
                if abs(scan_precursor_mz - precursor_mz) > ppm_tol:
                    continue
                mz_array, intensity_array, charge_array, _ = raw_file.get_scan_from_scan_number(scan_num)
                fragment_count = np.sum(intensity_array > 1000)
                if rt_diff < best_rt_diff:
                    best_scan = {
                        'scan_num': scan_num,
                        'rt': rt,
                        'mz_array': mz_array,
                        'intensity_array': intensity_array,
                        'precursor_mz': scan_precursor_mz,
                        'fragment_count': fragment_count
                    }
                    best_rt_diff = rt_diff
        except Exception:
            continue
    if best_scan is None:
        print(f"No suitable MS2 scan found for {analyte} near RT {target_rt}")
        return
    valid_mz = [frag['fragment_mz'] for frag in valid_fragments]
    ms2_mz = np.array(best_scan['mz_array'])
    ms2_intensity = np.array(best_scan['intensity_array'])
    filtered_indices = []
    for i, mz in enumerate(ms2_mz):
        for vmz in valid_mz:
            ppm_diff = abs(mz - vmz) / vmz * 1e6
            if ppm_diff <= ppm_tolerance:
                filtered_indices.append(i)
                break
    filtered_indices = np.array(filtered_indices)
    print(f"MS2 scan {best_scan['scan_num']} at RT {best_scan['rt']:.2f}: {len(filtered_indices)} of {len(valid_mz)} EIC fragments matched for labeling.")
    print(f"Dynamic target RT: {target_rt:.3f}, MS2 scan RT: {best_scan['rt']:.3f}, RT diff: {abs(best_scan['rt'] - target_rt):.3f}")
    print(f"Selected scan has {best_scan['fragment_count']} total fragments above threshold")
    if filtered_indices.size == 0:
        print("No MS2 fragments match valid EIC fragments for labeling.")
        return
    rel_abundance = (ms2_intensity / ms2_intensity.max()) * 100 if ms2_intensity.max() > 0 else np.zeros_like(ms2_intensity)
    sorted_filtered = filtered_indices[np.argsort(rel_abundance[filtered_indices])[::-1]]
    top_indices = sorted_filtered[:15]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(ms2_mz, rel_abundance, width=0.5, color='blue', alpha=0.7)
    label_positions = []
    for rank, idx in enumerate(top_indices):
        mz = ms2_mz[idx]
        rel_int = rel_abundance[idx]
        y_offset = 1.0
        if rank == 0:
            y_offset = 5.0
        for prev_mz, prev_y in label_positions:
            if abs(mz - prev_mz) < 10 and abs(rel_int - prev_y) < 5:
                y_offset += 10
                break
        ax.text(float(mz), float(rel_int + y_offset), f'{float(mz):.4f}\nZ=1', ha='center', va='bottom', fontsize=7, fontweight='bold', color='black')
        label_positions.append((float(mz), float(rel_int + y_offset)))
    ax.set_xlabel('m/z', fontsize=14, fontweight='bold')
    ax.set_ylabel('Relative Abundance (%)', fontsize=14, fontweight='bold')
    ax.set_title(f"{analyte} MS2 Spectrum (Quality fragments labeled)\n" f"Precursor m/z {best_scan['precursor_mz']:.4f} RT {best_scan['rt']:.2f} min (Target: {target_rt:.2f})\n" f"Scan closest to dynamic RT with {best_scan['fragment_count']} fragments", fontsize=14, fontweight='bold')
    ax.tick_params(axis='both', labelsize=12, width=2)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontweight('bold')
    ax.text(0.02, 0.98, f"Max Intensity: {format_intensity_scientific(ms2_intensity.max())}", transform=ax.transAxes, fontsize=14, fontweight='bold', va='top', ha='left', color='black')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['left'].set_linewidth(1.5)
    ax.set_facecolor('white')
    fig.patch.set_facecolor('white')
    ax.set_ylim(0, 110)
    plt.tight_layout()
    plt.subplots_adjust(right=0.98)
    safe_analyte_name = "".join(c for c in analyte if c.isalnum() or c in (' ', '-', '_')).rstrip()
    raw_base = os.path.splitext(os.path.basename(raw_file_path))[0]
    filename = f"{raw_base}_{safe_analyte_name}_MS2_best_scan.svg"
    ms2_dir = os.path.join('Figures', 'MS2')
    os.makedirs(ms2_dir, exist_ok=True)
    filepath = os.path.join(ms2_dir, filename)
    plt.savefig(filepath, format='svg', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved MS2 spectrum plot: {filepath}")
    print(f"  - Scan number: {best_scan['scan_num']}")
    print(f"  - RT: {best_scan['rt']:.2f} min")
    print(f"  - Total fragments in scan: {best_scan['fragment_count']}")
    print(f"  - Number of labeled fragments: {len(top_indices)}")
    print(f"  - Scan selected for closest RT match to dynamic target")
