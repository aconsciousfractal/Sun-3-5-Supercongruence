"""Finite eta certificates for the paper's modular periods and CM geometry.

The finite residuals yield identities only with the paper's modularity,
holomorphy and valence arguments. Binomial-period comparisons are regressions.
"""
from fractions import Fraction as F
from math import comb, gcd
from .arithmetic import require, eta_quot, mul, power, inv, eval_series, seq

DIVISORS = (1, 2, 3, 6)
DEFINITIONS = {
    'A': {1: -5, 2: 7, 3: 7, 6: -5},
    'B': {1: 7, 2: -5, 3: -5, 6: 7},
    'J': {1: 2, 2: 2, 3: 2, 6: 2},
    'h': {1: -5, 2: 1, 3: -1, 6: 5},
    'h3': {1: -12, 3: 12},
    'R': {1: -12, 2: 12, 3: 12, 6: -12},
    'Rh': {1: -17, 2: 13, 3: 11, 6: -7},
}


def cusp_orders(r):
    """Ligozat orders; cusp denominators in the order 1,2,3,6."""
    return [sum((F(6*gcd(c, d)**2*e, 24*gcd(c, 6//c)*c*d)
                 for d, e in r.items()), F(0)) for c in DIVISORS]


def add(*terms):
    require(bool(terms) and len({len(t) for t in terms}) == 1,
            'unequal series precision')
    return [sum(row) for row in zip(*terms)]


def scale(a, value):
    return [value*x for x in a]


def theta(a):
    return [i*x for i, x in enumerate(a)]


def logarithmic_coefficients(r, n):
    """q d(log eta quotient)/dq, independently from expanded coefficients."""
    shift, rem = divmod(sum(d*e for d, e in r.items()), 24)
    require(rem == 0, 'nonintegral logarithmic shift')
    return [shift] + [-sum(d*sum(e for k, e in r.items() if d % k == 0)
                          for d in range(1, m+1) if m % d == 0)
                      for m in range(1, n+1)]


def period_residuals(Y, J, ell, a, b, c):
    n = len(Y)-1
    require(len(J) == len(ell) == len(Y), 'unequal period precision')
    require(n >= 8, 'period certificate needs coefficients q^0 through q^8')
    require(all(type(x) is int for values in (Y,J,ell) for x in values) and
            all(type(x) is int for x in (a,b,c)), 'period certificate requires integers')
    dY = theta(Y)
    ddY = theta(dY)
    W = add(mul(Y, ell, n), scale(dY, -2))
    Y2 = mul(Y, Y, n)
    J2 = mul(J, J, n)
    p1 = add(mul(W, W, n), scale(mul(Y2, Y2, n), -1),
             scale(mul(J, Y2, n), 4*a), scale(J2, -16*c))
    p2 = add(scale(mul(Y, ddY, n), 2), scale(mul(dY, dY, n), -3),
             scale(mul(J, Y2, n), -4*b), scale(J2, 12*c))
    return W, p1, p2


def validate_period(Y, J, ell, parameters):
    result = period_residuals(Y, J, ell, *parameters)
    require(not any(result[1]+result[2]), 'nonzero period certificate residual')
    return result


def first_nonzero(a):
    return next(({'degree': i, 'coefficient': x} for i, x in enumerate(a) if x), None)


def validate_geometry(h,h3,rh):
    require(len(h) == len(h3) == len(rh) and len(h) >= 11,
            'geometry certificate needs common coefficients q^0 through q^10')
    require(all(type(x) is int for values in (h,h3,rh) for x in values),
            'geometry certificate requires integer coefficients')
    n = len(h)-1
    h2 = mul(h,h,n)
    e1 = add(h3,scale(mul(h,h3,n),9),scale(h,-1),scale(h2,-16),
             scale(mul(h2,h,n),-64))
    e2 = add(rh,scale([1]+[0]*n,-1),scale(h,-17),scale(h2,-72))
    require(not any(e1+e2), 'nonzero CM geometry residual')
    return e1,e2


def saw(x):
    return F(0) if x.denominator == 1 else x-x.numerator//x.denominator-F(1, 2)


def dedekind(d, c):
    return sum((saw(F(k, c))*saw(F(d*k, c)) for k in range(1, c)), F(0))


def certificates():
    n = 20
    # Euler-product multiplication and logarithmic-derivative recurrence do
    # not share their coefficient generation algorithms.
    arrays = {key: eta_quot(r, n) for key, r in DEFINITIONS.items() if key != 'R'}
    for key, values in arrays.items():
        require(values == eta_quot(DEFINITIONS[key], n, 'logarithmic_derivative'),
                f'eta engines disagree: {key}')
    A, B, J = (arrays[key] for key in ('A', 'B', 'J'))
    require(A[:3] == [1, 5, 13] and B[:3] == [0, 1, -7], 'eta normalization')
    require(mul(A, B, n) == J, 'A B differs from J')
    ell = logarithmic_coefficients(DEFINITIONS['J'], n)
    require(mul(J, ell, n) == theta(J), 'logarithmic derivative disagrees')
    periods, mutations = {}, {}
    for kind, parameters, sign in [('raw', (10, 3, 9), 1), ('franel', (7, 2, -8), -1)]:
        Y = add(A, scale(B, sign))
        W, p1, p2 = validate_period(Y, J, ell, parameters)
        periods[kind] = {'parameters': list(parameters), 'theta_q0_to_q20': Y,
                         'W_q0_to_q20': W, 'P1_residuals': p1, 'P2_residuals': p2,
                         'weight': 8, 'group_index': 12, 'valence_bound': 8,
                         'required_q_zero_through': 8, 'order_lower_bound': 9}
        for i, label in enumerate(('a', 'b', 'c')):
            bad = list(parameters)
            bad[i] += 1
            _, r1, r2 = period_residuals(Y, J, ell, *bad)
            witness = {'P1': first_nonzero(r1), 'P2': first_nonzero(r2)}
            require(witness['P1'] is not None or witness['P2'] is not None,
                    'parameter mutation escaped detection')
            mutations[f'{kind}_{label}_plus_one'] = witness
    metadata = {}
    for name, r in DEFINITIONS.items():
        s1 = sum(d*e for d, e in r.items())
        s2 = sum((6//d)*e for d, e in r.items())
        valuations = {str(ell): sum(e for d, e in r.items() if d % ell == 0)
                      for ell in (2, 3)}
        require(s1 % 24 == s2 % 24 == 0, f'eta modularity congruence: {name}')
        require(all(v % 2 == 0 for v in valuations.values()), f'eta character: {name}')
        metadata[name] = {'exponents': [r.get(d, 0) for d in DIVISORS],
                          'weight': str(F(sum(r.values()), 2)),
                          'cusp_orders': list(map(str, cusp_orders(r))),
                          'mod24_sums': [s1, s2], 'character_valuations': valuations}
    require(cusp_orders(DEFINITIONS['h']) == [-1, 0, 0, 1], 'Hauptmodul cusp orders')
    h, h3, rh = (arrays[key] for key in ('h', 'h3', 'Rh'))
    e1,e2 = validate_geometry(h,h3,rh)
    blocks = [
        {'name': 'E1', 'q_zero_through': 8, 'base_weight': 10,
         'multiplier_exponents': [17, 0, 3, 0],
         'positive_monomials': [[5,0,15,0], [0,1,14,5], [12,1,2,5], [7,2,1,10], [2,3,0,15]],
         'coefficients': [1,9,-1,-16,-64], 'valence_weight': 240, 'order_lower_bound': 242},
        {'name': 'E2', 'q_zero_through': 10, 'base_weight': 13,
         'multiplier_exponents': [17,0,2,7],
         'positive_monomials': [[0,13,13,0], [17,0,2,7], [12,1,1,12], [7,2,0,17]],
         'coefficients': [1,-1,-17,-72], 'valence_weight': 312, 'order_lower_bound': 329}]
    h_exp = metadata['h']['exponents']
    h3_exp = metadata['h3']['exponents']
    term_exponents = {
        'E1': [h3_exp, [x+y for x,y in zip(h_exp,h3_exp)], h_exp,
               [2*x for x in h_exp], [3*x for x in h_exp]],
        'E2': [metadata['Rh']['exponents'], [0]*4, h_exp, [2*x for x in h_exp]]}
    for block in blocks:
        positive = [[x+y for x,y in zip(r, block['multiplier_exponents'])]
                    for r in term_exponents[block['name']]]
        require(positive == block['positive_monomials'], 'denominator-clearing exponents')
        require(all(min(r) >= 0 and sum(r) == 2*block['base_weight'] for r in positive),
                'clearing monomial weight or holomorphy')
        shift = F(sum(d*e for d,e in zip(DIVISORS, block['multiplier_exponents'])), 24)
        require(24*(shift+block['q_zero_through']+1) == block['order_lower_bound'],
                'valence order miscount')
        require(block['valence_weight'] == 24*block['base_weight'] and
                block['order_lower_bound'] > block['valence_weight'], 'insufficient valence bound')
    require(mul([1,6], [-1,24,288], 3) == [-1,18,432,1728], 'CM h factorization')
    require(scale(mul([-1,-6,18], [-1,24,288], 4), -1) == [-1,18,450,1296,-5184],
            'CM t factorization')
    matrices = [(1,1,2,3), (1,2,1,3), (3,1,2,1), (3,2,1,1)]
    phases = []
    for a,b,c,d in matrices:
        require(a*d-b*c == 1, 'eta transformation determinant')
        phases.append(F(a+d,12*c)-dedekind(d,c)-F(1,4))
    require(phases == [F(-1,12), F(1,12), F(-1,12), F(1,12)], 'W3 phases')
    require(phases[0]+phases[3] == phases[1]+phases[2] == 0, 'W3 phase cancellation')
    n = 60
    a = eta_quot(DEFINITIONS['A'], n)
    b = eta_quot(DEFINITIONS['B'], n)
    ab = mul(a,b,n)
    plus, minus = add(a,b), add(a,scale(b,-1))
    tplus = mul(ab,power(plus,-2,n),n)
    tminus = mul(ab,power(minus,-2,n),n)
    for kind, params, Y, t in [('raw',(10,3,9),plus,tplus), ('franel',(7,2,-8),minus,tminus)]:
        direct = [sum(comb(j,k)**2*comb(2*k,k) for k in range(j+1)) if kind == 'raw'
                  else sum(comb(j,k)**3 for k in range(j+1)) for j in range(n+1)]
        require(seq(n,*params) == direct, f'{kind} recurrence vs binomial definition')
        require(eval_series([comb(2*j,j)*v for j,v in enumerate(direct)],t,n) == Y,
                f'{kind} binomial period regression')
    require(mul(tminus, inv([1]+[4*x for x in tminus[1:]],n),n) == tplus,
            'rational parameter transport')
    return {'schema_version': 1, 'status': 'PASS', 'computed_q_degree': 20,
            'cusp_denominators': list(DIVISORS), 'eta_metadata': metadata,
            'eta_coefficients': arrays, 'logarithmic_J': ell, 'period_certificates': periods,
            'geometry_residuals': {'E1': e1, 'E2': e2}, 'valence_closures': blocks,
            'CM_polynomial_factorizations': True, 'W3_matrices': matrices,
            'W3_phases_in_pi_i': list(map(str,phases)),
            'raw_character': {'1':1,'2':-1,'3':1,'6':-1},
            'franel_character': {'1':1,'2':1,'3':-1,'6':-1},
            'period_regression': {'through_q_degree': n, 'definition_checks_per_sequence': n+1,
                                  'raw_theta_first_12': plus[:12], 'franel_theta_first_12': minus[:12],
                                  'raw_t_first_10': tplus[:10]},
            'parameter_mutation_witnesses': mutations}
