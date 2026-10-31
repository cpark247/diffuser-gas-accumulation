# Case setups

One directory per configuration, each a complete OpenFOAM case without results:

```
cases/
    precursor/        <!-- inflow generation, if used -->
    baseline/         smooth diverging channel
    <structure_A>/    surface-structure variant
    <structure_B>/
```

Each case directory contains `0.orig/`, `constant/`, `system/`, an `Allrun` and a short `README.md` with:

| Item | Value |
|---|---|
| Solver | |
| Mesh (cells, Δ at the wall) | |
| Time step / max CFL | |
| Simulated time, averaging window | |
| Inlet void fraction, bubble size classes | |
| MPI ranks, wall time, core-hours | |

Mesh files are not committed: `Allrun` regenerates them (blockMesh / snappyHexMesh). Boundary data for recycled inflow (`constant/boundaryData/`) are large; publish them on Zenodo and fetch them in `Allrun` if needed.
