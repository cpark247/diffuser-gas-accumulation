# 6 Conclusions and limitations

[← 5 Results: 3D LES](05_3d_les.md) · [Overview](../README.md)

## Conclusions

1. **Timing of turbulence relative to phase separation decides.** Steps and bars can both break up air pockets, but only if they raise mixing *upstream* of the phase-separation point. Structures that add turbulence downstream of it do not disperse the pocket. Pre-conditioning the flow before separation is the controlling mechanism.
2. **Dispersion and hydraulic performance are decoupled.** The solid step removes the pocket and improves pressure recovery. The bars reduce the continuous pocket, but their form drag and wake losses bring pressure recovery below the unmodified diffuser. Mitigation structures must be designed for both goals.
3. **At the bubble scale, breakup competes with coalescence.** Coalescence drives accumulation, breakup drives dispersion. Effective dispersion needs not only turbulent kinetic energy but a high dissipation rate. The step raises both; the bars raise k but hardly ε, and their breakup activity decays quickly behind the first bars, so their effect is weaker and threshold-sensitive. Experimental confirmation of this mechanism is still open.
4. **2D URANS is useful for screening but misleading for placement.** It predicts flow and phase separation too far upstream, which is enough to turn an effective structure (bars) into an ineffective one in the model. 3D LES places separation correctly.

## What this means for pumps

The diffuser emulates phase separation in radial impeller channels. The results suggest evaluating anti-accumulation features by *where* they generate dissipation relative to the separation point and by their pressure losses, not only by the turbulence they add.

## Limitations

| Limitation | Consequence | Next step |
|---|---|---|
| Kernel constants taken from other applications, uncalibrated | Predicted bubble size distribution effectively monodisperse, unlike the measurement | Calibrate coalescence and breakup kernels for this flow |
| Coalescence and breakup kernels are grid-dependent | No strict grid independence of the bubble size distribution (and of the 2D pocket size) | Resolution-aware kernel parameters; separate numerical from model error |
| Unclosed multiphase subgrid terms neglected in the LES | Acceptable for large coherent interfaces, unverified for dispersed regions | Formulate and assess subgrid interfacial terms |
| One operating point in 3D (Case 4, where bars are least effective) | Conclusions on bars rest on a weak-effect case | LES of further operating points |
| Threshold-based air volumes | Grid-dependent, sensitive to post-processing choice | Read them as morphology indicators (dispersed vs continuous) rather than exact volumes |
| Spanwise skew of the air pocket | Physical origin unclear (corner attachment? Görtler instability?) | Dedicated experimental and numerical study |

Mono- versus polydisperse modelling did **not** change the size or position of the air pocket or the phase-separation point, so the main conclusions do not depend on the bubble size distribution.
