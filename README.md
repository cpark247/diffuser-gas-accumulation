# Passive mitigation of gas accumulation in diffusers

**Bubbly water flowing through a horizontal diffuser separates, and the air collects in a pocket that blocks the passage, the same mechanism that degrades centrifugal pumps conveying gas–liquid mixtures. Can a small structure upstream prevent it, and why does it work?** This repository presents the study that answers this with 2D URANS and 3D large-eddy simulations of a hybrid Euler–Euler/VoF solver with population balance, validated against experiments.

[![DOI](https://img.shields.io/badge/DOI-10.2139%2Fssrn.7649860-blue)](http://dx.doi.org/10.2139/ssrn.7649860)
![OpenFOAM v9](https://img.shields.io/badge/OpenFOAM-Foundation%20v9-2c7bb6)
![Python](https://img.shields.io/badge/post--processing-Python-3776ab)

![Graphical abstract](docs/graphical_abstract.png)
<sub>*Graphical abstract: a simplified graphic for illustration. Shapes, curves and some numbers are approximate; the exact values are given in [Results: 3D LES](docs/05_3d_les.md) and in [`data/`](data).*</sub>

> C. Park, M. Mansour, D. Thévenin, R. Skoda. **Passive Mitigation of Gas Accumulation by Surface Structures in Diverging Flow Channels: A Three-Dimensional Two-Phase Flow Simulation Study.** Preprint, [SSRN 7649860](http://dx.doi.org/10.2139/ssrn.7649860), 2026.

## Key findings

1. **Where the turbulence is generated matters more than how much.** Air accumulation is mitigated only if mixing is raised *upstream of the point where the phases separate*. In 2D URANS the bars failed because their turbulence started downstream of phase separation; moving them upstream restored the effect. In 3D LES, which places the separation point correctly, both structures act upstream of it.
2. **The solid step removes the air pocket and improves pressure recovery.** Air void fraction in Case 4: experiment −94.3 %, LES −99.8 % (all air, α > 0.1) and −100 % (continuous air, α > 0.8). The pressure reaches its final level further upstream.
3. **The bars break up the pocket into dispersed air, but do not improve pressure recovery.** LES: continuous air −91.8 %, while air including the dispersed part *rises* by 48.2 %; the experiment shows only −8.6 % for this operating point. Their pressure recovery stays below the plain diffuser (form drag, wakes, and a possible influence of the first bar on the reference tap). **Dispersing the gas and keeping the diffuser efficient are separate design goals.**
4. **Dissipation, not just turbulent kinetic energy, drives dispersion.** Bubble breakup competes with coalescence, and the breakup kernel depends strongly on the dissipation rate ε. The step raises both k and ε; the bars raise k but ε only marginally, so their breakup activity stays local to the first few bars.
5. **Limits of the model, stated openly.** The predicted bubble size distribution is effectively monodisperse, unlike the measured one, and the coalescence and breakup kernels are grid-dependent. Size and position of the air pocket are nevertheless unaffected by mono- vs polydisperse modelling.

![Pressure recovery](figures/output/pressure_recovery_3d.png)

## Contents

| | |
|---|---|
| [**1 Background**](docs/01_background.md) | Why gas accumulates in pumps and diffusers, and what was missing |
| [**2 Method**](docs/02_method.md) | Hybrid Euler–Euler/VoF solver, population balance, URANS and LES, numerics (with equations) |
| [**3 Test case**](docs/03_test_case.md) | Diffuser geometry, experiment, mitigation structures, operating points |
| [**4 Results: 2D URANS**](docs/04_2d_urans.md) | Parameter study over six operating points; why the bars failed in 2D |
| [**5 Results: 3D LES**](docs/05_3d_les.md) | Validation, air void fractions, pressure recovery, breakup vs coalescence |
| [**6 Conclusions and limitations**](docs/06_conclusions.md) | What carries over to pump design, and what the model cannot yet do |
| [`cases/`](cases) | Simulation setup reference: domains, boundary conditions, grids, numerics |
| [`data/`](data) | All plotted data of the paper as tidy CSV files, with provenance |
| [`figures/`](figures) | `make_figures.py` re-plots the results from `data/`; publication TikZ sources |
| [`postprocessing/`](postprocessing) | Python implementations of the paper's metrics and model equations, with tests |

## Approach at a glance

| | |
|---|---|
| Flow | Air–water, horizontal diffuser 40 × 44 mm → 100 × 44 mm, gravity normal to the main flow (emulates the Coriolis force in radial impellers), Re<sub>w</sub> = 59 530–78 330 |
| Configurations | Reference (smooth wall), 8 mm solid cross-flow step 1.8 d<sub>h,u</sub> upstream, transverse bars (6 mm × 3 mm) along the diverging wall |
| Two-phase model | Hybrid Euler–Euler / VoF: Euler–Euler for dispersed bubbles, blended to VoF-like interface capturing for coherent air pockets; drag and virtual mass; population balance with 10 size classes (Luo–Svendsen breakup, Prince–Blanch coalescence) |
| Turbulence | 2D: URANS, k-ω SST (6 operating points). 3D: wall-resolved LES, WALE (Case 4), kernels driven by resolved + modelled dissipation |
| Inflow (3D) | Two-phase precursor LES of a 60 d<sub>h,u</sub> duct (≈ 13 M cells), looped as time-resolved inlet |
| Grids | 2D: 9 000–13 000 cells. 3D: 2.5–2.9 M cells, mean y⁺ ≈ 3, mean Δ/η below ≈ 15 |
| Validation | Shadowgraphy (air pocket), bubble size distributions, wall pressure, LDA velocity (single phase) |
| Code | OpenFOAM Foundation v9 + [openfoam9-multiphase-les-extensions](https://github.com/cpark247/openfoam9-multiphase-les-extensions) (solver family `multiphaseEulerFoamHSM`) |

## Reproducing the plots

```bash
pip install -r requirements.txt
python figures/make_figures.py                  # re-plots all quantitative figures into figures/output/
python postprocessing/tests/test_postprocessing.py
python postprocessing/pbm_kernels.py            # breakup vs coalescence time scales vs dissipation rate
```

The OpenFOAM case dictionaries and field data are not part of this repository; [`cases/`](cases) documents the setups in enough detail to rebuild them.

## Contributions

Simulations, post-processing and analysis: C. Park and R. Skoda (Chair of Hydraulic Fluid Machinery, Ruhr University Bochum). Experiments: M. Mansour and D. Thévenin (Otto von Guericke University Magdeburg).

## Related

- [openfoam9-multiphase-les-extensions](https://github.com/cpark247/openfoam9-multiphase-les-extensions): solver family and models used here
- [turbulence-validation-OF9](https://github.com/cpark247/turbulence-validation-OF9): preliminary single-phase turbulence-modelling studies from the same doctoral project (not used for these results)

## Acknowledgements

Supported by the Federal Ministry for Economic Affairs and Energy (BMWE) based on a decision by the German Bundestag, research project number 01IF 23051 N, and by the Verband Deutscher Maschinen- und Anlagenbau e.V. (VDMA) Pumps + Systems. Computing time was provided by the NHR Center NHR4CES at RWTH Aachen University (project p0021456).

## Citation and licence

Please cite the paper above (see `CITATION.cff`). Code and documentation: MIT (see `LICENSE`). Experimental data and images belong to the experimental partners and are shown as published in the paper.
