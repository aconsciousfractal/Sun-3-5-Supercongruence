"""Optional exact formal identities from the paper (requires pinned SymPy).
These checks complement the written derivations; no prime sweep proves a theorem.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
import sympy as S

def require_zero(label,expression,output):
    reduced=S.factor(S.cancel(expression))
    if reduced != 0:
        raise ArithmeticError(f'{label}: nonzero residual {reduced}')
    output[label]=str(reduced)

def main(out):
    if S.__version__ != '1.14.0':
        raise RuntimeError('Symbolic verification requires SymPy 1.14.0')
    checks={}
    t,a,b,c=S.symbols('t a b c')
    y0,y1,y2,y3=S.symbols('y0 y1 y2 y3')
    D=1-4*a*t+16*c*t*t; thD=t*S.diff(D,t)
    I=D*(2*y0*y2-y1*y1)+thD*y0*y1+4*t*(-b+3*c*t)*y0*y0
    thI=t*S.diff(I,t)+y1*S.diff(I,y0)+y2*S.diff(I,y1)+y3*S.diff(I,y2)
    LY=D*y3+(-6*a*t+48*c*t*t)*y2+(-2*(a+2*b)*t+44*c*t*t)*y1+(-2*b*t+12*c*t*t)*y0
    require_zero('theta_I_minus_2Y_LY',thI-2*y0*LY,checks)
    # Conversion of the weight-8 identity into the differential invariant.
    e2=D*y0*y0; de=(thD*y0*y0+2*D*y0*y1)/2
    K=2*y0*(e2*y2+de*y1)-3*e2*y1*y1+4*t*(-b+3*c*t)*y0**4
    require_zero('weight8_identity_minus_Y_squared_I',K-y0*y0*I,checks)
    j,lam,ell,u0,u1,u2=S.symbols('j lam ell u0 u1 u2')
    U0=j*j*u0
    U1=j**4*u1+2*lam*j**3*u0
    U2=j**6*u2+6*lam*j**5*u1+6*lam**2*j**4*u0
    require_zero('weight4_W_covariance',U0*(j*j*ell+4*lam*j)-2*U1-j**4*(u0*ell-2*u1),checks)
    require_zero('weight8_bracket_covariance',2*U0*U2-3*U1**2-j**8*(2*u0*u2-3*u1**2),checks)
    aa,bb,cc,dd=S.symbols('A B C D')
    M=S.Matrix([[aa,bb],[6*cc,dd]])
    W3=S.Matrix([[3,1],[6,3]]); W6=S.Matrix([[0,-1],[6,0]])
    pred3=S.Matrix([[3*aa+6*cc-6*bb-2*dd,-aa-2*cc+3*bb+dd],
                    [6*aa+18*cc-12*bb-6*dd,-2*aa-6*cc+6*bb+3*dd]])
    pred6=S.Matrix([[dd,-cc],[-6*bb,aa]])
    for name,w,pred in [('W3',W3,pred3),('W6',W6,pred6)]:
        require_zero(name+'_normalizer',sum(v*v for v in (w*M*w.inv()-pred)),checks)
    require_zero('W3_square',sum(v*v for v in (W3**2-3*S.Matrix([[5,2],[12,5]]))),checks)
    require_zero('W6_square',sum(v*v for v in (W6**2+6*S.eye(2))),checks)
    require_zero('W3W6_square',sum(v*v for v in ((W3*W6)**2+18*S.eye(2))),checks)
    h=S.symbols('h')
    require_zero('CM_h_factorization',27*h*(1+8*h)**2-(1+9*h)-(6*h+1)*(288*h*h+24*h-1),checks)
    require_zero('CM_t_factorization',54*h*(1+17*h+72*h*h)-(1+18*h+72*h*h)**2+(18*h*h-6*h-1)*(288*h*h+24*h-1),checks)
    # Character and determinant factor identities, with delta^2=-3.
    x,y,delta=S.symbols('x y delta'); norm=x*x+3*y*y
    def quadratic_reduce(expr):
        return S.rem(S.Poly(S.expand(expr),delta),S.Poly(delta*delta+3,delta)).as_expr()
    require_zero('even_CM_root_identity',quadratic_reduce((x+y*delta)**2*(x-y*delta)**2-norm**2),checks)
    require_zero('odd_CM_root_identity',quadratic_reduce(-(x-y*delta)**2*(3*y-x*delta)**2-3*norm**2),checks)
    require_zero('trace_square_identity',quadratic_reduce((x+y*delta)**2+(x-y*delta)**2-(4*x*x-2*norm)),checks)
    p=S.symbols('p'); n=p-1
    require_zero('highest_resonance',16*c*n*n+32*c*n+12*c-4*c*(2*p-1)*(2*p+1),checks)
    mutation=S.expand(2*U0*U2-2*U1**2-j**8*(2*u0*u2-2*u1**2))
    if mutation == 0:
        raise ArithmeticError('Incorrect bracket covariance mutation accepted')
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({'schema_version':1,'status':'PASS',
        'scope':'polynomial/rational identities in formal indeterminates',
        'identity_count':len(checks),'residuals':checks,'incorrect_bracket_covariance_residual':str(S.factor(mutation)),
        'ok':True},indent=2)+'\n',encoding='utf-8')
    print(f'PASS {len(checks)} symbolic identities; incorrect bracket coefficient rejected.')
    print('Mutation residual:',S.factor(mutation))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True)
    main(p.parse_args().out)
