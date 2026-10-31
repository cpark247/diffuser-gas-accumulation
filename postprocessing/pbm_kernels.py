"""
Reference implementation of the model equations of the paper (Section 2): blending functions
of the hybrid Euler-Euler/VoF solver, the population-balance kernels and the breakup and
coalescence time scales used to explain dispersion.

This is a standalone NumPy/SciPy transcription for analysis and teaching, not the solver code
(the solver is C++ in OpenFOAM, see OpenFOAM-PhD-Extensions). SI units throughout.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.integrate import quad

# Fluid properties (air-water)
SIGMA = 0.07275        # surface tension [N/m]
RHO_W = 998.0          # water density [kg/m^3]
NU_W = 1.0e-6          # kinematic viscosity of water [m^2/s]
G = 9.81               # gravitational acceleration [m/s^2]

# Kernel constants (paper Table: original values, C1 corrected)
C1, H0, HF = 0.356, 1e-4, 1e-8          # Prince & Blanch (1990)
C4, C5, BETA = 0.923, 11.4, 2.05        # Luo & Svendsen (1996)

# Size classes used in the paper: 10 classes, 0.25 ... 4.75 mm, spacing 0.5 mm
SIZE_CLASSES_M = np.arange(0.25, 4.76, 0.5) * 1e-3


# --------------------------------------------------------------------------- blending
def c_alpha(alpha_a, a_b=35.0, a_min=0.1, a_max=0.9):
    """Interface-resolution blending C_alpha (Haensch et al. 2012): 0 = Euler-Euler, 1 = VoF-like."""
    alpha_a = np.asarray(alpha_a, float)
    return (0.5 * np.tanh(a_b * (alpha_a - a_min)) + 0.5) * (0.5 * np.tanh(a_b * (a_max - alpha_a)) + 0.5)


def c_beta(alpha_a, b_min=1e-4, b_max=0.8):
    """Drag blending C_beta: drag active in dispersed regions, clipped to b_min inside air pockets."""
    a = np.clip(np.asarray(alpha_a, float), 1e-12, 1.0)
    return np.minimum(np.maximum((1 - a) * b_max / ((1 - b_max) * a), b_min / a), 1.0)


# --------------------------------------------------------------------------- PBM helpers
def sauter_mean_diameter(fractions, diameters=SIZE_CLASSES_M):
    """d_32 = (sum_i f_i / d_i)^-1 for size fractions f_i (normalised internally)."""
    f = np.asarray(fractions, float)
    f = f / f.sum()
    return 1.0 / np.sum(f / np.asarray(diameters, float))


def kolmogorov_length(eps, nu=NU_W):
    return (nu ** 3 / eps) ** 0.25


def rise_velocity(d, sigma=SIGMA, rho=RHO_W, g=G):
    """Bubble rise velocity magnitude u_r used in the buoyancy collision term."""
    return math.sqrt(2.14 * sigma / (rho * d) + 0.505 * g * d)


def c_gamma(alpha_a):
    """Coalescence amplification in dense regions (Liao et al. 2015): 1 below alpha=0.8."""
    if alpha_a < 0.8:
        return 1.0
    return min(1.0 / (1.0 - alpha_a) ** 2, 1e5) if alpha_a < 1.0 else 1e5


# --------------------------------------------------------------------------- kernels
def coalescence_kernel(d_i, d_j, eps, alpha_a=0.0, sigma=SIGMA, rho=RHO_W):
    """Prince & Blanch (1990) coalescence kernel Gamma(d_i, d_j) [m^3/s] with C_Gamma.

    Collision frequency (turbulent + buoyancy-driven) times coalescence efficiency.
    Laminar-shear collisions are not included, as in the paper.
    """
    r_ij = 1.0 / (1.0 / d_i + 1.0 / d_j)
    a_ij = math.pi / 4.0 * (d_i + d_j) ** 2
    collision = (C1 * math.pi * (d_i + d_j) ** 2 * eps ** (1 / 3) * math.sqrt(d_i ** (2 / 3) + d_j ** (2 / 3))
                 + a_ij * abs(rise_velocity(d_i) - rise_velocity(d_j)))
    efficiency = math.exp(-math.sqrt(r_ij ** 3 * rho / (16.0 * sigma)) * math.log(H0 / HF) * eps ** (1 / 3) / r_ij ** (2 / 3))
    return c_gamma(alpha_a) * collision * efficiency


def breakup_kernel(d_mother, volume_fraction, eps, alpha_w=1.0, sigma=SIGMA, rho=RHO_W, nu=NU_W):
    """Luo & Svendsen (1996) binary breakup kernel Omega [1/s].

    ``volume_fraction`` is the daughter-to-mother volume ratio v_i/v_j in (0, 1); the
    increase of surface energy enters through c_f. The integral over the dimensionless eddy
    size xi from xi_min = C5*eta/d to 1 is evaluated numerically here (the solver uses the
    incomplete Gamma function, which is equivalent).
    """
    fv = float(volume_fraction)
    cf = fv ** (2 / 3) + (1 - fv) ** (2 / 3) - 1.0
    xi_min = min(C5 * kolmogorov_length(eps, nu) / d_mother, 1.0)
    b = 12.0 * cf * sigma / (BETA * rho * eps ** (2 / 3) * d_mother ** (5 / 3))

    def integrand(xi):
        return (1 + xi) ** 2 / xi ** (11 / 3) * math.exp(-b / xi ** (11 / 3))

    integral, _ = quad(integrand, xi_min, 1.0, limit=200)
    return C4 * alpha_w * (eps / d_mother ** 2) ** (1 / 3) * integral


# --------------------------------------------------------------------------- time scales
def coalescence_time_scale(d32, eps, alpha_a):
    """t_c = v0 / (Gamma(v0, v0) * alpha_a), v0 = pi/6 d32^3 (Buffo et al. 2016). Lower = more coalescence."""
    v0 = math.pi / 6.0 * d32 ** 3
    return v0 / (coalescence_kernel(d32, d32, eps, alpha_a) * alpha_a)


def breakup_time_scale(d32, eps, alpha_w=1.0, volume_fraction=0.5):
    """t_b = 1 / Omega(v0). Lower = more breakup.

    The daughter volume ratio at which Omega is evaluated is a parameter (default: equal
    binary split, 0.5).
    """
    return 1.0 / breakup_kernel(d32, volume_fraction, eps, alpha_w)


if __name__ == "__main__":
    # Small demonstration: how the dissipation rate shifts the balance between breakup and coalescence
    d32 = 1.4e-3
    print(f"{'eps [m2/s3]':>12} {'t_b [s]':>12} {'t_c [s]':>12}")
    for eps in (0.5, 1.0, 5.0, 20.0, 100.0):
        print(f"{eps:12.3g} {breakup_time_scale(d32, eps):12.4g} {coalescence_time_scale(d32, eps, 0.01):12.4g}")
