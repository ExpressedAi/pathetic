import numpy as np
from .phase_k import K_pq_from_frames, pooling_curve, sham_scramble
from .diffeo_test import diffeo_invariance_test

def bootstrap_ci(samples, alpha=0.05, B=1000, rng=None):
    if rng is None:
        rng = np.random.default_rng()
    n = len(samples)
    means = []
    for _ in range(B):
        idx = rng.integers(0, n, size=n)
        means.append(np.mean(np.array(samples)[idx]))
    lo = np.percentile(means, 100*alpha/2)
    hi = np.percentile(means, 100*(1-alpha/2))
    return float(lo), float(hi)

def e0_calibration(Phi):
    G = Phi.T @ Phi
    err = np.linalg.norm(G - np.eye(G.shape[0]), ord='fro')
    return err

def e1_vibration(theta):
    z = np.exp(1j*theta)
    R = np.abs(np.mean(z))
    circ_var = 1 - R
    return R, circ_var

def e3_micro_nudge_effect(K_base, K_nudged):
    return K_nudged - K_base

def run_probe(Phi_t, Phi_tp, lambdas_t, lambdas_tp, taus=(0.0,1.0,2.0,4.0), ratios=((1,1),(2,1),(3,2)), rng=None, n_bootstrap=1000):
    if rng is None:
        rng = np.random.default_rng()
    report = {}

    K11, theta = K_pq_from_frames(Phi_t, Phi_tp, 1,1)
    pool11 = pooling_curve(Phi_t, Phi_tp, lambdas_t, lambdas_tp, taus, 1,1)

    # Sham test
    K11_shams = []
    pool11_shams = []
    for _ in range(min(20, n_bootstrap//50)):
        Phi_tp_sham = sham_scramble(Phi_tp, rng)
        K_s, _ = K_pq_from_frames(Phi_t, Phi_tp_sham, 1,1)
        pool_s = pooling_curve(Phi_t, Phi_tp_sham, lambdas_t, lambdas_tp, taus, 1,1)
        K11_shams.append(K_s)
        pool11_shams.append(pool_s[-1])

    K11_sham_mean = float(np.mean(K11_shams))
    K11_sham_ci = bootstrap_ci(K11_shams, alpha=0.05, B=min(200, n_bootstrap//5), rng=rng)
    pool_sham_mean = float(np.mean(pool11_shams))
    pool_sham_ci = bootstrap_ci(pool11_shams, alpha=0.05, B=min(200, n_bootstrap//5), rng=rng)

    report['P1_sham'] = {
        'K11': float(K11),
        'K11_sham_mean': K11_sham_mean,
        'K11_sham_ci': K11_sham_ci,
        'pool11': list(map(float, pool11)),
        'pool_sham_mean': pool_sham_mean,
        'pool_sham_ci': pool_sham_ci
    }

    # E2: Diffeo invariance
    K_before, K_after, delta_K = diffeo_invariance_test(Phi_t, Phi_tp, rng=rng)
    report['E2_diffeo'] = {
        'K_before': K_before,
        'K_after': K_after,
        'delta_K': delta_K,
        'invariant': delta_K < 0.02
    }

    # Ordering
    order0 = []
    orderL = []
    for p,q in ratios:
        k_curve = pooling_curve(Phi_t, Phi_tp, lambdas_t, lambdas_tp, taus, p,q)
        order0.append((p,q,float(k_curve[0])))
        orderL.append((p,q,float(k_curve[-1])))
    report['P3_ordering_tau0'] = sorted(order0, key=lambda x: -x[2])
    report['P3_ordering_tauL'] = sorted(orderL, key=lambda x: -x[2])

    report['theta_R'] = float(np.abs(np.mean(np.exp(1j*theta))))
    report['theta_circ_var'] = float(1 - report['theta_R'])

    return report
