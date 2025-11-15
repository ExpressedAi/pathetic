import numpy as np

def get_low_mode_frames(d=10):
    # TODO: replace with your Ricci outputs.
    n = 512
    rng = np.random.default_rng(0)
    A = rng.standard_normal((n,d)); B = rng.standard_normal((n,d))
    Qa, _ = np.linalg.qr(A)
    Qb, _ = np.linalg.qr(B)
    U, _, Vt = np.linalg.svd(rng.standard_normal((d,d)))
    R = U @ Vt
    eps = 0.1
    Qb = Qa @ (np.eye(d) + eps * (R - np.eye(d)))
    lambdas = np.linspace(0.5, 5.0, d)
    return Qa, Qb, lambdas, lambdas + 0.1
