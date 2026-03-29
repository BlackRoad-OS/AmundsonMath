"""
03-yang-mills.py — The Amundson Framework and Yang-Mills Mass Gap
================================================================

HONEST ASSESSMENT: Moderate connection.

Yang-Mills asks: prove that for any compact simple gauge group G, the
quantum Yang-Mills theory exists in R^4 and has a positive mass gap.

The mass gap means the lightest particle has mass m > 0, even though
the classical equations describe massless fields.

G(n) connection:
  - G(0) = 0 (vacuum has zero energy)
  - G(1) = 1/2 (first excited state has nonzero energy)
  - The GAP between G(0) and G(1) is exactly 1/2
  - This is a mass gap: the discrete spectrum doesn't start at zero

Whether this has anything to do with Yang-Mills gauge theory specifically
is an open question. The gap 1/2 comes from integer arithmetic, not from
gauge invariance. But the STRUCTURE — a discrete spectrum with zero
ground state and positive first excitation — is exactly what Yang-Mills
mass gap requires.

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
print("YANG-MILLS MASS GAP AND THE AMUNDSON SPECTRUM")
print("=" * 70)

print("""
The Yang-Mills mass gap problem:
  Given a compact simple gauge group G (like SU(2) or SU(3)),
  prove that the quantum Yang-Mills theory on R^4:
    1. EXISTS (mathematically well-defined)
    2. Has a MASS GAP: the lowest energy state above vacuum has mass m > 0

In lattice QCD, the mass gap is computed numerically and found to be
nonzero. But no rigorous proof exists for the continuum theory.
""")


# ============================================================
# PART 1: The Mass Gap in the Amundson Spectrum
# ============================================================

print("=" * 70)
print("PART 1: THE MASS GAP G(1) - G(0) = 1/2")
print("=" * 70)

print(f"\nG(0) = {G(0)} = {float(G(0)):.1f}  (vacuum)")
print(f"G(1) = {G(1)} = {float(G(1)):.4f}  (first excitation)")
print(f"Mass gap = G(1) - G(0) = {G(1) - G(0)} = {float(G(1) - G(0)):.4f}")

print(f"\nAll gaps in the Amundson spectrum:")
for n in range(12):
    gap = G(n + 1) - G(n)
    print(f"  G({n+1}) - G({n}) = {str(gap):20s} = {float(gap):.10f}")

print("""
Every gap is positive. The spectrum is strictly increasing.
The first gap (the "mass gap") is exactly 1/2.

COMPARISON WITH LATTICE QCD:
  - Lattice QCD computes the glueball mass gap numerically
  - For SU(3): m_gap ~ 1.5 GeV (in physical units)
  - The ratio m_gap / Lambda_QCD ~ 4-5

In the Amundson spectrum, the gap structure is:
  G(1)/1 = 1/2
  G(2)/2 = 4/9
  G(3)/3 = 27/64
  G(n)/n -> 1/e = 0.36788...

The sequence G(n)/n DECREASES to 1/e. In physical terms, the
"gap per unit energy" shrinks but never reaches zero.
""")


# ============================================================
# PART 2: Partition Function
# ============================================================

print("=" * 70)
print("PART 2: PARTITION FUNCTION Z(beta) WITH G(n) SPECTRUM")
print("=" * 70)

print("""
In quantum field theory, the partition function is:
  Z(beta) = sum_n exp(-beta * E_n)

With G(n) energy levels:
  Z_G(beta) = sum_{n=0}^{inf} exp(-beta * G(n))
            = 1 + sum_{n=1}^{inf} exp(-beta * G(n))

The mass gap controls the LOW-TEMPERATURE behavior:
  Z_G(beta) ~ 1 + exp(-beta * 1/2) + ...  as beta -> infinity

The 1/2 gap means the partition function decays as exp(-beta/2)
at large beta, which is exactly the signature of a mass gap.
""")

print(f"{'beta':>6} {'Z_G(beta)':>15} {'Z_G - 1':>15} {'exp(-beta/2)':>15} {'Ratio':>10}")
print("-" * 65)

for beta in [0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0]:
    Z = sum(math.exp(-beta * G_float(n)) for n in range(200))
    gap_term = math.exp(-beta * 0.5)
    ratio = (Z - 1) / gap_term if gap_term > 1e-15 else float('inf')
    print(f"{beta:6.1f} {Z:15.8f} {Z - 1:15.8f} {gap_term:15.8f} {ratio:10.4f}")

print("""
At large beta, Z_G - 1 ~ exp(-beta/2), confirming the mass gap controls
the exponential decay. The ratio approaches a constant, meaning the
higher levels contribute a fixed multiplicative correction.

