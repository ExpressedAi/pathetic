import numpy as np

def orthonormalize(X):
    Q, R = np.linalg.qr(X)
    s = np.sign(np.diag(R)); s[s==0]=1.0
    Q = Q @ np.diag(s)
    return Q

def procrustes(Phi_t, Phi_tp):
    U = Phi_t.T @ Phi_tp
    W, S, Vt = np.linalg.svd(U, full_matrices=False)
    R = W @ Vt
    Phi_tp_aligned = Phi_tp @ R.T
    return Phi_tp_aligned, R

def principal_angles_from_R(R):
    w = np.linalg.eigvals(R)
    theta = np.angle(w)
    theta = (theta + np.pi) % (2*np.pi) - np.pi
    return theta

def K_pq_from_frames(Phi_t, Phi_tp, p=1, q=1):
    Phi_tp_aligned, R = procrustes(Phi_t, Phi_tp)
    theta = principal_angles_from_R(R)
    ephi = p*theta  # reference is Phi_t; Procrustes absorbed it
    return np.abs(np.mean(np.exp(1j*ephi))), theta

def heat_kernel_pool_frame(Phi, lambdas, tau):
    d = Phi.shape[1]
    A = np.diag(np.exp(-tau * np.array(lambdas[:d])))
    return Phi @ A

def pooling_curve(Phi_t, Phi_tp, lambdas_t, lambdas_tp, taus=(0.0, 1.0, 2.0, 4.0), p=1, q=1):
    ks = []
    for tau in taus:
        Pt = heat_kernel_pool_frame(Phi_t, lambdas_t, tau)
        Ptp = heat_kernel_pool_frame(Phi_tp, lambdas_tp, tau)
        K, _ = K_pq_from_frames(Pt, Ptp, p=p, q=q)
        ks.append(K)
    return np.array(ks)

def random_orthogonal(d, rng=None):
    if rng is None:
        rng = np.random.default_rng()
    A = rng.standard_normal((d,d))
    Q, R = np.linalg.qr(A)
    s = np.sign(np.diag(R)); s[s==0]=1.0
    return Q @ np.diag(s)

def sham_scramble(Phi_tp, rng=None):
    if rng is None:
        rng = np.random.default_rng()
    d = Phi_tp.shape[1]
    Q = random_orthogonal(d, rng)
    return Phi_tp @ Q
