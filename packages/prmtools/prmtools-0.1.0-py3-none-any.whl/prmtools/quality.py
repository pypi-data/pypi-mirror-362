import numpy as np
def assess_peak_quality(rt_array, intensity_array, min_peak_height_ratio=0.3, min_left_trend=0.3, max_right_trend=-0.3):
    """
    Assess if a peak follows good Gaussian behavior and calculate S/N ratio.
    Parameters:
        rt_array: np.ndarray, retention time values
        intensity_array: np.ndarray, intensity values
        min_peak_height_ratio: float, minimum ratio of peak height to apex intensity
        min_left_trend: float, minimum correlation for left side
        max_right_trend: float, maximum correlation for right side
    Returns:
        dict with peak quality metrics
    """
    if len(rt_array) < 3 or len(intensity_array) < 3:
        return {'is_good_peak': False, 'reason': 'insufficient_points', 'SNR': 0}
    apex_idx = int(np.argmax(intensity_array))
    apex_intensity = float(intensity_array[apex_idx])
    if apex_idx == 0 or apex_idx == len(intensity_array) - 1:
        return {'is_good_peak': False, 'reason': 'apex_at_edge', 'SNR': 0}
    peak_width = max(1, len(intensity_array) // 4)
    peak_start = max(0, apex_idx - peak_width)
    peak_end = min(len(intensity_array), apex_idx + peak_width)
    baseline_region = np.concatenate([
        intensity_array[:peak_start],
        intensity_array[peak_end:]
    ])
    if len(baseline_region) < 3:
        avg_baseline = float(np.min(intensity_array))
        noise_std = float(np.std(intensity_array)) * 0.1
    else:
        avg_baseline = float(np.median(baseline_region))
        noise_std = float(np.std(baseline_region - avg_baseline))
    snr = (apex_intensity - avg_baseline) / noise_std if noise_std > 0 else 0
    peak_height = apex_intensity - avg_baseline
    if peak_height < apex_intensity * min_peak_height_ratio:
        return {'is_good_peak': False, 'reason': 'low_peak_height', 'SNR': 0}
    left_side = intensity_array[:apex_idx]
    right_side = intensity_array[apex_idx+1:]
    if len(left_side) > 1:
        left_trend = float(np.corrcoef(range(len(left_side)), left_side)[0, 1])
        if left_trend < min_left_trend:
            return {'is_good_peak': False, 'reason': 'poor_left_trend', 'SNR': 0}
    if len(right_side) > 1:
        right_trend = float(np.corrcoef(range(len(right_side)), right_side)[0, 1])
        if right_trend > max_right_trend:
            return {'is_good_peak': False, 'reason': 'poor_right_trend', 'SNR': 0}
    left_width = apex_idx
    right_width = len(intensity_array) - apex_idx - 1
    symmetry = min(left_width, right_width) / max(left_width, right_width) if max(left_width, right_width) > 0 else 0
    snr = apex_intensity / avg_baseline if avg_baseline > 0 else 0
    return {
        'is_good_peak': True,
        'apex_intensity': apex_intensity,
        'baseline': avg_baseline,
        'peak_height': peak_height,
        'symmetry': symmetry,
        'apex_rt': float(rt_array[apex_idx]),
        'SNR': snr
    }

def integrate_eic_gaussian(consolidated_fragments, raw_fragments, analyte, target_rt, integration_window=0.2, output_dir='.'): 
    from scipy.signal import savgol_filter
    ppm_tolerance = 20
    valid_fragments = []
    for idx, frag in enumerate(consolidated_fragments):
        if not isinstance(frag, dict):
            print(f"  Skipping invalid consolidated fragment (not a dict): {frag}")
            continue
        mz = frag['fragment_mz']
        matching = [
            f for f in raw_fragments
            if abs(f['fragment_mz'] - mz) / mz * 1e6 <= ppm_tolerance
        ]
        if not matching:
            continue
        matching.sort(key=lambda x: x['rt'])
        rt_array = np.array([f['rt'] for f in matching])
        intensity_array = np.array([f['intensity'] for f in matching])
        if len(rt_array) >= 5:
            window_length = min(11, len(rt_array))
            if window_length % 2 == 0:
                window_length -= 1
            if window_length < 3:
                window_length = 3
            polyorder = min(2, window_length - 1)
            try:
                smoothed = savgol_filter(intensity_array, window_length=window_length, polyorder=polyorder)
                smoothed = np.maximum(smoothed, 0)
            except ValueError:
                smoothed = intensity_array
        else:
            smoothed = intensity_array
        apex_idx = np.argmax(smoothed)
        apex_rt = rt_array[apex_idx]
        apex_intensity = smoothed[apex_idx]
        win_start = target_rt - integration_window
        win_end = target_rt + integration_window
        if not (win_start <= apex_rt <= win_end):
            print(f"  Fragment m/z {mz:.4f}: apex outside integration window ({apex_rt:.3f} not in [{win_start:.3f}, {win_end:.3f}])")
            continue
        quality = assess_peak_quality(rt_array, smoothed)
        if not quality['is_good_peak']:
            print(f"  Fragment m/z {mz:.4f}: poor peak quality ({quality['reason']})")
            continue
        in_window_mask = (rt_array >= win_start) & (rt_array <= win_end)
        window_rt = rt_array[in_window_mask]
        window_intensity = smoothed[in_window_mask]
        if len(window_rt) == 0:
            continue
        if len(window_rt) >= 3:
            try:
                from scipy.interpolate import interp1d
                interp_rt = np.linspace(window_rt.min(), window_rt.max(), len(window_rt) * 3)
                interp_func = interp1d(window_rt, window_intensity, kind='cubic', bounds_error=False, fill_value=0)
                interp_intensity = interp_func(interp_rt)
                interp_intensity = np.maximum(interp_intensity, 0)
            except:
                interp_rt = window_rt
                interp_intensity = window_intensity
        else:
            interp_rt = window_rt
            interp_intensity = window_intensity
        if len(interp_rt) > 1:
            eic_area = np.trapz(interp_intensity, interp_rt)
        else:
            eic_area = 0
        if len(rt_array) > 1:
            total_area = np.trapz(smoothed, rt_array)
        else:
            total_area = 0
        frag['EIC_Area'] = eic_area
        frag['Total_EIC_Area'] = total_area
        frag['Max_Absolute_Intensity'] = np.max(interp_intensity) if len(interp_intensity) > 0 else 0
        frag['EIC_Points'] = list(zip(rt_array.tolist(), smoothed.tolist()))
        frag['EIC_Points_Window'] = list(zip(interp_rt.tolist(), interp_intensity.tolist()))
        frag['max_intensity_raw'] = np.max(smoothed)
        frag['apex_rt'] = apex_rt
        frag['apex_intensity'] = apex_intensity
        frag['peak_quality'] = quality
        valid_fragments.append(frag)
        print(f"  Fragment m/z {mz:.4f}: VALID (apex: {apex_rt:.3f}, area: {eic_area:.2f}, quality: {quality['peak_height']:.0f})")
    print(f"Valid fragments after Gaussian assessment: {len(valid_fragments)}/{len(consolidated_fragments)}")
    return valid_fragments
