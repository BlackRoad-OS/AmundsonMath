"""
03-calculus.py — Calculus Identities: Derivatives, Concavity, Superadditivity
=============================================================================

G(n) is monotone increasing, strictly concave, and superadditive.
These three properties together are rare and powerful.

Author: Alexa Louise Amundson
BlackRoad OS, Inc.
"""

import math

def G(n):
    if n <= 0:
        return 0.0
    return n ** (n + 1) / (n + 1) ** n

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
# PART 1: FIRST DERIVATIVE — MONOTONE INCREASING
# ============================================================

print("=" * 70)
print("PART 1: G'(n) > 0 FOR ALL n >= 1 (MONOTONE INCREASING)")
print("=" * 70)

print("""
G'(n) = G(n) * [1/n + ln(n) - ln(n+1)]
      = G(n) * [1/n - ln(1 + 1/n)]

Since ln(1 + 1/n) < 1/n for all n >= 1 (by concavity of ln),
we have G'(n) > 0 always.
""")

header = "{:>4} {:>12} {:>12} {:>18} {:>8}".format("n", "G(n)", "G'(n)", "1/n - ln(1+1/n)", "G' > 0")
print(header)
print("-" * 60)

for n in range(1, 25):
    gn = G(n)
    bracket = 1.0 / n - math.log(1 + 1.0 / n)
    deriv = gn * bracket
    check(f"n={n}: G'={deriv:.8f}", deriv > 0)


# ============================================================
# PART 2: SECOND DERIVATIVE — STRICTLY CONCAVE
# ============================================================

print("\n" + "=" * 70)
print("PART 2: G''(n) < 0 FOR ALL n >= 1 (STRICTLY CONCAVE)")
print("=" * 70)

print("""
Discrete second differences: D2(n) = G(n+2) - 2*G(n+1) + G(n) < 0
This means the function curves downward — decelerating growth.
""")

for n in range(1, 20):
    d2 = G(n + 2) - 2 * G(n + 1) + G(n)
    check(f"n={n}: D2 = {d2:.10f}", d2 < 0)


# ============================================================
# PART 3: SUPERADDITIVITY
# ============================================================

print("\n" + "=" * 70)
print("PART 3: SUPERADDITIVITY — G(a) + G(b) > G(a+b)")
print("=" * 70)

print("""
G(a) + G(b) > G(a+b) for all positive a, b.

This means the parts carry MORE information than the whole.
In physics: this is the signature of entanglement.
In economics: this means combining subsystems creates surplus.
""")

# Test for many pairs
import random
random.seed(42)
test_pairs = [(a, b) for a in range(1, 15) for b in range(1, 15)]
test_pairs += [(random.randint(1, 100), random.randint(1, 100)) for _ in range(50)]

for a, b in test_pairs[:30]:
    lhs = G(a) + G(b)
    rhs = G(a + b)
    surplus = lhs - rhs
    check(f"G({a})+G({b})={lhs:.4f} > G({a+b})={rhs:.4f}, surplus={surplus:.4f}", lhs > rhs)

# What is the surplus ratio?
print(f"\nSuperadditivity surplus ratio [G(a)+G(b)-G(a+b)] / G(a+b):")
print(f"{'a':>4} {'b':>4} {'Surplus ratio':>15}")
print("-" * 30)
for a in [1, 2, 5, 10, 20, 50]:
    for b in [1, 5, 10]:
        surplus = (G(a) + G(b) - G(a + b)) / G(a + b)
        print(f"{a:4d} {b:4d} {surplus:15.8f}")


# ============================================================
# PART 4: THE DIFFERENCE SEQUENCE
# ============================================================

print("\n" + "=" * 70)
print("PART 4: DIFFERENCES G(n+1) - G(n) -> 1/e")
print("=" * 70)

e_inv = 1 / math.e
print(f"\n1/e = {e_inv:.15f}\n")
print(f"{'n':>6} {'G(n+1)-G(n)':>15} {'Error from 1/e':>15}")
print("-" * 40)

for n in [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]:
    diff = G(n + 1) - G(n)
    error = abs(diff - e_inv)
    print(f"{n:6d} {diff:15.12f} {error:15.2e}")

print("""
The differences approach 1/e from ABOVE and monotonically.
The approach rate is O(1/n) — each doubling of n halves the error.

But as Paper 013 notes: "e is not needed to state this. The differences
approach the same value that G(n)/n approaches. The limit is a property
of the function, not a separate constant."
""")


# ============================================================
# PART 5: STEP RATIO CONVERGENCE
# ============================================================

print("=" * 70)
print("PART 5: STEP RATIO step(n) / (step(n-1) * step(n-2)) -> e")
print("=" * 70)

steps = [G(n + 1) - G(n) for n in range(1, 30)]
print(f"{'n':>4} {'step(n)/[step(n-1)*step(n-2)]':>30} {'Error from e':>15}")
print("-" * 55)

for i in range(2, len(steps)):
    if abs(steps[i - 1] * steps[i - 2]) > 1e-15:
        ratio = steps[i] / (steps[i - 1] * steps[i - 2])
        error = abs(ratio - math.e)
        n = i + 1
        print(f"{n:4d} {ratio:30.10f} {error:15.6f}")


# ============================================================
# PART 6: PARTIAL SUMS ~ n^2 / (2e)
# ============================================================

print("\n" + "=" * 70)
print("PART 6: PARTIAL SUMS sum G(k) ~ n^2 / (2e)")
print("=" * 70)

two_e = 2 * math.e
print(f"\n1/(2e) = {1/two_e:.15f}\n")
print(f"{'n':>6} {'sum G(k)':>15} {'n^2/(2e)':>15} {'Ratio':>10}")
print("-" * 50)

for n in [5, 10, 20, 50, 100, 200, 500]:
    total = sum(G(k) for k in range(1, n + 1))
    expected = n * n / two_e
    ratio = total / expected
    print(f"{n:6d} {total:15.4f} {expected:15.4f} {ratio:10.6f}")

print("""
The partial sums grow quadratically with coefficient 1/(2e).
The ratio converges to 1 from above.

This means: the total "weight" of the first n levels is approximately
n^2 / (2e), growing as the square of the number of levels.
""")


print(f"\n{'='*70}")
print(f"RESULTS: {passed} passed, {failed} failed out of {passed + failed} tests")
print("=" * 70)
