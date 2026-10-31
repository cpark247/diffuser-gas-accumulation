#!/usr/bin/env python3
"""
Re-plot the quantitative results of the paper from the CSV files in ../data.

    python make_figures.py              # writes PNGs to ./output
    python make_figures.py --pdf        # also writes PDFs

Every figure is drawn only from the extracted data, so the plots can be checked
against the numbers in data/ and restyled freely.
"""
from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
OUT = HERE / "output"

# One colour per configuration, used in every figure (Okabe-Ito, colour-blind safe),
# plus a line style as secondary encoding.
CFG = {
    "reference": dict(color="#D55E00", ls="-", label="Reference"),
    "step": dict(color="#0072B2", ls="--", label="Solid step"),
    "bars": dict(color="#009E73", ls="-.", label="Bars"),
    "shifted_bars": dict(color="#009E73", ls=":", label="Shifted bars"),
}
INK, MUTED, GRID = "#1f2328", "#6e7781", "#d0d7de"

plt.rcParams.update({
    "font.size": 9, "axes.labelsize": 9, "axes.titlesize": 9.5, "legend.fontsize": 8,
    "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED,
    "text.color": INK, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.5,
    "axes.spines.top": False, "axes.spines.right": False, "lines.linewidth": 1.6,
    "savefig.dpi": 200, "savefig.bbox": "tight", "figure.dpi": 100,
})


def read(name: str) -> list[dict]:
    with open(DATA / name, encoding="utf-8") as f:
        rows = [line for line in f if not line.startswith("#")]
    return list(csv.DictReader(rows))


def diffuser_span(ax):
    """Shade the diverging section (x/d_h,u from 0 to the end of the wall contour)."""
    wall = read("diffuser_upper_wall_contour.csv")
    x = np.array([float(r["x_over_dhu"]) for r in wall])
    y = np.array([float(r["y_over_dhu"]) for r in wall])
    end = x[np.nonzero(np.abs(np.diff(y)) > 1e-9)[0].max() + 1]
    ax.axvspan(0, end, color="#f2f4f7", zorder=0, lw=0)
    return end


def save(fig, name, pdf):
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / f"{name}.png")
    if pdf:
        fig.savefig(OUT / f"{name}.pdf")
    plt.close(fig)
    print(f"wrote output/{name}.png")


def fig_pressure_recovery(pdf):
    rows = read("pressure_recovery_3d.csv")
    fig, axes = plt.subplots(1, 3, figsize=(9.0, 2.9), sharey=True)
    for ax, cfg in zip(axes, ("reference", "step", "bars")):
        r = [q for q in rows if q["configuration"] == cfg]
        x = np.array([float(q["x_over_dhu"]) for q in r])
        e, de = (np.array([float(q[k]) for q in r]) for k in ("exp_cp", "exp_uncertainty"))
        s, ds = (np.array([float(q[k]) for q in r]) for k in ("sim_cp", "sim_temporal_std"))
        c = CFG[cfg]["color"]
        ax.fill_between(x, s - ds, s + ds, color=c, alpha=0.15, lw=0, label="LES ±1 temporal std")
        ax.plot(x, s, color=c, ls=CFG[cfg]["ls"], marker="o", ms=4, label="3D LES")
        ax.errorbar(x, e, yerr=de, fmt="s", ms=4, color=INK, capsize=2.5, lw=1, label="Experiment")
        ax.set_title(CFG[cfg]["label"])
        ax.set_xlabel(r"$x/d_\mathrm{h,u}$")
    axes[0].set_ylabel(r"$(p_i-p_2)/(p_8-p_2)$")
    axes[0].legend(loc="lower right", frameon=False)
    fig.suptitle("Wall-pressure recovery, Case 4 (Re$_w$ = 59 530)", x=0.01, y=1.04, ha="left", fontsize=10)
    save(fig, "pressure_recovery_3d", pdf)


