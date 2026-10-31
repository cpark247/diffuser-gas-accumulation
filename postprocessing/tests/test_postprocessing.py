"""
Checks for the post-processing modules. Run from the repository root:

    python -m pytest postprocessing/tests        # or: python postprocessing/tests/test_postprocessing.py
"""
import csv
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "postprocessing"))

import diffuser_metrics as dm  # noqa: E402
import pbm_kernels as pk  # noqa: E402


def read(name):
    with open(ROOT / "data" / name, encoding="utf-8") as f:
        return list(csv.DictReader(line for line in f if not line.startswith("#")))


def test_avf_thresholds():
    alpha = np.array([0.0, 0.05, 0.3, 0.85, 1.0])
    vol = np.ones(5)
    assert dm.air_void_fraction(alpha, vol, 0.8) == (0.85 + 1.0) / 5
    assert dm.air_void_fraction(alpha, vol, 0.1) == (0.3 + 0.85 + 1.0) / 5
    vc, vd, vt = dm.continuous_dispersed_volumes(alpha, vol)
    assert math.isclose(vc + vd, vt)


def test_relative_changes_match_paper_table():
    """The bracketed percentages in the paper's AVF table follow from its absolute values."""
    rows = {r["configuration"]: r for r in read("air_void_fraction_3d.csv")}
    ref = rows["reference"]
    for cfg in ("step", "bars"):
        for col_abs, col_rel in (("exp_avf", "exp_change_percent"),
                                 ("sim_avf_alpha_gt_0p1", "sim_change_alpha_gt_0p1_percent"),
                                 ("sim_avf_alpha_gt_0p8", "sim_change_alpha_gt_0p8_percent")):
            got = dm.relative_change(float(rows[cfg][col_abs]), float(ref[col_abs]))
            assert abs(got - float(rows[cfg][col_rel])) < 0.06, (cfg, col_abs, got)


def test_streamwise_fractions_sum_to_one():
    rng = np.random.default_rng(0)
    x, alpha, vol = rng.uniform(0, 10, 1000), rng.uniform(0, 1, 1000), rng.uniform(1, 2, 1000)
    _, fc, fd = dm.streamwise_air_fractions(x, alpha, vol, bins=20)
    assert math.isclose(fc.sum() + fd.sum(), 1.0, rel_tol=1e-12)


def test_pressure_recovery_normalisation():
    assert np.allclose(dm.pressure_recovery([1.0, 2.0, 3.0], 1.0, 3.0), [0.0, 0.5, 1.0])


def test_blending_functions():
    assert pk.c_alpha(0.5) > 0.99 and pk.c_alpha(0.0) < 0.05 and pk.c_alpha(1.0) < 0.05
    assert pk.c_beta(0.01) == 1.0
    assert math.isclose(pk.c_beta(1.0), 1e-4)


def test_sauter_mean_diameter():
    f = np.zeros(10); f[3] = 1.0
    assert math.isclose(pk.sauter_mean_diameter(f), pk.SIZE_CLASSES_M[3])


def test_experimental_d32_matches_paper():
    """Paper: measured d32 ~ 1.8 mm (Case 5) and 1.9 mm (Case 6)."""
    rows = read("bubble_size_distribution_experiment.csv")
    for case, expected in ((5, 1.8), (6, 1.9)):
        r = [q for q in rows if q["dataset"] == f"experiment_case{case}"]
        d = np.array([float(q["d_center_mm"]) for q in r])
        n = np.array([float(q["bubble_count"]) for q in r])
        assert abs((n * d**3).sum() / (n * d**2).sum() - expected) < 0.06


def test_breakup_faster_at_higher_dissipation():
    t = [pk.breakup_time_scale(1.4e-3, eps) for eps in (1.0, 10.0, 100.0)]
    assert t[0] > t[1] > t[2] > 0


def test_coalescence_amplified_in_air_pockets():
    assert pk.coalescence_kernel(1e-3, 1e-3, 1.0, alpha_a=0.9) > 50 * pk.coalescence_kernel(1e-3, 1e-3, 1.0, alpha_a=0.5)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok ", name)
