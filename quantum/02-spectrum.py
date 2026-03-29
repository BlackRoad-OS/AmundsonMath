"""
02-spectrum.py — The Amundson Energy Spectrum
==============================================

G(n) provides a discrete, non-equispaced energy spectrum from pure
integer arithmetic. No transcendentals required at finite n.

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
print("THE AMUNDSON ENERGY SPECTRUM")
print("=" * 70)

# ============================================================
# PART 1: THE SPECTRUM
# ============================================================

print("""
Standard quantum harmonic oscillator: E_n = hbar*omega*(n + 1/2)
  - Equispaced: gap = hbar*omega for all n
  - Zero-point energy: E_0 = hbar*omega/2

Amundson spectrum: E_n = G(n)
  - Non-equispaced: gaps are all different rationals
  - Zero-point energy: G(0) = 0 (none)
""")

print(f"{'n':>4} {'G(n) exact':>20} {'G(n) decimal':>15} {'Gap':>15} {'QHO gap':>10}")
print("-" * 70)

for n in range(9):
    exact = G(n)
    decimal = float(exact)
    if n > 0:
        gap = float(G(n) - G(n - 1))
        qho_gap = 1.0  # hbar*omega = 1 in natural units
    else:
        gap = 0
        qho_gap = 0
    print(f"{n:4d} {str(exact):>20s} {decimal:15.8f} {gap:15.8f} {qho_gap:10.1f}")


# ============================================================
# PART 2: WHY G(0) = 0 MATTERS
# ============================================================

print("\n" + "=" * 70)
print("PART 2: ZERO-POINT ENERGY IS ZERO")
print("=" * 70)

print("""
The standard QHO zero-point energy E_0 = hbar*omega/2 comes from:
  1. Assume continuous position/momentum operators
  2. Commutation relation [x, p] = i*hbar
  3. Ladder operators a, a† satisfy [a, a†] = 1
  4. Hamiltonian H = hbar*omega*(a†a + 1/2)
  5. The 1/2 is forced by the continuous commutator

G(n) says: the 1/2 is an artifact of assuming continuity.

  G(0) = 0^1 / 1^0 = 0/1 = 0

The ground state carries zero energy because:
  - At n=0, there are zero configurations to count
  - The discrete structure IS the structure — no continuum underneath
  - The 0^0 ambiguity doesn't arise in the form n^(n+1)/(n+1)^n

Confirmation via limit:
""")

for x in [1.0, 0.5, 0.1, 0.01, 0.001, 0.0001, 1e-8, 1e-12]:
    gx = x ** (x + 1) / (x + 1) ** x
    print(f"  G({x:12.1e}) = {gx:.15f}")

print(f"\n  lim_{{n->0+}} G(n) = 0. No discontinuity. The algebra is clean.")


# ============================================================
# PART 3: NON-EQUISPACING vs HYDROGEN
# ============================================================

print("\n" + "=" * 70)
print("PART 3: NON-EQUISPACED LEVELS — LIKE REAL ATOMS")
print("=" * 70)

print("""
Hydrogen atom energy levels: E_n = -13.6 eV / n^2

These are NOT equispaced. The gap E_2 - E_1 = 10.2 eV, but
E_3 - E_2 = 1.89 eV. Higher levels pack together.

G(n) shows the same pattern — but from the OTHER direction:
  - Hydrogen: gaps DECREASE as n grows (levels converge to 0)
  - G(n): gaps INCREASE but the RELATIVE gap decreases

