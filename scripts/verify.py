"""Replay exact finite certificates and bounded regressions without changing the repository."""
import argparse
import contextlib
import io
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0,str(ROOT))

from companion.arithmetic import natural
from companion.evidence import CORE_FILES, SYMBOLIC_FILE, write_json, compare_expected, read_json
from companion import eta, primes, invariant, modpoly


def run(directory,bound,symbolic=False):
    natural(bound,'prime bound',7)
    results = [eta.certificates(), primes.regression(bound),
               invariant.certificates(min(bound,199)), modpoly.certificates()]
    for name,data in zip(CORE_FILES[:4],results):
        write_json(directory/name,data)
    symbolic_count = None
    if symbolic:
        try:
            from companion.symbolic import main as symbolic_main
        except ImportError as exc:
            raise RuntimeError('Explicit --symbolic requires requirements-symbolic.txt') from exc
        with contextlib.redirect_stdout(io.StringIO()):
            symbolic_main(directory/SYMBOLIC_FILE)
        symbolic_count = read_json(directory/SYMBOLIC_FILE)['identity_count']
    summary = {'schema_version':1,'status':'PASS','scope':'finite certificates and bounded regressions',
               'bound_inclusive':bound,'prime_count':results[1]['prime_count'],
               'split_count':results[1]['split_count'],'inert_count':results[1]['inert_count'],
               'original_definition_checks':results[1]['original_definition_checks'],
               'endpoint_checks':results[1]['endpoint_checks'],
               'period_identity_count':4,'period_q_degree':20,
               'invariant_bound_inclusive':min(bound,199),
               'invariant_polynomial_count':results[2]['polynomial_count'],
               'modular_polynomial_count':len(results[3]['polynomials']),
               'modular_polynomial_integer_coefficients':results[3]['total_integer_coefficients'],
               'symbolic_requested':symbolic,'symbolic_identity_count':symbolic_count}
    write_json(directory/CORE_FILES[4],summary)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bound',type=int,default=1999,help='inclusive prime regression bound (>=7)')
    parser.add_argument('--out',type=Path,help='write evidence to an explicit empty directory')
    parser.add_argument('--expected',type=Path,help='compare independent replay with a frozen evidence directory')
    parser.add_argument('--symbolic',action='store_true',help='also run explicit SymPy 1.14.0 formal checks')
    args = parser.parse_args()
    natural(args.bound,'prime bound',7)
    if args.out is not None:
        directory = args.out.resolve()
        if directory.exists() and (not directory.is_dir() or any(directory.iterdir())):
            raise ValueError('--out must be a new or empty directory; existing evidence is never overwritten')
        directory.mkdir(parents=True,exist_ok=True)
        summary = run(directory,args.bound,args.symbolic)
        if args.expected is not None:
            compare_expected(directory,args.expected,args.symbolic)
    else:
        with tempfile.TemporaryDirectory(prefix='sun35-replay-') as scratch:
            directory = Path(scratch)
            summary = run(directory,args.bound,args.symbolic)
            if args.expected is not None:
                compare_expected(directory,args.expected,args.symbolic)
    import json
    print(json.dumps(summary,sort_keys=True,separators=(',',':')))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, ArithmeticError, RuntimeError) as exc:
        print('SUN35_REPLAY_FAIL: '+str(exc),file=sys.stderr)
        raise SystemExit(1)
