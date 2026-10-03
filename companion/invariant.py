"""Finite invariant regression, exact resonances, and a singular-point control."""
from math import comb
from .arithmetic import require, natural, seq, mul, primes


def invariant(u,a,b,c):
    require(bool(u), 'empty invariant polynomial')
    require(all(type(x) is int for x in u) and all(type(x) is int for x in (a,b,c)),
            'invariant requires integer coefficients and parameters')
    degree = 2*len(u)
    v = [j*x for j,x in enumerate(u)]
    w = [j*j*x for j,x in enumerate(u)]
    uv, uu = mul(u,v,degree), mul(u,u,degree)
    core = [2*x-y for x,y in zip(mul(u,w,degree),mul(v,v,degree))]
    result = mul([1,-4*a,16*c],core,degree)
    aux = mul([0,-4*a,32*c],uv,degree)
    aux2 = mul([0,-4*b,12*c],uu,degree)
    return [x+y+z for x,y,z in zip(result,aux,aux2)]


def evaluate(a,t,modulus):
    value = 0
    for c in reversed(a):
        value = (value*t+c) % modulus
    return value


def validate_invariant(g,p,parameters):
    from .arithmetic import prime_domain
    prime_domain(p)
    require(len(g) > p, 'invariant resonance needs the index-p coefficient')
    require(all(type(x) is int for x in g), 'invariant resonance requires integer coefficients')
    a,b,c = parameters
    I = invariant(g[:p],a,b,c)
    require(len(I) == 2*p+1, 'invariant degree allocation')
    require(I[p] == -2*p*p*g[p], 'exact degree-p resonance')
    require(I[2*p] == 4*c*(2*p-1)*(2*p+1)*g[p-1]**2, 'exact degree-2p resonance')
    require(all(v % (p*p) == 0 for v in I), f'nonzero invariant modulo p^2 at p={p}')
    return I


def certificates(bound=199):
    natural(bound, 'invariant bound', 7)
    rows, coefficient_count = [], 0
    for kind, params in [('raw',(10,3,9)),('franel',(7,2,-8))]:
        values = seq(bound,*params)
        g = [comb(2*j,j)*v for j,v in enumerate(values)]
        for p in primes(bound):
            if p < 5:
                continue
            I = validate_invariant(g,p,params)
            coefficient_count += len(I)
            rows.append({'kind':kind,'p':p,'coefficient_count':len(I),
                         'all_zero_mod_p2':True,'exact_resonances':[str(I[p]),str(I[2*p])]})
    require(bool(rows), 'empty invariant window')
    f = seq(10,7,2,-8)
    gf = [comb(2*n,n)*v for n,v in enumerate(f)]
    require(evaluate(gf,8,11) == 0 and evaluate(gf,8,121) == 44, 'singular-point control')
    require((1-28*8-128*8*8) % 11 == 0, 'singular-point discriminant')
    return {'schema_version':1,'status':'PASS','bound_inclusive':bound,
            'polynomial_count':len(rows),'coefficient_count':coefficient_count,'rows':rows,
            'singular_control':{'p':11,'franel_t':8,'U_mod_p':0,'U_mod_p2':44,'D_mod_p':0}}
