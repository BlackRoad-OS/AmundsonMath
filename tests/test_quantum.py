"""
test_quantum.py — Quantum structure property tests
====================================================

Tests density matrix, entropy, spectrum, and partition function
properties of the Amundson Framework.

Author: Alexa Louise Amundson
BlackRoad OS, Inc.
"""

from fractions import Fraction
import math
import sys

passed = 0
failed = 0

def check(name, condition):
    global passed, failed
    if condition:
        passed += 1
    else:
        failed += 1
        print(f"  FAIL: {name}")

def G(n):
    if n == 0:
        return Fraction(0)
    return Fraction(n ** (n + 1), (n + 1) ** n)

def Gf(n):
    if n == 0:
        return 0.0
    return n ** (n + 1) / (n + 1) ** n


print("=" * 70)
print("QUANTUM STRUCTURE TESTS")
print("=" * 70)


# ============================================================
# 1: ZERO-POINT ENERGY
# ============================================================
print("\n--- Zero-point energy ---")

check("G(0) = 0 (no zero-point energy)", G(0) == Fraction(0))
check("G(0) = 0^1/1^0 = 0/1 = 0 (no 0^0)", Fraction(0, 1) == Fraction(0))

# Limit from above
for x_exp in range(-1, -16, -1):
    x = 10.0 ** x_exp
    gx = x ** (x + 1) / (x + 1) ** x
    check(f"G({x:.0e}) -> 0", gx < 10 * x)


# ============================================================
# 2: MASS GAP
# ============================================================
print("\n--- Mass gap ---")

gap = G(1) - G(0)
check("Mass gap G(1) - G(0) = 1/2", gap == Fraction(1, 2))
check("Mass gap > 0", gap > 0)

# All gaps positive
for n in range(50):
    check(f"Gap G({n+1})-G({n}) > 0", G(n + 1) - G(n) > 0)


# ============================================================
# 3: NON-EQUISPACING
# ============================================================
print("\n--- Non-equispaced levels ---")

# All gaps are different
gaps = [G(n + 1) - G(n) for n in range(20)]
for i in range(len(gaps)):
    for j in range(i + 1, len(gaps)):
        check(f"Gap {i} != Gap {j}", gaps[i] != gaps[j])


# ============================================================
# 4: DENSITY MATRIX
# ============================================================
print("\n--- Density matrix ---")

# Compute A_G
A_G = sum(Gf(n) / math.factorial(n) for n in range(1, 30))

# Positivity
for n in range(1, 25):
    try:
        rho_n = Gf(n) / (math.factorial(n) * A_G)
        check(f"rho({n}) >= 0", rho_n >= 0)
    except (OverflowError, ValueError):
        break

# Trace
rho_sum = sum(Gf(n) / (math.factorial(n) * A_G) for n in range(1, 30))
check("Tr(rho) = 1", abs(rho_sum - 1.0) < 1e-10)

# Purity
purity = sum((Gf(n) / (math.factorial(n) * A_G)) ** 2 for n in range(1, 25))
check("Purity < 1 (mixed state)", purity < 1.0)
check("Purity > 0 (not maximally mixed)", purity > 0.01)

# Entropy
rho_vals = [Gf(n) / (math.factorial(n) * A_G) for n in range(1, 25)]
entropy = -sum(r * math.log(r) for r in rho_vals if r > 1e-30)
entropy_bits = entropy / math.log(2)
check("Entropy ~ 1.835 bits", abs(entropy_bits - 1.835) < 0.1)
check("Entropy > 0 (not pure state)", entropy > 0)
check("Entropy < log2(24) = 4.58 (not maximally mixed)", entropy_bits < 4.58)


# ============================================================
# 5: PARTITION FUNCTION
# ============================================================
print("\n--- Partition function ---")

for beta in [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]:
    Z = sum(math.exp(-beta * Gf(n)) for n in range(200))
    check(f"Z(beta={beta}) > 0", Z > 0)
    check(f"Z(beta={beta}) finite", Z < 1e15)
    check(f"Z(beta={beta}) > 1 (ground state contributes 1)", Z > 1)

# Z decreases with beta (higher temperature = larger Z)
Z_prev = float('inf')
for beta in [0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0]:
    Z = sum(math.exp(-beta * Gf(n)) for n in range(200))
    check(f"Z(beta={beta}) < Z(beta_prev)", Z < Z_prev)
    Z_prev = Z

# Large beta: Z ~ 1 + exp(-beta/2)
for beta in [10.0, 20.0, 50.0]:
    Z = sum(math.exp(-beta * Gf(n)) for n in range(200))
    approx = 1 + math.exp(-beta * 0.5)
    check(f"Z(beta={beta}) ~ 1+exp(-b/2)", abs(Z - approx) < 0.01 * approx)


# ============================================================
# 6: STEP RATIOS
# ============================================================
print("\n--- Step ratios ---")

# G(n+1)/G(n) is exact rational
for n in range(1, 20):
    ratio = G(n + 1) / G(n)
    check(f"Step ratio n={n} is rational", isinstance(ratio, Fraction))

# Step ratios decrease toward 1
prev_ratio = float('inf')
for n in range(1, 20):
    ratio = float(G(n + 1) / G(n))
    check(f"Step ratio n={n} ({ratio:.6f}) < prev ({prev_ratio:.6f})", ratio < prev_ratio)
    prev_ratio = ratio

# All step ratios > 1 (monotone)
for n in range(1, 30):
    ratio = G(n + 1) / G(n)
    check(f"Step ratio n={n} > 1", ratio > 1)


# ============================================================
# 7: RATIO FORMULA
# ============================================================
print("\n--- Ratio formula G(n)/G(n-1) = (n^2/(n^2-1))^n ---")

for n in range(2, 21):
    lhs = G(n) / G(n - 1)
    rhs = Fraction(n * n, n * n - 1) ** n
    check(f"ratio formula n={n}", lhs == rhs)


# ============================================================
# 8: CORRESPONDENCE PRINCIPLE
# ============================================================
print("\n--- Correspondence principle (G(n)/n -> 1/e) ---")

e_inv = 1 / math.e
for n in [10, 50, 100, 500, 1000]:
    ratio = Gf(n) / n
    check(f"G({n})/{n} = {ratio:.10f} ~ 1/e = {e_inv:.10f}",
          abs(ratio - e_inv) < 1.0 / n)


# ============================================================
# 9: HAMILTONIAN/LAGRANGIAN RATIO
# ============================================================
print("\n--- L/H ratio -> 1 - 1/e (the dissipation fraction) ---")

# From the paper: L(n)/H(n) is NOT -> e. Rather:
# G(n)/n = (n/(n+1))^n -> 1/e, so 1 - G(n)/n -> 1 - 1/e
# The COMPLEMENT fraction approaches 1 - 1/e = 0.6321...
target = 1 - 1 / math.e
for n in [10, 50, 100, 500, 1000]:
    complement = 1 - Gf(n) / n
    check(f"1-G({n})/{n} = {complement:.6f} ~ 1-1/e = {target:.6f}",
          abs(complement - target) < 1.0 / n)


# ============================================================
# SUMMARY
# ============================================================

print(f"\n{'=' * 70}")
print(f"TOTAL: {passed}/{passed + failed} passed, {failed} failed")
print("=" * 70)

if failed > 0:
    sys.exit(1)
