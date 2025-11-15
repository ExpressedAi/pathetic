# Ricci Flow S² Falsifier Report (auto)

**Instrument:** principal-angle K; Procrustes alignment; pooling via heat-kernel attenuation.
**Tests:** P1 (sham), P2 (sensitivity), P3 (ordering), E2 (isometry invariance).

## P1 — Sham collapse (ε = 0.20)
- K11 (signal): 0.999850
- K11 (sham mean): 0.072454
- K11 (sham 95% CI): (0.05255100521189406, 0.09868865263798265)
- pool11 (signal): ['0.999850', '0.999901', '0.999901', '0.999901', '0.999901']
- pool_sham (mean): 0.158002
- pool_sham (95% CI): (0.1060850013872306, 0.2121202797068007)
PASS criteria: K11_sham_mean ≤ 0.15 and pool_sham_mean ≤ 0.20

## P2 — Sensitivity (K vs ε)
- ε=0.05 → K11=0.999999, K11_sham=0.076976
- ε=0.20 → K11=0.999850, K11_sham=0.072454
- ε=0.40 → K11=0.997680, K11_sham=0.085492
- Approx slope dK/dε ≈ -6.627765e-03 (should be < 0)

## P3 — Low-order ordering
- τ0 ordering: [(1, 1, 0.9998504373663567), (2, 1, 0.9994018252571145), (3, 2, 0.9986543910082532)]
- τL ordering: [(1, 1, 0.9999009170282106), (2, 1, 0.9996037174355448), (3, 2, 0.9991085491652391)]
PASS criteria: K_{1:1} ≥ K_{2:1} ≥ K_{3:2} at τ0 and τL.

## E2 — Isometry invariance
- ΔK under random SO(3) rotation: 0.0000e+00 (target |ΔK| < 1e-2)
