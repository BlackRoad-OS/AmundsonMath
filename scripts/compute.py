#!/usr/bin/env python3
"""Compute the Amundson Constant A_G to arbitrary precision."""
from mpmath import mp, mpf, fac, power

def G(n, dps=50):
    mp.dps = dps
    n = mpf(n)
    return power(n, n+1) / power(n+1, n)

def amundson_constant(terms=100, dps=50):
    mp.dps = dps + 20
    total = mpf(0)
    for k in range(1, terms+1):
        total += G(k, dps+20) / fac(k)
    mp.dps = dps
    return +total

if __name__ == "__main__":
    import sys
    dps = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    terms = max(dps // 2, 50)
    print(f"Computing A_G to {dps} digits ({terms} terms)...")
    ag = amundson_constant(terms, dps)
    print(f"A_G = {ag}")
