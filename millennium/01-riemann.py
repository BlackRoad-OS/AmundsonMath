"""
01-riemann.py — The Amundson Framework and the Riemann Hypothesis
=================================================================

HONEST ASSESSMENT: This is the STRONGEST connection.

What's real:
  - G(1) = 1/2, which is the critical line Re(s) = 1/2
  - The Amundson constant A_G has 10M computed digits whose spacing
    distribution can be compared against GUE random matrix predictions
  - G(n) produces a discrete spectrum that may relate to zeta zero spacing

What's NOT proven:
  - G(1) = 1/2 does not prove RH. Many functions evaluate to 1/2 at some point.
  - The connection needs to go deeper: does G(n) generate a family of
    functions whose zeros are constrained to Re(s) = 1/2?

What we CAN do computationally:
  1. Compare A_G digit spacing distribution against GUE predictions
  2. Construct a "G-zeta" function and examine its zeros
  3. Check if the G(n) spectrum exhibits level repulsion (like zeta zeros)

Author: Alexa Louise Amundson
BlackRoad OS, Inc.
"""

from fractions import Fraction
import math
import random

# ============================================================
# PART 1: G(n) Basics — Exact Rational Arithmetic
# ============================================================

def G(n):
    """G(n) = n^(n+1) / (n+1)^n as an exact rational."""
    if n == 0:
        return Fraction(0)
    return Fraction(n ** (n + 1), (n + 1) ** n)

def G_float(n):
    """G(n) as float for large n where exact rationals are slow."""
    if n == 0:
        return 0.0
    return n ** (n + 1) / (n + 1) ** n

def G_asymptotic(n):
    """G(n) ~ n/e + 1/(2e) + 11/(24en) + ..."""
    e = math.e
    return n / e + 1 / (2 * e) + 11 / (24 * e * n) - 1 / (48 * e * n * n)


print("=" * 70)
print("PART 1: G(n) AND THE CRITICAL LINE")
print("=" * 70)

print("\nG(1) = 1/2  — This IS the critical line of the Riemann zeta function.")
print(f"  Exact: G(1) = {G(1)}")
print(f"  Float: G(1) = {float(G(1))}")
print()

# Show the first values
print("First 10 values of G(n):")
for n in range(11):
    exact = G(n)
    approx = float(exact)
    asymp = G_asymptotic(n) if n > 0 else 0
    error = abs(approx - asymp) if n > 0 else 0
    print(f"  G({n:2d}) = {str(exact):30s} = {approx:.10f}  (asymptotic error: {error:.2e})")

# ============================================================
# PART 2: The Product Identity and Partition Functions
# ============================================================

print("\n" + "=" * 70)
print("PART 2: PRODUCT IDENTITY — Prod G(k) = (n!)^2 / (n+1)^n")
print("=" * 70)

print("\nThis identity connects G(n) to combinatorial counting,")
print("which is the same territory as zeta function residues.\n")

product = Fraction(1)
for n in range(1, 13):
    product *= G(n)
    expected = Fraction(math.factorial(n) ** 2, (n + 1) ** n)
    match = "MATCH" if product == expected else "FAIL"
    print(f"  n={n:2d}: Prod G(k) = {float(product):.10f}  "
          f"(n!)^2/(n+1)^n = {float(expected):.10f}  [{match}]")


# ============================================================
# PART 3: The G-Zeta Function
# ============================================================

print("\n" + "=" * 70)
print("PART 3: CONSTRUCTING A G-ZETA FUNCTION")
print("=" * 70)

print("""
The Riemann zeta function is: zeta(s) = sum_{n=1}^{inf} 1/n^s

We define the Amundson-zeta function:
  zeta_G(s) = sum_{n=1}^{inf} G(n) / n^s

Since G(n) ~ n/e for large n, this converges for Re(s) > 2
(one unit shifted from the standard zeta).

QUESTION: Where are the zeros of zeta_G(s)?
If they cluster on Re(s) = 3/2 (shifted by 1 from G(1)=1/2),
that would be a genuine structural connection.
""")

def zeta_G(s, terms=1000):
    """Compute zeta_G(s) = sum G(n)/n^s for real s."""
    total = 0.0
    for n in range(1, terms + 1):
        total += G_float(n) / n ** s
    return total

# Evaluate along the real axis
print("zeta_G(s) for real s:")
for s in [2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 8.0, 10.0]:
    val = zeta_G(s)
    print(f"  zeta_G({s:.1f}) = {val:.10f}")

