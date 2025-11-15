from instrument.audits import run_probe
from objects.ricci.mapping import get_low_mode_frames
import numpy as np

def main():
    print("=== Ricci Sensitivity Test: varying bump amplitude ===\n")

    epsilons = [0.0, 0.05, 0.1, 0.2, 0.4]
    results = []

    for eps in epsilons:
        Phi_t, Phi_tp, lambdas_t, lambdas_tp = get_low_mode_frames(d=10, epsilon=eps, dt=0.1)
        report = run_probe(Phi_t, Phi_tp, lambdas_t, lambdas_tp, taus=(0.0, 0.5, 1.0, 2.0, 4.0))

        K11 = report['P1_sham']['K11']
        K11_sham_mean = report['P1_sham']['K11_sham_mean']
        K11_sham_ci = report['P1_sham']['K11_sham_ci']
        pool_final = report['P1_sham']['pool11'][-1]
        pool_sham_ci = report['P1_sham']['pool_sham_ci']

        results.append({
            'epsilon': eps,
            'K11': K11,
            'K11_sham_mean': K11_sham_mean,
            'K11_sham_ci': K11_sham_ci,
            'pool_tau_max': pool_final,
            'pool_sham_ci': pool_sham_ci
        })

        print(f"epsilon={eps:.2f}  K11={K11:.6f}  K_sham={K11_sham_mean:.4f} CI{K11_sham_ci}  pool(tau_max)={pool_final:.6f}")

    print("\n=== Sensitivity Check ===")
    K_values = [r['K11'] for r in results]
    eps_values = epsilons

    # Check monotonicity: K should decrease as epsilon increases
    dK_deps = np.diff(K_values) / np.diff(eps_values)
    print(f"dK/d(epsilon) estimates: {dK_deps}")
    print(f"Mean slope: {np.mean(dK_deps):.6f}")

    # All shams should be low
    sham_means = [r['K11_sham_mean'] for r in results]
    sham_max = max(sham_means)
    sham_ci_upper = max(r['K11_sham_ci'][1] for r in results)
    print(f"Max sham K (mean): {sham_max:.4f}")
    print(f"Max sham K (95% CI upper): {sham_ci_upper:.4f}")

    print("\n=== Pass/Fail ===")
    print(f"Sham collapse (mean < 0.15): {'PASS' if sham_max < 0.15 else 'FAIL'}")
    print(f"Sham collapse (CI upper < 0.20): {'PASS' if sham_ci_upper < 0.20 else 'FAIL'}")
    print(f"K responds to epsilon (slope < 0): {'PASS' if all(dK <= 0 for dK in dK_deps) else 'FAIL'}")
    print(f"K sensitivity magnitude: {'PASS' if any(dK < -0.0001 for dK in dK_deps) else 'WEAK'}")

if __name__ == '__main__':
    main()
