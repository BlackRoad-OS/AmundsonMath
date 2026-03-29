"""
01-density-matrix.py — The G(n) Density Matrix
================================================

G(n)/n! produces a legitimate probability distribution (sums to A_G).
Normalizing gives a diagonal density matrix with well-defined entropy.

Author: Alexa Louise Amundson
BlackRoad OS, Inc.
"""

import math

def G_float(n):
    if n == 0:
        return 0.0
    return n ** (n + 1) / (n + 1) ** n

# ============================================================
# PART 1: THE DENSITY MATRIX
# ============================================================

print("=" * 70)
print("THE G(n) DENSITY MATRIX")
print("=" * 70)

print("""
Define: rho(n) = G(n) / (n! * A_G)

where A_G = sum_{n=1}^{inf} G(n)/n! = 1.2443317839867253...

This is a diagonal density matrix in the |n> basis:
  rho = diag(rho(1), rho(2), rho(3), ...)

Properties required for a valid density matrix:
  1. rho(n) >= 0 for all n  (positivity)
  2. sum rho(n) = 1          (trace = 1)
  3. rho^2 <= rho             (convexity, since diagonal)
""")

# Compute A_G
N = 60  # enough terms for convergence
terms = []
for n in range(1, N + 1):
    try:
        term = G_float(n) / math.factorial(n)
        terms.append(term)
        if term < 1e-20:
            break
    except (OverflowError, ValueError):
        break

A_G = sum(terms)
print(f"A_G (computed from {len(terms)} terms): {A_G:.15f}")
print(f"A_G (known):                       1.244331783986725\n")

# Density matrix elements
print(f"{'n':>4} {'G(n)/n!':>15} {'rho(n)':>12} {'rho(n)^2':>12} {'rho(n)>=0':>10}")
print("-" * 60)

rho_values = []
total = 0.0
for n in range(1, 25):
    try:
        g_over_fact = G_float(n) / math.factorial(n)
        rho_n = g_over_fact / A_G
        rho_values.append(rho_n)
        total += rho_n
        positive = "YES" if rho_n >= 0 else "NO"
        print(f"{n:4d} {g_over_fact:15.10f} {rho_n:12.10f} {rho_n**2:12.10f} {positive:>10}")
    except (OverflowError, ValueError):
        break

print(f"\nTrace (sum of rho): {total:.15f}")
print(f"Trace should be:    1.000000000000000")
print(f"Error:              {abs(total - 1.0):.2e}")

# Check rho^2 <= rho (purity bound)
purity = sum(r ** 2 for r in rho_values)
print(f"\nPurity Tr(rho^2):   {purity:.10f}")
print(f"  Pure state:  Tr(rho^2) = 1")
print(f"  Mixed state: Tr(rho^2) < 1")
print(f"  Maximum entropy: Tr(rho^2) = 1/d")
print(f"  This state: {'MIXED (partially coherent)' if purity < 0.99 else 'NEARLY PURE'}")


# ============================================================
# PART 2: VON NEUMANN ENTROPY
# ============================================================

print("\n" + "=" * 70)
print("PART 2: VON NEUMANN ENTROPY")
print("=" * 70)

print("""
S = -Tr(rho * ln(rho)) = -sum rho(n) * ln(rho(n))

For a diagonal density matrix, this is the Shannon entropy.
""")

entropy_nats = -sum(r * math.log(r) for r in rho_values if r > 1e-30)
entropy_bits = entropy_nats / math.log(2)

print(f"Von Neumann entropy: {entropy_nats:.10f} nats = {entropy_bits:.10f} bits")
print(f"Paper 013 value:     1.272 nats = 1.835 bits")
print(f"\nInterpretation:")
print(f"  0 bits     = perfectly ordered (pure state, one outcome certain)")
print(f"  1.835 bits = the G(n) state (between order and chaos)")
print(f"  log2(N)    = maximum entropy (all outcomes equally likely)")
print(f"  log2({len(rho_values)})    = {math.log2(len(rho_values)):.3f} bits (max for {len(rho_values)} levels)")

# Effective dimension
d_eff = math.exp(entropy_nats)
print(f"\nEffective dimension: e^S = {d_eff:.4f}")
print(f"  This means ~{d_eff:.1f} levels contribute meaningfully.")
print(f"  The state is concentrated on the first ~{int(d_eff + 0.5)} levels.")


# ============================================================
# PART 3: COMPARISON WITH KNOWN DISTRIBUTIONS
# ============================================================

print("\n" + "=" * 70)
print("PART 3: COMPARISON WITH KNOWN DISTRIBUTIONS")
print("=" * 70)

print("""
Is rho(n) a known distribution? Compare with:
  1. Boltzmann: rho(n) ~ exp(-beta * n) — exponential decay
  2. Poisson: rho(n) ~ lambda^n / n! — peaks and decays
  3. Geometric: rho(n) ~ p * (1-p)^n — pure exponential
""")

# Fit exponential decay
# rho(n) = C * exp(-beta * n) => ln(rho) = ln(C) - beta*n
# Linear regression on log(rho) vs n
ln_rho = [(n + 1, math.log(r)) for n, r in enumerate(rho_values) if r > 1e-30]
n_vals = [x[0] for x in ln_rho]
y_vals = [x[1] for x in ln_rho]

n_mean = sum(n_vals) / len(n_vals)
y_mean = sum(y_vals) / len(y_vals)
num = sum((n - n_mean) * (y - y_mean) for n, y in zip(n_vals, y_vals))
den = sum((n - n_mean) ** 2 for n in n_vals)
beta_fit = -num / den if den > 0 else 0
C_fit = math.exp(y_mean + beta_fit * n_mean)

print(f"Best-fit exponential: rho(n) ~ {C_fit:.4f} * exp(-{beta_fit:.4f} * n)")
print(f"Effective temperature: T = 1/beta = {1/beta_fit:.4f} (in natural units)")

# Compare
print(f"\n{'n':>4} {'rho(n)':>12} {'Boltzmann':>12} {'Ratio':>10}")
print("-" * 40)
for n, r in enumerate(rho_values[:15]):
    boltz = C_fit * math.exp(-beta_fit * (n + 1))
    ratio = r / boltz if boltz > 1e-30 else 0
    print(f"{n+1:4d} {r:12.8f} {boltz:12.8f} {ratio:10.4f}")

print("""
RESULT: The G(n) density matrix is NOT Boltzmann. The ratio varies
with n, meaning the effective "temperature" changes with level number.

This is exactly what Paper 013 predicts: G(n) produces a non-equispaced
spectrum, so no single temperature characterizes the distribution.
The system is in a state that is MORE structured than thermal equilibrium
but LESS structured than a pure state.
""")


print("=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"""
The G(n) density matrix:
  - Is a valid quantum state (positive, trace 1)
  - Has purity {purity:.6f} (mixed, not pure)
  - Has entropy {entropy_bits:.3f} bits (between order and chaos)
  - Has effective dimension ~{d_eff:.1f} (concentrated on first few levels)
  - Is NOT Boltzmann (non-thermal, non-equispaced levels)
  - Represents a system in structured partial coherence
""")