def fig_air_void_fraction(pdf):
    rows = {r["configuration"]: r for r in read("air_void_fraction_3d.csv")}
    metrics = [("exp_avf", "Experiment\n(shadowgraphy)"),
               ("sim_avf_alpha_gt_0p1", "3D LES\n" + r"$\bar\alpha_a>0.1$ (incl. dispersed)"),
               ("sim_avf_alpha_gt_0p8", "3D LES\n" + r"$\bar\alpha_a>0.8$ (continuous)")]
    cfgs = ("reference", "step", "bars")
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    w = 0.26
    for i, cfg in enumerate(cfgs):
        vals = [float(rows[cfg][m]) for m, _ in metrics]
        xs = np.arange(len(metrics)) + (i - 1) * w
        ax.bar(xs, vals, width=w - 0.02, color=CFG[cfg]["color"], label=CFG[cfg]["label"], zorder=2)
        for x, v in zip(xs, vals):
            ax.text(x, v + 0.004, f"{v:.3g}", ha="center", va="bottom", fontsize=7, color=INK)
    ax.set_xticks(np.arange(len(metrics)), [m[1] for m in metrics])
    ax.set_ylabel("Air void fraction [-]")
    ax.grid(axis="x", visible=False)
    ax.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.22))
    ax.set_ylim(0, 0.28)
    ax.set_title("Accumulated air in the diffuser, Case 4", loc="left")
    save(fig, "air_void_fraction_3d", pdf)


def fig_relative_accumulation_2d(pdf):
    rows = read("air_accumulation_relative_2d.csv")
    fig, axes = plt.subplots(1, 3, figsize=(9.0, 2.7), sharey=False)
    for ax, cfg in zip(axes, ("step", "bars", "shifted_bars")):
        r = [q for q in rows if q["configuration"] == cfg]
        cases = [f"Case {q['case']}" for q in r]
        x = np.arange(len(r))
        ax.bar(x - 0.18, [float(q["exp_percent_of_reference"]) for q in r], 0.34, color="#8c959f",
               label="Experiment (original bars)" if cfg == "shifted_bars" else "Experiment", zorder=2)
        ax.bar(x + 0.18, [float(q["sim2d_percent_of_reference"]) for q in r], 0.34, color=CFG[cfg]["color"], label="2D URANS", zorder=2)
        ax.axhline(100, color=INK, lw=0.8, ls=":")
        ax.set_xticks(x, cases)
        ax.set_title(CFG[cfg]["label"] + (" (simulation only)" if cfg == "shifted_bars" else ""))
        ax.grid(axis="x", visible=False)
        ax.legend(frameon=False, loc="upper left")
    axes[0].set_ylabel("Accumulation size,\n% of reference")
    save(fig, "relative_accumulation_2d", pdf)


def fig_bubble_size(pdf):
    exp = read("bubble_size_distribution_experiment.csv")
    fig, ax = plt.subplots(figsize=(5.6, 2.9))
    for ds, col in (("experiment_case5", "#8c959f"), ("experiment_case6", INK)):
        r = [q for q in exp if q["dataset"] == ds]
        d = np.array([float(q["d_center_mm"]) for q in r])
        n = np.array([float(q["number_density"]) for q in r])
        cnt = np.array([float(q["bubble_count"]) for q in r])
        d32 = (cnt * d**3).sum() / (cnt * d**2).sum()
        ax.step(d, n, where="mid", color=col, label=f"Case {ds[-1]}  ($d_{{32}}$ = {d32:.2f} mm)")
    classes = np.arange(0.25, 4.76, 0.5)
    ax.plot(classes, np.full_like(classes, -0.004), "|", color=CFG["step"]["color"], ms=8,
            label="Simulation size classes (10)")
    ax.set_xlim(0, 5); ax.set_ylim(-0.008, None)
    ax.set_xlabel("Bubble diameter [mm]"); ax.set_ylabel("Number density [-]")
    ax.set_title("Measured bubble size distribution upstream of the diffuser, Re$_w$ = 78 330", loc="left")
    ax.legend(frameon=False)
    save(fig, "bubble_size_distribution", pdf)


def fig_velocity_profiles(pdf):
    rows = read("velocity_profiles_single_phase.csv")
    wall = read("diffuser_upper_wall_contour.csv")
    fig, ax = plt.subplots(figsize=(9.0, 3.2))
    ax.plot([float(r["x_over_dhu"]) for r in wall], [float(r["y_over_dhu"]) for r in wall], color=MUTED, lw=1)
    ax.axhline(0, color=MUTED, lw=1)
    style = {"experiment": dict(ls="none", marker="o", ms=3, color=INK, label="Experiment (LDA)"),
             "sim_2d": dict(ls="--", color="#8c959f", lw=1.2, label="2D URANS"),
             "sim_3d": dict(ls="-", color=CFG["step"]["color"], lw=1.4, label="3D LES")}
    by = defaultdict(list)
    for r in rows:
        by[(int(r["station"]), r["source"])].append(r)
    seen = set()
    for (st, src), r in sorted(by.items()):
        x0 = float(r[0]["x_over_dhu"])
        ax.plot([x0, x0], [0, 1.2], color=GRID, lw=0.6, zorder=0)
        kw = dict(style[src]); lab = kw.pop("label")
        ax.plot([x0 + float(q["c_over_cbulk"]) for q in r], [float(q["y_over_dhu"]) for q in r],
                label=None if src in seen else lab, **kw)
        seen.add(src)
    ax.set_xlabel(r"$x/d_\mathrm{h,u} + c/c_\mathrm{bulk}$"); ax.set_ylabel(r"$y/d_\mathrm{h,u}$ (from centreline)")
    ax.set_aspect("equal"); ax.set_ylim(-0.05, 1.3)
    ax.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.62))
    ax.set_title("Single-phase velocity profiles at mid-span, Re = 59 530", loc="left")
    save(fig, "velocity_profiles_single_phase", pdf)


