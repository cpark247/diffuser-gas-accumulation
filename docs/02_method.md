# 2 Simulation method

[← 1 Background](01_background.md) · [Overview](../README.md) · [3 Test case →](03_test_case.md)

Python transcriptions of the equations on this page are in [`postprocessing/pbm_kernels.py`](../postprocessing/pbm_kernels.py).

## 2.1 Hybrid Euler–Euler / VoF two-phase model

Mass and momentum are solved for each phase φ (w = water, a = air), isothermal, without mass transfer; both phases are treated as incompressible and share one pressure field:

$$
\frac{\partial \alpha_\varphi}{\partial t}+\nabla\cdot(\alpha_\varphi \mathbf{c}_\varphi)+\underbrace{C_\alpha\,\nabla\cdot\big(\mathbf{c}_\mathrm{c}\,\alpha_\varphi(1-\alpha_\varphi)\big)}_{\text{interface compression}}=0
$$

$$
\frac{\partial \alpha_\varphi\rho_\varphi\mathbf{c}_\varphi}{\partial t}+\nabla\cdot(\alpha_\varphi\rho_\varphi\mathbf{c}_\varphi\mathbf{c}_\varphi^T)+\nabla\cdot(\alpha_\varphi\rho_\varphi\mathbf{R}^\mathrm{eff}_\varphi)
=\alpha_\varphi\rho_\varphi\mathbf{g}-\alpha_\varphi\nabla p\pm C_\beta\mathbf{M}_{\mathrm{d},\varphi}\pm\mathbf{M}_{\mathrm{vm},\varphi}+C_\alpha\mathbf{M}_{\mathrm{s},\varphi}
$$

**Interfacial forces.** In horizontal bubbly flow and in pump flow, drag and virtual mass dominate; lift and wall lubrication are neglected.

- Drag (Schiller–Naumann, spherical bubbles), with the Sauter mean diameter from the population balance as bubble size:
  $\mathbf{M}_\mathrm{d,a}=\tfrac{3}{4}\tfrac{\rho_\mathrm{w}}{d_\mathrm{B}}\alpha_\mathrm{a}C_\mathrm{D}|\mathbf{c}_\mathrm{w}-\mathbf{c}_\mathrm{a}|(\mathbf{c}_\mathrm{w}-\mathbf{c}_\mathrm{a})$,
  $d_{32}=\big(\sum_i f_i/d_{\mathrm{B},i}\big)^{-1}$
- Virtual mass with $C_\mathrm{vm}=0.5$:
  $\mathbf{M}_\mathrm{vm,a}=-C_\mathrm{vm}\alpha_\mathrm{a}\rho_\mathrm{w}\big(\tfrac{D\mathbf{c}_\mathrm{a}}{Dt}-\tfrac{D\mathbf{c}_\mathrm{w}}{Dt}\big)$
  (the paper corrects a density typo, ρ<sub>a</sub> → ρ<sub>w</sub>, in the preceding publication)
- Surface tension (continuum surface force), only active in VoF mode: $\mathbf{M}_{\mathrm{s},\varphi}=\sigma\kappa_\varphi\nabla\alpha_\varphi$, σ = 0.07275 N/m

**Switching between the two regimes.** Two blending functions make the model hybrid:

| Function | Purpose | Definition |
|---|---|---|
| $C_\alpha$ | Turns on interface compression and surface tension where a coherent interface exists (0 = Euler–Euler, 1 = VoF-like) | $\big[\tfrac12\tanh(a_B(\alpha_\mathrm{a}-a_\min))+\tfrac12\big]\big[\tfrac12\tanh(a_B(a_\max-\alpha_\mathrm{a}))+\tfrac12\big]$, $a_B=35$, $a_\min=0.1$, $a_\max=0.9$ |
| $C_\beta$ | Keeps drag active in dispersed regions, switches it (almost) off inside air pockets | $\min\!\big(\max\big(\tfrac{(1-\alpha_\mathrm{a})b_\max}{(1-b_\max)\alpha_\mathrm{a}},\tfrac{b_\min}{\alpha_\mathrm{a}}\big),1\big)$, $b_\min=10^{-4}$, $b_\max=0.8$ |

The compression velocity is $\mathbf{c}_\mathrm{c}=|\mathbf{c}_\mathrm{m}|\,\nabla\alpha_\varphi/|\nabla\alpha_\varphi|$ with the volume-fraction-averaged mixture velocity $\mathbf{c}_\mathrm{m}$.

## 2.2 Population balance

A multi-size-group (MUSIG-type) method with **10 bubble size classes** (0.25–4.75 mm, Δd = 0.5 mm) sharing one air velocity field. For each class:

$$
\frac{\partial f_i\alpha_\mathrm{a}\rho_\mathrm{a}}{\partial t}+\nabla\cdot(f_i\alpha_\mathrm{a}\rho_\mathrm{a}\mathbf{c}_\mathrm{a})=B_{\mathrm{c},i}-D_{\mathrm{c},i}+B_{\mathrm{b},i}-D_{\mathrm{b},i}
$$

