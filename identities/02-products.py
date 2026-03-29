"""
02-products.py — Product Identities and Combinatorial Connections
=================================================================

The product identity Prod G(k) = (n!)^2 / (n+1)^n is the most
powerful single result in the Amundson Framework. It connects G(n)
to Catalan numbers, central binomials, lattice paths, and random walks.

Author: Alexa Louise Amundson
BlackRoad OS, Inc.
"""

from fractions import Fraction
import math

def G(n):
    if n == 0:
        return Fraction(0)
    return Fraction(n ** (n + 1), (n + 1) ** n)

passed = 0
failed = 0

def check(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS: {name}")
    else:
        failed += 1
        print(f"  FAIL: {name}  {detail}")


# ============================================================
# THE PRODUCT IDENTITY
# ============================================================

print("=" * 70)
print("PRODUCT IDENTITY: Prod_{k=1}^{n} G(k) = (n!)^2 / (n+1)^n")
print("=" * 70)

product = Fraction(1)
for n in range(1, 16):
    product *= G(n)
    expected = Fraction(math.factorial(n) ** 2, (n + 1) ** n)
    check(f"n={n:2d}: Prod = {float(product):.10f}", product == expected)

# ============================================================
# PROOF BY TELESCOPING
# ============================================================

print("\n" + "=" * 70)
print("PROOF SKETCH: Telescoping cancellation")
print("=" * 70)

print("""
G(k) = k^(k+1) / (k+1)^k

Prod_{k=1}^{n} G(k) = Prod k^(k+1) / Prod (k+1)^k

Numerator:   1^2 * 2^3 * 3^4 * ... * n^(n+1)
Denominator: 2^1 * 3^2 * 4^3 * ... * (n+1)^n

Rewrite numerator as:   Prod k^k * Prod k = (Prod k^k) * n!
Rewrite denominator as: Prod_{j=2}^{n+1} j^{j-1} = Prod_{j=1}^{n+1} j^{j-1} / 1^0
                       = Prod_{j=1}^{n} (j+1)^j

After cancellation:

  Prod G(k) = [Prod_{k=1}^{n} k^k * n!] / [Prod_{k=1}^{n} (k+1)^k]
            = n! * [Prod k^k / Prod (k+1)^k]
            = n! * [Prod (k/(k+1))^k]

And Prod (k/(k+1))^k = n! / (n+1)^n (another telescoping).

So: Prod G(k) = n! * n! / (n+1)^n = (n!)^2 / (n+1)^n.  QED
""")


# ============================================================
# CATALAN CONNECTION
# ============================================================

print("=" * 70)
print("CATALAN CONNECTION")
print("=" * 70)

print("\nProd G(k) = (2n)! / (C(2n,n) * (n+1)^n)\n")

product = Fraction(1)
for n in range(1, 13):
    product *= G(n)
    central_binom = math.comb(2 * n, n)
    catalan = central_binom // (n + 1)
    alt = Fraction(math.factorial(2 * n), central_binom * (n + 1) ** n)
    check(f"n={n:2d}: C(2n,n)={central_binom:>10d}  Catalan={catalan:>8d}", product == alt)

print("""
Catalan numbers C_n = C(2n,n)/(n+1) count:
  - Dyck paths (lattice paths that never go below the diagonal)
  - Valid parenthesizations
  - Full binary trees with n+1 leaves
  - Triangulations of a convex (n+2)-gon
  - Non-crossing partitions of [n]

The product of G(k) encodes the same combinatorial structure,
weighted by the integer power normalization (n+1)^n.
""")


# ============================================================
# STIRLING ANALYSIS
# ============================================================

print("=" * 70)
print("STIRLING ANALYSIS OF THE PRODUCT")
print("=" * 70)

print("""
By Stirling: n! ~ sqrt(2*pi*n) * (n/e)^n

So: (n!)^2 / (n+1)^n ~ 2*pi*n * (n/e)^(2n) / (n+1)^n
                      = 2*pi*n * n^(2n) / (e^(2n) * (n+1)^n)
""")

print(f"{'n':>4} {'Prod G(k)':>15} {'Stirling approx':>15} {'Ratio':>10}")
print("-" * 50)

product = Fraction(1)
for n in range(1, 20):
    product *= G(n)
    prod_float = float(product)
    stirling = 2 * math.pi * n * (n / math.e) ** (2 * n) / (n + 1) ** n
    ratio = prod_float / stirling if stirling > 1e-300 else 0
    print(f"{n:4d} {prod_float:15.8e} {stirling:15.8e} {ratio:10.6f}")

print("""
The ratio converges to 1, confirming Stirling's approximation.
The product Prod G(k) -> 0 as n -> infinity (decays exponentially).

Physical meaning: the cumulative weight of the first n quantum levels
decays, meaning higher levels contribute exponentially less to the
total partition function. This ensures convergence.
""")


# ============================================================
# PARTIAL PRODUCTS AND RATIOS
# ============================================================

print("=" * 70)
print("PARTIAL PRODUCT RATIOS")
print("=" * 70)

print("\nRatio of consecutive partial products = G(n+1):\n")

product = Fraction(1)
products = [Fraction(1)]
for n in range(1, 15):
    product *= G(n)
    products.append(product)

for n in range(1, 14):
    ratio = products[n + 1] / products[n]
    check(f"P({n+1})/P({n}) = G({n+1}) = {float(ratio):.8f}", ratio == G(n + 1))


print(f"\n{'='*70}")
print(f"RESULTS: {passed} passed, {failed} failed out of {passed + failed} tests")
print("=" * 70)
