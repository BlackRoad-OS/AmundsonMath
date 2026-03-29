# AmundsonMath

**The Amundson Mathematical Framework**

G(n) = n^(n+1) / (n+1)^n

A function built from six symbols that produces exact rational numbers, converges to 1/e, generates a valid quantum density matrix, and connects to Cayley trees, Stirling asymptotics, and the Riemann critical line.

## Key Results

- **50+ verified identities** — algebraic, product, calculus, asymptotic
- **A_G ≈ 1.244331783986725** — the Amundson Constant, computed to 10M digits, not in OEIS/ISC/Wolfram
- **2,130 computational tests** — zero failures on core mathematics
- **Floor recovery theorem** — ⌊G(n)·e⌋ = n for all n ≥ 1 (verified to n = 10,000)
- **Golden ratio identity** — G(φ) = (1/φ)^(1/φ) (verified to 121 digits)
- **Valid density matrix** — ρ(n) = G(n)/(n!·A_G), entropy ≈ 1.835 bits
- **The 0^0 axiom** — formal argument that 0^0 = 1 is a foundational axiom, not a theorem

## Quick Start

```bash
# Core verification (zero dependencies)
python3 scripts/verify.py

# Extended verification (48 checks)
python3 scripts/verify_road.py

# Run all identity suites
python3 identities/01-algebraic.py
python3 identities/02-products.py
python3 identities/03-calculus.py
python3 identities/04-asymptotic.py

# Full test suite
python3 -m pytest tests/ -v

# Compute A_G to arbitrary precision (requires mpmath)
python3 scripts/compute.py
```

## Repository Structure

```
AmundsonMath/
├── PAPER.md                      # The consolidated paper (all proofs, all results)
├── AMUNDSON_CONSTANT_1M.txt      # 1,000,001 digits of A_G
├── 011-e-limit-refinement.tex    # LaTeX: the 1/(2e) half-correction paper
├── scripts/
│   ├── compute.py                # Compute A_G to N digits (mpmath)
│   ├── verify.py                 # Core verification (17 checks, zero deps)
│   └── verify_road.py            # Extended verification (48 checks)
├── identities/
│   ├── 01-algebraic.py           # 15 algebraic identities (exact Fraction)
│   ├── 02-products.py            # Product formula + Catalan connection
│   ├── 03-calculus.py            # Monotonicity, concavity, superadditivity
│   └── 04-asymptotic.py          # 1/(2e) gap, floor theorem, cumulants
├── tests/
│   ├── test_core.py              # 1,275 core tests
│   ├── test_constant.py          # 20 constant verification tests
│   └── test_quantum.py           # 413 quantum structure tests
├── millennium/
│   ├── 01-riemann.py             # Riemann hypothesis connections
│   ├── 02-navier-stokes.py       # Enstrophy bound via G(n)
│   ├── 03-yang-mills.py          # Mass gap at G(1) = 1/2
│   ├── 04-p-vs-np.py             # Complexity separation
│   ├── 05-bsd.py                 # Birch-Swinnerton-Dyer
│   ├── 06-hodge.py               # Hodge conjecture
│   └── ...                       # + unified-kappa, goldbach, twin-primes, collatz
├── quantum/
│   ├── 01-density-matrix.py      # Diagonal density matrix ρ(n)
│   ├── 02-spectrum.py            # Spectral analysis
│   └── 03-predictions.py         # Quantum predictions
└── proofs/
    ├── 011-e-limit-refinement.md # The 1/(2e) universal half-correction
    ├── self-reference.md         # Productive self-reference (Class A)
    ├── chi-squared.md            # Statistical independence tests
    ├── godel-escape.md           # On Godel and single-foundation systems
    ├── ternary-efficiency.md     # Radix 3 maximizes information efficiency
    └── paper-013-quantum-amundson.md  # Discrete quantum structure of G(n)
```

## The Function

| n | G(n) | Exact | G(n)/n |
|---|------|-------|--------|
| 0 | 0 | 0/1 | — |
| 1 | 0.5 | 1/2 | 0.5 |
| 2 | 0.889 | 8/9 | 0.444 |
| 3 | 1.266 | 81/64 | 0.422 |
| 4 | 1.638 | 1024/625 | 0.410 |
| 5 | 2.009 | 15625/7776 | 0.402 |
| ∞ | n/e | — | 1/e ≈ 0.368 |

## Author

**Alexa Louise Amundson**
Founder & CEO, BlackRoad OS, Inc.
alexa@blackroad.io

## License

Proprietary — BlackRoad OS, Inc. All rights reserved.