**Coalescence**, Prince & Blanch (1990), turbulent and buoyancy-driven collisions times a film-drainage efficiency:

$$
\Gamma(d_i,d_j)=C_\Gamma\Big(C_1\pi(d_i+d_j)^2\varepsilon_\mathrm{w}^{1/3}\sqrt{d_i^{2/3}+d_j^{2/3}}+A_{ij}|u_{r,i}-u_{r,j}|\Big)\exp\!\Big(-\sqrt{\tfrac{r_{ij}^3\rho_\mathrm{w}}{16\sigma}}\ln\tfrac{h_0}{h_f}\,\tfrac{\varepsilon_\mathrm{w}^{1/3}}{r_{ij}^{2/3}}\Big)
$$

with $r_{ij}=(1/d_i+1/d_j)^{-1}$, $A_{ij}=\tfrac{\pi}{4}(d_i+d_j)^2$, $u_{r,i}=\sqrt{2.14\sigma/(\rho_\mathrm{w}d_i)+0.505\,g\,d_i}$. The factor $C_\Gamma=1$ for α<sub>a</sub> < 0.8 and $\min(1/(1-\alpha_\mathrm{a})^2,10^5)$ above (Liao et al. 2015), so coalescence is amplified at least 25-fold inside dense air regions.

**Binary breakup**, Luo & Svendsen (1996):

$$
\Omega(d_i,d_j)=C_4\alpha_\mathrm{w}\Big(\frac{\varepsilon_\mathrm{w}}{d_j^2}\Big)^{1/3}\int_{\xi_\min}^1\frac{(1+\xi)^2}{\xi^{11/3}}\exp\!\Big(-\frac{12c_f\sigma}{\beta\rho_\mathrm{w}\varepsilon_\mathrm{w}^{2/3}d_j^{5/3}\xi^{11/3}}\Big)\mathrm{d}\xi
$$

with $c_f=(v_i/v_j)^{2/3}+(1-v_i/v_j)^{2/3}-1$ and $\xi_\min=C_5\eta/d_j$ (η: Kolmogorov length). The integral is evaluated with the incomplete Gamma function.

| Kernel | Constants (original values; C<sub>1</sub> calculation error corrected) |
|---|---|
| Coalescence | C<sub>1</sub> = 0.356, h<sub>0</sub> = 10⁻⁴ m, h<sub>f</sub> = 10⁻⁸ m |
| Breakup | C<sub>4</sub> = 0.923, C<sub>5</sub> = 11.4, β = 2.05 |

Both kernels were developed for other applications (bubble columns, stirred vessels) and are used uncalibrated; see the [limitations](06_conclusions.md#limitations). The kernels connect to the flow through α<sub>a</sub>, **c**<sub>a</sub> and, most importantly, the water-phase dissipation rate ε<sub>w</sub>.

## 2.3 Turbulence

| | URANS (2D) | LES (3D) |
|---|---|---|
| Model | k-ω SST (Menter 1994), per phase | WALE subgrid model (Nicoud & Ducros 1999), per phase |
| Wall treatment | Automatic wall functions, y⁺ = 20–45 | Wall-resolved, mean y⁺ ≈ 3 (max < 5) |
| ε<sub>w</sub> for the kernels | From the SST model | Resolved + modelled, evaluated instantaneously (below) |

Subgrid contributions to interfacial momentum transfer and surface tension that arise from filtering the two-phase equations are neglected, considered acceptable for the large, coherent interfaces and high Reynolds number here.

**Dissipation rate in the LES.** The kernels need an instantaneous ε, and at this resolution the subgrid part is not negligible:

$$
\varepsilon=\varepsilon_\mathrm{res}+\varepsilon_\mathrm{mod},\qquad \varepsilon_\mathrm{mod}=2\nu_t s_{ij}s_{ij},\qquad \varepsilon_\mathrm{res}\approx\tilde\varepsilon_\mathrm{res}=2\nu s_{ij}s_{ij}
$$

Using the instantaneous resolved strain rate instead of the fluctuating part avoids an arbitrary running-mean window. The two differ only by the mean-flow dissipation $2\nu\bar s_{ij}\bar s_{ij}$, which matters only near walls, and the approximation is known to hold in separated flows.

## 2.4 Numerics

- Implementation: extension of `multiphaseEulerFoam` in **OpenFOAM Foundation v9** (blending functions, interface compression, surface tension, drag switch, population balance coupling); see [OpenFOAM-PhD-Extensions](https://github.com/cpark247/OpenFOAM-PhD-Extensions).
- Pressure–velocity coupling: PIMPLE with pressure relaxation; up to 20 outer iterations with 3 PISO correctors each, until residuals drop by four orders of magnitude.
- Phase fractions: explicit MULES with 3 sub-cycles at the start of each time step; then momentum, pressure, turbulence and finally the population balance.
- Time step: max CFL 1.0 (URANS) and 0.3 (LES).

| Term | LES | URANS |
|---|---|---|
| Momentum convection | Central differencing | Second-order upwind |
| Phase-fraction convection | Second-order TVD with limiter near the interface, blending to first-order upwind in dispersed regions | same as LES |
| k, ω | – | van Leer |
