"""Bounded prime regressions and exact certificates for both split CM classes."""
from fractions import Fraction as F
from math import comb
from .arithmetic import (require, natural, prime_domain, seq, primes,
                         representation, egcd, qmul, qdiv, weighted_mod)


def cm_matrix(p, x, y, matrix=None, character=1, determinant_scale=None):
    """Verify a CM matrix by determinant, coset, image, root, norm and trace.

    The optional inputs expose the actual algebraic checks to corruption tests.
    They are not parameters of the theorem or of the prime enumeration.
    """
    prime_domain(p)
    require(type(x) is int and type(y) is int and x > 0 and y > 0 and
            x*x+3*y*y == p, 'invalid split-prime representation')
    require(character in (-1, 1), 'invalid character sign')
    if y % 2 == 0:
        divisor, a, b = egcd(x, 3*y)
        require(divisor == 1, 'CM Bezout obstruction: even y')
        expected, e = (a,b,-3*y,x), 1
    else:
        divisor, a0, b = egcd(3*y,x)
        require(divisor == 1, 'CM Bezout obstruction: odd y')
        expected, e = (3*a0,b,-3*x,3*y), 3
    M = expected if matrix is None else tuple(matrix)
    require(len(M) == 4 and all(type(v) is int for v in M), 'invalid CM matrix entries')
    a,b,c,d = M
    require(a*d-b*c == e and c % 6 == 0, 'CM matrix determinant or level')
    if e == 3:
        require(a % 3 == c % 3 == 0, 'CM W3 coset fractions')
        V = (a-2*b,-a//3+b,c-2*d,-c//3+d)
        require(V[0]*V[3]-V[1]*V[2] == 1 and V[2] % 6 == 0, 'CM matrix outside W3 coset')
    k = b*x-a*y if e == 1 else b*y-(a//3)*x
    image = qdiv((b,F(a,3)),(d,F(c,3)))
    require(image == (F(k,p),F(1,3*p)), 'CM image differs from (beta+k)/p')
    lam = (d,F(c,3))
    scale = e if determinant_scale is None else determinant_scale
    require(type(scale) in (int,F), 'CM determinant factor must be exact rational')
    root = qdiv((character*scale*p*p,0),qmul(lam,lam))
    desired = qmul((x,y),(x,y)) if e == 1 else tuple(-v for v in qmul((x,-y),(x,-y)))
    require(root == desired, 'CM character or determinant normalization')
    norm = qmul(root,(root[0],-root[1]))
    epsilon = (-1)**((p-1)//2)
    require(norm == (p*p,0) and 2*root[0] == epsilon*(4*x*x-2*p), 'CM trace or norm')
    return {'p':p,'x':x,'y':y,'e':e,'matrix':list(M),'k':k,'k_mod_p':k % p,
            'root_coefficients_Q_delta':list(map(str,root)),
            'trace':int(2*root[0]),'norm':p*p}


def regression(bound=1999):
    natural(bound, 'prime bound', 7)
    aa, ff = seq(bound,10,3,9), seq(bound,7,2,-8)
    cs = [comb(2*n,n) for n in range(bound+1)]
    ga, gf = [c*v for c,v in zip(cs,aa)], [c*v for c,v in zip(cs,ff)]
    direct_count = min(bound,199)
    for n in range(direct_count):
        require(aa[n] == sum(comb(n,k)**2*comb(2*k,k) for k in range(n+1)),
                f'raw binomial definition n={n}')
        require(ff[n] == sum(comb(n,k)**3 for k in range(n+1)), f'Franel binomial definition n={n}')
    rows, cms = [], []
    split = inert = 0
    classes = {'1':0,'7':0}
    for p in primes(bound):
        if p < 5:
            continue
        modulus = p*p
        B = weighted_mod(ga,54,p)
        epsilon = (-1)**((p-1)//2)
        require((ga[p]-6) % modulus == 0, f'raw endpoint p={p}')
        require((gf[p]-4) % modulus == 0, f'Franel endpoint p={p}')
        if p % 3 == 1:
            split += 1
            classes[str(p % 12)] += 1
            x,y = representation(p)
            target = (4*x*x-2*p) % modulus
            cms.append(cm_matrix(p,x,y))
        else:
            inert += 1
            x = y = target = 0
        require((epsilon*B-target) % modulus == 0, f'original conjecture p={p}')
        T = bridge = None
        if p > 5:
            T = weighted_mod(gf,50,p)
            character = 1 if pow(3,(p-1)//2,p) == 1 else -1
            bridge = (B-character*T) % modulus
            require(T == target and bridge == 0, f'Franel companion and transport p={p}')
        rows.append({'p':p,'class_mod_12':p % 12,'x':x,'y':y,'epsilon':epsilon,
                     'B_mod_p2':B,'T50_mod_p2':T,'target_mod_p2':target,
                     'conjecture_residue':(epsilon*B-target) % modulus,'transport_residue':bridge})
    require(bool(rows) and split > 0 and inert > 0, 'empty prime branch window')
    terms5 = [ga[n]*pow(54,-n,25) % 25 for n in range(5)]
    require(terms5 == [1,14,15,15,5] and sum(terms5) % 25 == 0, 'exceptional prime p=5')
    # Both classes receive fixed exact controls even for a requested short window.
    controls = [cm_matrix(p,*representation(p)) for p in (7,13)]
    require({r['e'] for r in controls} == {1,3}, 'missing split CM class control')
    return {'schema_version':1,'status':'PASS','bound_inclusive':bound,
            'last_prime':rows[-1]['p'],'prime_count':len(rows),'split_count':split,'inert_count':inert,
            'split_mod12_counts':classes,'original_definition_checks':2*direct_count,
            'endpoint_checks':2*len(rows),'p5_addends_mod25':terms5,
            'rows':rows,'cm_matrices':cms,'both_CM_class_controls':controls}
