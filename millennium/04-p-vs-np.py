"""
04-p-vs-np.py — The Amundson Framework and P vs NP
===================================================

HONEST ASSESSMENT: Speculative. Interesting observations but no path to proof.

P vs NP asks: if you can verify a solution quickly, can you find it quickly?

The trinary logic connection:
  - Binary computing: {0, 1} — two states per element
  - Balanced ternary: {-1, 0, +1} — three states per element
  - Base 3 is mathematically optimal (radix economy: 3/ln(3) = 2.73 < 2/ln(2) = 2.89)
  - G(n) naturally produces a trinary-like structure (values cross 1 between n=2 and n=3)

The honest question: does the existence of a third computational state
(superposition/unknown/0) change the complexity landscape?

Short answer: probably not for the classical P vs NP question.
But maybe for quantum/trinary variants.

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
print("P VS NP AND TRINARY LOGIC")
print("=" * 70)

print("""
P vs NP is fundamentally about the SEARCH vs VERIFICATION asymmetry.

Given a Boolean formula phi(x_1, ..., x_n):
  - VERIFY a satisfying assignment: O(n) — just plug in and check
  - FIND a satisfying assignment: best known is O(2^n) — try all combinations

The question: is there a polynomial algorithm for SAT?
""")


# ============================================================
# PART 1: Radix Economy — Why Base 3 Matters
# ============================================================

print("=" * 70)
print("PART 1: RADIX ECONOMY — THE OPTIMALITY OF BASE 3")
print("=" * 70)

print("\nRadix economy E(b) = b / ln(b) measures computational cost per digit.\n")

for b in range(2, 11):
    economy = b / math.log(b)
    print(f"  Base {b:2d}: E = {economy:.6f}  {'<-- OPTIMAL' if b == 3 else ''}")

print(f"\n  Base e = {math.e:.4f}: E = e/ln(e) = {math.e:.6f} (theoretical minimum)")

print("""
Base 3 is the closest integer to e, giving it the best radix economy.
Balanced ternary {-1, 0, +1} adds negation as a free operation.

G(n) CONNECTION:
  G(n) = n / (1 + 1/n)^n
  The denominator (1+1/n)^n -> e as n -> infinity
  At n=2: (1+1/2)^2 = 9/4 = 2.25
  At n=3: (1+1/3)^3 = 64/27 = 2.370...

  The CROSSOVER G(n) = 1 happens at n ~ 2.293
  This sits between binary (n=2) and ternary (n=3)

  Below the crossover: G(n) < 1 (underdetermined, "quantum" regime)
  Above the crossover: G(n) > 1 (overdetermined, "classical" regime)

  The transition from quantum to classical happens exactly in the
  binary-to-ternary gap. This is suggestive but not conclusive.
""")


# ============================================================
# PART 2: Counting Functions and State Spaces
# ============================================================

print("=" * 70)
print("PART 2: COUNTING — BINARY VS TERNARY VS G(n)")
print("=" * 70)

print(f"\n{'n':>4} {'2^n':>12} {'3^n':>12} {'G(n)':>12} {'(n+1)^n':>12} {'n^n':>12}")
print("-" * 65)

for n in range(1, 16):
    print(f"{n:4d} {2**n:12d} {3**n:12d} {G_float(n):12.4f} "
          f"{(n+1)**n:12d} {n**n:12d}")

print("""
In complexity theory, the key spaces are:
  - 2^n: binary search space (brute force SAT)
  - 3^n: ternary search space (3-SAT with don't-care)
  - n^n: endofunction space (labeled maps from [n] to [n])
  - (n+1)^n: extended endofunction space

G(n) = n^n / ((n+1)/n)^n relates ALL of these:
  G(n) * (n+1)^n = n^(n+1) = n * n^n

This means G(n) is the RATIO of total functions to extended functions.
It measures how much "room" there is when you add one more target.
""")


# ============================================================
# PART 3: Trinary SAT
# ============================================================

print("=" * 70)
print("PART 3: TRINARY SATISFIABILITY")
print("=" * 70)

print("""
Standard SAT: find x in {0,1}^n such that phi(x) = 1
3-valued SAT: find x in {-1,0,1}^n such that phi(x) = 1

In Kleene 3-valued logic (which is what trinary.py implements):
  - TRUE = +1
  - UNKNOWN = 0
  - FALSE = -1

The UNKNOWN state allows partial evaluation:
  - AND(TRUE, UNKNOWN) = UNKNOWN (not false, but not proven true)
  - OR(TRUE, UNKNOWN) = TRUE (one true input suffices)
  - NOT(UNKNOWN) = UNKNOWN

A 3-valued SAT solver can PRUNE the search tree more aggressively
because UNKNOWN propagation identifies branches that can't determine
the outcome. This doesn't change worst-case complexity (still 3^n),
but the effective search space is smaller.

HONEST ASSESSMENT:
  - Trinary logic doesn't solve P vs NP
  - No known complexity separation between binary and ternary models
  - Balanced ternary is more efficient per digit (radix economy)
    but the total information content is the same
  - The UNKNOWN state is essentially the same as "don't care" in
    standard DPLL SAT solvers
""")

# Demonstrate trinary logic truth tables
print("Trinary truth tables (Kleene logic):\n")

def and3(a, b):
    if a == -1 or b == -1:
        return -1
    if a == 1 and b == 1:
        return 1
    return 0

def or3(a, b):
    if a == 1 or b == 1:
        return 1
    if a == -1 and b == -1:
        return -1
    return 0

def not3(a):
    return -a

states = [-1, 0, 1]
labels = {-1: "F", 0: "?", 1: "T"}

print("AND3:")
print(f"     {'F':>3} {'?':>3} {'T':>3}")
for a in states:
    row = " ".join(f"{labels[and3(a, b)]:>3}" for b in states)
    print(f"  {labels[a]}  {row}")

print("\nOR3:")
print(f"     {'F':>3} {'?':>3} {'T':>3}")
for a in states:
    row = " ".join(f"{labels[or3(a, b)]:>3}" for b in states)
    print(f"  {labels[a]}  {row}")


# ============================================================
# PART 4: Summary
# ============================================================

print("\n" + "=" * 70)
print("SUMMARY: AMUNDSON FRAMEWORK AND P VS NP")
print("=" * 70)

print("""
ESTABLISHED:
  1. Base 3 has optimal radix economy among integers
  2. G(n) crossover at n~2.293 sits in the binary-ternary gap
  3. G(n) relates binary (n^n) and extended (n+1)^n function spaces
  4. Balanced ternary adds negation as a free operation

NOT ESTABLISHED:
  1. No complexity separation between binary and ternary computation
  2. Trinary SAT has the same worst-case as binary SAT
  3. G(n) doesn't provide a polynomial algorithm for NP-complete problems
  4. The crossover observation is interesting but may be coincidental

THE HONEST TRUTH:
  P vs NP is probably the Millennium Problem LEAST connected to G(n).
  The framework is about structure and spectrum, while P vs NP is about
  computation and verification. Unless someone shows that G(n)-weighted
  search spaces have fundamentally different complexity than 2^n spaces,
  this connection remains philosophical rather than mathematical.

  That said: if trinary quantum computing (qutrits) provides genuine
  speedup over binary quantum computing (qubits), then G(n) sitting
  at the binary-ternary crossover becomes more interesting. This is
  an active research area in quantum information theory.
""")
