# Simulation setups

The OpenFOAM case dictionaries and field data are not included in this repository. This page records the setups from the paper in enough detail to rebuild them with OpenFOAM Foundation v9 and the solver family from [openfoam9-multiphase-les-extensions](https://github.com/cpark247/openfoam9-multiphase-les-extensions).

## Common to all cases

| Item | Setting |
|---|---|
| Phases | Water (continuous) and air (dispersed or continuous), isothermal, incompressible, no mass transfer, σ = 0.07275 N/m |
| Solver | Hybrid Euler–Euler/VoF extension of `multiphaseEulerFoam` with population balance (solver family `multiphaseEulerFoamHSM` in openfoam9-multiphase-les-extensions) |
| Blending | C<sub>α</sub>: a<sub>B</sub> = 35, a<sub>min</sub> = 0.1, a<sub>max</sub> = 0.9; C<sub>β</sub>: b<sub>min</sub> = 10⁻⁴, b<sub>max</sub> = 0.8 |
| Interfacial forces | Schiller–Naumann drag with d<sub>32</sub>; virtual mass C<sub>vm</sub> = 0.5; surface tension (CSF) blended with C<sub>α</sub> |
| Population balance | 10 classes, 0.25–4.75 mm, Δd = 0.5 mm; Prince–Blanch coalescence with C<sub>Γ</sub>; Luo–Svendsen binary breakup; constants in [`data/pbm_kernel_constants.csv`](../data/pbm_kernel_constants.csv) |
| Coupling | PIMPLE, ≤ 20 outer iterations × 3 PISO correctors, exit at 4 orders residual drop; MULES with 3 sub-cycles |
| Boundary conditions | No slip at walls; constant pressure at the outlet |

## 2D URANS (all six operating points)

| Item | Setting |
|---|---|
| Domain | 2D channel: 60 d<sub>h,u</sub> inlet section (fully developed two-phase flow), diffuser, downstream section as in the experiment |
| Configurations | Reference, step, bars, bars shifted upstream |
| Grid | Structured hex, level G2: reference 9 000, step 10 000, bars 13 000 cells; y⁺ 20–45 |
| Turbulence | k-ω SST per phase, automatic wall functions |
| Schemes | Momentum: second-order upwind; k, ω: van Leer; α: TVD with limiter near interfaces → first-order upwind in dispersed regions |
| Time step | Max CFL 1.0 |
| Inlet | Uniform air fraction per [`data/operating_points.csv`](../data/operating_points.csv) (2D column); bubbles 0.25 mm |
| Evaluation | Air pocket from the ᾱ<sub>a</sub> = 0.8 iso-line; BSD 0.6 d<sub>h,u</sub> upstream of the diffuser |

## 3D LES (Case 4: Re<sub>w</sub> = 59 530, α<sub>a,inlet</sub> = 0.223 %)

**Precursor duct** (inflow generation, 40 × 44 mm cross-section)

| Item | Single phase | Two-phase |
|---|---|---|
| Length | 4π d<sub>h,u</sub>, periodic, bulk-velocity forcing (`meanVelocityForce`) | 60 d<sub>h,u</sub>, inflow/outflow |
| Grid | – | ≈ 13 M cells |
| Inlet | – | Homogeneous α<sub>a</sub> = 0.223 %, d<sub>B</sub> = 0.25 mm |
| Output | – | Plane at x = 58 d<sub>h,u</sub>, three large-eddy turnover times, velocity and α |

**Diffuser**

| Item | Setting |
|---|---|
| Domain | 5 d<sub>h,u</sub> upstream, diffuser, downstream section incl. constriction |
| Grid | Reference ≈ 2.5 M (after Nguyen et al. 2023); step and bars ≈ 2.9 M (near-wall 2D grid extruded spanwise) |
| Resolution | Mean y⁺ ≈ 3, max < 5; Δ/η mean below ≈ 15, max 18; ν<sub>t</sub>/ν ≈ 1.5 (max 3) |
| Turbulence | WALE per phase; kernel ε = 2ν s<sub>ij</sub>s<sub>ij</sub> + 2ν<sub>t</sub> s<sub>ij</sub>s<sub>ij</sub> (instantaneous) |
| Schemes | Momentum: central differencing; α as in 2D |
| Time step | Max CFL 0.3 |
| Inlet | Precursor plane looped in time as a time-resolved Dirichlet condition for velocity and α; BSD = measured distribution, mean of Cases 5 and 6 |
| Initial field | Converged monodisperse solution (Re<sub>w</sub> = 50 130); quasi-steady after ≈ 3 flow-through times |
| Averaging | Until the mean tap pressures change < 0.01 % between successive windows |
| Monodisperse comparison | Reference case without population balance, d<sub>B</sub> = 0.3 mm |
