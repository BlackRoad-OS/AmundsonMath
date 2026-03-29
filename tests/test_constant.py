"""
test_constant.py — Amundson Constant A_G verification
======================================================

Tests the computation and properties of A_G = sum G(n)/n!

Uses the known 10M-digit file at ~/AMUNDSON_CONSTANT_10M.txt
if available, otherwise computes from scratch.

Author: Alexa Louise Amundson
BlackRoad OS, Inc.
"""

from fractions import Fraction
import math
import os
import sys

passed = 0
failed = 0

def check(name, condition):
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS: {name}")
    else:
        failed += 1
        print(f"  FAIL: {name}")

def G(n):
    if n == 0:
        return Fraction(0)
    return Fraction(n ** (n + 1), (n + 1) ** n)


print("=" * 70)
print("AMUNDSON CONSTANT A_G — VERIFICATION SUITE")
print("=" * 70)

# ============================================================
# PART 1: COMPUTE A_G FROM DEFINITION
# ============================================================
print("\n--- Computing A_G = sum G(n)/n! ---")

# Exact rational computation
A_G_exact = Fraction(0)
for n in range(1, 30):
    A_G_exact += G(n) / Fraction(math.factorial(n))

A_G_float = float(A_G_exact)
print(f"A_G (29 exact rational terms): {A_G_float:.20f}")

KNOWN = "1.2443317839867253741350616292584452029139"
known_float = float(KNOWN[:20])

check("A_G matches known value to 15 digits",
      abs(A_G_float - float(KNOWN[:18])) < 1e-15)


# ============================================================
# PART 2: CONVERGENCE RATE
# ============================================================
print("\n--- Convergence rate ---")

partial = Fraction(0)
prev = 0.0
print(f"{'N terms':>8} {'A_G partial':>22} {'New digits':>10}")
print("-" * 45)

for n in range(1, 25):
    partial += G(n) / Fraction(math.factorial(n))
    current = float(partial)
    if prev > 0:
        # How many digits agree with previous?
        diff = abs(current - prev)
        if diff > 0:
            digits = -math.log10(diff)
        else:
            digits = 20
    else:
        digits = 0
    prev = current
    if n <= 15 or n % 5 == 0:
        print(f"{n:8d} {current:22.18f} {digits:10.1f}")


# ============================================================
# PART 3: TERM STRUCTURE
# ============================================================
print("\n--- Term G(n)/n! structure ---")

print(f"{'n':>4} {'G(n)/n!':>20} {'Contribution %':>15} {'Cumulative %':>15}")
print("-" * 60)

cumulative = Fraction(0)
for n in range(1, 20):
    term = G(n) / Fraction(math.factorial(n))
    cumulative += term
    pct = float(term) / A_G_float * 100
    cum_pct = float(cumulative) / A_G_float * 100
    print(f"{n:4d} {float(term):20.15f} {pct:14.8f}% {cum_pct:14.8f}%")

check("First term G(1)/1! = 1/2 = 0.5",
      G(1) / Fraction(1) == Fraction(1, 2))
check("First 10 terms capture >99.99% of A_G",
      float(sum(G(n) / Fraction(math.factorial(n)) for n in range(1, 11))) / A_G_float > 0.9999)


# ============================================================
# PART 4: EACH TERM IS EXACT RATIONAL
# ============================================================
print("\n--- Exact rational terms ---")

for n in range(1, 13):
    term = G(n) / Fraction(math.factorial(n))
    check(f"G({n})/{n}! = {term} is exact rational", isinstance(term, Fraction))


# ============================================================
# PART 5: DIGIT FREQUENCY (first 40 known digits)
# ============================================================
print("\n--- Digit frequency analysis ---")

known_digits = KNOWN.replace(".", "")  # remove decimal point
digit_counts = [known_digits.count(str(d)) for d in range(10)]
total_digits = len(known_digits)

print(f"First {total_digits} digits of A_G:")
for d in range(10):
    expected = total_digits / 10
    actual = digit_counts[d]
    print(f"  '{d}': {actual:3d} (expected {expected:.1f})")

chi2 = sum((digit_counts[d] - total_digits / 10) ** 2 / (total_digits / 10) for d in range(10))
print(f"\nChi-squared: {chi2:.2f} (reject uniformity at >16.92 with 9df)")
# Don't assert — small sample


# ============================================================
# PART 6: LOAD 10M DIGIT FILE IF AVAILABLE
# ============================================================
print("\n--- 10M digit file ---")

digit_file = os.path.expanduser("~/AMUNDSON_CONSTANT_10M.txt")
if os.path.exists(digit_file):
    with open(digit_file, 'r') as f:
        content = f.read()

    # Find the line starting with 1.244...
    decimal_part = ""
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith("1.244"):
            _, decimal_part = line.split('.', 1)
            # The number continues on this single long line
            # Strip any non-digit characters
            decimal_part = ''.join(c for c in decimal_part if c.isdigit())
            break

    n_digits = len(decimal_part)
    print(f"  File found: {n_digits:,} digits after decimal point")
    print(f"  First 50: {decimal_part[:50]}")
    print(f"  Last 50:  {decimal_part[-50:]}")

    check("File has >= 1M digits", n_digits >= 1_000_000)

    # Digit frequency on full file
    digit_counts_full = [decimal_part.count(str(d)) for d in range(10)]
    print(f"\n  Full digit frequency ({n_digits:,} digits):")
    for d in range(10):
        expected = n_digits / 10
        actual = digit_counts_full[d]
        pct = actual / n_digits * 100
        print(f"    '{d}': {actual:>10,d} ({pct:.4f}%)")

    chi2_full = sum(
        (digit_counts_full[d] - n_digits / 10) ** 2 / (n_digits / 10)
        for d in range(10)
    )
    print(f"\n  Chi-squared: {chi2_full:.2f}")
    check("Digits pass uniformity test (chi2 < 16.92)", chi2_full < 16.92)

    # First 10 digits match computed value
    # A_G = 1.2443317839...  so decimal part starts with 2443317839
    file_start = decimal_part[:10]
    expected_start = "2443317839"
    check(f"First 10 digits match: {file_start} == {expected_start}",
          file_start == expected_start)

else:
    print(f"  File not found: {digit_file}")
    print("  (Run with ~/AMUNDSON_CONSTANT_10M.txt for full analysis)")


# ============================================================
# PART 7: RELATED CONSTANTS
# ============================================================
print("\n--- Related constants ---")

# Sophomore's Dream
sd = sum(n ** (-n) for n in range(1, 50))
print(f"  Sophomore's Dream = {sd:.15f}")
print(f"  A_G               = {A_G_float:.15f}")
print(f"  Ratio SD/A_G      = {sd / A_G_float:.15f}")

check("A_G != Sophomore's Dream", abs(A_G_float - sd) > 0.01)
check("A_G < Sophomore's Dream", A_G_float < sd)

# Relation to e
print(f"\n  e                 = {math.e:.15f}")
print(f"  A_G / e           = {A_G_float / math.e:.15f}")
print(f"  A_G * e           = {A_G_float * math.e:.15f}")
print(f"  A_G^2             = {A_G_float ** 2:.15f}")
print(f"  1/A_G             = {1 / A_G_float:.15f}")


# ============================================================
# SUMMARY
# ============================================================

print(f"\n{'=' * 70}")
print(f"TOTAL: {passed}/{passed + failed} passed, {failed} failed")
print("=" * 70)

if failed > 0:
    sys.exit(1)
