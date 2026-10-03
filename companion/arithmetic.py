"""Integer and rational arithmetic used by the finite companion.

Series are coefficient lists in ascending degree. Truncation degree is inclusive.
All scientific acceptance checks raise exceptions, including under Python -O.
"""
from __future__ import annotations
from fractions import Fraction
from math import isqrt


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ArithmeticError(message)


def natural(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f'{name} must be an integer >= {minimum}')


def prime_domain(p, minimum=5):
    natural(p, 'prime', minimum)
    if any(p % d == 0 for d in range(2, isqrt(p) + 1)):
        raise ValueError(f'{p} is not prime')


def mul(a, b, n):
    natural(n, 'truncation degree')
    c = [0] * (n + 1)
    for i, x in enumerate(a[:n + 1]):
        if x:
            for j, y in enumerate(b[:n + 1 - i]):
                if y:
                    c[i + j] += x * y
    return c


def inv(a, n):
    natural(n, 'truncation degree')
    require(bool(a), 'empty series has no inverse')
    require(a[0] == 1, 'series inverse requires constant coefficient one')
    b = [1] + [0] * n
    for j in range(1, n + 1):
        b[j] = -sum(a[k] * b[j-k] for k in range(1, min(j, len(a)-1)+1))
    return b


def power(a, k, n):
    natural(n, 'truncation degree')
    if type(k) is not int:
        raise ValueError('series exponent must be an integer')
    if k < 0:
        return power(inv(a, n), -k, n)
    b = [1] + [0] * n
    while k:
        if k & 1:
            b = mul(b, a, n)
        a = mul(a, a, n)
        k //= 2
    return b


def eta_quot(exps, n, engine='product'):
    """Coefficients q^0..q^n; only integer nonnegative leading orders admitted."""
    natural(n, 'eta truncation degree')
    require(bool(exps), 'empty eta quotient')
    require(all(type(d) is int and d > 0 and type(r) is int
                for d, r in exps.items()), 'invalid eta exponents')
    if engine not in ('product', 'logarithmic_derivative'):
        raise ValueError('unknown eta expansion engine')
    shift, rem = divmod(sum(d * r for d, r in exps.items()), 24)
    require(rem == 0 and shift >= 0, 'nonintegral or negative q order')
    if shift > n:
        return [0] * (n + 1)
    m = n - shift
    e = [0] + [sum(r for d, r in exps.items() if k % d == 0)
               for k in range(1, m + 1)]
    a = [1] + [0] * m
    if engine == 'product':
        for k in range(1, m + 1):
            if e[k] >= 0:
                for _ in range(e[k]):
                    for j in range(m, k - 1, -1):
                        a[j] -= a[j-k]
            else:
                for _ in range(-e[k]):
                    for j in range(k, m + 1):
                        a[j] += a[j-k]
    elif engine == 'logarithmic_derivative':
        b = [0] + [sum(d * e[d] for d in range(1, j + 1) if j % d == 0)
                   for j in range(1, m + 1)]
        for j in range(1, m + 1):
            numerator = -sum(b[k] * a[j-k] for k in range(1, j + 1))
            a[j], rem = divmod(numerator, j)
            require(rem == 0, f'Euler recurrence nonintegral at {j}')
    else:
        raise ValueError('unknown eta expansion engine')
    return [0] * shift + a


def eta_pair(n):
    return (eta_quot({1: -5, 2: 7, 3: 7, 6: -5}, n),
            eta_quot({1: 7, 2: -5, 3: -5, 6: 7}, n))


def eval_series(cs, t, n):
    require(bool(t) and t[0] == 0, 'formal composition requires zero constant term')
    out = [0] * (n + 1)
    for c in reversed(cs):
        out = mul(out, t, n)
        out[0] += c
    return out


def seq(upto, A, B, C):
    natural(upto, 'sequence upper index')
    require(all(type(v) is int for v in (A, B, C)), 'noninteger recurrence parameters')
    u = [1, B]
    for n in range(1, upto):
        num = (A*n*(n+1)+B)*u[-1] - C*n*n*u[-2]
        v, rem = divmod(num, (n+1)**2)
        require(rem == 0, 'nonintegral recurrence')
        u.append(v)
    return u[:upto+1]


def primes(bound):
    natural(bound, 'prime upper bound', 2)
    return [p for p in range(2, bound + 1)
            if all(p % d for d in range(2, isqrt(p) + 1))]


def representation(p):
    prime_domain(p)
    require(p % 3 == 1, 'representation requires a split prime')
    for y in range(1, isqrt(p // 3) + 1):
        x = isqrt(p - 3*y*y)
        if x*x + 3*y*y == p:
            return x, y
    raise ArithmeticError(f'no x^2+3y^2 representation for {p}')


def egcd(a, b):
    old_r, r, old_s, s, old_t, t = a, b, 1, 0, 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r-q*r
        old_s, s = s, old_s-q*s
        old_t, t = t, old_t-q*t
    return old_r, old_s, old_t


def qmul(a, b):
    """Q[delta], delta^2=-3."""
    return a[0]*b[0]-3*a[1]*b[1], a[0]*b[1]+a[1]*b[0]


def qdiv(a, b):
    norm = b[0]*b[0]+3*b[1]*b[1]
    require(norm != 0, 'division by zero in Q[delta]')
    num = qmul(a, (b[0], -b[1]))
    return Fraction(num[0], norm), Fraction(num[1], norm)


def polynomial_remainder(a, b):
    require(bool(a) and bool(b), 'empty polynomial')
    a = [Fraction(x) for x in a]
    b = [Fraction(x) for x in b]
    require(b[-1] != 0, 'zero leading denominator')
    while len(a) >= len(b):
        c = a[-1] / b[-1]
        off = len(a)-len(b)
        for j, x in enumerate(b):
            a[off+j] -= c*x
        while len(a) > 1 and not a[-1]:
            a.pop()
    return a


def weighted_mod(gs, denom, p):
    prime_domain(p)
    require(len(gs) >= p, 'insufficient coefficients for prime truncation')
    require(all(type(v) is int for v in gs[:p]), 'prime truncation requires integer coefficients')
    require(type(denom) is int and denom % p != 0, 'denominator is not a p-adic unit')
    m = p*p
    d = pow(denom, -1, m)
    total, factor = 0, 1
    for g in gs[:p]:
        total = (total + (g % m)*factor) % m
        factor = factor*d % m
    return total
