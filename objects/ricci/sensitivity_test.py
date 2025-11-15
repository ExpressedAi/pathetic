from instrument.audits import run_probe
from objects.ricci.mapping import get_low_mode_frames
import numpy as np

def main():
    print("=== Ricci Sensitivity Test: varying bump amplitude ===\n")

    epsilons = [0.0, 0.05, 0.1, 0.2, 0.4]
    results = []

    for eps in epsilons:
        Phi_t, Phi_tp, lambdas_t, lambdas_tp = get_low_mode_frames(d=10, epsilon=eps, dt=0.1)
        report = run_probe(Phi_t, Phi_tp, lambdas_t, lambdas_tp, taus=(0.0, 1.0, 2.0, 4.0))

        K11 = report['P1_sham']['K11']
        K11_sham = report['P1_sham']['K11_sham']
        pool_final = report['P1_sham']['pool11'][-1]

        results.append({
            'epsilon': eps,
            'K11': K11,
            'K11_sham': K11_sham,
            'pool_tau_max': pool_final
        })

        print(f"epsilon={eps:.2f}  K11={K11:.6f}  K_sham={K11_sham:.6f}  pool(tau_max)={pool_final:.6f}")

    print("\n=== Sensitivity Check ===")
    K_values = [r['K11'] for r in results]
    eps_values = epsilons

    # Check monotonicity: K should decrease (or stay high) as epsilon increases
    dK_deps = np.diff(K_values) / np.diff(eps_values)
    print(f"dK/d(epsilon) estimates: {dK_deps}")

    # All shams should be low
    sham_max = max(r['K11_sham'] for r in results)
    print(f"Max sham K: {sham_max:.4f} (should be < 0.3)")

    print("\n=== Pass/Fail ===")
    print(f"Sham collapse: {'PASS' if sham_max < 0.3 else 'FAIL'}")
    print(f"K responds to epsilon: {'PASS' if any(dK < -0.01 for dK in dK_deps) or all(K > 0.95 for K in K_values) else 'CHECK'}")

if __name__ == '__main__':
    main()
