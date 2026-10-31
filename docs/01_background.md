# 1 Background

[← Overview](../README.md) · [2 Method →](02_method.md)

## Gas accumulation in pumps

Centrifugal pumps are designed for liquids but are routinely used for gas–liquid mixtures: in nuclear and geothermal plants, the pulp and paper industry, wastewater treatment and oil production. A gas content of only about 1 % can already disturb liquid conveyance. The reason is **phase separation inside the impeller channels**:

- In radial impellers the Coriolis force points towards the blade pressure side, creating pressure gradients across the passage.
- The widening flow passage promotes flow separation and recirculation, especially at part load.
- Because air is much lighter than water, the pressure gradients drive the phases apart, and gas collects on the blade suction side in the separated region.

At higher gas contents coherent **gas pockets** form, block the channel, and can lead to a complete breakdown of head and efficiency.

## Why a diffuser

A rotating impeller is hard to instrument. A **horizontal diffuser with a gradually increasing opening angle** reproduces the essential mechanism in a controllable setting: the diverging walls provoke flow separation, and gravity, acting normal to the main flow, plays the role of the Coriolis force by pushing the air across the passage. Experiments on this diffuser (Mansour et al.) showed that

- a sizeable air pocket forms even at an inlet air volume fraction of about 0.05 %;
- the pocket grows with the air flow rate, while the water flow rate has a non-monotonic effect, traced back to turbulence intensity;
- reducing separation or raising turbulence mitigates the accumulation: large transverse **bars** helped at high flow rates, and **solid steps** of 5–8 mm height worked best over a broad operating range.

## What simulation adds, and what was missing

Experiments give the size and position of the air pocket and wall pressures, but limited local information. CFD can show *why* a structure works. For this flow, however, the usual models fall short:

| Approach | Limitation for this flow |
|---|---|
| Euler–Euler two-fluid | Assumes a homogeneous bubble–liquid mixture in every cell; fits bubbly flow but not coherent gas pockets |
| Volume of Fluid | Resolves interfaces, but only for structures much larger than the cells; cannot represent small dispersed bubbles |
| Monodisperse bubbles | A single bubble size cannot represent breakup and coalescence |
| RANS | Averages away the turbulent structures that break bubbles up |

A **hybrid Euler–Euler/VoF solver** (Hundshagen et al.) handles both regimes in one framework. It had been used for LES of this diffuser with a constant bubble diameter (Nguyen et al. 2023) and, combined with a population balance model, for pump flows.

## Contribution of this study

This work combines **turbulence-resolving LES**, a **polydisperse population balance** and the **transition from dispersed bubbles to coherent air pockets** in one simulation, and applies it to the two most effective passive structures from the experiments, a solid step and transverse bars. The aim is to explain the mechanisms by which they mitigate air accumulation, which the experiments alone could not resolve.
