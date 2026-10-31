"""
Air-accumulation metrics used in the paper, written for plain NumPy arrays of cell data
(e.g. exported from OpenFOAM with fluidfoam, PyVista or the `foamToVTK` utility).

All functions take time-averaged cell values: air volume fraction ``alpha`` (alpha_a bar),
cell volumes ``vol`` and, where needed, the streamwise cell-centre coordinate ``x``.
"""
from __future__ import annotations

import numpy as np

CONTINUOUS_THRESHOLD = 0.8   # alpha_a > 0.8: continuous air (introduced in the paper)
DISPERSED_THRESHOLD = 0.1    # alpha_a > 0.1: includes dispersed air (Nguyen et al. 2023)


def air_void_fraction(alpha, vol, threshold, region_volume=None, region_mask=None):
    """Air void fraction (AVF) as defined in the paper.

    Sum of alpha*V over cells with alpha > threshold, divided by the volume of the
    evaluated diffuser portion (measured from the diffuser inlet, as in the experiment).

    Parameters
    ----------
    alpha, vol : array_like
        Time-averaged air volume fraction and cell volume per cell.
    threshold : float
        Volume-fraction threshold (0.1 or 0.8 in the paper).
    region_mask : array_like of bool, optional
        Cells belonging to the evaluated diffuser portion. Default: all cells.
    region_volume : float, optional
        Volume of the evaluated portion. Default: sum of ``vol`` over ``region_mask``.
    """
    alpha = np.asarray(alpha, float)
    vol = np.asarray(vol, float)
    mask = np.ones_like(alpha, bool) if region_mask is None else np.asarray(region_mask, bool)
    if region_volume is None:
        region_volume = vol[mask].sum()
    sel = mask & (alpha > threshold)
    return float((alpha[sel] * vol[sel]).sum() / region_volume)


def relative_change(value, reference):
    """Relative change in percent, as given in brackets in the paper's AVF table."""
    return 100.0 * (value - reference) / reference


def continuous_dispersed_volumes(alpha, vol, threshold=CONTINUOUS_THRESHOLD):
    """Split the time-averaged air volume into continuous (alpha > threshold) and dispersed parts.

    Returns (V_a_continuous, V_a_dispersed, V_a_total).
    """
    alpha = np.asarray(alpha, float)
    vol = np.asarray(vol, float)
    va = alpha * vol
    cont = alpha > threshold
    return float(va[cont].sum()), float(va[~cont].sum()), float(va.sum())


def streamwise_distribution(x, values, vol, bins):
    """Cross-section integral of a cell quantity along x.

    Bins cells by their streamwise coordinate and sums ``values`` (already volume
    weighted, e.g. alpha*V) in each bin. Returns (bin_centres, sums).
    """
    x = np.asarray(x, float)
    values = np.asarray(values, float)
    edges = np.asarray(bins, float) if np.ndim(bins) else np.linspace(x.min(), x.max(), int(bins) + 1)
    idx = np.clip(np.digitize(x, edges) - 1, 0, len(edges) - 2)
    sums = np.bincount(idx, weights=values, minlength=len(edges) - 1)
    return 0.5 * (edges[1:] + edges[:-1]), sums


def streamwise_air_fractions(x, alpha, vol, bins, threshold=CONTINUOUS_THRESHOLD):
    """Streamwise V_a,c/V_a and V_a,d/V_a (paper figure 'continuous and dispersed air').

    Each cross-sectional slice is normalised by the total air volume V_a of the whole
    domain, so the curves of one configuration integrate to one together.
    """
    alpha = np.asarray(alpha, float)
    vol = np.asarray(vol, float)
    va = alpha * vol
    cont = alpha > threshold
    xc, vc = streamwise_distribution(x, np.where(cont, va, 0.0), vol, bins)
    _, vd = streamwise_distribution(x, np.where(cont, 0.0, va), vol, bins)
    total = va.sum()
    return xc, vc / total, vd / total


def alpha_rms(alpha_mean, alpha_sq_mean):
    """RMS of the air volume fraction from the running means of alpha and alpha^2."""
    return np.sqrt(np.maximum(np.asarray(alpha_sq_mean) - np.asarray(alpha_mean) ** 2, 0.0))


def pressure_recovery(p, p2, p8):
    """Normalised wall-pressure recovery (p_i - p_2)/(p_8 - p_2) used in the paper."""
    return (np.asarray(p, float) - p2) / (p8 - p2)
