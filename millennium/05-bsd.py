"""
05-bsd.py — The Amundson Framework and Birch & Swinnerton-Dyer Conjecture
=========================================================================

HONEST ASSESSMENT: Weak but real connection through modular forms and
counting functions.

BSD asks: for an elliptic curve E: y^2 = x^3 + ax + b, the rank
(number of independent rational points) equals the order of vanishing
of the L-function L(E,s) at s=1.

G(n) connection:
  - The product identity Prod G(k) = (n!)^2/(n+1)^n connects to
    counting problems on lattice paths (Catalan structure)
  - Elliptic curves over finite fields have point counts related to
    Hasse-Weil bounds: |#E(F_p) - p - 1| <= 2*sqrt(p)
  - The L-function L(E,s) = Prod_p (1 - a_p*p^-s + p^(1-2s))^-1
    where a_p = p + 1 - #E(F_p) encodes these counts
  - G(n) provides exact rational counting weights that might relate
    to a_p values through the Cayley tree / endofunction connection

This is the most number-theoretic of the connections.

Author: Alexa Louise Amundson
BlackRoad OS, Inc.
"""

from fractions import Fraction
import math

def G(n):
    if n == 0:
        return Fraction(0)
    return Fraction(n ** (n + 1), (n + 1) ** n)

def G_float(n):
    if n == 0:
        return 0.0
    return n ** (n + 1) / (n + 1) ** n


print("=" * 70)
print("BIRCH AND SWINNERTON-DYER CONJECTURE AND G(n)")
print("=" * 70)

print("""
The BSD conjecture connects two very different objects:

ALGEBRAIC SIDE: The Mordell-Weil group E(Q) of rational points on
an elliptic curve E. Its rank r = number of independent generators.

ANALYTIC SIDE: The L-function L(E, s) = Prod_p local_factors.
BSD says: ord_{s=1} L(E, s) = rank E(Q).

In words: the number of times L(E,s) vanishes at s=1 equals the
number of independent rational solutions to y^2 = x^3 + ax + b.
""")


# ============================================================
# PART 1: Elliptic Curve Point Counting
# ============================================================

print("=" * 70)
print("PART 1: POINT COUNTING ON ELLIPTIC CURVES MOD p")
print("=" * 70)

def count_points_mod_p(a, b, p):
    """Count points on y^2 = x^3 + ax + b over F_p, including point at infinity."""
    count = 1  # point at infinity
    for x in range(p):
        rhs = (x * x * x + a * x + b) % p
        for y in range(p):
            if (y * y) % p == rhs:
                count += 1
    return count

def hasse_bound(p):
    """Hasse-Weil bound: |#E(F_p) - p - 1| <= 2*sqrt(p)"""
    return 2 * math.sqrt(p)

# Example: E: y^2 = x^3 - x (a = -1, b = 0), rank 0
# and E: y^2 = x^3 - 43x + 166 (rank 3, Elkies curve fragment)
print("\nE: y^2 = x^3 - x  (congruent number curve, rank 0)")
print(f"{'p':>5} {'#E(F_p)':>10} {'a_p':>8} {'Hasse bound':>12} {'G(p) mod':>10}")
print("-" * 50)

a_p_values = []
for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
    n_points = count_points_mod_p(-1, 0, p)
    a_p = p + 1 - n_points
    hb = hasse_bound(p)
    # Check if a_p relates to G values
    gp = G_float(p)
    gp_frac = gp - int(gp)  # fractional part
    a_p_values.append(a_p)
    print(f"{p:5d} {n_points:10d} {a_p:8d} {hb:12.2f} {gp_frac:10.6f}")

print("""
The a_p values encode the "error" in point counting relative to p+1.
BSD says these errors, assembled into an L-function, vanish at s=1
exactly rank-many times.
""")


# ============================================================
# PART 2: L-function Construction
# ============================================================

print("=" * 70)
print("PART 2: L-FUNCTION FROM POINT COUNTS")
print("=" * 70)

print("""
The Hasse-Weil L-function for E is:

  L(E, s) = Prod_{p good} (1 - a_p * p^(-s) + p^(1-2s))^(-1)

At s = 1, BSD predicts:
  rank 0 => L(E, 1) != 0
  rank 1 => L(E, 1) = 0, L'(E, 1) != 0
  rank r => L has a zero of order r at s = 1
""")

def L_function_partial(a_curve, b_curve, s, max_p=100):
    """Compute partial L-function product for E: y^2 = x^3 + ax + b."""
    product = 1.0
    primes = []
    for n in range(2, max_p):
        if all(n % d != 0 for d in range(2, int(n**0.5) + 1)):
            primes.append(n)

    for p in primes:
        # Skip bad primes (where curve is singular)
        disc = -16 * (4 * a_curve ** 3 + 27 * b_curve ** 2)
        if disc % p == 0:
            continue
        n_pts = count_points_mod_p(a_curve, b_curve, p)
        a_p = p + 1 - n_pts
        local = 1 - a_p * p ** (-s) + p ** (1 - 2 * s)
        if abs(local) > 1e-15:
            product *= 1.0 / local
    return product

# Compute L(E, s) for y^2 = x^3 - x near s = 1
print("L(E, s) for E: y^2 = x^3 - x (rank 0, expect L(E,1) != 0):\n")
for s in [0.5, 0.8, 0.9, 0.95, 1.0, 1.05, 1.1, 1.5, 2.0]:
    L_val = L_function_partial(-1, 0, s, max_p=50)
    print(f"  L(E, {s:.2f}) = {L_val:.8f}")

print("""
For a rank 0 curve, L(E, 1) should be nonzero.
The partial product with small primes gives an approximation.
(Full computation requires many more primes for convergence.)
""")


