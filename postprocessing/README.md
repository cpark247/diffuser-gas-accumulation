# Post-processing

Python implementations of the metrics and model equations used in the paper, for NumPy arrays of cell data exported from OpenFOAM (e.g. with fluidfoam or PyVista).

| Module | Content |
|---|---|
| [`diffuser_metrics.py`](diffuser_metrics.py) | Air void fraction with thresholds (0.1 / 0.8), relative change, continuous vs dispersed air volume, streamwise cross-section integrals, α<sub>a,rms</sub>, normalised pressure recovery |
| [`pbm_kernels.py`](pbm_kernels.py) | Blending functions C<sub>α</sub>, C<sub>β</sub>; Sauter mean diameter; Prince–Blanch coalescence and Luo–Svendsen breakup kernels; breakup and coalescence time scales t<sub>b</sub>, t<sub>c</sub> |
| [`tests/test_postprocessing.py`](tests/test_postprocessing.py) | Unit checks, including consistency with the paper: the relative AVF changes follow from the table values, and the measured d<sub>32</sub> (≈ 1.8 / 1.9 mm) is recovered from the BSD data |

```bash
python postprocessing/tests/test_postprocessing.py    # or: python -m pytest postprocessing/tests
python postprocessing/pbm_kernels.py                  # t_b and t_c over a range of dissipation rates
```

`pbm_kernels.py` is a standalone transcription of the equations for analysis, not the C++ solver code. It reproduces the qualitative point of the paper: the breakup time scale drops by orders of magnitude as the dissipation rate rises, while the coalescence time scale changes little.

Example output:

```
 eps [m2/s3]      t_b [s]      t_c [s]
         0.5         3820       0.2158
           1         47.5       0.1952
           5       0.1629        0.179
          20      0.01282        0.213
         100     0.001883       0.4224
```
(d<sub>32</sub> = 1.4 mm, α<sub>a</sub> = 0.01 for t<sub>c</sub>, equal binary split for t<sub>b</sub>.)
