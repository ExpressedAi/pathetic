import numpy as np
from instrument.phase_k import orthonormalize
from instrument.audits import run_probe

def synthetic_frames(n=512, d=10, coherence=0.85, rng=None):
    if rng is None:
        rng = np.random.default_rng(1)
    A = rng.standard_normal((n,d)); B = rng.standard_normal((n,d))
    Qa, _ = np.linalg.qr(A); Qb, _ = np.linalg.qr(B)
    Qb = orthonormalize(coherence*Qa + (1-coherence)*Qb)
    lambdas = np.linspace(0.5, 5.0, d)
    return Qa, Qb, lambdas, lambdas

def main():
    Qa, Qb, la, lb = synthetic_frames(coherence=0.85)
    report = run_probe(Qa, Qb, la, lb, taus=(0.0,0.5,1.0,2.0))
    print('=== Instrument Demo Report ===')
    for k,v in report.items():
        print(k, ':', v)

if __name__ == '__main__':
    main()
