"""Exact finite Hecke modular-polynomial reconstruction. General degree bounds are proved in the note, not inferred here."""
from .arithmetic import mul, inv, power, eta_pair, prime_domain, natural

def modular_poly(p, qbound, kind='raw'):
    prime_domain(p)
    natural(qbound, 'modular polynomial q-bound', (p + 1) // 2 + 1)
    if kind not in ('raw', 'franel'):
        raise ValueError('unknown period')
    n = qbound
    aa, bb = eta_pair(p * n)
    H = [a + b if kind == 'raw' else a - b for a, b in zip(aa, bb)]
    powers = [1] + [0] * (p * n)
    psums = [None]
    for j in range(1, p + 1):
        powers = mul(powers, H, p * n)
        psums.append([p * powers[p * i] for i in range(n + 1)])
    es = [[1] + [0] * n]
    for j in range(1, p + 1):
        v = [0] * (n + 1)
        for i in range(1, j + 1):
            z = mul(es[j - i], psums[i], n)
            for l, x in enumerate(z):
                v[l] += (-1) ** (i - 1) * x
        if any((x % j for x in v)):
            raise ValueError('Newton not integer')
        es.append([x // j for x in v])
    hi = inv(H[:n + 1], n)
    hipow = [1] + [0] * n
    hp = [H[j // p] if j % p == 0 else 0 for j in range(n + 1)]
    alpha = mul(hp, hi, n)
    Ecoeff = []
    for j in range(p + 1):
        Ecoeff.append([(-1) ** j * p ** (2 * (p - j)) * x for x in mul(es[j], hipow, n)])
        hipow = mul(hipow, hi, n)
    Tqs = []
    for j in range(p + 2):
        v = Ecoeff[j][:] if j <= p else [0] * (n + 1)
        if j:
            z = mul(alpha, Ecoeff[j - 1], n)
            v = [x - y for x, y in zip(v, z)]
        Tqs.append(v)
    theta = H[:n + 1]
    tab = mul(mul(aa[:n + 1], bb[:n + 1], n), power(hi, 2, n), n)
    polys = []
    for j, v in enumerate(Tqs):
        residual = v[:]
        poly = []
        tcur = [1] + [0] * n
        for d in range(j // 2 + 1):
            coef = residual[d]
            poly.append(coef)
            for k, x in enumerate(tcur):
                residual[k] -= coef * x
            tcur = mul(tcur, tab, n)
        if any(residual):
            raise ValueError(('degree fail', p, j, residual))
        polys.append(poly)
    return (polys, tab, theta)
