# Data

All quantitative data shown in the paper, as tidy CSV files. Each file starts with a `#` comment line describing its content and source, followed by a header row. Read with e.g. `pandas.read_csv(path, comment="#")`.

The plotted series were extracted from the pgfplots sources of the publication figures; tables were transcribed from the paper.

| File | Content | Paper source |
|---|---|---|
| `operating_points.csv` | Cases 1–6: Re<sub>w</sub>, inlet air fraction in experiment and 2D simulation | Operating-point table |
| `pressure_taps.csv` | Positions of transducers P1–P8 | Transducer table |
| `diffuser_upper_wall_contour.csv` | Upper-wall contour (x/d<sub>h,u</sub>, y/d<sub>h,u</sub> from the centreline) | Velocity-profile figure source |
| `grids.csv` | 2D and 3D grids, cell counts, resolution notes | Setup sections |
| `pbm_kernel_constants.csv` | Coalescence and breakup kernel constants | Kernel constants table |
| `bubble_size_distribution_experiment.csv` | Measured BSD, Cases 5 and 6: bin edges, counts, number density | Experimental BSD figure |
| `air_accumulation_relative_2d.csv` | Accumulation size relative to reference, experiment vs 2D URANS, for step, bars, shifted bars | 2D bar-chart figure |
| `velocity_profiles_single_phase.csv` | Mid-span velocity profiles at 12 stations: LDA, 2D URANS, 3D LES | Velocity-profile figure |
| `air_void_fraction_3d.csv` | AVF of reference, step, bars: experiment and LES with two thresholds | AVF table |
| `pressure_recovery_3d.csv` | (p<sub>i</sub>−p<sub>2</sub>)/(p<sub>8</sub>−p<sub>2</sub>) at P1–P8: experiment ± uncertainty, LES ± temporal std | Pressure-recovery figure |
| `streamwise_profiles_3d.csv` | Long format: continuous/dispersed air fraction, α<sub>a,rms</sub>, ᾱ<sub>w</sub>k̄<sub>w</sub><sup>+</sup>, ᾱ<sub>w</sub>ε̄<sub>w</sub><sup>+</sup> along x | Streamwise-distribution figures |
| `statistical_convergence_p4.csv` | Successively averaged pressure at P4 (reference) | Convergence figure |

**Ownership.** Experimental values (bubble size distributions, LDA profiles, measured pressures and AVFs) come from the experimental partners at Otto von Guericke University Magdeburg (M. Mansour, D. Thévenin) as published in the paper. Simulation values are from C. Park and R. Skoda.
