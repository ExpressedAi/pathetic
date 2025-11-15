from instrument.audits import run_probe
from objects.ricci.mapping import get_low_mode_frames

def main():
    Phi_t, Phi_tp, lambdas_t, lambdas_tp = get_low_mode_frames(d=10)
    report = run_probe(Phi_t, Phi_tp, lambdas_t, lambdas_tp, taus=(0.0, 0.5, 1.0, 2.0, 4.0))
    print('=== Ricci Probe Report (S^2 bump scaffold) ===')
    for k,v in report.items():
        print(k, ':', v)

if __name__ == '__main__':
    main()
