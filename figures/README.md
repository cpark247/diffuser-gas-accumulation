# Figures

## Re-plotted from data

`make_figures.py` draws every quantitative result from the CSV files in [`../data`](../data) into `output/`:

```bash
python make_figures.py          # PNG
python make_figures.py --pdf    # PNG + PDF
```

Colours follow the configuration throughout (reference, solid step, bars; Okabe–Ito, colour-blind safe), with line styles as a second cue.

| Output | Paper figure | Data |
|---|---|---|
| `pressure_recovery_3d.png` | Pressure recovery, 3D LES vs experiment | `pressure_recovery_3d.csv` |
| `air_void_fraction_3d.png` | AVF table (as a chart) | `air_void_fraction_3d.csv` |
| `relative_accumulation_2d.png` | Relative accumulation size, 2D | `air_accumulation_relative_2d.csv` |
| `bubble_size_distribution.png` | Measured BSD | `bubble_size_distribution_experiment.csv` |
| `velocity_profiles_single_phase.png` | Single-phase velocity profiles | `velocity_profiles_single_phase.csv`, `diffuser_upper_wall_contour.csv` |
| `streamwise_air_3d.png` | Continuous/dispersed air and α<sub>a,rms</sub> | `streamwise_profiles_3d.csv` |
| `streamwise_turbulence_3d.png` | Streamwise k<sup>+</sup> and ε<sup>+</sup> | `streamwise_profiles_3d.csv` |
| `statistical_convergence_p4.png` | Statistical convergence | `statistical_convergence_p4.csv` |

## Paper figures

The figures as published (contour plots from the simulations, shadowgraphy images from the experiment, geometry drawings) are in [`../docs/images`](../docs/images) and are used in the documentation pages.

## TikZ / pgfplots sources

[`tikz/`](tikz) holds the standalone LaTeX sources of the publication's charts and sketches, with the data files they read (`tikz/data/`, the BSD CSVs). Compile with `pdflatex <file>.tex` (needs `pgfplots` and `siunitx`).

| Source | Paper figure |
|---|---|
| `diffuser_geometry_standalone.tex` | Diffuser sketch |
| `crossflow_step_geometry_standalone.tex` | Cross-flow step |
| `BSD_exp_standalone.tex` | Measured bubble size distribution |
| `2D_air_void_fraction_barGraphs_standalone.tex` | Relative accumulation size, 2D |
| `stat_convergence_standalone.tex` | Statistical convergence |
| `1Ph_vel_validation_standalone.tex` | Single-phase velocity profiles |
| `3D_LES_combined_pressure_validation-standalone.tex` | Pressure recovery |
| `combined_contAir_alphaAirRMS_standalone.tex` | Continuous/dispersed air and α<sub>a,rms</sub> |
| `combined_tkeWater_epsWater.tex` | Streamwise k<sup>+</sup> and ε<sup>+</sup> |

Figures that composite simulation renderings (contour plots) are included as images only.