def _streamwise(ax, rows, quantity, ylabel):
    end = diffuser_span(ax)
    for cfg in ("reference", "step", "bars"):
        r = [q for q in rows if q["configuration"] == cfg and q["quantity"] == quantity]
        ax.plot([float(q["x_over_dhu"]) for q in r], [float(q["value"]) for q in r],
                color=CFG[cfg]["color"], ls=CFG[cfg]["ls"], label=CFG[cfg]["label"])
    ax.set_ylabel(ylabel); ax.set_xlim(-2, 15)
    return end


def fig_streamwise(pdf):
    rows = read("streamwise_profiles_3d.csv")
    fig, axes = plt.subplots(3, 1, figsize=(6.4, 6.6), sharex=True)
    _streamwise(axes[0], rows, "continuous_air_fraction", r"$V_\mathrm{a,c}/V_\mathrm{a}$")
    _streamwise(axes[1], rows, "dispersed_air_fraction", r"$V_\mathrm{a,d}/V_\mathrm{a}$")
    end = _streamwise(axes[2], rows, "alpha_a_rms", r"$\alpha_\mathrm{a,rms}$")
    axes[0].legend(frameon=False, ncol=3, loc="upper right")
    axes[0].text(end / 2, axes[0].get_ylim()[1] * 0.95, "diffuser", ha="center", va="top", color=MUTED, fontsize=8)
    axes[-1].set_xlabel(r"$x/d_\mathrm{h,u}$")
    axes[0].set_title("Continuous vs dispersed air and air pulsation (3D LES, Case 4)", loc="left")
    save(fig, "streamwise_air_3d", pdf)

    fig, axes = plt.subplots(2, 1, figsize=(6.4, 4.6), sharex=True)
    _streamwise(axes[0], rows, "alpha_w_k_plus", r"$\bar\alpha_w \bar k_w^+$")
    _streamwise(axes[1], rows, "alpha_w_eps_plus", r"$\bar\alpha_w \bar\varepsilon_w^+$")
    for ax in axes:
        ax.axvline(-1.8, color=CFG["step"]["color"], lw=0.8, ls=":")
    axes[0].text(-1.7, axes[0].get_ylim()[1] * 0.97, "step", color=CFG["step"]["color"], fontsize=8, va="top")
    axes[0].legend(frameon=False, ncol=3, loc="upper right")
    axes[-1].set_xlabel(r"$x/d_\mathrm{h,u}$")
    axes[0].set_title("Mixing (k) and breakup driver (ε), water phase (3D LES, Case 4)", loc="left")
    save(fig, "streamwise_turbulence_3d", pdf)


def fig_convergence(pdf):
    rows = read("statistical_convergence_p4.csv")
    x = np.array([float(r["averaging_window_quarter_ftt"]) for r in rows])
    y = np.array([float(r["p_over_patm"]) for r in rows])
    fig, ax = plt.subplots(figsize=(4.6, 2.6))
    pref, tol = 1.01713, 1e-4
    ax.axhspan(pref * (1 - tol), pref * (1 + tol), color="#f2f4f7", lw=0, label="±0.01 % of converged mean")
    ax.plot(x, y, color=CFG["reference"]["color"])
    ax.set_xlabel("Averaging window [0.25 FTT]"); ax.set_ylabel(r"$\bar p_4/p_\mathrm{atm}$")
    ax.ticklabel_format(axis="y", useOffset=False)
    ax.legend(frameon=False, loc="lower right")
    ax.set_title("Statistical convergence, tap P4 (reference)", loc="left")
    save(fig, "statistical_convergence_p4", pdf)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pdf", action="store_true", help="also write PDF versions")
    a = ap.parse_args()
    for f in (fig_pressure_recovery, fig_air_void_fraction, fig_relative_accumulation_2d, fig_bubble_size,
              fig_velocity_profiles, fig_streamwise, fig_convergence):
        f(a.pdf)


if __name__ == "__main__":
    main()
