import numpy as np
from scipy.special import sph_harm

def sphere_mesh_fibonacci(N=512):
    """Fibonacci lattice on S^2."""
    indices = np.arange(0, N, dtype=float) + 0.5
    phi = np.arccos(1 - 2*indices/N)
    theta = np.pi * (1 + 5**0.5) * indices
    x = np.sin(phi) * np.cos(theta)
    y = np.sin(phi) * np.sin(theta)
    z = np.cos(phi)
    return np.column_stack([x, y, z]), theta, phi

def spherical_harmonic_basis(theta, phi, lmax=10):
    """Generate spherical harmonic basis up to degree lmax."""
    basis = []
    for l in range(lmax+1):
        for m in range(-l, l+1):
            Y = sph_harm(m, l, theta, phi)
            basis.append(Y.real if m >= 0 else Y.imag)
    return np.array(basis).T

def laplacian_eigenvalues_sphere(lmax=10):
    """Eigenvalues -l(l+1) for spherical harmonics."""
    evals = []
    for l in range(lmax+1):
        for m in range(-l, l+1):
            evals.append(l*(l+1))
    return np.array(evals)

def perturbed_metric_coefficients(lmax=10, bump_l=3, bump_m=0, epsilon=0.1, rng=None):
    """Metric perturbation as spherical harmonic expansion coefficients."""
    if rng is None:
        rng = np.random.default_rng(0)
    n_modes = sum(2*l+1 for l in range(lmax+1))

    # Start near round metric (small random perturbation)
    coeffs = rng.normal(0, 0.01, n_modes)

    # Add a targeted bump at (l,m)
    idx = sum(2*l+1 for l in range(bump_l)) + (bump_m + bump_l)
    if idx < n_modes:
        coeffs[idx] += epsilon

    return coeffs

def ricci_flow_step(coeffs, lambdas, dt=0.05, damping=0.9):
    """
    Simplified Ricci flow: high-frequency modes decay faster.
    Real Ricci flow on S^2 with perturbation converges to round metric.
    We simulate decay toward round (coeffs -> 0) with rate ~ eigenvalue.
    """
    decay = np.exp(-damping * lambdas * dt)
    return coeffs * decay

def build_eigenfunction_matrix(basis, coeffs, d=10, coupling_strength=0.1):
    """
    Reconstruct metric perturbation, then return 'low modes' of perturbed Laplacian.
    Simplified: use spherical harmonic basis directly; low modes = first d basis functions
    with coupling from metric coefficients.
    """
    n, n_modes = basis.shape
    # Start with base spherical harmonics
    Phi = basis[:, :d].copy()

    # Apply coupling from metric perturbation
    # Each mode gets mixed with higher modes weighted by coefficients
    perturbation = basis @ coeffs
    mixing_matrix = np.eye(d)

    # Create mode mixing based on coefficients
    for i in range(d):
        for j in range(d):
            if i != j:
                mixing_matrix[i, j] = coupling_strength * coeffs[min(i+j, n_modes-1)]

    # Apply mixing
    Phi = Phi @ mixing_matrix

    # Orthonormalize
    Phi, _ = np.linalg.qr(Phi)
    return Phi

def simulate_ricci_flow(epsilon=0.1, dt=0.05, lmax=10, d=10, N=512, rng=None):
    """
    Generate two snapshots: (t, t+dt) for S^2 Ricci flow with bump.

    Returns:
        Phi_t, Phi_tp: (N, d) eigenfunction matrices
        lambdas_t, lambdas_tp: (d,) eigenvalue arrays
    """
    if rng is None:
        rng = np.random.default_rng(42)

    # Mesh
    xyz, theta, phi = sphere_mesh_fibonacci(N)
    basis = spherical_harmonic_basis(theta, phi, lmax=lmax)
    lambdas_all = laplacian_eigenvalues_sphere(lmax=lmax)

    # Initial metric perturbation
    coeffs_t = perturbed_metric_coefficients(lmax=lmax, bump_l=3, bump_m=0, epsilon=epsilon, rng=rng)

    # Flow one step
    coeffs_tp = ricci_flow_step(coeffs_t, lambdas_all, dt=dt, damping=0.9)

    # Build eigenfunction matrices with coupling strength scaled by epsilon
    coupling_t = 0.8 * epsilon
    coupling_tp = 0.8 * epsilon * np.exp(-0.9 * dt)  # decays with flow

    Phi_t = build_eigenfunction_matrix(basis, coeffs_t, d=d, coupling_strength=coupling_t)
    Phi_tp = build_eigenfunction_matrix(basis, coeffs_tp, d=d, coupling_strength=coupling_tp)

    # Eigenvalues (low modes of round S^2 + perturbation)
    lambdas_base = lambdas_all[:d].astype(float)
    lambdas_t = lambdas_base + 0.1 * epsilon * np.abs(coeffs_t[:d])
    lambdas_tp = lambdas_base + 0.1 * epsilon * np.abs(coeffs_tp[:d])

    return Phi_t, Phi_tp, lambdas_t, lambdas_tp