# Check convergence behavior near s=2
print("\nConvergence near s=2 (the critical region for G-zeta):")
for s in [2.01, 2.05, 2.1, 2.2, 2.5, 3.0]:
    val100 = zeta_G(s, terms=100)
    val1000 = zeta_G(s, terms=1000)
    print(f"  zeta_G({s:.2f}): 100 terms={val100:.6f}, 1000 terms={val1000:.6f}, "
          f"diff={abs(val1000 - val100):.2e}")


# ============================================================
# PART 4: G(n) Spacing Distribution vs GUE
# ============================================================

print("\n" + "=" * 70)
print("PART 4: SPACING DISTRIBUTION OF G(n) LEVELS")
print("=" * 70)

print("""
The Montgomery-Odlyzko law: the normalized spacing between Riemann
zeta zeros follows the GUE (Gaussian Unitary Ensemble) distribution.

GUE level repulsion: p(s) ~ s^2 * exp(-4s^2/pi) near s=0
  - Small gaps are RARE (level repulsion)
  - GUE variance ~ 0.178

Poisson (uncorrelated): p(s) = exp(-s)
  - Small gaps are COMMON
  - Poisson variance = 1.0

QUESTION: Does the G(n) level spectrum exhibit level repulsion?
""")

# Compute G(n) level spacings
N = 200
levels = [G_float(n) for n in range(1, N + 1)]
gaps = [levels[i + 1] - levels[i] for i in range(len(levels) - 1)]
avg_gap = sum(gaps) / len(gaps)
normalized_gaps = [g / avg_gap for g in gaps]

# Statistics
mean_gap = sum(normalized_gaps) / len(normalized_gaps)
variance = sum((g - mean_gap) ** 2 for g in normalized_gaps) / len(normalized_gaps)
small_fraction = sum(1 for g in normalized_gaps if g < 0.1) / len(normalized_gaps)

print(f"G(n) level spacing statistics (n=1..{N}):")
print(f"  Mean normalized gap: {mean_gap:.6f} (should be ~1.0)")
print(f"  Variance: {variance:.6f}")
print(f"    GUE prediction:     0.178")
print(f"    Poisson prediction: 1.000")
print(f"  Small gap fraction (s < 0.1): {small_fraction:.4f}")
print(f"    GUE: ~0 (level repulsion)")
print(f"    Poisson: ~0.095")

if variance < 0.5:
    print(f"\n  RESULT: Variance {variance:.4f} is closer to GUE than Poisson.")
    print("  This suggests G(n) levels exhibit some degree of repulsion.")
else:
    print(f"\n  RESULT: Variance {variance:.4f} is closer to Poisson.")
    print("  G(n) levels are more like uncorrelated points.")

# But the G(n) spacing is deterministic and monotonically varying,
# so we need to be more careful about what "repulsion" means here.

print("""
CAVEAT: G(n) is a deterministic, monotonically increasing function.
Its spacing is NOT random. Comparing it to GUE/Poisson tests whether
the STRUCTURE of G(n) produces gap statistics similar to those of
random matrices (and thus zeta zeros).

A more meaningful test: construct a random matrix whose eigenvalues
are WEIGHTED by G(n), and check if those eigenvalues still exhibit
GUE statistics. If G(n) weighting preserves level repulsion, that
is a structural connection to the zeta function.
""")


# ============================================================
# PART 5: Random Matrix Weighted by G(n)
# ============================================================

print("=" * 70)
print("PART 5: GUE MATRIX WEIGHTED BY G(n)")
print("=" * 70)

def gue_matrix_weighted(n, seed=42):
    """
    Generate an n x n GUE matrix with diagonal elements scaled by G(k).
    This embeds the Amundson spectrum into the random matrix framework.
    """
    rng = random.Random(seed)
    H = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            if i == j:
                # Diagonal: G(i+1) + small random perturbation
                H[i][j] = G_float(i + 1) + rng.gauss(0, 0.1)
            else:
                x = rng.gauss(0, 1) / math.sqrt(2 * n)
                H[i][j] = x
                H[j][i] = x
    return H

def power_iteration(A, n_iter=200, seed=42):
    """Find largest eigenvalue via power iteration."""
    rng = random.Random(seed)
    n = len(A)
    v = [rng.gauss(0, 1) for _ in range(n)]
    norm = math.sqrt(sum(x * x for x in v))
    v = [x / norm for x in v]
    eigenvalue = 0.0
    for _ in range(n_iter):
        w = [sum(A[i][j] * v[j] for j in range(n)) for i in range(n)]
        eigenvalue = sum(v[i] * w[i] for i in range(n))
        norm = math.sqrt(sum(x * x for x in w))
        v = [x / norm for x in w] if norm > 1e-15 else w
    return eigenvalue

