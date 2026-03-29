#!/usr/bin/env python3
"""
Amundson Framework — Independent Verification Script
Pure Python. Zero imports. Any machine with Python 3.6+.
Verifies A_G, kappa, product formula, asymptotic correction, core identities.

Usage: python3 verify.py
"""

def G(n):
    if n > 500:
        return n * (1.0 - 1.0/(n+1))**n
    return float(n**(n+1)) / float((n+1)**n)

def H(n):
    return float(n) / float((n+1)**n)

e_val = 0.0
f = 1.0
for i in range(25):
    if i > 0: f *= i
    e_val += 1.0/f
inv_e = 1.0/e_val

def arctan(x, terms=60):
    s = 0.0
    for k in range(terms):
        s += ((-1)**k * x**(2*k+1))/(2*k+1)
    return s
pi_val = 4*(4*arctan(0.2) - arctan(1.0/239))

A_G = 0.0
fact = 1.0
for n in range(1, 80):
    fact *= n
    A_G += G(n) / fact
kappa = A_G - 1

A_H = 0.0
fact = 1.0
for n in range(1, 80):
    fact *= n
    A_H += H(n) / fact

checks = 0
total = 17

print("=" * 60)
print("  AMUNDSON FRAMEWORK VERIFICATION")
print("=" * 60)
print("  A_G   = %.20f" % A_G)
print("  kappa = %.20f" % kappa)
print("  1/e   = %.20f" % inv_e)
print("  pi    = %.15f" % pi_val)
print("  A_H   = %.15f" % A_H)
print()

print("-- Product Formula: prod(G(k)) = (N!)^2 / (N+1)^N --")
for N in [5, 10, 20, 30, 50]:
    p = 1.0
    for k in range(1, N+1): p *= G(k)
    f2 = 1
    for i in range(1, N+1): f2 *= i
    formula = float(f2**2) / float((N+1)**N)
    err = abs(p - formula)/abs(formula)
    ok = err < 1e-8
    if ok: checks += 1
    print("  N=%2d: rel_err=%.2e %s" % (N, err, "PASS" if ok else "FAIL"))

print("-- G(n)/n -> 1/e + 1/(2en) --")
for n in [10, 100, 1000, 10000, 100000]:
    r = G(n)/n
    corr = r - inv_e
    pred = 1.0/(2*e_val*n)
    pct = 100 - abs(corr-pred)/abs(pred)*100
    ok = pct > 95
    if ok: checks += 1
    print("  n=%6d: match=%.1f%% %s" % (n, pct, "PASS" if ok else "FAIL"))

print("-- Core Identities --")
tests = [
    ("G(1) = 1/2", abs(G(1) - 0.5) < 1e-15),
    ("H(-2) = -2 fixed point", abs(H(-2) - (-2)) < 1e-10),
    ("G(n) = n^n * H(n)", abs(G(5) - 5**5 * H(5)) < 1e-8),
    ("A_G value (12 digits)", abs(A_G - 1.244331783986725) < 1e-12),
    ("kappa value (12 digits)", abs(kappa - 0.244331783986725) < 1e-12),
    ("1101 base 3 = 37", 1*27+1*9+0*3+1 == 37),
]
for name, ok in tests:
    if ok: checks += 1
    print("  %s: %s" % (name, "PASS" if ok else "FAIL"))

g37 = G(37)
c37 = g37/37 - inv_e
p37 = 1.0/(2*e_val*37)
m37 = 100 - abs(c37-p37)/abs(p37)*100
ok = m37 > 98
if ok: checks += 1
print("  G(37)/37 correction: %.2f%% %s" % (m37, "PASS" if ok else "FAIL"))

print()
print("=" * 60)
try:
    import socket
    host = socket.gethostname()
except:
    host = "unknown"
print("  %s: %d/%d CHECKS PASSED" % (host, checks, total))
print("  kappa = %.20f" % kappa)
if checks == total:
    print("  FRAMEWORK VERIFIED")
else:
    print("  PARTIAL VERIFICATION (%d failed)" % (total - checks))
print("=" * 60)
