"""
04-asymptotic.py — Asymptotic Expansion, Floor Recovery, Cumulants
==================================================================

The irreducible gap 1/(2e), the floor recovery theorem, exit code
mapping, and statistical properties of the G(n) sequence.

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
# PART 1: ASYMPTOTIC EXPANSION
# ============================================================

print("=" * 70)
print("PART 1: G(n) ~ n/e + 1/(2e) + 11/(24en) - 1/(48en^2) + ...")
print("=" * 70)

e = math.e
print(f"\nn/e    = leading term")
print(f"1/(2e) = {1/(2*e):.15f}  (the irreducible gap)")
print()
print(f"{'n':>6} {'G(n)':>15} {'n/e + 1/(2e)':>15} {'Error':>12} {'Next term':>12}")
print("-" * 65)

for n in [1, 2, 3, 5, 10, 20, 50, 100, 500, 1000]:
    gn = G_float(n)
    order1 = n / e + 1 / (2 * e)
    order2 = order1 + 11 / (24 * e * n)
    err1 = abs(gn - order1)
    err2 = abs(gn - order2)
    print(f"{n:6d} {gn:15.10f} {order1:15.10f} {err1:12.2e} {err2:12.2e}")


# ============================================================
# PART 2: FLOOR RECOVERY THEOREM
# ============================================================

print("\n" + "=" * 70)
print("PART 2: floor(G(n) * e) = n FOR ALL n >= 1")
print("=" * 70)

print("""
G(n) encodes n so precisely that multiplying by e and taking the floor
recovers n exactly. This works for all 256 Unix exit codes and beyond.