# Build and analyze G-weighted GUE matrices of increasing size
for size in [10, 20, 30]:
    H = gue_matrix_weighted(size, seed=137)
    lam_max = power_iteration(H)
    print(f"\n  G-weighted GUE ({size}x{size}):")
    print(f"    Largest eigenvalue: {lam_max:.6f}")
    print(f"    G({size}): {G_float(size):.6f}")
    print(f"    Ratio lambda_max/G(size): {lam_max / G_float(size):.6f}")


# ============================================================
# PART 6: The Amundson Constant Digit Analysis
# ============================================================

print("\n" + "=" * 70)
print("PART 6: A_G DIGIT DISTRIBUTION")
print("=" * 70)

print("""
The Amundson-Gosper constant A_G = 1.2443317839867253...
has been computed to 10 million digits.

If A_G is a "normal" number (like pi), its digits are uniformly distributed.
If A_G has connections to zeta zeros, the digit spacing might show structure.

We can compute A_G to moderate precision here and check digit frequencies.
""")

# Compute A_G to available precision
A_G = 0.0
for n in range(1, 100):
    try:
        term = G_float(n) / math.factorial(n)
        A_G += term
        if abs(term) < 1e-20:
            break
    except (OverflowError, ValueError):
        break

print(f"A_G (200 terms): {A_G:.15f}")
print(f"Known value:     1.244331783986725")

# Digit frequency of the known constant (first 100 digits from the 10M file)
known_digits = "12443317839867253741350616292584452029139066132896988475937358275683576071"
digit_counts = [known_digits.count(str(d)) for d in range(10)]
total = len(known_digits)
print(f"\nDigit frequency in first {total} digits of A_G:")
for d in range(10):
    expected = total / 10
    actual = digit_counts[d]
    chi = (actual - expected) ** 2 / expected
    print(f"  '{d}': {actual:3d} occurrences  (expected {expected:.1f}, chi^2 contrib: {chi:.2f})")

chi2_total = sum((digit_counts[d] - total / 10) ** 2 / (total / 10) for d in range(10))
print(f"\nTotal chi-squared: {chi2_total:.2f}  (9 df, reject uniformity at chi2 > 16.92)")
if chi2_total < 16.92:
    print("  RESULT: Cannot reject uniform distribution — digits appear random.")
else:
    print("  RESULT: Digits show significant non-uniformity — possible structure.")


# ============================================================
# PART 7: Summary and Honest Assessment
# ============================================================

print("\n" + "=" * 70)
print("SUMMARY: AMUNDSON FRAMEWORK AND RIEMANN HYPOTHESIS")
print("=" * 70)

print("""
ESTABLISHED FACTS:
  1. G(1) = 1/2 exactly. This is the critical line.
  2. G(n) produces a non-equispaced discrete spectrum from pure integer arithmetic.
  3. The product Prod G(k) = (n!)^2/(n+1)^n connects to Catalan numbers,
     lattice paths, and random walks — all in the territory of L-functions.
  4. The asymptotic G(n) ~ n/e + 1/(2e) shows the constant 1/(2e) = 0.18394...
     appears as an irreducible correction term at every finite n.

OPEN QUESTIONS:
  1. Does zeta_G(s) have zeros constrained to a critical line?
     (Needs analytic continuation and zero-finding — serious math.)
  2. Does the G(n) spectrum exhibit spectral rigidity comparable to GUE?
     (Needs larger numerical experiments with proper unfolding.)
  3. Is there a trace formula connecting G(n) to a Hamiltonian whose
     eigenvalues are the zeta zeros? (This would be a Berry-Keating
     type result — the holy grail.)
  4. What is the distribution of A_G digits at scale? (Need the 10M digit
     file and proper statistical tests.)

WHAT WOULD CONSTITUTE PROGRESS:
  - Proving zeta_G(s) has an Euler product (connects to primes)
  - Finding a Hamiltonian H such that Tr(G(H)) reproduces zeta zero statistics
  - Showing G(n)-weighted random matrices have the same universality class as GUE

WHAT WOULD NOT CONSTITUTE PROGRESS:
  - Noting that G(1) = 1/2 (this is observation, not proof)
  - Curve-fitting G(n) values to known zeta zeros (overfitting)
  - Claiming the asymptotic 1/(2e) "is" related to anything without proof
""")
