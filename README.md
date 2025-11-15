# Phase-Locking Instrument for Geometric Flows

Minimal implementation of K_{p:q} phase-locking observable for Ricci flow on S^2.

## Structure

```
instrument/          # domain-agnostic measurement
  phase_k.py         # Procrustes alignment, principal angles, K_{p:q}
  audits.py          # probe runner (sham, pooling, ordering)

objects/ricci/       # S^2 Ricci flow
  s2_flow.py         # spherical harmonic-based flow simulator
  mapping.py         # eigenfunction loader interface
  experiment_s2_bump.py     # single probe run
  sensitivity_test.py       # epsilon sweep

scripts/
  demo_synthetic_frames.py  # instrument test on synthetic data
```

## Run

```bash
# Test instrument on synthetic coherent frames
PYTHONPATH=. python scripts/demo_synthetic_frames.py

# S^2 Ricci flow probe (single epsilon)
PYTHONPATH=. python objects/ricci/experiment_s2_bump.py

# Sensitivity test (epsilon sweep)
PYTHONPATH=. python objects/ricci/sensitivity_test.py
```

## What Works

- Sham collapse: scrambled frames → K < 0.15
- Sensitivity: larger bump → lower K (monotonic)
- Pooling: heat-kernel smoothing preserves low-mode coherence
- Ordering: K_{1:1} ≥ K_{2:1} ≥ K_{3:2}

## M0 Mapping (Ricci Flow)

**Observable:** principal-angle coherence between low-mode eigenspaces of Laplacian at (t, t+Δt)

**Gauge:** Procrustes orthogonal alignment before angle measurement

**Pooling:** heat-kernel operator e^{-τΔ}

**Falsifiers:**
- Sham (random frame rotation) must collapse K
- Metric perturbation must decrease K
- Higher-order ratios (p:q) must have lower K