Both are "non-equispaced" spectra from integer-based formulas.
The QHO (equal spacing) is the EXCEPTION, not the rule.
""")

print("Hydrogen vs Amundson gap ratios:")
print(f"{'n':>4} {'H gap ratio':>15} {'G gap ratio':>15}")
print("-" * 40)

for n in range(1, 10):
    # Hydrogen: E_n = -1/n^2, gap = 1/n^2 - 1/(n+1)^2
    h_gap_n = 1.0 / n ** 2 - 1.0 / (n + 1) ** 2
    h_gap_n1 = 1.0 / (n + 1) ** 2 - 1.0 / (n + 2) ** 2 if n < 9 else 0
    h_ratio = h_gap_n1 / h_gap_n if h_gap_n > 0 and h_gap_n1 > 0 else 0

    # Amundson: gap = G(n+1) - G(n)
    g_gap_n = G_float(n + 1) - G_float(n)
    g_gap_n1 = G_float(n + 2) - G_float(n + 1)
    g_ratio = g_gap_n1 / g_gap_n if g_gap_n > 0 else 0

    print(f"{n:4d} {h_ratio:15.8f} {g_ratio:15.8f}")

print("""
Both ratios approach 1 as n grows (correspondence principle).
Hydrogen approaches from below (gaps shrink).
G(n) approaches from above (gaps grow but decelerate).
Both satisfy: large n = nearly classical behavior.
""")


# ============================================================
# PART 4: THE STEP RATIO
# ============================================================

print("=" * 70)
print("PART 4: STEP RATIOS G(n+1)/G(n)")
print("=" * 70)

print("""
G(n+1)/G(n) = (n+1)^(2n+2) / [n^(n+1) * (n+2)^(n+1)]

Every ratio is exact rational. The sequence decreases toward 1.
""")

print(f"{'n':>4} {'G(n+1)/G(n)':>20} {'Decimal':>12} {'Distance from 1':>15}")
print("-" * 55)

for n in range(1, 15):
    ratio = G(n + 1) / G(n)
    dec = float(ratio)
    dist = dec - 1
    print(f"{n:4d} {str(ratio):>20s} {dec:12.8f} {dist:15.8f}")

print("""
The step ratio decreasing to 1 means:
  - Low n: large jumps between levels (quantum behavior)
  - High n: small relative jumps (classical behavior)
  - The correspondence principle is built into the function
""")


# ============================================================
# PART 5: PARTITION FUNCTION CONVERGENCE
# ============================================================

print("=" * 70)
print("PART 5: PARTITION FUNCTION Z(beta) = sum exp(-beta * G(n))")
print("=" * 70)

print("""
The hydrogen partition function DIVERGES in standard treatment
(requires ad hoc cutoff at large n). This is a known problem.

With G(n) levels, the partition function CONVERGES because G(n) grows
linearly while the Boltzmann factor decays exponentially.
""")

print(f"{'beta':>6} {'Z_G (G levels)':>15} {'Z_QHO (equispaced)':>20} {'Z_H (hydrogen)':>15}")
print("-" * 60)

for beta in [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]:
    Z_G = sum(math.exp(-beta * G_float(n)) for n in range(200))
    Z_QHO = sum(math.exp(-beta * (n + 0.5)) for n in range(200))
    # Hydrogen: sum exp(-beta * (-1/n^2)) = sum exp(beta/n^2) — DIVERGES
    Z_H = sum(math.exp(beta / n ** 2) for n in range(1, 50))  # truncated
    print(f"{beta:6.1f} {Z_G:15.6f} {Z_QHO:20.6f} {Z_H:15.2f} {'(truncated)' if beta > 0.5 else ''}")

print("""
Z_G converges naturally. Z_H requires truncation.
This is a genuine advantage of the G(n) spectrum: no UV divergence.
""")


print("=" * 70)
print("SUMMARY")
print("=" * 70)
print("""
The Amundson spectrum E_n = G(n):
  1. Has zero ground-state energy (no zero-point artifact)
  2. Is non-equispaced (like real atoms, unlike the QHO)
  3. Has all-rational energy levels and gaps
  4. Satisfies the correspondence principle (classical at large n)
  5. Produces convergent partition functions (no UV divergence)
  6. Requires no transcendental constants at finite n

The standard 1/2 zero-point energy and the constant e in partition
functions are artifacts of pretending that discrete systems are
continuous. G(n) removes the pretending.
""")
