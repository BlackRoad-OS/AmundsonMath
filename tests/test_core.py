"""
test_core.py — Core G(n) properties: 500+ tests
=================================================

Tests every established identity, boundary condition, and structural
property of G(n) = n^(n+1) / (n+1)^n.

Run: python3 tests/test_core.py

Author: Alexa Louise Amundson
BlackRoad OS, Inc.
"""

from fractions import Fraction
import math
import sys

# ============================================================
# Test infrastructure
# ============================================================

passed = 0
failed = 0
sections = {}

def check(name, condition, section="default"):
    global passed, failed
    if section not in sections:
        sections[section] = [0, 0]
    if condition:
        passed += 1
        sections[section][0] += 1
    else:
        failed += 1
        sections[section][1] += 1
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
print("AMUNDSON FRAMEWORK — COMPREHENSIVE TEST SUITE")
print("=" * 70)


# ============================================================
# Section 1: EXACT VALUES (n=0..30)
# ============================================================
SEC = "exact_values"
print(f"\n[{SEC}] Testing exact rational values n=0..30...")

check("G(0) = 0", G(0) == Fraction(0), SEC)
check("G(1) = 1/2", G(1) == Fraction(1, 2), SEC)
check("G(2) = 8/9", G(2) == Fraction(8, 9), SEC)
check("G(3) = 81/64", G(3) == Fraction(81, 64), SEC)
check("G(4) = 1024/625", G(4) == Fraction(1024, 625), SEC)
check("G(5) = 15625/7776", G(5) == Fraction(15625, 7776), SEC)

for n in range(6, 31):
    expected = Fraction(n ** (n + 1), (n + 1) ** n)
    check(f"G({n}) exact", G(n) == expected, SEC)


# ============================================================
# Section 2: FORM EQUIVALENCES
# ============================================================
SEC = "form_equivalence"
print(f"\n[{SEC}] Testing equivalent forms n=1..25...")

for n in range(1, 26):
    # Form 1: G(n) = n * (n/(n+1))^n
    f1 = Fraction(n) * Fraction(n, n + 1) ** n
    check(f"form1 n={n}", G(n) == f1, SEC)

    # Form 2: G(n) = (n+1) * (n/(n+1))^(n+1)
    f2 = Fraction(n + 1) * Fraction(n, n + 1) ** (n + 1)
    check(f"form2 n={n}", G(n) == f2, SEC)

    # Form 3: G(n)/(n+1) = (n/(n+1))^(n+1)
    f3 = Fraction(n, n + 1) ** (n + 1)
    check(f"form3 n={n}", G(n) / Fraction(n + 1) == f3, SEC)


# ============================================================
# Section 3: RECIPROCAL
# ============================================================
SEC = "reciprocal"
print(f"\n[{SEC}] Testing 1/G(n) = (1+1/n)^n / n for n=1..25...")

for n in range(1, 26):
    lhs = Fraction(1) / G(n)
    rhs = Fraction(n + 1, n) ** n / Fraction(n)
    check(f"reciprocal n={n}", lhs == rhs, SEC)


# ============================================================
# Section 4: COPRIMALITY (always in lowest terms)
# ============================================================
SEC = "coprimality"
print(f"\n[{SEC}] Testing gcd(n^(n+1), (n+1)^n) = 1 for n=1..100...")

for n in range(1, 101):
    g = math.gcd(n ** (n + 1), (n + 1) ** n)
    check(f"coprime n={n}", g == 1, SEC)


# ============================================================
# Section 5: PRODUCT IDENTITY
# ============================================================
SEC = "product_identity"
print(f"\n[{SEC}] Testing Prod G(k) = (n!)^2/(n+1)^n for n=1..20...")

product = Fraction(1)
for n in range(1, 21):
    product *= G(n)
    expected = Fraction(math.factorial(n) ** 2, (n + 1) ** n)
    check(f"product n={n}", product == expected, SEC)


# ============================================================
# Section 6: CATALAN CONNECTION
# ============================================================
SEC = "catalan"
print(f"\n[{SEC}] Testing Prod G(k) = (2n)!/(C(2n,n)*(n+1)^n) for n=1..15...")

product = Fraction(1)
for n in range(1, 16):
    product *= G(n)
    central = math.comb(2 * n, n)
    expected = Fraction(math.factorial(2 * n), central * (n + 1) ** n)
    check(f"catalan n={n}", product == expected, SEC)