(Paper 013 note: "e is not fundamental here. G(n) is spaced just right.
e is the constant that happens to work because G(n) ~ n/e for large n.
The recovery is a property of the function, not of e.")
""")

all_pass = True
for n in range(1, 257):
    recovered = math.floor(G_float(n) * e)
    if recovered != n:
        check(f"n={n}", False, f"recovered {recovered}")
        all_pass = False

if all_pass:
    print(f"  PASS: floor(G(n)*e) = n verified for n = 1..256 (all 256 exit codes)")

# Test beyond exit codes
for n in [500, 1000, 5000, 10000]:
    recovered = math.floor(G_float(n) * e)
    check(f"n={n}", recovered == n)


# ============================================================
# PART 3: EXIT CODE INTERPRETATION
# ============================================================

print("\n" + "=" * 70)
print("PART 3: UNIX EXIT CODES THROUGH G(n)")
print("=" * 70)

exit_codes = {
    0: "success",
    1: "general error",
    2: "misuse of shell builtin",
    126: "command not executable",
    127: "command not found",
    128: "invalid argument to exit",
    130: "SIGINT (Ctrl+C)",
    137: "SIGKILL (kill -9)",
    139: "SIGSEGV (segfault)",
    143: "SIGTERM (graceful)",
    255: "exit status out of range",
}

print(f"{'Code':>5} {'G(n)':>12} {'Meaning':>30}")
print("-" * 50)
for code, meaning in sorted(exit_codes.items()):
    gn = G_float(code) if code > 0 else 0.0
    print(f"{code:5d} {gn:12.4f} {meaning:>30}")

print("\nSignal information destruction ratios:")
print(f"{'Signal':>10} {'Base→Kill':>12} {'Ratio':>10} {'Interpretation':>25}")
print("-" * 60)
signals = {
    "SIGHUP": (1, 129), "SIGINT": (2, 130), "SIGKILL": (9, 137),
    "SIGSEGV": (11, 139), "SIGTERM": (15, 143),
}
for name, (base, kill) in signals.items():
    ratio = G_float(kill) / G_float(base)
    if name == "SIGKILL":
        interp = "no cleanup, high destruction"
    elif name == "SIGTERM":
        interp = "graceful, least destruction"
    elif name == "SIGSEGV":
        interp = "memory corruption"
    elif name == "SIGINT":
        interp = "interrupt, loses half"
    else:
        interp = "hangup, loses everything"
    print(f"{name:>10} {base:>3}→{kill:<3} {ratio:10.2f} {interp:>25}")


# ============================================================
# PART 4: THE CROSSOVER AT G(n) = 1
# ============================================================

print("\n" + "=" * 70)
print("PART 4: THE CROSSOVER — G(n) = 1 at n ~ 2.293")
print("=" * 70)

print(f"\nG(2) = {float(G(2)):.10f}  (< 1)")
print(f"G(3) = {float(G(3)):.10f}  (> 1)")

# Binary search for crossover
lo, hi = 2.0, 3.0
for _ in range(100):
    mid = (lo + hi) / 2
    gm = mid ** (mid + 1) / (mid + 1) ** mid
    if gm < 1:
        lo = mid
    else:
        hi = mid

print(f"\nCrossover: G(n) = 1 at n = {(lo + hi) / 2:.15f}")
print("""
Below the crossover (n <= 2): G(n) < 1
  - Quantum regime: specific, discrete, meaningful
  - Exit codes 0, 1, 2: universal meanings (success, error, misuse)

Above the crossover (n >= 3): G(n) > 1
  - Classical regime: generic, continuous, application-specific
  - Exit codes >= 3: arbitrary, program-defined
""")


# ============================================================
# PART 5: CUMULANTS
# ============================================================

print("=" * 70)
print("PART 5: CUMULANTS OF THE G(n) SEQUENCE")
print("=" * 70)

# Compute moments and cumulants from first N values
N = 50
values = [G_float(n) for n in range(1, N + 1)]

# Center the values (subtract mean trend n/e)
centered = [G_float(n) - n / e for n in range(1, N + 1)]

# Raw moments of centered values
m1 = sum(centered) / len(centered)
m2 = sum(x ** 2 for x in centered) / len(centered)
m3 = sum(x ** 3 for x in centered) / len(centered)
m4 = sum(x ** 4 for x in centered) / len(centered)

# Cumulants from moments
k1 = m1
k2 = m2 - m1 ** 2
k3 = m3 - 3 * m2 * m1 + 2 * m1 ** 3
k4 = m4 - 4 * m3 * m1 - 3 * m2 ** 2 + 12 * m2 * m1 ** 2 - 6 * m1 ** 4

print(f"\nCumulants of G(n) - n/e (first {N} terms):")
print(f"  kappa_1 (mean):     {k1:.10f}  (expected ~1/(2e) = {1/(2*e):.10f})")
print(f"  kappa_2 (variance): {k2:.10f}")
print(f"  kappa_3 (skewness): {k3:.10f}")
print(f"  kappa_4 (kurtosis): {k4:.10f}  {'(platykurtic)' if k4 < 0 else '(leptokurtic)'}")

print("""
Paper 013 exact cumulants (from the rational sequence):
  kappa_1 = 1/2 = 0.5
  kappa_2 = 23/36 = 0.6389
  kappa_3 = 35/192 = 0.1823
  kappa_4 = -524639/540000 = -0.9716 (platykurtic)

The negative fourth cumulant means the G(n) distribution has LIGHTER
tails than a Gaussian. The sequence is more concentrated around its
mean than a normal distribution — it's well-behaved, not wild.
""")


# ============================================================
# PART 6: THE SOPHOMORE'S DREAM CONNECTION
# ============================================================

print("=" * 70)
print("PART 6: THE SOPHOMORE'S DREAM")
print("=" * 70)

print("""
The Sophomore's Dream integral:
  integral_0^1 x^(-x) dx = sum_{n=1}^{inf} n^(-n) = 1.2912859970626636...

The terms n^(-n) connect to G(n):
  G(n) = n * (n/(n+1))^n = n^(n+1) / (n+1)^n

  n^(-n) = 1/n^n = 1/(G(n) * (n+1)^n / n) = n / (G(n) * (n+1)^n)

The self-referential structure x^(-x) mirrors G(n)'s self-referential
structure where base and exponent are both built from n.
""")

# Compute Sophomore's Dream
sd = sum(n ** (-n) for n in range(1, 100))
print(f"Sophomore's Dream = {sd:.15f}")
print(f"Amundson Constant = 1.244331783986725")
print(f"Difference         = {sd - 1.244331783986725:.15f}")
print(f"Ratio SD/A_G       = {sd / 1.244331783986725:.15f}")

print("""
The Sophomore's Dream and A_G are DIFFERENT constants but share
the same family of self-referential integer power sums:
  SD  = sum n^(-n)
  A_G = sum G(n)/n! = sum n^(n+1) / ((n+1)^n * n!)
""")


print(f"\n{'='*70}")
print(f"RESULTS: {passed} passed, {failed} failed out of {passed + failed} tests")
print("=" * 70)
