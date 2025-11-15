from .s2_flow import simulate_ricci_flow

def get_low_mode_frames(d=10, epsilon=0.1, dt=0.05):
    """
    Returns eigenfunction frames from S^2 Ricci flow simulation.

    Parameters:
        d: number of low modes
        epsilon: bump perturbation amplitude
        dt: flow time step

    Returns:
        Phi_t, Phi_tp: (N, d) eigenfunction matrices at t and t+dt
        lambdas_t, lambdas_tp: (d,) eigenvalue arrays
    """
    return simulate_ricci_flow(epsilon=epsilon, dt=dt, d=d)