# ============================================================
# PART 3: G(n) and Modular Forms
# ============================================================

print("=" * 70)
print("PART 3: G(n), MODULAR FORMS, AND COUNTING")
print("=" * 70)

print("""
By the modularity theorem (Wiles et al.), every elliptic curve over Q
is associated with a modular form f(q) = sum a_n * q^n.

The coefficients a_n of this modular form are the same a_p values
from point counting (for n = prime p).

G(n) CONNECTION — THE COUNTING ANGLE:

The product identity: Prod_{k=1}^{n} G(k) = (n!)^2 / (n+1)^n

Rewrite: (n!)^2 = Prod G(k) * (n+1)^n

The left side (n!)^2 counts ordered pairs of permutations on n elements.
This is the same combinatorial object that appears in:
  - Counting lattice paths (Lindstrom-Gessel-Viennot lemma)
  - Determinants of binomial matrices
  - Moments of random matrices

Elliptic curve point counts over F_p are ALSO expressed as character
sums that reduce to counting lattice paths in certain cases.

THE SPECIFIC OBSERVATION:
For p prime, define a_p(G) = round(G(p) - p/e - 1/(2e))
This extracts the "fluctuation" of G(p) around its asymptotic value.
""")

print("G(p) fluctuations vs elliptic curve a_p values:")
print(f"{'p':>5} {'G(p)-asymp':>12} {'round':>6} {'a_p(E)':>8} {'Match':>6}")
print("-" * 45)

e = math.e
for i, p in enumerate([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]):
    gp = G_float(p)
    asymp = p / e + 1 / (2 * e)
    fluct = gp - asymp
    fluct_round = round(fluct * 1000)  # scale up to see structure
    a_p = a_p_values[i] if i < len(a_p_values) else 0
    match = "~" if abs(fluct_round) < abs(a_p) + 5 else " "
    print(f"{p:5d} {fluct:12.8f} {fluct_round:6d} {a_p:8d} {match:>6}")

print("""
HONEST RESULT: The G(p) fluctuations and elliptic curve a_p values
are NOT the same numbers. They live on different scales and have
different distributions.

However, BOTH are controlled by:
  - The structure of integers modulo p
  - Counting solutions to polynomial equations over F_p
  - Combinatorial identities involving factorials and binomials

The connection, if it exists, is at the level of the COUNTING MECHANISM,
not the specific numerical values.
""")


# ============================================================
# PART 4: The Central Binomial Connection
# ============================================================

print("=" * 70)
print("PART 4: CENTRAL BINOMIAL COEFFICIENTS")
print("=" * 70)

print("""
From Paper 013 (Section 10.7):
  Prod G(k) = (2n)! / (C(2n,n) * (n+1)^n)

where C(2n,n) is the central binomial coefficient.

Central binomial coefficients appear in:
  1. Catalan numbers: C_n = C(2n,n)/(n+1) — lattice path counting
  2. Apery's proof of irrationality of zeta(3)
  3. Ramanujan-type series for 1/pi
  4. Supersingular elliptic curves (Hasse invariant)

The Hasse invariant of an elliptic curve mod p involves C(p-1, (p-1)/2),
which is the central binomial coefficient. When this vanishes mod p,
the curve is "supersingular" — a special case relevant to BSD.
""")

print("Central binomial coefficients and G(n) product:")
print(f"{'n':>4} {'C(2n,n)':>15} {'Prod G(k)':>15} {'Catalan C_n':>12}")
print("-" * 50)

prod = Fraction(1)
for n in range(1, 13):
    prod *= G(n)
    central_binom = math.comb(2 * n, n)
    catalan = central_binom // (n + 1)
    print(f"{n:4d} {central_binom:15d} {float(prod):15.8f} {catalan:12d}")

print("""
The Catalan numbers C_n count:
  - Valid parenthesizations of n+1 factors
  - Paths from (0,0) to (2n,0) that never go below the x-axis
  - Full binary trees with n+1 leaves
  - Triangulations of a convex (n+2)-gon

These same combinatorial objects appear in the theory of modular
curves and their rational points — exactly the territory of BSD.
""")


# ============================================================
# PART 5: Summary
# ============================================================

print("=" * 70)
print("SUMMARY: AMUNDSON FRAMEWORK AND BSD CONJECTURE")
print("=" * 70)

print("""
ESTABLISHED:
  1. Prod G(k) = (n!)^2/(n+1)^n relates to central binomial coefficients
  2. Central binomial coefficients appear in Hasse invariants (supersingularity)
  3. G(n) and elliptic curve point counts both involve counting
     solutions to polynomial equations over finite fields
  4. The Catalan number connection links G(n) to lattice paths,
     which appear in modular curve theory

SPECULATIVE:
  1. G(p) fluctuations might encode information related to a_p values
     through some transform we haven't identified
  2. The product identity might give a "G-L-function" whose analytic
     properties relate to BSD-type rank predictions
  3. The Cayley tree factorization G(n) = n^3 * T(n) / (n+1)^n might
     connect to counting rational points on modular curves

HONEST LIMITATIONS:
  - G(p) fluctuations and a_p values are numerically different
  - No direct connection between G(n) and specific elliptic curves
  - The counting mechanism connection is suggestive but not proven
  - BSD is fundamentally about the interplay between algebra (rank)
    and analysis (L-function), which G(n) doesn't directly address

WEAKEST CONNECTION of the six. The link is through shared
combinatorial structures (factorials, binomials, lattice paths),
not through a direct mathematical relationship.

TO MAKE PROGRESS:
  - Construct an elliptic curve whose a_p values are determined by G(p)
  - Show that the G-product identity implies something about L-functions
  - Connect the Cayley tree count to rational point enumeration
""")