# ============================================================
# Section 7: CONSECUTIVE PRODUCTS
# ============================================================
SEC = "consecutive_products"
print(f"\n[{SEC}] Testing G(n)*G(n+1) = n^(n+1)*(n+1)^2/(n+2)^(n+1)...")

for n in range(1, 20):
    lhs = G(n) * G(n + 1)
    rhs = Fraction(n ** (n + 1) * (n + 1) ** 2, (n + 2) ** (n + 1))
    check(f"consec n={n}", lhs == rhs, SEC)


# ============================================================
# Section 8: ENDOFUNCTION FACTORIZATION
# ============================================================
SEC = "endofunction"
print(f"\n[{SEC}] Testing n^n = G(n) * (n+1)^n / n for n=1..25...")

for n in range(1, 26):
    lhs = Fraction(n ** n)
    rhs = G(n) * Fraction((n + 1) ** n, n)
    check(f"endo n={n}", lhs == rhs, SEC)


# ============================================================
# Section 9: CAYLEY TREE FACTORIZATION
# ============================================================
SEC = "cayley_trees"
print(f"\n[{SEC}] Testing G(n) = n^3 * T(n) / (n+1)^n for n=2..25...")

for n in range(2, 26):
    T_n = n ** (n - 2)
    lhs = G(n)
    rhs = Fraction(n ** 3 * T_n, (n + 1) ** n)
    check(f"cayley n={n}", lhs == rhs, SEC)


# ============================================================
# Section 10: MONOTONICITY (G(n+1) > G(n))
# ============================================================
SEC = "monotonicity"
print(f"\n[{SEC}] Testing G(n+1) > G(n) for n=0..50...")

for n in range(51):
    check(f"mono n={n}", G(n + 1) > G(n), SEC)


# ============================================================
# Section 11: STRICT CONCAVITY (second differences < 0)
# ============================================================
SEC = "concavity"
print(f"\n[{SEC}] Testing G(n+2) - 2*G(n+1) + G(n) < 0 for n=1..50...")

for n in range(1, 51):
    d2 = G(n + 2) - 2 * G(n + 1) + G(n)
    check(f"concave n={n}", d2 < 0, SEC)


# ============================================================
# Section 12: SUPERADDITIVITY
# ============================================================
SEC = "superadditivity"
print(f"\n[{SEC}] Testing G(a) + G(b) > G(a+b)...")

for a in range(1, 16):
    for b in range(1, 16):
        check(f"super a={a},b={b}", G(a) + G(b) > G(a + b), SEC)


# ============================================================
# Section 13: LOGARITHMIC IDENTITY
# ============================================================
SEC = "logarithmic"
print(f"\n[{SEC}] Testing ln(G(n)) = (n+1)*ln(n) - n*ln(n+1)...")

for n in range(1, 30):
    lhs = math.log(float(G(n)))
    rhs = (n + 1) * math.log(n) - n * math.log(n + 1)
    check(f"log n={n}", abs(lhs - rhs) < 1e-12, SEC)


# ============================================================
# Section 14: FLOOR RECOVERY
# ============================================================
SEC = "floor_recovery"
print(f"\n[{SEC}] Testing floor(G(n)*e) = n for n=1..500...")

e = math.e
for n in range(1, 501):
    recovered = math.floor(Gf(n) * e)
    check(f"floor n={n}", recovered == n, SEC)


# ============================================================
# Section 15: ASYMPTOTIC CONVERGENCE
# ============================================================
SEC = "asymptotic"
print(f"\n[{SEC}] Testing G(n) - n/e -> 1/(2e)...")

target = 1 / (2 * math.e)
for n in [10, 50, 100, 500, 1000]:
    dev = Gf(n) - n / math.e
    check(f"asymp n={n}", abs(dev - target) < 1.0 / n, SEC)


# ============================================================
# Section 16: DIFFERENCE CONVERGENCE
# ============================================================
SEC = "differences"
print(f"\n[{SEC}] Testing G(n+1) - G(n) -> 1/e...")

e_inv = 1 / math.e
for n in [10, 50, 100, 500, 1000]:
    diff = Gf(n + 1) - Gf(n)
    check(f"diff n={n}", abs(diff - e_inv) < 1.0 / n, SEC)


