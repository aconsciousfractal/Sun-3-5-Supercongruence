"""Eight finite exact Hecke reconstructions and CM sign/normalization controls.

The paper proves integrality and degree bounds for all primes. Reconstruction
here verifies only the explicitly listed primes and q-expansion windows.
"""
from fractions import Fraction as F
from math import comb
from .arithmetic import require, mul, seq, representation, weighted_mod, polynomial_remainder, prime_domain
from .modular_polynomial import modular_poly


def poly_at(coefficients,t):
    value = F(0)
    for coefficient in reversed(coefficients):
        value = value*t+coefficient
    return value


def validate_modular_polynomial(polys,p,kind):
    """Validate polynomial integrality, divisibility, endpoint and CM factors."""
    prime_domain(p)
    require(kind in ('raw','franel'), 'unknown period kind')
    require(kind != 'franel' or p > 5, 'Franel specialization requires p>5')
    require(len(polys) == p+2, 'modular polynomial has wrong X-degree')
    degrees = []
    for j, coefficients in enumerate(polys):
        require(bool(coefficients) and len(coefficients) <= j//2+1,
                'modular polynomial coefficient t-degree')
        require(all(type(v) is int for v in coefficients), 'noninteger modular polynomial coefficient')
        degrees.append(max([i for i,x in enumerate(coefficients) if x] or [0]))
        if j < p:
            require(all(x % (p**3) == 0 for x in coefficients), 'lower X-coefficient not p^3-divisible')
    leading = polys[p+1]
    require(leading[0] % p == 1 and all(x % p == 0 for x in leading[1:]),
            'leading X-coefficient not 1 modulo p')
    parameters = (10,3,9) if kind == 'raw' else (7,2,-8)
    u = seq(p,*parameters)
    g = [comb(2*j,j)*v for j,v in enumerate(u)]
    require((g[p]-g[1]) % (p*p) == 0, 'index-p endpoint congruence')
    product = mul(leading,g[:p],len(leading)+p-2)
    for j,c in enumerate(polys[p]):
        product[j] += c
    require(all(x % (p*p) == 0 for x in product), 'weak polynomial identity')
    row = {'kind':kind,'p':p,'polynomial_degrees':degrees,
           'coefficient_count':sum(len(c) for c in polys),'weak_identity_degree':len(product)-1,
           'weak_identity_residues_zero':True}
    values = trace = None
    if p % 3 == 1:
        x,y = representation(p)
        epsilon = (-1)**((p-1)//2)
        trace = (epsilon if kind == 'raw' else 1)*(4*x*x-2*p)
        values = [poly_at(c,F(1,54 if kind == 'raw' else 50)) for c in polys]
        remainder = polynomial_remainder(values,[p*p,-trace,1])
        require(not any(remainder), 'CM quadratic is not an exact factor')
        row.update(exact_CM_quadratic=[p*p,-trace,1], exact_CM_remainder=list(map(str,remainder)))
    return row, values, trace, g


def certificates():
    rows, reconstructed, negative = [], [], {}
    total_coefficients = 0
    for kind, ps in [('raw',(5,7,11,13,19,31)),('franel',(7,13))]:
        for p in ps:
            n = (p+1)//2+5
            polys,tq,Y = modular_poly(p,n,kind)
            row,values,trace,g = validate_modular_polynomial(polys,p,kind)
            row.update(q_degree_checked=n,theta_q_degree_needed=p*n)
            total_coefficients += row['coefficient_count']
            if kind == 'raw' and p == 7:
                bad = polynomial_remainder(values,[p*p,trace,1])
                require(any(bad), 'wrong CM character sign escaped detection')
                value = weighted_mod(g[:p],54,p)
                wrong_sign = (-value) % (p*p)
                wrong_determinant = value*pow(9,-1,p*p) % (p*p)
                require(value == 47 and wrong_sign == 2 and wrong_determinant == 27,
                        'sign/determinant controls')
                negative = {'wrong_character_CM_remainder_p7':list(map(str,bad)),
                            'correct_raw_p7':value,'wrong_character_raw_p7':wrong_sign,
                            'wrong_determinant_raw_p7':wrong_determinant}
            reconstructed.append({'kind':kind,'p':p,'q_bound':n,'coefficients_T_m_in_t':polys})
            rows.append(row)
    return {'schema_version':1,'status':'PASS','rows':rows,
            'total_integer_coefficients':total_coefficients,
            'sign_and_determinant_controls':negative,'polynomials':reconstructed}