This is exactly the behavior expected from a theory with a mass gap.
""")


# ============================================================
# PART 3: Connection to Gauge Theory Structure
# ============================================================

print("=" * 70)
print("PART 3: GAUGE THEORY STRUCTURE")
print("=" * 70)

print("""
HONEST ASSESSMENT OF THE CONNECTION:

Yang-Mills mass gap is specifically about:
  - SU(N) gauge fields on R^4
  - The self-interaction of gauge bosons (gluons for SU(3))
  - Confinement: why quarks are never seen free
  - Asymptotic freedom: coupling decreases at high energy

What G(n) provides:
  - A discrete spectrum with exact mass gap 1/2
  - Product identity connecting levels to combinatorial counting
  - No continuum assumption required
  - Convergent partition function (no UV divergence)

What G(n) does NOT provide:
  - Any connection to gauge invariance or SU(N) structure
  - Confinement mechanism
  - Running coupling constant
  - Dimensional analysis (G(n) is dimensionless)

THE GAP: G(n) has a mass gap, but so does any discrete spectrum
with E_0 = 0 and E_1 > 0. The question is whether G(n) is the
RIGHT discrete spectrum — the one that emerges from quantizing
the Yang-Mills Lagrangian.

TO MAKE PROGRESS: One would need to show that the Hamiltonian
of SU(N) Yang-Mills on a lattice, in some limit, has eigenvalues
that follow the G(n) spacing. This is a very specific claim that
requires actual lattice QCD computation.
""")

# The Cayley tree connection
print("=" * 70)
print("PART 3b: CAYLEY TREE OBSERVATION")
print("=" * 70)

print("""
G(n) = n^3 * T(n) / (n+1)^n   where T(n) = n^(n-2) (Cayley tree count)

Cayley trees count labeled trees on n vertices. In lattice gauge theory,
the STRONG COUPLING EXPANSION represents gauge configurations as trees
on the lattice. The partition function at strong coupling is:

  Z_strong ~ sum over trees T

If G(n) counts these trees (weighted by n^3/(n+1)^n), then the product
identity Prod G(k) = (n!)^2/(n+1)^n is the strong-coupling partition
function of the gauge theory.

This is SPECULATIVE but testable: compute the strong-coupling expansion
of SU(2) lattice gauge theory and compare the combinatorial weights
with G(n) values.
""")

for n in range(1, 11):
    T_n = n ** (n - 2) if n >= 2 else 1
    gn = G_float(n)
    cayley_weight = n ** 3 * T_n / (n + 1) ** n
    print(f"  n={n:2d}: G(n) = {gn:.8f}  "
          f"n^3 * T(n) / (n+1)^n = {cayley_weight:.8f}  "
          f"Match: {abs(gn - cayley_weight) < 1e-10}")


# ============================================================
# PART 4: Summary
# ============================================================

print("\n" + "=" * 70)
print("SUMMARY: AMUNDSON FRAMEWORK AND YANG-MILLS")
print("=" * 70)

print("""
ESTABLISHED:
  1. G(n) spectrum has a mass gap of exactly 1/2
  2. Partition function Z_G(beta) decays as exp(-beta/2) at large beta
  3. G(n) factors through Cayley tree count T(n) = n^(n-2)
  4. Product identity gives exact combinatorial partition function

SPECULATIVE:
  1. The Cayley tree factorization might connect to strong-coupling
     lattice gauge theory
  2. G(n) might be the natural spectrum for a quantized gauge field
     on a discrete lattice

HONEST LIMITATIONS:
  - Having a mass gap is necessary but not sufficient
  - No gauge invariance or SU(N) structure in G(n) itself
  - The connection to actual Yang-Mills requires lattice QCD computation
  - This is the weakest of the three strong connections (after Riemann
    and Navier-Stokes)
""")