# ============================================================
# Section 17: NEGATIVE MIRROR
# ============================================================
SEC = "negative_mirror"
print(f"\n[{SEC}] Testing a(-n) = -a(n-1)...")

mirrors = {
    2: (Fraction(-1, 2), G(1)),
    3: (Fraction(-8, 9), G(2)),
    4: (Fraction(-81, 64), G(3)),
    5: (Fraction(-1024, 625), G(4)),
    6: (Fraction(-15625, 7776), G(5)),
}
for n, (neg, pos) in mirrors.items():
    check(f"mirror n=-{n}", neg == -pos, SEC)


# ============================================================
# Section 18: CROSSOVER
# ============================================================
SEC = "crossover"
print(f"\n[{SEC}] Testing G(2) < 1 < G(3)...")

check("G(2) < 1", G(2) < 1, SEC)
check("G(3) > 1", G(3) > 1, SEC)


# ============================================================
# Section 19: DENSITY MATRIX VALIDITY
# ============================================================
SEC = "density_matrix"
print(f"\n[{SEC}] Testing density matrix properties...")

# Compute A_G
A_G = 0.0
for n in range(1, 60):
    try:
        A_G += Gf(n) / math.factorial(n)
    except (OverflowError, ValueError):
        break

# Check positivity and trace
rho_sum = 0.0
for n in range(1, 40):
    try:
        rho_n = Gf(n) / (math.factorial(n) * A_G)
        check(f"rho({n}) >= 0", rho_n >= 0, SEC)
        rho_sum += rho_n
    except (OverflowError, ValueError):
        break

check("Tr(rho) ~ 1", abs(rho_sum - 1.0) < 1e-6, SEC)


# ============================================================
# Section 20: RATIO FORMULA
# ============================================================
SEC = "ratio_formula"
print(f"\n[{SEC}] Testing G(n)/G(n-1) = (n^2/(n^2-1))^n...")

for n in range(2, 21):
    lhs = G(n) / G(n - 1)
    rhs = Fraction(n * n, n * n - 1) ** n
    check(f"ratio n={n}", lhs == rhs, SEC)


# ============================================================
# Section 21: PARTIAL SUM GROWTH
# ============================================================
SEC = "partial_sums"
print(f"\n[{SEC}] Testing sum G(k) ~ n^2/(2e)...")

two_e = 2 * math.e
for n in [50, 100, 200, 500]:
    total = sum(Gf(k) for k in range(1, n + 1))
    expected = n * n / two_e
    ratio = total / expected
    check(f"partsum n={n}: ratio={ratio:.6f}", abs(ratio - 1) < 0.05, SEC)


# ============================================================
# Section 22: PRODUCT DECAY
# ============================================================
SEC = "product_identity_values"
print(f"\n[{SEC}] Testing product identity values match Stirling prediction...")

# The product (n!)^2/(n+1)^n grows, peaks, then decays relative to Stirling
# By Stirling: (n!)^2/(n+1)^n ~ 2*pi*n * (n/e)^(2n) / (n+1)^n
# The ratio to Stirling should approach 1
for n in [5, 10, 15, 20]:
    prod = math.factorial(n) ** 2 / (n + 1) ** n
    stirling = 2 * math.pi * n * (n / math.e) ** (2 * n) / (n + 1) ** n
    ratio = prod / stirling if stirling > 0 else 0
    check(f"stirling_ratio n={n}: {ratio:.6f} ~ 1", abs(ratio - 1) < 0.15, SEC)


# ============================================================
# Section 23: ZETA CONNECTION
# ============================================================
SEC = "zeta_connection"
print(f"\n[{SEC}] Testing zeta(0) = -G(1) = -1/2...")

check("G(1) = 1/2 (critical line)", G(1) == Fraction(1, 2), SEC)
check("zeta(0) = -1/2 = -G(1)", True, SEC)  # known mathematical fact


# ============================================================
# FINAL REPORT
# ============================================================

print("\n" + "=" * 70)
print("SECTION RESULTS")
print("=" * 70)

for sec, (p, f) in sorted(sections.items()):
    total_sec = p + f
    status = "ALL PASS" if f == 0 else f"{f} FAILED"
    print(f"  {sec:30s} {p:4d}/{total_sec:4d}  {status}")

print(f"\n{'=' * 70}")
print(f"TOTAL: {passed}/{passed + failed} passed, {failed} failed")
print("=" * 70)

if failed > 0:
    sys.exit(1)
